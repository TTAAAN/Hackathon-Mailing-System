"""Core data models and domain entities for the mailing system."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from mailing_system.config import PROJECT_ROOT


@dataclass(frozen=True)
class EventConfig:
    """Encapsulates fixed event metadata and branding."""
    name: str = "ITM Innovation Hackathon 2026"
    date: str = "12, 13, and 19th September 2026"
    venue: str = "American University of Phnom Penh (AUPP)"
    organizer_name: str = "ITM Innovation Hackathon Team"
    organizer_address: str = "American University of Phnom Penh, Phnom Penh, Cambodia"
    support_email: str = "support@itm-hackathon.tech"
    banner_image_path: Union[str, Path] = (
        PROJECT_ROOT / "mailing_system" / "templates" / "assets" / "banner.png"
    )
    telegram_link: str = ""


@dataclass(frozen=True)
class Attendee:
    """Individual pass holder data."""
    name: str
    email: str
    team_name: str
    ticket_id: str

    @property
    def ticket_code(self) -> str:
        return self.ticket_id

    @property
    def is_solo(self) -> bool:
        return not self.team_name or self.team_name.strip().lower() == "solo participant"


@dataclass(frozen=True)
class Applicant:
    """Recipient data model representing a hackathon applicant / attendee."""
    name: str
    email: str
    team_name: str = "Solo Participant"
    ticket_id: str = ""

    @property
    def ticket_code(self) -> str:
        return self.ticket_id

    @property
    def is_solo(self) -> bool:
        return not self.team_name or self.team_name.strip().lower() == "solo participant"


@dataclass
class DeliveryResult:
    """Outcome report for an email delivery attempt."""
    recipient_email: str
    ticket_id: Optional[str] = None
    name: Optional[str] = None
    team_name: Optional[str] = None
    status: str = "FAILED"
    http_status: Optional[int] = None
    zepto_code: Optional[str] = None
    error_message: Optional[str] = None
    details: Optional[List[Dict[str, Any]]] = None
    request_id: Optional[str] = None
    attempts: int = 0
    timestamp: Optional[str] = None
