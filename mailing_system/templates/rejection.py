"""HTML and plain-text templates for rejection / application update emails."""

from __future__ import annotations

from mailing_system.core.models import Applicant, EventConfig


class RejectionTemplate:
    """Generates customized HTML and plain-text rejection emails."""

    @staticmethod
    def render_html(applicant: Applicant, event: EventConfig) -> str:
        if applicant.is_solo:
            greeting = f"Dear {applicant.name},"
            opening = (
                f"Thank you for taking the time and initiative to apply for the {event.name}. "
                f"Our team deeply appreciates the thought and dedication you poured into your application."
            )
            submission_text = "your application"
        else:
            greeting = f"Dear {applicant.name},"
            opening = (
                f"Thank you and team '{applicant.team_name}' for taking the time and initiative to apply "
                f"for the {event.name}. Our team deeply appreciates the thought and dedication your team "
                f"invested in this submission."
            )
            submission_text = f"team {applicant.team_name}'s application"

        return f"""\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Application Update - {event.name}</title>
</head>
<body style="margin: 0; padding: 0; background-color: #ffffff; font-family: Arial, Helvetica, sans-serif; font-size: 15px; line-height: 1.6; color: #222222;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" bgcolor="#ffffff">
    <tr>
      <td align="center" style="padding: 24px 12px;">
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="max-width: 560px; text-align: left;">

          <!-- Greeting & Appreciation -->
          <tr>
            <td style="padding-bottom: 16px; font-size: 15px; color: #333333; line-height: 1.6;">
              {greeting}<br /><br />
              {opening}
            </td>
          </tr>

          <!-- Decision -->
          <tr>
            <td style="padding-bottom: 16px; font-size: 15px; color: #333333; line-height: 1.6;">
              Following careful review of all submissions, we regret to inform you that {submission_text} was not selected for this season. We received numerous impressive applications, and this was a genuinely difficult decision.
            </td>
          </tr>

          <!-- Reassurance -->
          <tr>
            <td style="padding-bottom: 16px; font-size: 15px; color: #333333; line-height: 1.6;">
              We want to emphasize that this outcome does not diminish the value of your work or potential. Many qualified candidates did not advance simply due to limited spots. We encourage you to keep pursuing your vision.
            </td>
          </tr>

          <!-- Encouragement -->
          <tr>
            <td style="padding-bottom: 20px; font-size: 15px; color: #333333; line-height: 1.6;">
              We strongly encourage you to continue developing your ideas, and we would love to see your application again in our next seasons. We hope you will stay connected with us and follow our updates for our next seasons.
            </td>
          </tr>

          <!-- Support & Questions -->
          <tr>
            <td style="padding-bottom: 24px; font-size: 15px; color: #333333; line-height: 1.6;">
              Should you have any questions, feel free to reach out at <a href="mailto:{event.support_email}" style="color: #1a5fb4;">{event.support_email}</a>.
            </td>
          </tr>

          <!-- Sign-off -->
          <tr>
            <td style="padding-top: 16px; border-top: 1px solid #eeeeee; font-size: 12px; color: #888888; line-height: 1.6;">
              Best regards,<br />
              <strong>{event.organizer_name}</strong><br />
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
        if applicant.is_solo:
            opening = (
                f"Thank you for taking the time and initiative to apply for the {event.name}. "
                f"Our team deeply appreciates the thought and dedication you poured into your application."
            )
            submission_text = "your application"
        else:
            opening = (
                f"Thank you and team '{applicant.team_name}' for taking the time and initiative to apply "
                f"for the {event.name}. Our team deeply appreciates the thought and dedication your team "
                f"invested in this submission."
            )
            submission_text = f"team {applicant.team_name}'s application"

        return (
            f"Dear {applicant.name},\n\n"
            f"{opening}\n\n"
            f"Following careful review of all submissions, we regret to inform you that {submission_text} was not "
            f"selected for this season. We received numerous impressive applications, and this was a genuinely "
            f"difficult decision.\n\n"
            f"We want to emphasize that this outcome does not diminish the value of your work or potential. Many "
            f"qualified candidates did not advance simply due to limited spots. We encourage you to keep pursuing "
            f"your vision.\n\n"
            f"We strongly encourage you to continue developing your ideas, and we would love to see your "
            f"application again in our next seasons. We hope you will stay connected with us and follow our "
            f"updates for future opportunities and programs.\n\n"
            f"Should you have any questions, feel free to reach out at {event.support_email}.\n\n"
            f"Best regards,\n"
            f"{event.organizer_name}\n"
            f"Support: {event.support_email}"
        )
