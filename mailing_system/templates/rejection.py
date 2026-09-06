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
                f"Thank you and team {applicant.team_name} for taking the time and initiative to apply "
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

          <!-- Decision & Capacity -->
          <tr>
            <td style="padding-bottom: 16px; font-size: 15px; color: #333333; line-height: 1.6;">
              We received an extraordinary volume of exceptional submissions this year. Due to strict physical venue capacity at {event.venue}, our selection process was intensely competitive, and <strong>we regret to inform you that we are unable to offer {submission_text} an invitation to participate in this edition.</strong>
            </td>
          </tr>

          <!-- Reassurance & Encouragement -->
          <tr>
            <td style="padding-bottom: 16px; font-size: 15px; color: #333333; line-height: 1.6;">
              Please know that <strong>this decision is not a reflection of your talent, capability, or potential as a creator.</strong> With razor-thin margins between applications, many impressive submissions simply could not be accommodated. Your trajectory as a builder is never defined by a single weekend—what matters most is your curiosity and drive to keep solving real problems.
            </td>
          </tr>
          <tr>
            <td style="padding-bottom: 20px; font-size: 15px; color: #333333; line-height: 1.6;">
              We strongly encourage you to continue developing your ideas, and we would love to see your application again in our future events and cohorts.
            </td>
          </tr>

          <!-- Support & Questions -->
          <tr>
            <td style="padding-bottom: 24px; font-size: 15px; color: #333333; line-height: 1.6;">
              If you have any questions, please feel free to reply directly to this email or reach us at <a href="mailto:{event.support_email}" style="color: #1a5fb4;">{event.support_email}</a>.
            </td>
          </tr>

          <!-- Sign-off -->
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
        if applicant.is_solo:
            opening = (
                f"Thank you for taking the time and initiative to apply for the {event.name}. "
                f"Our team deeply appreciates the thought and dedication you poured into your application."
            )
            submission_text = "your application"
        else:
            opening = (
                f"Thank you and team {applicant.team_name} for taking the time and initiative to apply "
                f"for the {event.name}. Our team deeply appreciates the thought and dedication your team "
                f"invested in this submission."
            )
            submission_text = f"team {applicant.team_name}'s application"

        return (
            f"Dear {applicant.name},\n\n"
            f"{opening}\n\n"
            f"We received an extraordinary volume of exceptional submissions this year. Due to strict physical "
            f"venue capacity at {event.venue}, our selection process was intensely competitive, and we regret to "
            f"inform you that we are unable to offer {submission_text} an invitation to participate in this edition.\n\n"
            f"Please know that this decision is in no way a reflection of your talent, capability, or potential as "
            f"a creator. With razor-thin margins between applications, many impressive submissions simply could not "
            f"be accommodated. Your trajectory as a builder is never defined by a single weekend—what matters most "
            f"is your curiosity and drive to keep solving real problems.\n\n"
            f"We strongly encourage you to continue developing your ideas, and we would love to see your application "
            f"again in our future events and cohorts.\n\n"
            f"If you have any questions, please feel free to reply directly to this email or reach us at {event.support_email}.\n\n"
            f"Warm regards,\n"
            f"{event.organizer_name}\n"
            f"{event.organizer_address}\n"
            f"{event.support_email}"
        )
