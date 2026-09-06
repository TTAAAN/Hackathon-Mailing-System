"""Mailer client for sending rejection and application update notifications."""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Tuple

from mailing_system.config import PROJECT_ROOT
from mailing_system.core.models import Applicant, DeliveryResult, EventConfig
from mailing_system.logger import get_logger
from mailing_system.templates.rejection import RejectionTemplate
from mailing_system.transport.utils import encode_image, send_and_report, utc_now_iso
from mailing_system.transport.zepto_client import ZeptoMailerBase

LOG_DIR = PROJECT_ROOT / "logs"
logger = get_logger("mailers.rejection")


class RejectionMailer(ZeptoMailerBase):
    """Client service for sending rejection notices via ZeptoMail."""

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
        super().__init__(
            token=token,
            sender_email=sender_email,
            sender_name=sender_name,
            reply_to_email=reply_to_email,
            reply_to_name=reply_to_name,
            region=region,
            event_config=event_config,
            max_rate_per_sec=max_rate_per_sec,
            max_retries=max_retries,
            timeout=timeout,
        )
        self._cached_banner_b64 = encode_image(Path(self.event_config.banner_image_path))

    def send_rejection(self, applicant: Applicant) -> DeliveryResult:
        """Compose payload and dispatch a rejection email."""
        if not self._cached_banner_b64:
            err = "Failed to load inline banner image."
            logger.error("❌ PRE-CHECK FAILURE for '%s': %s", applicant.email, err)
            return DeliveryResult(
                recipient_email=applicant.email,
                name=applicant.name,
                team_name=applicant.team_name,
                status="FAILED",
                error_message=err,
                attempts=0,
                timestamp=utc_now_iso(),
            )

        if applicant.is_solo:
            subject = f"Update Regarding Your Application - {self.event_config.name}"
        else:
            subject = f"Update Regarding Your Application - {self.event_config.name} ({applicant.team_name})"

        subject = f"ITM Innovation Hackathon - Application Result"


        payload = self._build_common_payload(
            to_email=applicant.email,
            to_name=applicant.name,
            subject=subject,
            html_body=RejectionTemplate.render_html(applicant, self.event_config),
            text_body=RejectionTemplate.render_plain(applicant, self.event_config),
            inline_images=[
                {"content": self._cached_banner_b64, "mime_type": "image/png", "cid": "banner_img"}
            ],
        )

        dispatch = self._dispatch(payload)
        result = self._result_from_dispatch(
            recipient_email=applicant.email,
            dispatch=dispatch,
            name=applicant.name,
            team_name=applicant.team_name,
        )

        if result.status == "SUCCESS":
            logger.info(
                "✅ SUCCESS: Sent rejection to '%s' [Solo: %s | Team: %s] (ReqID: %s)",
                applicant.email,
                applicant.is_solo,
                applicant.team_name,
                result.request_id,
            )
        return result

    def send_batch(
        self,
        applicants: List[Applicant],
        failed_report_path: Path = LOG_DIR / "failed_rejections.json",
        success_report_path: Path = LOG_DIR / "success_rejections.json",
    ) -> Tuple[List[DeliveryResult], List[DeliveryResult]]:
        """Send rejection notices to a list of applicants in batch with reports."""
        return send_and_report(
            self.send_rejection,
            applicants,
            success_report_path=success_report_path,
            failed_report_path=failed_report_path,
        )
