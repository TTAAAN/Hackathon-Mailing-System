import unittest

from mailing_system.core.models import Applicant, EventConfig
from mailing_system.templates.acceptance import AcceptanceTemplate
from mailing_system.templates.rejection import RejectionTemplate


class TemplateTests(unittest.TestCase):
    def setUp(self):
        self.event = EventConfig(
            name="Test Hackathon 2026",
            date="10-12 October 2026",
            venue="Main Hall",
            organizer_name="Organizing Team",
            support_email="support@example.com",
            telegram_link="https://t.me/testhack",
        )

    def test_acceptance_template_solo(self):
        applicant = Applicant(name="Alice", email="alice@example.com", team_name="Solo Participant")
        html = AcceptanceTemplate.render_html(applicant, self.event)
        plain = AcceptanceTemplate.render_plain(applicant, self.event)

        self.assertIn("Dear Alice,", html)
        self.assertIn("Test Hackathon 2026", html)
        self.assertIn("https://t.me/testhack", html)
        self.assertIn("Dear Alice,", plain)
        self.assertNotIn("and team Solo Participant", plain)

    def test_acceptance_template_team(self):
        applicant = Applicant(name="Bob", email="bob@example.com", team_name="ByteBuilders")
        html = AcceptanceTemplate.render_html(applicant, self.event)
        plain = AcceptanceTemplate.render_plain(applicant, self.event)

        self.assertIn("team ByteBuilders", html)
        self.assertIn("and team ByteBuilders", plain)

    def test_rejection_template_solo(self):
        applicant = Applicant(name="Charlie", email="charlie@example.com", team_name="")
        html = RejectionTemplate.render_html(applicant, self.event)
        plain = RejectionTemplate.render_plain(applicant, self.event)

        self.assertIn("Dear Charlie,", html)
        self.assertIn("unable to offer your application an invitation", html)
        self.assertIn("unable to offer your application an invitation", plain)

    def test_rejection_template_team(self):
        applicant = Applicant(name="David", email="david@example.com", team_name="CodeWizards")
        html = RejectionTemplate.render_html(applicant, self.event)
        plain = RejectionTemplate.render_plain(applicant, self.event)

        self.assertIn("team CodeWizards", html)
        self.assertIn("team CodeWizards", plain)


if __name__ == "__main__":
    unittest.main()
