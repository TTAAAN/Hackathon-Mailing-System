"""HTML and plain-text templates for reserved attendance confirmation emails."""

from __future__ import annotations

from mailing_system.core.models import Applicant, EventConfig


class ReservedConfirmationTemplate:
    """Generates customized HTML and plain-text emails confirming a reserved spot after attendance verification."""

    @staticmethod
    def render_html(applicant: Applicant, event: EventConfig) -> str:
        greeting = f"Dear {applicant.name},"

        if applicant.is_solo:
            opening_paragraph = (
                f"Thank you for verifying your availability! We have received your confirmation that you can attend, "
                f"and <strong>your reserved spot for the {event.name} is now officially secured.</strong>"
            )
        else:
            opening_paragraph = (
                f"Thank you for verifying your availability! We have received confirmation that your team "
                f"'{applicant.team_name}' can attend, and <strong>your reserved spot for the {event.name} "
                f"is now officially secured.</strong>"
            )

        telegram_section = (
            f'Please make sure to join our official <a href="{event.telegram_link}" style="color: #1a5fb4; font-weight: bold; text-decoration: underline;">Participant Telegram Group</a>. All important schedule updates, mentor announcements, and challenges will be coordinated through this channel.'
            if event.telegram_link
            else "All important schedule updates, mentor announcements, and challenges will be coordinated via email."
        )

        return f"""\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{event.name} - Reserved Spot Confirmed</title>
</head>
<body style="margin: 0; padding: 0; background-color: #ffffff; font-family: Arial, Helvetica, sans-serif; font-size: 15px; line-height: 1.6; color: #222222;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" bgcolor="#ffffff">
    <tr>
      <td align="center" style="padding: 24px 12px;">
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="max-width: 560px; text-align: left;">

          <!-- Greeting & Confirmation -->
          <tr>
            <td style="padding-bottom: 16px; font-size: 15px; color: #333333; line-height: 1.6;">
              {greeting}<br /><br />
              {opening_paragraph}
            </td>
          </tr>

          <!-- Context & Acknowledgment -->
          <tr>
            <td style="padding-bottom: 16px; font-size: 15px; color: #333333; line-height: 1.6;">
              We truly appreciate your prompt response and commitment to join us. We are preparing an intensive, exciting event packed with collaboration and hands-on building, and we are glad to have you with us.
            </td>
          </tr>

          <!-- Dates & Venue -->
          <tr>
            <td style="padding-bottom: 16px; font-size: 15px; color: #333333; line-height: 1.6;">
              The event will be held at <strong>{event.venue}</strong> on <strong>{event.date}</strong>.<br /><br />
              {telegram_section}
            </td>
          </tr>

          <!-- Logistics & Changes -->
          <tr>
            <td style="padding-bottom: 24px; font-size: 15px; color: #333333; line-height: 1.6;">
              Please make sure your laptop, chargers, and development setup are ready for the event. If your availability changes or if an emergency arises, please notify us immediately through one of our team member in the telegram group.
            </td>
          </tr>

          <!-- Sign-off -->
          <tr>
            <td style="padding-bottom: 24px; font-size: 15px; color: #333333; line-height: 1.6;">
              We look forward to welcoming you at {event.venue}!
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
        target_mention = "your reserved spot" if applicant.is_solo else f"the reserved spot for team '{applicant.team_name}'"
        telegram_info = (
            f"Please join our official Participant Telegram Group right away for all announcements and updates:\n{event.telegram_link}\n\n"
            if event.telegram_link
            else ""
        )

        return (
            f"Dear {applicant.name},\n\n"
            f"Thank you for verifying your availability! We have received your confirmation that you can attend, "
            f"and {target_mention} for the {event.name} is now officially secured.\n\n"
            f"We truly appreciate your prompt response and commitment. We are preparing an intensive, exciting event "
            f"packed with collaboration and hands-on building, and we are glad to have you with us.\n\n"
            f"The event will take place at {event.venue} on {event.date}.\n\n"
            f"{telegram_info}"
            f"Please make sure your laptop, chargers, and development setup are ready. If your availability changes "
            f"or an emergency arises, please notify us immediately by contacting one of our team in telegram.\n\n"
            f"We look forward to welcoming you at {event.venue}!\n\n"
            f"Warm regards,\n"
            f"{event.organizer_name}\n"
            f"{event.organizer_address}\n"
            f"{event.support_email}"
        )
