import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock

from mailing_system.db.manager import DatabaseManager
from mailing_system.db.repository import load_recipients, resolve_db_path
from mailing_system.integrations.sheets_syncer import SheetsSyncer


class SyncerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_name = str(Path(self.temp_dir.name) / "test_syncer_db.db")
        self.table_name = "test_recipients"
        self.db_manager = DatabaseManager(self.db_name, self.table_name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_sync_to_db(self):
        mock_worksheet = MagicMock()
        mock_worksheet.get_all_records.return_value = [
            {"Full Name": "Alice Wonderland", "Email Address": "alice@test.com", "Team Name": "Wonderland", "Extra Col": "ignored"},
            {"Full Name": "Bob Builder", "Email Address": "bob@test.com", "Team Name": "Solo Participant", "Other": "123"},
        ]

        syncer = SheetsSyncer(mock_worksheet, self.db_manager)
        success = syncer.sync_to_db()
        self.assertTrue(success)

        db_path = resolve_db_path(self.db_name)
        recipients = load_recipients(db_path, self.table_name)
        self.assertEqual(len(recipients), 2)
        self.assertEqual(recipients[0].name, "Alice Wonderland")
        self.assertEqual(recipients[0].email, "alice@test.com")
        self.assertEqual(recipients[0].team_name, "Wonderland")
        self.assertEqual(recipients[1].name, "Bob Builder")
        self.assertTrue(recipients[1].is_solo)


if __name__ == "__main__":
    unittest.main()
