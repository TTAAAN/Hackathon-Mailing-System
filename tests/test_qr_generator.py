import unittest

from mailing_system.qrcode_generator import (
    build_qr_image,
    build_qr_png_bytes,
    build_qr_png_base64,
)


class QRGeneratorTests(unittest.TestCase):
    def test_build_qr_image_success(self):
        img = build_qr_image("TICKET-12345")
        self.assertIsNotNone(img)
        self.assertEqual(img.size, (330, 330))

    def test_build_qr_image_empty_raises(self):
        with self.assertRaises(ValueError) as ctx:
            build_qr_image("")
        self.assertIn("ticket_id is required", str(ctx.exception))

        with self.assertRaises(ValueError) as ctx:
            build_qr_image("   ")
        self.assertIn("ticket_id is required", str(ctx.exception))

        with self.assertRaises(ValueError) as ctx:
            build_qr_image(None)
        self.assertIn("ticket_id is required", str(ctx.exception))

    def test_build_qr_png_bytes(self):
        png_bytes = build_qr_png_bytes("TICKET-12345")
        self.assertTrue(isinstance(png_bytes, bytes))
        self.assertTrue(png_bytes.startswith(b"\x89PNG\r\n\x1a\n"))

    def test_build_qr_png_base64(self):
        png_b64 = build_qr_png_base64("TICKET-12345")
        self.assertTrue(isinstance(png_b64, str))
        self.assertTrue(len(png_b64) > 0)


if __name__ == "__main__":
    unittest.main()
