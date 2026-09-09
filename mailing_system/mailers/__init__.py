"""Mailer services."""

from mailing_system.mailers.acceptance import AcceptanceMailer
from mailing_system.mailers.qr import QRMailer, ZeptoMailer
from mailing_system.mailers.rejection import RejectionMailer

__all__ = ["AcceptanceMailer", "QRMailer", "RejectionMailer", "ZeptoMailer"]
