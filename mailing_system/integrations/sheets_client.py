"""Google Sheets API client helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import gspread

from mailing_system.config import PROJECT_ROOT


def get_sheet_from_config(config: Dict[str, Any]) -> gspread.Worksheet:
    """Create and return a configured Google Worksheet client."""
    cfg = config["google_sheets"]

    credentials_path = Path(cfg["credentials_path"])
    if not credentials_path.is_absolute():
        credentials_path = PROJECT_ROOT / credentials_path

    gc = gspread.service_account(
        filename=str(credentials_path),
        scopes=cfg.get("scopes", ["https://www.googleapis.com/auth/spreadsheets"]),
    )
    sh = gc.open_by_key(cfg["spreadsheet_key"])
    return sh.get_worksheet_by_id(cfg["worksheet_id"])
