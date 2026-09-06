"""Recipient data repository and SQLite query operations."""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, List, Optional, Set

from mailing_system.config import PROJECT_ROOT
from mailing_system.core.models import Applicant
from mailing_system.logger import get_logger

logger = get_logger("db.repository")


def resolve_db_path(db_name: str | Path) -> Path:
    """Resolve a SQLite database path to an absolute Path under the project root."""
    db_path = Path(db_name)
    if db_path.suffix != ".db":
        db_path = db_path.with_suffix(".db")
    if not db_path.is_absolute():
        db_path = PROJECT_ROOT / db_path
    return db_path


def get_table_columns(conn: sqlite3.Connection, table_name: str) -> Set[str]:
    """Inspect and return existing column names for a table."""
    return {row[1] for row in conn.execute(f"PRAGMA table_info({table_name})").fetchall()}


def pick_column(columns: Set[str], candidates: Iterable[str]) -> Optional[str]:
    """Return the first candidate column name present in the table schema."""
    for candidate in candidates:
        if candidate in columns:
            return candidate
    return None


def ensure_sent_at_column(db_path: Path, table_name: str) -> bool:
    """Add a nullable ``sent_at TEXT`` column to ``table_name`` if missing."""
    with sqlite3.connect(db_path) as conn:
        cols = get_table_columns(conn, table_name)
        if "sent_at" in cols:
            return False
        conn.execute(f"ALTER TABLE {table_name} ADD COLUMN sent_at TEXT")
        conn.commit()
        return True


def update_sent_at_for(
        db_path: Path,
        table_name: str,
        emails: Iterable[str],
        sent_ts: Optional[str] = None,
) -> int:
    """Stamp ``sent_at`` timestamp on rows matching the provided email addresses."""
    cleaned_emails = [str(e).strip() for e in emails if str(e).strip()]
    if not cleaned_emails:
        return 0

    sent_ts = sent_ts or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with sqlite3.connect(db_path) as conn:
        cols = get_table_columns(conn, table_name)
        if "sent_at" not in cols:
            return 0
        email_col = pick_column(cols, ("email_address", "email"))
        if not email_col:
            return 0

        placeholders = ",".join("?" * len(cleaned_emails))
        cur = conn.execute(
            f"UPDATE {table_name} SET sent_at = ? "
            f"WHERE {email_col} IN ({placeholders}) AND (sent_at IS NULL OR TRIM(sent_at) = '')",
            [sent_ts, *cleaned_emails],
        )
        updated = cur.rowcount or 0
        conn.commit()
    return updated


def clean_text(value: Any) -> str:
    """Strip whitespace and convert None to empty string."""
    if value is None:
        return ""
    return str(value).strip()


def load_recipients(
        db_path: Path,
        table_name: str,
        skip_sent: bool = True,
        require_ticket: bool = False,
) -> List[Applicant]:
    """Load recipients from the SQLite database table as Applicant objects."""
    if not db_path.exists():
        raise FileNotFoundError(f"Database file not found: {db_path}")

    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cols = get_table_columns(conn, table_name)

        name_col = pick_column(cols, ("full_name", "name"))
        email_col = pick_column(cols, ("email_address", "email"))
        team_col = pick_column(cols, ("team_name", "team"))
        ticket_col = pick_column(cols, ("ticket_code", "ticket_id", "ticket"))

        missing = [
            label
            for label, col in (("full name", name_col), ("email address", email_col))
            if col is None
        ]
        if require_ticket and ticket_col is None:
            missing.append("ticket_code")

        if missing:
            raise ValueError(
                f"Table '{table_name}' is missing required columns: {', '.join(missing)}"
            )

        selected_cols = [name_col, email_col]
        if team_col:
            selected_cols.append(team_col)
        if ticket_col:
            selected_cols.append(ticket_col)

        where_clauses = [
            f"{email_col} IS NOT NULL",
            f"TRIM({email_col}) != ''",
        ]
        if skip_sent and "sent_at" in cols:
            where_clauses.append("(sent_at IS NULL OR TRIM(COALESCE(sent_at, '')) = '')")

        query = f"SELECT {', '.join(selected_cols)} FROM {table_name} WHERE {' AND '.join(where_clauses)}"
        rows = conn.execute(query).fetchall()

        applicants: List[Applicant] = []
        for row in rows:
            name = clean_text(row[name_col])
            email = clean_text(row[email_col])
            team = clean_text(row[team_col]) if team_col else "Solo Participant"
            ticket_id = clean_text(row[ticket_col]) if ticket_col else ""

            if not name or not email:
                logger.warning("Skipping row with missing name or email: %r", dict(row))
                continue

            if require_ticket and not ticket_id:
                logger.error("Recipient '%s' is missing 'ticket_code'. Canceling procedure.", email)
                raise ValueError(
                    f"Recipient row for '{email}' is missing required 'ticket_code'. Canceling procedure."
                )

            applicants.append(
                Applicant(
                    name=name,
                    email=email,
                    team_name=team or "Solo Participant",
                    ticket_id=ticket_id,
                )
            )

        return applicants
