"""Project configuration loader and environment resolver."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_config(config_file: str | Path | None = None) -> Dict[str, Any]:
    """Load project configuration from YAML.

    Relative paths are resolved against PROJECT_ROOT so callers can use the
    default ``config.yaml`` from any working directory.
    """
    if config_file is None:
        config_path = PROJECT_ROOT / "config.yaml"
    else:
        config_path = Path(config_file)
        if not config_path.is_absolute():
            config_path = PROJECT_ROOT / config_path

    if not config_path.exists():
        return {}

    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}
