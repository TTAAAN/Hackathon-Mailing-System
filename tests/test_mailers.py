import unittest
from unittest.mock import patch

from mailing_system.core.models import Applicant, DeliveryResult
from mailing_system.mailers.acceptance import AcceptanceMailer
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
