"""Email template generators."""

from mailing_system.templates.acceptance import AcceptanceTemplate
from mailing_system.templates.dropped import DroppedTemplate
from mailing_system.templates.qr import QRTemplate
from mailing_system.templates.rejection import RejectionTemplate
from mailing_system.templates.reserved_confirmation import ReservedConfirmationTemplate

__all__ = ["AcceptanceTemplate", "QRTemplate", "RejectionTemplate", "ReservedConfirmationTemplate", "DroppedTemplate"]
