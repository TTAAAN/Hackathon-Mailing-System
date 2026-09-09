"""Mailer client for sending entry passes with embedded QR code."""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Tuple, Union

from mailing_system.config import PROJECT_ROOT
from mailing_system.core.models import Applicant, Attendee, DeliveryResult, EventConfig
from mailing_system.logger import get_logger
from mailing_system.qrcode_generator import build_qr_png_base64
from mailing_system.templates.qr import QRTemplate
from mailing_system.transport.utils import encode_image, send_and_report, utc_now_iso
from mailing_system.transport.zepto_client import ZeptoMailerBase

LOG_DIR = PROJECT_ROOT / "logs"
logger = get_logger("mailers.qr")


class QRMailer(ZeptoMailerBase):
    """Client service for sending transactional event passes via ZeptoMail."""

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

    def send_pass(self, attendee: Union[Attendee, Applicant]) -> DeliveryResult:
        """Dispatches an entry pass to a single attendee with automatic retries."""
        try:
            qr_b64 = build_qr_png_base64(attendee.ticket_id)
        except ValueError as exc:
            err = str(exc)
            logger.error("❌ PRE-CHECK FAILURE for '%s': %s", attendee.email, err)
            return DeliveryResult(
                recipient_email=attendee.email,
                ticket_id=attendee.ticket_id,
                name=attendee.name,
                team_name=attendee.team_name,
                status="FAILED",
                http_status=None,
                zepto_code="LOCAL_QR_ERROR",
                error_message=err,
                details=None,
                request_id=None,
                attempts=0,
                timestamp=utc_now_iso(),
            )

        if not qr_b64 or not self._cached_banner_b64:
            err = "Failed to load inline images (QR or Banner missing/corrupt)."
            logger.error("❌ PRE-CHECK FAILURE for '%s': %s", attendee.email, err)
            return DeliveryResult(
                recipient_email=attendee.email,
                ticket_id=attendee.ticket_id,
                name=attendee.name,
                team_name=attendee.team_name,
                status="FAILED",
                http_status=None,
                zepto_code="LOCAL_FILE_ERROR",
                error_message=err,
                details=None,
                request_id=None,
                attempts=0,
                timestamp=utc_now_iso(),
            )

        payload = self._build_common_payload(
            to_email=attendee.email,
            to_name=attendee.name,
            subject=f"Your Hackathon Entry Pass for '{attendee.name}' ({attendee.team_name})",
            html_body=QRTemplate.render_html(attendee, self.event_config),
            text_body=QRTemplate.render_plain(attendee, self.event_config),
            inline_images=[
                {"content": self._cached_banner_b64, "mime_type": "image/png", "cid": "banner_img"},
                {"content": qr_b64, "mime_type": "image/png", "cid": "qr_img"},
            ],
        )

        dispatch = self._dispatch(payload)
        result = self._result_from_dispatch(
            recipient_email=attendee.email,
            dispatch=dispatch,
            name=attendee.name,
            team_name=attendee.team_name,
            ticket_id=attendee.ticket_id,
        )

        if result.status == "SUCCESS":
            logger.info(
                "✅ SUCCESS: Sent to '%s' [Team: %s | Pass: %s] (ReqID: %s)",
                attendee.email,
                attendee.team_name,
                attendee.ticket_id,
                result.request_id,
            )
        return result

    def send_qr(self, attendee: Union[Attendee, Applicant]) -> DeliveryResult:
        """Alias for send_pass."""
        return self.send_pass(attendee)

    def send_batch(
        self,
        attendees: List[Union[Attendee, Applicant]],
        failed_report_path: Path = LOG_DIR / "failed_emails.json",
        success_report_path: Path = LOG_DIR / "success_emails.json",
    ) -> Tuple[List[DeliveryResult], List[DeliveryResult]]:
        """Dispatches passes to multiple attendees and dumps results to JSON."""
        return send_and_report(
            self.send_pass,
            attendees,
            success_report_path=success_report_path,
            failed_report_path=failed_report_path,
        )


ZeptoMailer = QRMailer
