"""Centralized logging setup for the mailing system.

Emits formatted records to both stderr and size-rotated log files in GMT+7.
"""

from __future__ import annotations

import logging
import sys
from datetime import datetime, timedelta, timezone
from logging.handlers import RotatingFileHandler
from pathlib import Path

from mailing_system.config import PROJECT_ROOT

GMT_PLUS_7 = timezone(timedelta(hours=7))
LOG_DIR = PROJECT_ROOT / "logs"
LOG_FILE = LOG_DIR / "app.log"
MAX_BYTES = 10 * 1024 * 1024
BACKUP_COUNT = 5

_FORMAT = "[%(asctime)s] - [%(levelname)s] - [%(name)s]: %(message)s"
_DATEFMT = "%Y-%m-%d %H:%M:%S %z"


class GMT7Formatter(logging.Formatter):
    """Formatter that renders timestamps in GMT+7 regardless of host timezone."""

    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, tz=GMT_PLUS_7)
        return dt.strftime(datefmt or _DATEFMT)


_configured = False


def _configure_root_logging() -> None:
    """Attach universal handlers to the root logger exactly once."""
    global _configured
    if _configured:
        return

    root = logging.getLogger()
    _configured = True

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=MAX_BYTES,
        backupCount=BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(logging.INFO)

    formatter = GMT7Formatter(_FORMAT, datefmt=_DATEFMT)
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    root.addHandler(file_handler)
    root.addHandler(console_handler)
    root.setLevel(logging.DEBUG)


def get_logger(name: str) -> logging.Logger:
    """Return a logger configured with universal handlers.

    Args:
        name: Logger component name (e.g. "mailers.acceptance", "db.repository").
    """
    _configure_root_logging()
    return logging.getLogger(name)
