"""HTML and plain-text templates for entry passes with embedded QR code."""

from __future__ import annotations

from typing import Union

from mailing_system.core.models import Applicant, Attendee, EventConfig


class PassTemplate:
    """Generates customized HTML and plain-text entry pass email bodies."""

    @staticmethod
    def render_html(attendee: Union[Attendee, Applicant], event: EventConfig) -> str:
        return f"""\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{event.name} - Entry Pass</title>
</head>
<body style="margin: 0; padding: 0; background-color: #ffffff; font-family: Arial, Helvetica, sans-serif; font-size: 15px; line-height: 1.5; color: #222222;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" bgcolor="#ffffff">
    <tr>
      <td align="center" style="padding: 20px 12px;">
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="max-width: 560px; text-align: left;">
          <tr>
            <td style="padding-bottom: 24px;">
              <img src="cid:banner_img" alt="{event.name} Banner" width="560" style="display: block; width: 100%; max-width: 560px; height: auto; border: 0;" />
            </td>
          </tr>
          <tr>
            <td style="padding-bottom: 16px; font-size: 22px; font-weight: bold; color: #111111;">
              Your Official Hackathon Entry Pass
            </td>
          </tr>
          <tr>
            <td style="padding-bottom: 16px; font-size: 15px; color: #333333; line-height: 1.6;">
              Hi {attendee.name},<br /><br />
              Once again, <strong>huge congratulations on {attendee.team_name} being selected for the {event.name}!</strong> We were incredibly impressed by your application and are thrilled to welcome you.<br /><br />
              Below is your <strong>official check-in ticket</strong>. You will need this pass to access the venue on the day of the event.
            </td>
          </tr>
          <tr>
            <td style="padding-bottom: 20px; font-size: 15px; color: #333333; line-height: 1.6;">
              <strong>Check-in Instructions:</strong><br />
              When you arrive at the venue, please proceed to the registration desk and present the QR code below. Please arrive at least 30 minutes before kickoff.
            </td>
          </tr>
          <tr>
            <td align="center" style="padding: 8px 0 24px 0;">
              <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center">
                <tr>
                  <td align="center" style="border: 1px solid #cccccc; padding: 18px; background-color: #ffffff; border-radius: 8px;">
                    <img src="cid:qr_img" alt="Entry QR Code" width="200" height="200" style="display: block; width: 200; height: 200; max-width: 100%; border: 0;" />
                    <div style="margin-top: 14px; font-family: Courier, monospace; font-size: 16px; font-weight: bold; color: #111111; letter-spacing: 0.5px;">
                      Scan This
                    </div>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
          <tr>
            <td style="padding-bottom: 24px;">
               <table role="presentation" width="100%" cellspacing="0" cellpadding="8" border="0" style="border-top: 1px solid #eeeeee; border-bottom: 1px solid #eeeeee; font-size: 14px;">
                 <tr><td width="120" style="color: #666666; font-weight: bold;">Attendee ID:</td><td style="color: #111111;">{attendee.name}</td></tr>
                 <tr><td style="color: #666666; font-weight: bold;">Participant ID:</td><td style="color: #111111;">{attendee.ticket_id}</td></tr>
                 <tr><td style="color: #666666; font-weight: bold;">Team Name:</td><td style="color: #111111; font-weight: bold;">{attendee.team_name}</td></tr>
                 <tr><td style="color: #666666; font-weight: bold;">Email:</td><td style="color: #111111;">{attendee.email}</td></tr>
                 <tr><td style="color: #666666; font-weight: bold;">Venue:</td><td style="color: #111111;">{event.venue}</td></tr>
                 <tr><td style="color: #666666; font-weight: bold;">Date:</td><td style="color: #111111;">{event.date}</td></tr>
               </table>
            </td>
          </tr>
          <tr>
            <td style="padding-bottom: 20px; font-size: 14px; color: #333333; line-height: 1.6;">
              <strong>Questions or need support?</strong><br />
              Reply directly to this email or reach out to <a href="mailto:{event.support_email}" style="color: #1a5fb4;">{event.support_email}</a>.
            </td>
          </tr>
          <tr>
            <td style="padding-top: 16px; border-top: 1px solid #eeeeee; font-size: 12px; color: #888888; line-height: 1.6;">
              {event.organizer_name} &middot; {event.organizer_address}<br />
              Support: <a href="mailto:{event.support_email}" style="color: #888888;">{event.support_email}</a>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""

    @staticmethod
    def render_plain(attendee: Union[Attendee, Applicant], event: EventConfig) -> str:
        return (
            f"{event.name.upper()} — YOUR ENTRY PASS\n\n"
            f"Hi {attendee.name},\n\n"
            f"Congratulations on {attendee.team_name} being selected for the {event.name}!\n\n"
            f"Participant ID: {attendee.ticket_id}\n\n"
            f"PASS DETAILS\n"
            f"Attendee: {attendee.name}\n"
            f"Team: {attendee.team_name}\n"
            f"Email: {attendee.email}\n"
            f"Venue: {event.venue}\n"
            f"Date: {event.date}\n\n"
            f"Please present your Participant ID or QR Code at the registration desk.\n\n"
            f"Need help? Contact: {event.support_email}\n"
            f"--\n{event.organizer_name}\n{event.organizer_address}"
        )


QRTemplate = PassTemplate
