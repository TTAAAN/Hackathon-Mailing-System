"""Email template generators."""

from mailing_system.templates.acceptance import AcceptanceTemplate
from mailing_system.templates.qr import PassTemplate, QRTemplate
from mailing_system.templates.rejection import RejectionTemplate

__all__ = ["AcceptanceTemplate", "PassTemplate", "QRTemplate", "RejectionTemplate"]
