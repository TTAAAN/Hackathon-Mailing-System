"""HTML and plain-text templates for entry passes with embedded QR code."""

from __future__ import annotations

import html
from typing import Union

from mailing_system.core.models import Applicant, Attendee, EventConfig


class QRTemplate:
    """Generates customized HTML and plain-text entry pass email bodies."""

    @staticmethod
    def render_html(attendee: Union[Attendee, Applicant], event: EventConfig) -> str:
        safe_name = html.escape(str(attendee.name))
        safe_team = html.escape(str(attendee.team_name))
        safe_ticket_id = html.escape(str(attendee.ticket_id))
        safe_email = html.escape(str(attendee.email))
        safe_event_name = html.escape(str(event.name))
        safe_venue = html.escape(str(event.venue))
        safe_date = html.escape(str(event.date))

        return f"""\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{safe_event_name} - Check-in Pass</title>
</head>
<body style="margin: 0; padding: 0; background-color: #ffffff; font-family: Arial, Helvetica, sans-serif; font-size: 15px; line-height: 1.5; color: #222222;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" bgcolor="#ffffff">
    <tr>
      <td align="center" style="padding: 20px 12px;">
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="max-width: 560px; text-align: left;">
          <tr>
            <td style="padding-bottom: 16px; font-size: 15px; color: #333333; line-height: 1.6;">
              Hi {safe_name},<br /><br />
              Once again, <strong>huge congratulations on '{safe_team}' being selected for the {safe_event_name}!</strong><br /><br />
              Below is your <strong>official check-in pass</strong>. You will need this pass to access the venue on the day of the event.
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
                    <!-- 240x240 for optimal scanning distance -->
                    <img src="cid:qr_img" 
                         alt="Check-in QR Code" 
                         width="240" 
                         height="240" 
                         style="display: block; width: 240px; height: 240px; max-width: 100%; border: 0;" />
                    <div style="margin-top: 14px; font-family: Courier, monospace; font-size: 15px; font-weight: bold; color: #111111; letter-spacing: 0.5px;">
                      ID: {safe_ticket_id}
                    </div>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
          <tr>
            <td style="padding-bottom: 24px;">
               <table role="presentation" width="100%" cellspacing="0" cellpadding="8" border="0" style="border-top: 1px solid #eeeeee; border-bottom: 1px solid #eeeeee; font-size: 14px;">
                 <tr><td width="120" style="color: #666666; font-weight: bold;">Attendee Name:</td><td style="color: #111111;">{safe_name}</td></tr>
                 <tr><td style="color: #666666; font-weight: bold;">Check-in ID:</td><td style="color: #111111;">{safe_ticket_id}</td></tr>
                 <tr><td style="color: #666666; font-weight: bold;">Team Name:</td><td style="color: #111111;">{safe_team}</td></tr>
                 <tr><td style="color: #666666; font-weight: bold;">Email:</td><td style="color: #111111;">{safe_email}</td></tr>
                 <tr><td style="color: #666666; font-weight: bold;">Venue:</td><td style="color: #111111;">{safe_venue}</td></tr>
                 <tr><td style="color: #666666; font-weight: bold;">Date:</td><td style="color: #111111;">{safe_date}</td></tr>
               </table>
            </td>
          </tr>
          <tr>
            <td style="padding-bottom: 20px; font-size: 14px; color: #333333; line-height: 1.6;">
              <strong>Questions or need support?</strong><br />
              Reply directly to this email or reach out to <a href="mailto:{event.support_email}" style="color: #1a5fb4;">{event.support_email}</a>.<br />
              For fast support, message us on Telegram: <a href="https://t.me/ITMTechnicalSupport" target="_blank" style="color: #1a5fb4; text-decoration: none; font-weight: bold;">@ITMTechnicalSupport</a>
            </td>
          </tr>
          <tr>
            <td style="padding-top: 16px; border-top: 1px solid #eeeeee; font-size: 12px; color: #888888; line-height: 1.6;">
              {event.organizer_name} &middot; {event.organizer_address}<br />
              Email: <a href="mailto:{event.support_email}" style="color: #888888;">{event.support_email}</a> &middot; Telegram: <a href="https://t.me/ITMTechnicalSupport" target="_blank" style="color: #888888;">@ITMTechnicalSupport</a>
            </td>
          </tr>

          <!-- Banner -->
          <tr>
            <td style="padding-top: 32px;">
              <img src="cid:banner_img" alt="{safe_event_name} Banner" width="560" style="display: block; width: 100%; max-width: 560px; height: auto; border: 0;" />
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
            f"{event.name.upper()} — YOUR CHECK-IN PASS\n\n"
            f"Hi {attendee.name},\n\n"
            f"Congratulations on '{attendee.team_name}' being selected for the {event.name}!\n\n"
            f"Below are your check-in details. Please present your Check-in ID or QR code at the registration desk.\n\n"
            f"PASS DETAILS\n"
            f"Attendee Name: {attendee.name}\n"
            f"Check-in ID:   {attendee.ticket_id}\n"
            f"Team Name:     {attendee.team_name}\n"
            f"Email:         {attendee.email}\n"
            f"Venue:         {event.venue}\n"
            f"Date:          {event.date}\n\n"
            f"Need help? Contact: {event.support_email}\n"
            f"Fast Support (Telegram): @ITMTechnicalSupport (https://t.me/ITMTechnicalSupport)\n"
            f"--\n{event.organizer_name}\n{event.organizer_address}"
        )