"""Command-line interfaces."""

from mailing_system.cli.main import main
from mailing_system.cli.send import run_send
from mailing_system.cli.sync import run_sync

__all__ = ["main", "run_send", "run_sync"]
