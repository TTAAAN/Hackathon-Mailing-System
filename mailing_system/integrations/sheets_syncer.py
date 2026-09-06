"""Sync Google Sheets recipient records into local SQLite database."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Optional

import gspread
import numpy as np
import pandas as pd

from mailing_system.db.manager import DatabaseManager
from mailing_system.db.repository import (
    ensure_sent_at_column,
    resolve_db_path,
)
from mailing_system.logger import get_logger

logger = get_logger("integrations.sheets_syncer")


class SheetsSyncer:
    """Synchronizes Google Sheets rows into the database."""

    def __init__(self, worksheet: gspread.Worksheet, db_manager: DatabaseManager):
        self.worksheet = worksheet
        self.db = db_manager

    def sync_to_db(self) -> bool:
        """Download all worksheet records and store them in the database table."""
        records = self.worksheet.get_all_records()

        if not records:
            logger.warning("No records found in the specified worksheet.")
            return False

        df = pd.DataFrame(records)
        df.replace("", np.nan, inplace=True)
        df.columns = [str(col).strip().replace(" ", "_").lower() for col in df.columns]

        # Check required ticket_code column
        ticket_col = next((col for col in df.columns if col in ("ticket_code", "ticket_id", "ticket")), None)
        if not ticket_col:
            logger.error("Worksheet is missing required 'ticket_code' column. Canceling the whole procedure.")
            return False

        # Validate that each row has ticket_code
        ticket_series = df[ticket_col].astype(str).str.strip()
        invalid_mask = (
            df[ticket_col].isna()
            | (ticket_series == "")
            | (ticket_series.str.lower() == "nan")
            | (ticket_series.str.lower() == "none")
        )
        if invalid_mask.any():
            logger.error(
                "Found %d row(s) missing 'ticket_code'. Canceling the whole procedure.",
                int(invalid_mask.sum()),
            )
            return False

        # Keep only required recipient fields
        name_col = next((col for col in df.columns if col in ("full_name", "name")), None)
        email_col = next((col for col in df.columns if col in ("email_address", "email")), None)
        team_col = next((col for col in df.columns if col in ("team_name", "team")), None)

        keep_cols = [col for col in (name_col, email_col, team_col, ticket_col) if col is not None]
        if "sent_at" in df.columns:
            keep_cols.append("sent_at")

        df = df[keep_cols]
        if ticket_col != "ticket_code" and "ticket_code" not in df.columns:
            df.rename(columns={ticket_col: "ticket_code"}, inplace=True)

        db_path = resolve_db_path(self.db.db_name)

        try:
            with sqlite3.connect(db_path) as conn:
                df.to_sql(name=self.db.table_name, con=conn, if_exists="fail", index=False)
        except ValueError:
            logger.info(f"Table '{self.db.table_name}' already exists; ensuring schema.")
            return self._ensure_schema(db_path)

        self._ensure_schema(db_path)
        logger.info(f"Successfully loaded {len(df)} rows into table '{self.db.table_name}'.")
        return True

    def _ensure_schema(self, db_path: Path) -> bool:
        try:
            added_sent = ensure_sent_at_column(db_path, self.db.table_name)
            if added_sent:
                logger.info("Added 'sent_at' column to table '%s'.", self.db.table_name)
        except Exception:
            logger.exception("Failed to ensure schema on '%s'.", self.db.table_name)
        return True
