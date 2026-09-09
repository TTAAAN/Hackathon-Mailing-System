"""HTML and plain-text templates for dropped participants who are unable to attend."""

from __future__ import annotations

from mailing_system.core.models import Applicant, EventConfig


class DroppedTemplate:
    """Generates customized HTML and plain-text emails for participants marked as dropped."""

    @staticmethod
    def render_html(applicant: Applicant, event: EventConfig) -> str:
        greeting = f"Dear {applicant.name},"

        if applicant.is_solo:
            opening = (
                f"Thank you for reaching out and letting us know regarding your availability for the {event.name}. "
                f"We have officially recorded your response that you will be unable to join us for this edition."
            )
            participant_mention = "you"
        else:
            opening = (
                f"Thank you for reaching out and letting us know regarding your team's availability for the {event.name}. "
                f"We have officially recorded your response that team '{applicant.team_name}' will be unable to join us for this edition."
            )
            participant_mention = f"team '{applicant.team_name}'"

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

          <!-- Regret & Recognition of Passing -->
          <tr>
            <td style="padding-bottom: 16px; font-size: 15px; color: #333333; line-height: 1.6;">
              Having successfully passed the selection stage, your application stood out for its creativity and technical promise. While we are genuinely sorry that we won't see {participant_mention} on event day, we completely understand that schedule conflicts and unexpected commitments can arise.
            </td>
          </tr>

          <!-- Releasing Spot & Appreciation -->
          <tr>
            <td style="padding-bottom: 16px; font-size: 15px; color: #333333; line-height: 1.6;">
              We truly appreciate you taking the time to inform us in advance. By letting us know early, you have allowed us to offer this spot to an applicant on our waiting list.
            </td>
          </tr>

          <!-- Hope to see again in future seasons -->
          <tr>
            <td style="padding-bottom: 20px; font-size: 15px; color: #333333; line-height: 1.6;">
              Given the strength of your submission, we would love to see you apply again for our future seasons and upcoming programs. We hope you will stay connected with our community and follow our future announcements.
            </td>
          </tr>

          <!-- Support & Mistake Check -->
          <tr>
            <td style="padding-bottom: 24px; font-size: 15px; color: #333333; line-height: 1.6;">
              If this was sent in error or if your availability happens to change, please do not hesitate to contact us immediately at <a href="mailto:{event.support_email}" style="color: #1a5fb4;">{event.support_email}</a>.
            </td>
          </tr>

          <!-- Sign-off -->
          <tr>
            <td style="padding-top: 16px; border-top: 1px solid #eeeeee; font-size: 12px; color: #888888; line-height: 1.6;">
              Warm regards,<br />
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
                f"Thank you for reaching out and letting us know regarding your availability for the {event.name}. "
                f"We have officially recorded your response that you will be unable to join us for this edition."
            )
            participant_mention = "you"
        else:
            opening = (
                f"Thank you for reaching out and letting us know regarding your team's availability for the {event.name}. "
                f"We have officially recorded your response that team '{applicant.team_name}' will be unable to join us for this edition."
            )
            participant_mention = f"team '{applicant.team_name}'"

        return (
            f"Dear {applicant.name},\n\n"
            f"{opening}\n\n"
            f"Having successfully passed the selection stage, your application stood out for its creativity and "
            f"technical promise. While we are genuinely sorry that we won't see {participant_mention} on event day, "
            f"we completely understand that schedule conflicts and unexpected commitments can arise.\n\n"
            f"We truly appreciate you taking the time to inform us in advance. By letting us know early, you have "
            f"allowed us to offer this spot to an applicant on our waiting list.\n\n"
            f"Given the strength of your submission, we would love to see you apply again for our future seasons "
            f"and upcoming programs. We hope you will stay connected with our community and follow our future announcements.\n\n"
            f"If this was sent in error or if your availability happens to change, please reach out to us immediately "
            f"at {event.support_email}.\n\n"
            f"Warm regards,\n"
            f"{event.organizer_name}\n"
            f"Support: {event.support_email}"
        )
