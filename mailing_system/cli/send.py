"""CLI entry point for dispatching acceptance, rejection, and QR pass emails."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional

from mailing_system.config import load_config
from mailing_system.core.models import Applicant, DeliveryResult, EventConfig
from mailing_system.db.repository import load_recipients, resolve_db_path, update_sent_at_for
from mailing_system.logger import get_logger
from mailing_system.mailers.acceptance import AcceptanceMailer
from mailing_system.mailers.qr import QRMailer
from mailing_system.mailers.rejection import RejectionMailer

logger = get_logger("cli.send")


def build_arg_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser for sending emails."""
    parser = argparse.ArgumentParser(
        description="Mailing utility: send acceptance, rejection, or QR pass emails to recipients."
    )
    parser.add_argument(
        "--mode",
        choices=("accept", "reject", "qr", "pass"),
        default="accept",
        help="Type of notification to send: accept, reject, qr, or pass (default: accept).",
    )
    parser.add_argument(
        "--confirm",
        action="store_true",
        help="Actually send emails. Without this flag, the command runs in dry-run mode.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optionally limit delivery to the first N recipients.",
    )
    parser.add_argument(
        "--region",
        default="us",
        help="ZeptoMail region to use: us, eu, in, au, ca, sa (default: us).",
    )
    parser.add_argument(
        "--token",
        default=None,
        help="ZeptoMail Send-Mail token (defaults to ZEPTOMAIL_TOKEN env var).",
    )
    parser.add_argument(
        "--config",
        "-c",
        default=None,
        help="Path to custom config.yaml file (default: config.yaml).",
    )
    return parser


def run_send(
    mode: str = "accept",
    confirm: bool = False,
    limit: Optional[int] = None,
    region: str = "us",
    token: Optional[str] = None,
    config_file: Optional[str] = None,
) -> int:
    config = load_config(config_file)
    db_cfg = config.get("database", {})
    db_name = db_cfg.get("name", "recipients_db")
    table_name = db_cfg.get("table_name", "recipients")
    db_path = resolve_db_path(db_name)

    require_ticket = mode in ("qr", "pass")
    logger.info("Loading recipients from %s [%s] (mode=%s)...", db_path, table_name, mode)
    try:
        recipients = load_recipients(db_path, table_name, skip_sent=True, require_ticket=require_ticket)
    except Exception as exc:
        logger.error("Failed to load records from database: %s", exc)
        return 1

    if not recipients:
        logger.info("No unsent recipients found in %s.%s.", db_name, table_name)
        return 0

    if require_ticket:
        missing_tickets = [r for r in recipients if not (r.ticket_id or "").strip()]
        if missing_tickets:
            logger.error("Found %d recipient(s) without ticket_code. Canceling procedure.", len(missing_tickets))
            return 1

    if limit and limit > 0:
        recipients = recipients[:limit]
        logger.info("Applied limit: will process %d recipient(s).", len(recipients))

    logger.info("Loaded %d unsent recipient(s) for delivery.", len(recipients))

    if not confirm:
        logger.info("DRY RUN: no emails will be sent. Re-run with --confirm to attempt delivery.")
        preview = recipients[:10]
        for r in preview:
            ticket_info = f" | Ticket: {r.ticket_id}" if r.ticket_id else ""
            logger.info("DRY RUN: %s <%s> | Team: %s%s", r.name, r.email, r.team_name, ticket_info)
        if len(recipients) > len(preview):
            logger.info("DRY RUN: ... and %d more records", len(recipients) - len(preview))
        return 0

    # User confirmation before sending
    token = token or os.environ.get("ZEPTOMAIL_TOKEN") or ""
    if not token:
        logger.error("Missing ZEPTOMAIL_TOKEN. Set it in your environment or pass --token.")
        return 1

    prompt = (
        f"Ready to send {len(recipients)} {mode.upper()} email(s) via ZeptoMail ({region.upper()}).\n"
        "Type 'YES' to proceed: "
    )
    try:
        confirmation = input(prompt)
    except (EOFError, KeyboardInterrupt):
        logger.info("\nAborted by user.")
        return 1

    if confirmation.strip() != "YES":
        logger.info("Confirmation was not 'YES'; aborting delivery.")
        return 1

    event_cfg_data = config.get("event", {})
    event_config = EventConfig(**event_cfg_data) if event_cfg_data else EventConfig()

    mail_cfg = config.get("mailing", {})
    sender_email = mail_cfg.get("sender_email")
    sender_name = mail_cfg.get("sender_name")
    reply_to_email = mail_cfg.get("reply_to_email")
    reply_to_name = mail_cfg.get("reply_to_name")

    if mode in ("qr", "pass"):
        mailer = QRMailer(
            token=token,
            region=region,
            sender_email=sender_email,
            sender_name=sender_name,
            reply_to_email=reply_to_email,
            reply_to_name=reply_to_name,
            event_config=event_config,
        )
    elif mode == "accept":
        mailer = AcceptanceMailer(
            token=token,
            region=region,
            sender_email=sender_email,
            sender_name=sender_name,
            reply_to_email=reply_to_email,
            reply_to_name=reply_to_name,
            event_config=event_config,
        )
    else:
        mailer = RejectionMailer(
            token=token,
            region=region,
            sender_email=sender_email,
            sender_name=sender_name,
            reply_to_email=reply_to_email,
            reply_to_name=reply_to_name,
            event_config=event_config,
        )

    logger.info("Beginning batch email delivery (%s)...", mode)
    try:
        successes, failures = mailer.send_batch(recipients)
    except Exception as exc:
        logger.exception("Unexpected error during sending: %s", exc)
        return 1
    finally:
        mailer.close()

    if successes:
        emails = [r.recipient_email for r in successes if getattr(r, "recipient_email", None)]
        if emails:
            try:
                updated = update_sent_at_for(db_path, table_name, emails)
                logger.info("Stamped sent_at on %d delivered recipient(s).", updated)
            except Exception:
                logger.exception("Failed to update sent_at in database.")

    logger.info("Delivery complete: %d succeeded, %d failed.", len(successes), len(failures))
    return 0 if not failures else 1


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()
    return run_send(
        mode=args.mode,
        confirm=args.confirm,
        limit=args.limit,
        region=args.region,
        token=args.token,
        config_file=args.config,
    )


if __name__ == "__main__":
    sys.exit(main())
