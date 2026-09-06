"""HTML and plain-text templates for acceptance emails."""

from __future__ import annotations

from mailing_system.core.models import Applicant, EventConfig


class AcceptanceTemplate:
    """Generates customized HTML and plain-text acceptance emails."""

    @staticmethod
    def render_html(applicant: Applicant, event: EventConfig) -> str:
        if applicant.is_solo:
            greeting = f"Dear {applicant.name},"
            opening_paragraph = (
                f"On behalf of the entire organizing committee, <strong>we are thrilled to officially "
                f"congratulate you on being accepted to the {event.name}!</strong>"
            )
        else:
            greeting = f"Dear {applicant.name},"
            opening_paragraph = (
                f"On behalf of the entire organizing committee, <strong>we are thrilled to officially "
                f"congratulate you and team '{applicant.team_name}' on being accepted to the {event.name}!</strong>"
            )

        telegram_section = (
            f'Please join our official <a href="{event.telegram_link}" style="color: #1a5fb4; font-weight: bold; text-decoration: underline;">Participant Telegram Group</a> right away. All important schedule updates, mentor announcements, and challenges will be coordinated through this channel.'
            if event.telegram_link
            else "All important schedule updates, mentor announcements, and challenges will be coordinated via email."
        )

        return f"""\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>ITM Innovation Hackathon - Application Result</title>
</head>
<body style="margin: 0; padding: 0; background-color: #ffffff; font-family: Arial, Helvetica, sans-serif; font-size: 15px; line-height: 1.6; color: #222222;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" bgcolor="#ffffff">
    <tr>
      <td align="center" style="padding: 24px 12px;">
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="max-width: 560px; text-align: left;">

          <!-- Greeting & Acceptance -->
          <tr>
            <td style="padding-bottom: 16px; font-size: 15px; color: #333333; line-height: 1.6;">
              {greeting}<br /><br />
              {opening_paragraph}
            </td>
          </tr>

          <!-- Recognition -->
          <tr>
            <td style="padding-bottom: 16px; font-size: 15px; color: #333333; line-height: 1.6;">
              We received an extraordinary volume of applications this year, and your submission stood out for its ambition, technical curiosity, and problem-solving potential. We cannot wait to see the ideas and solutions you bring to life.
            </td>
          </tr>

          <!-- Dates & Venue -->
          <tr>
            <td style="padding-bottom: 16px; font-size: 15px; color: #333333; line-height: 1.6;">
              The hackathon will be hosted at the <strong>{event.venue}</strong> on <strong>{event.date}</strong>.<br /><br />
              {telegram_section}
            </td>
          </tr>

          <!-- Gear & Support -->
          <tr>
            <td style="padding-bottom: 24px; font-size: 15px; color: #333333; line-height: 1.6;">
              Make sure your laptop, chargers, and development tools are prepared for Day 1. If you have any questions or need assistance, feel free to reply directly to this email or reach us at <a href="mailto:{event.support_email}" style="color: #1a5fb4;">{event.support_email}</a>.
            </td>
          </tr>

          <!-- Sign-off -->
          <tr>
            <td style="padding-bottom: 24px; font-size: 15px; color: #333333; line-height: 1.6;">
              Once again, huge congratulations! We look forward to seeing you at {event.venue}.
            </td>
          </tr>
          <tr>
            <td style="padding-top: 16px; border-top: 1px solid #eeeeee; font-size: 12px; color: #888888; line-height: 1.6;">
              Warm regards,<br />
              <strong>{event.organizer_name}</strong> &middot; {event.organizer_address}<br />
              Support: <a href="mailto:{event.support_email}" style="color: #888888;">{event.support_email}</a>
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
        team_mention = "" if applicant.is_solo else f" and team '{applicant.team_name}'"
        telegram_info = (
            f"Please join our official Participant Telegram Group right away for all announcements and updates:\n{event.telegram_link}\n\n"
            if event.telegram_link
            else ""
        )

        return (
            f"Dear {applicant.name},\n\n"
            f"On behalf of the entire organizing committee, we are thrilled to officially congratulate you{team_mention} "
            f"on being accepted to the {event.name}!\n\n"
            f"We received an extraordinary volume of applications this year, and your submission stood out for its ambition, "
            f"technical curiosity, and problem-solving potential. We cannot wait to see the ideas and solutions you bring to life.\n\n"
            f"The hackathon will take place at the {event.venue} on {event.date}.\n\n"
            f"{telegram_info}"
            f"Make sure your laptop, chargers, and development tools are prepared for Day 1. If you have any questions, "
            f"feel free to reply directly to this email or reach us at {event.support_email}.\n\n"
            f"Once again, huge congratulations! We look forward to seeing you at {event.venue}.\n\n"
            f"Warm regards,\n"
            f"{event.organizer_name}\n"
            f"{event.organizer_address}\n"
            f"{event.support_email}"
        )
