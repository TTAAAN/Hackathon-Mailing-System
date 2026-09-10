"""Generate QR code payloads in memory.

The mailer now renders QR images directly from ``ticket_id`` instead of reading
QR files from disk or reconstructing attendees from filenames.
"""

from __future__ import annotations

import base64
from io import BytesIO

import qrcode


def build_qr_image(ticket_id: str, error_correction=qrcode.constants.ERROR_CORRECT_M):
    clean_ticket_id = str(ticket_id or "").strip()
    if not clean_ticket_id:
        raise ValueError("ticket_id is required to generate a QR code.")

    qr = qrcode.QRCode(
        version=None,
        error_correction=error_correction,
        box_size=10,
        border=4,
    )
    qr.add_data(clean_ticket_id)
    qr.make(fit=True)
    return qr.make_image(fill_color="#000000", back_color="#FFFFFF")


def build_qr_png_bytes(ticket_id: str, error_correction=qrcode.constants.ERROR_CORRECT_H) -> bytes:
    """Render a QR image for ``ticket_id`` and return PNG bytes."""
    image = build_qr_image(ticket_id, error_correction=error_correction)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def build_qr_png_base64(ticket_id: str, error_correction=qrcode.constants.ERROR_CORRECT_H) -> str:
    """Render a QR image for ``ticket_id`` and return a base64-encoded PNG."""
    return base64.b64encode(build_qr_png_bytes(ticket_id, error_correction=error_correction)).decode("utf-8")
