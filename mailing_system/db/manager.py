"""Database manager and connection engine."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import create_async_engine

from mailing_system.logger import get_logger

logger = get_logger("db.manager")


class DatabaseManager:
    """Encapsulates SQLite database connection and engine initialization."""

    def __init__(self, db_name: str, table_name: str):
        """Initialize the database manager.

        Args:
            db_name: SQLite database file name (with or without .db extension).
            table_name: Default table name for recipient operations.
        """
        self.db_name = db_name if db_name.endswith(".db") else f"{db_name}.db"
        self.table_name = table_name
        self.engine = create_async_engine(
            f"sqlite+aiosqlite:///{self.db_name}",
            future=True,
        )

    def get_engine(self):
        """Return the configured SQLAlchemy async engine."""
        return self.engine
