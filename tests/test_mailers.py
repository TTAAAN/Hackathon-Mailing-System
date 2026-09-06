import unittest
from unittest.mock import patch

from mailing_system.core.models import Applicant, Attendee, DeliveryResult
from mailing_system.mailers.acceptance import AcceptanceMailer
from mailing_system.mailers.qr import QRMailer
from mailing_system.mailers.rejection import RejectionMailer


class DummyResponse:
    def __init__(self, status_code: int = 200, json_data: dict | None = None):
        self.status_code = status_code
        self._json_data = json_data or {}
        self.text = "OK"

    def json(self):
        return self._json_data


class MailerTests(unittest.TestCase):
    def test_acceptance_success(self):
        applicant = Applicant(name="Alice", email="alice@example.com", team_name="TeamAlpha")
        with patch.object(
            AcceptanceMailer,
            "_dispatch",
            return_value=(True, 200, {"data": [{"code": "TM_SUCCESS"}]}, "req-accept-1", 1, DummyResponse(200)),
        ):
            mailer = AcceptanceMailer()
            res = mailer.send_acceptance(applicant)
            self.assertEqual(res.status, "SUCCESS")
            self.assertEqual(res.recipient_email, "alice@example.com")
            self.assertEqual(res.name, "Alice")
            self.assertEqual(res.team_name, "TeamAlpha")

    def test_qr_pass_success(self):
        attendee = Attendee(name="Alice", email="alice@example.com", team_name="TeamAlpha", ticket_id="TCK-100")
        with patch.object(
            QRMailer,
            "_dispatch",
            return_value=(True, 200, {"data": [{"code": "TM_SUCCESS"}]}, "req-qr-1", 1, DummyResponse(200)),
        ):
            mailer = QRMailer()
            res = mailer.send_pass(attendee)
            self.assertEqual(res.status, "SUCCESS")
            self.assertEqual(res.recipient_email, "alice@example.com")
            self.assertEqual(res.name, "Alice")
            self.assertEqual(res.team_name, "TeamAlpha")
            self.assertEqual(res.ticket_id, "TCK-100")

    def test_qr_pass_missing_ticket(self):
        attendee = Attendee(name="Alice", email="alice@example.com", team_name="TeamAlpha", ticket_id="")
        mailer = QRMailer()
        res = mailer.send_pass(attendee)
        self.assertEqual(res.status, "FAILED")
        self.assertEqual(res.zepto_code, "LOCAL_QR_ERROR")
        self.assertIn("ticket_id is required", res.error_message)

    def test_rejection_success(self):
        applicant = Applicant(name="Bob", email="bob@example.com", team_name="TeamBeta")
        with patch.object(
            RejectionMailer,
            "_dispatch",
            return_value=(True, 200, {"data": [{"code": "TM_SUCCESS"}]}, "req-reject-1", 1, DummyResponse(200)),
        ):
            mailer = RejectionMailer()
            res = mailer.send_rejection(applicant)
            self.assertEqual(res.status, "SUCCESS")
            self.assertEqual(res.recipient_email, "bob@example.com")
            self.assertEqual(res.name, "Bob")
            self.assertEqual(res.team_name, "TeamBeta")


if __name__ == "__main__":
    unittest.main()
