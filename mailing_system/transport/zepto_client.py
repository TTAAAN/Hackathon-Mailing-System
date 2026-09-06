"""ZeptoMail HTTP transport base client with session pooling and retry logic."""

from __future__ import annotations

import random
import time
from typing import Any, Dict, List, Optional, Tuple

try:
    import requests
    from requests.adapters import HTTPAdapter
except Exception:
    requests = None
    HTTPAdapter = None

from mailing_system.core.models import DeliveryResult, EventConfig
from mailing_system.logger import get_logger
from mailing_system.transport.rate_limiter import RateLimiter
from mailing_system.transport.utils import utc_now_iso

logger = get_logger("transport.zepto_client")


class ZeptoMailerBase:
    """Base transport client for Zoho ZeptoMail API."""

    ENDPOINTS = {
        "us": "https://api.zeptomail.com/v1.1/email",
        "eu": "https://api.zeptomail.eu/v1.1/email",
        "in": "https://api.zeptomail.in/v1.1/email",
        "au": "https://api.zeptomail.com.au/v1.1/email",
        "ca": "https://api.zeptomail.ca/v1.1/email",
        "sa": "https://api.zeptomail.sa/v1.1/email",
    }

    def __init__(
        self,
        token: Optional[str] = None,
        sender_email: Optional[str] = None,
        sender_name: Optional[str] = None,
        reply_to_email: Optional[str] = None,
        reply_to_name: Optional[str] = None,
        region: str = "us",
        event_config: Optional[EventConfig] = None,
        max_rate_per_sec: float = 2.0,
        max_retries: int = 3,
        timeout: Tuple[float, float] = (10.0, 35.0),
    ):
        self.token = token or ""
        self.sender_email = sender_email or "result@mail.itm-hackathon.tech"
        self.sender_name = sender_name or "ITM Innovation Hackathon 2026"
        self.reply_to_email = reply_to_email or "support@itm-hackathon.tech"
        self.reply_to_name = reply_to_name or "ITM Hackathon Support"

        self.region = region.lower()
        self.endpoint = self.ENDPOINTS.get(self.region, self.ENDPOINTS["us"])
        self.event_config = event_config or EventConfig()

        self.max_retries = max_retries
        self.timeout = timeout
        self.rate_limiter = RateLimiter(max_rate_per_sec=max_rate_per_sec)

        if requests is not None:
            self._session = requests.Session()
            adapter = HTTPAdapter(pool_connections=10, pool_maxsize=10, max_retries=0)
            self._session.mount("https://", adapter)
            self._session.mount("http://", adapter)
        else:
            self._session = None

    def close(self) -> None:
        """Close underlying HTTP session."""
        try:
            if self._session:
                self._session.close()
        except Exception:
            pass

    def _get_headers(self) -> Dict[str, str]:
        auth_header = (
            self.token
            if self.token.lower().startswith("zoho-enczapikey")
            else f"Zoho-enczapikey {self.token}"
        )
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": auth_header,
        }

    def _build_common_payload(
        self,
        to_email: str,
        to_name: str,
        subject: str,
        html_body: str,
        text_body: str,
        inline_images: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """Compose standardized payload for ZeptoMail endpoint."""
        payload: Dict[str, Any] = {
            "from": {"address": self.sender_email.strip(), "name": self.sender_name.strip()},
            "to": [{"email_address": {"address": to_email.strip(), "name": to_name.strip()}}],
            "subject": subject,
            "htmlbody": html_body,
            "textbody": text_body,
            "track_opens": False,
            "track_clicks": False,
        }
        if inline_images:
            payload["inline_images"] = inline_images
        if self.reply_to_email:
            payload["reply_to"] = [
                {"address": self.reply_to_email.strip(), "name": self.reply_to_name.strip()}
            ]
        return payload

    def _result_from_dispatch(
        self,
        recipient_email: str,
        dispatch: tuple,
        name: Optional[str] = None,
        team_name: Optional[str] = None,
        ticket_id: Optional[str] = None,
    ) -> DeliveryResult:
        """Map dispatch result tuple to DeliveryResult object."""
        success, http_code, res_json, request_id, attempts, response = dispatch
        if success:
            zepto_code = (
                res_json.get("data", [{}])[0].get("code")
                if isinstance(res_json, dict)
                else None
            ) or "TM_SUCCESS"
            return DeliveryResult(
                recipient_email=recipient_email,
                ticket_id=ticket_id,
                name=name,
                team_name=team_name,
                status="SUCCESS",
                http_status=http_code,
                zepto_code=zepto_code,
                details=(res_json.get("data") if isinstance(res_json, dict) else None),
                request_id=request_id,
                attempts=attempts,
                timestamp=utc_now_iso(),
            )

        err_data = res_json.get("error", {}) if isinstance(res_json, dict) else {}
        last_zepto_code = (
            err_data.get("code") if isinstance(err_data, dict) else f"HTTP_{http_code}"
        )
        last_error_msg = (
            err_data.get("message")
            if isinstance(err_data, dict)
            else (response.text if response is not None else None)
        )
        return DeliveryResult(
            recipient_email=recipient_email,
            ticket_id=ticket_id,
            name=name,
            team_name=team_name,
            status="FAILED",
            http_status=http_code,
            zepto_code=last_zepto_code,
            error_message=last_error_msg,
            details=(err_data.get("details") if isinstance(err_data, dict) else None),
            request_id=request_id,
            attempts=attempts,
            timestamp=utc_now_iso(),
        )

    def _dispatch(self, payload: Dict[str, Any]):
        """Send payload with automatic retry, exponential backoff, and rate limiting."""
        attempts = 0
        last_http_code = None
        last_res_json = None
        request_id = None
        response = None

        while attempts < self.max_retries:
            attempts += 1
            self.rate_limiter.acquire()
            try:
                logger.debug("Dispatching payload to ZeptoMail (attempt %d)", attempts)
                if not self._session:
                    raise RuntimeError("requests library is required to dispatch emails")
                response = self._session.post(
                    self.endpoint,
                    json=payload,
                    headers=self._get_headers(),
                    timeout=self.timeout,
                )
                last_http_code = response.status_code
                try:
                    last_res_json = response.json()
                except ValueError:
                    last_res_json = {}
                request_id = last_res_json.get("request_id") or response.headers.get("x-request-id")

                if response.status_code in (200, 201):
                    return True, last_http_code, last_res_json, request_id, attempts, response

                if response.status_code in (400, 401, 403, 404, 422):
                    return False, last_http_code, last_res_json, request_id, attempts, response

                if response.status_code == 429:
                    retry_after = response.headers.get("Retry-After")
                    time.sleep(
                        float(retry_after)
                        if (retry_after and retry_after.isdigit())
                        else 2.0 * (2 ** attempts)
                    )
                    continue

                if response.status_code >= 500:
                    time.sleep(min(15.0, 2.0 * (2 ** attempts)) + random.uniform(0.1, 0.5))
                    continue

            except requests.exceptions.RequestException as re:
                logger.warning("Network error while dispatching: %s", re)
                time.sleep(2.0 * (2 ** attempts))
                continue

        return False, last_http_code, last_res_json, request_id, attempts, response
