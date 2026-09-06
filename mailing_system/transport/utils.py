"""Transport helpers: encoding, reporting, and timestamps."""

from __future__ import annotations

import base64
import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, List, Optional, Tuple

from mailing_system.core.models import DeliveryResult
from mailing_system.logger import get_logger

logger = get_logger("transport.utils")


def utc_now_iso() -> str:
    """Return the current UTC timestamp in ISO-8601 with a 'Z' suffix."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def encode_image(image_path: Path | str) -> Optional[str]:
    """Read an image file and return its base64-encoded string."""
    try:
        path = Path(image_path)
        if not path.exists():
            logger.warning("Image file not found: %s", path)
            return None
        with open(path, "rb") as fh:
            return base64.b64encode(fh.read()).decode("utf-8")
    except Exception:
        logger.exception("Failed to encode image: %s", image_path)
        return None


def send_and_report(
    send_fn: Callable[[Any], DeliveryResult],
    recipients: List[Any],
    success_report_path: Path,
    failed_report_path: Path,
) -> Tuple[List[DeliveryResult], List[DeliveryResult]]:
    """Execute ``send_fn`` on each recipient, partition results, and write JSON reports."""
    successes: List[DeliveryResult] = []
    failures: List[DeliveryResult] = []

    for recipient in recipients:
        result = send_fn(recipient)
        if result.status == "SUCCESS":
            successes.append(result)
        else:
            failures.append(result)

    failed_report_path.parent.mkdir(parents=True, exist_ok=True)
    success_report_path.parent.mkdir(parents=True, exist_ok=True)

    with open(failed_report_path, "w", encoding="utf-8") as f:
        json.dump([asdict(i) for i in failures], f, indent=2)

    with open(success_report_path, "w", encoding="utf-8") as f:
        json.dump([asdict(i) for i in successes], f, indent=2)

    return successes, failures
