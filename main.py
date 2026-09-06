#!/usr/bin/env python3
"""Project root entry point for the Hackathon Mailing System."""

import sys
from pathlib import Path

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from mailing_system.cli.main import main
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env file
    sys.exit(main())
