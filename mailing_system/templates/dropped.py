"""HTML and plain-text templates for dropped participants who are unable to attend."""

from __future__ import annotations

from mailing_system.core.models import Applicant, EventConfig


class DroppedTemplate:
    """Generates customized HTML and plain-text emails for participants marked as dropped."""

    @staticmethod
    def render_html(applicant: Applicant, event: EventConfig) -> str:
        greeting = f"Dear {applicant.name},"
        opening = (
            f"Thank you for reaching out and letting us know regarding your availability for the {event.name}. "
            f"We have officially recorded your response that you will be unable to join us for this edition."
        )

        return f"""\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Attendance Update - {event.name}</title>
</head>
<body style="margin: 0; padding: 0; background-color: #ffffff; font-family: Arial, Helvetica, sans-serif; font-size: 15px; line-height: 1.6; color: #222222;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" bgcolor="#ffffff">
    <tr>
      <td align="center" style="padding: 24px 12px;">
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="max-width: 560px; text-align: left;">

          <!-- Greeting & Acknowledgment -->
          <tr>
            <td style="padding-bottom: 16px; font-size: 15px; color: #333333; line-height: 1.6;">
              {greeting}<br /><br />
              {opening}
            </td>
          </tr>

          <!-- Recognition & Understanding -->
          <tr>
            <td style="padding-bottom: 16px; font-size: 15px; color: #333333; line-height: 1.6;">
              Your application stood out during the selection stage for its creativity and technical promise. We completely understand that schedule conflicts and unexpected commitments can arise.
            </td>
          </tr>

          <!-- Appreciation -->
          <tr>
            <td style="padding-bottom: 16px; font-size: 15px; color: #333333; line-height: 1.6;">
              We truly appreciate you taking the time to inform us in advance.
            </td>
          </tr>

          <!-- Hope to see again in the next season -->
          <tr>
            <td style="padding-bottom: 20px; font-size: 15px; color: #333333; line-height: 1.6;">
              Given the strength of your submission, we would love to see you again in the next season! We hope you will stay connected with our community and keep an eye out for our upcoming announcements.
            </td>
          </tr>

          <!-- Support & Mistake Check -->
          <tr>
            <td style="padding-bottom: 24px; font-size: 15px; color: #333333; line-height: 1.6;">
              If this was sent in error, you can reply directly to this email or reach out to <a href="https://t.me/ITMTechnicalSupport" style="color: #1a5fb4; text-decoration: underline;">@ITMTechnicalSupport</a> on Telegram for fast support.
            </td>
          </tr>

          <!-- Sign-off -->
          <tr>
            <td style="padding-top: 16px; border-top: 1px solid #eeeeee; font-size: 12px; color: #888888; line-height: 1.6;">
              Warm regards,<br />
              <strong>{event.organizer_name}</strong><br />
              Support: <a href="mailto:{event.support_email}" style="color: #888888;">{event.support_email}</a> | Telegram: <a href="https://t.me/ITMTechnicalSupport" style="color: #888888;">@ITMTechnicalSupport</a>
            </td>
          </tr>

          <!-- Banner -->
          <tr>
            <td style="padding-top: 32px;">
              <img src="cid:banner_img" alt="{event.name} Banner" width="560" style="display: block; width: 100%; max-width: 560px; height: auto; border: 0;" />
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""

    @staticmethod
    def render_plain(applicant: Applicant, event: EventConfig) -> str:
        opening = (
            f"Thank you for reaching out and letting us know regarding your availability for the {event.name}. "
            f"We have officially recorded your response that you will be unable to join us for this edition."
        )

        return (
            f"Dear {applicant.name},\n\n"
            f"{opening}\n\n"
            f"Your application stood out during the selection stage for its creativity and technical promise. "
            f"We completely understand that schedule conflicts and unexpected commitments can arise.\n\n"
            f"We truly appreciate you taking the time to inform us in advance.\n\n"
            f"Given the strength of your submission, we would love to see you again in the next season! "
            f"We hope you will stay connected with our community and keep an eye out for our upcoming announcements.\n\n"
            f"If this was sent in error, you can reply directly to this email "
            f"or contact @ITMTechnicalSupport on Telegram (https://t.me/ITMTechnicalSupport) for fast support.\n\n"
            f"Warm regards,\n"
            f"{event.organizer_name}\n"
            f"Support: {event.support_email} | Telegram: @ITMTechnicalSupport"
        )
