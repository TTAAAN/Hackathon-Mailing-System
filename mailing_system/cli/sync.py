"""CLI entry point to sync recipient data from Google Sheets to SQLite."""

from __future__ import annotations

import argparse
import sys

from mailing_system.config import load_config
from mailing_system.db.manager import DatabaseManager
from mailing_system.integrations.sheets_client import get_sheet_from_config
from mailing_system.integrations.sheets_syncer import SheetsSyncer
from mailing_system.logger import get_logger

logger = get_logger("cli.sync")


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Sync recipient data from Google Sheets into local SQLite database."
    )
    parser.add_argument(
        "--config",
        "-c",
        default=None,
        help="Path to custom config.yaml file (default: config.yaml).",
    )
    return parser


def run_sync(config_file: str | None = None) -> int:
    config = load_config(config_file)
    if not config:
        logger.error("Configuration file is missing or empty.")
        return 1

    db_cfg = config.get("database", {})
    db_name = db_cfg.get("name", "recipients_db")
    table_name = db_cfg.get("table_name", "recipients")

    logger.info("Connecting to Google Sheets...")
    worksheet = get_sheet_from_config(config)
    db_manager = DatabaseManager(db_name=db_name, table_name=table_name)

    syncer = SheetsSyncer(worksheet, db_manager)
    success = syncer.sync_to_db()
    return 0 if success else 1


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()
    return run_sync(args.config)


if __name__ == "__main__":
    sys.exit(main())
