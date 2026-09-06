"""Unified CLI dispatcher for the Hackathon Mailing System."""

from __future__ import annotations

import argparse
import sys

from mailing_system.cli.send import build_arg_parser as build_send_parser, run_send
from mailing_system.cli.sync import build_arg_parser as build_sync_parser, run_sync


def build_root_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mailing-system",
        description="Hackathon Mailing System: Sync attendee data and dispatch email campaigns.",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # 'send' subcommand
    send_sub = subparsers.add_parser(
        "send",
        help="Send acceptance or rejection email campaigns to applicants.",
        parents=[build_send_parser()],
        conflict_handler="resolve",
    )

    # 'sync' subcommand
    sync_sub = subparsers.add_parser(
        "sync",
        help="Sync recipient records from Google Sheets to local SQLite database.",
        parents=[build_sync_parser()],
        conflict_handler="resolve",
    )

    return parser


def main() -> int:
    parser = build_root_parser()
    args, unknown = parser.parse_known_args()

    # If invoked directly with send flags (e.g. `--mode accept` without specifying `send`)
    if args.command is None:
        if "--mode" in sys.argv or "--confirm" in sys.argv:
            send_parser = build_send_parser()
            send_args = send_parser.parse_args()
            return run_send(
                mode=send_args.mode,
                confirm=send_args.confirm,
                limit=send_args.limit,
                region=send_args.region,
                token=send_args.token,
                config_file=send_args.config,
            )
        parser.print_help()
        return 0

    if args.command == "send":
        return run_send(
            mode=args.mode,
            confirm=args.confirm,
            limit=args.limit,
            region=args.region,
            token=args.token,
            config_file=args.config,
        )
    elif args.command == "sync":
        return run_sync(config_file=args.config)

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
