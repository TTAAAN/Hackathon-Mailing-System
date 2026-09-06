import sqlite3
import tempfile
import unittest
from pathlib import Path

from mailing_system.db.repository import (
    ensure_sent_at_column,
    ensure_ticket_code_column,
    load_recipients,
    update_sent_at_for,
)


class RepositoryTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_recipients.db"
        self.table_name = "recipients"

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                f"""
                CREATE TABLE {self.table_name} (
                    full_name TEXT,
                    email_address TEXT,
                    team_name TEXT,
                    ticket_code TEXT
                )
                """
            )
            conn.execute(
                f"INSERT INTO {self.table_name} VALUES ('Alice', 'alice@example.com', 'TeamA', 'TCK-1')"
            )
            conn.execute(
                f"INSERT INTO {self.table_name} VALUES ('Bob', 'bob@example.com', 'Solo Participant', 'TCK-2')"
            )
            conn.commit()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_ensure_sent_at_column(self):
        added = ensure_sent_at_column(self.db_path, self.table_name)
        self.assertTrue(added)

        # Second call should return False (already exists)
        added_again = ensure_sent_at_column(self.db_path, self.table_name)
        self.assertFalse(added_again)

    def test_ensure_ticket_code_column(self):
        # Table already has ticket_code column -> should return False
        self.assertFalse(ensure_ticket_code_column(self.db_path, self.table_name))

        # Create table without ticket_code and test adding it
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("CREATE TABLE other_table (full_name TEXT, email_address TEXT)")
        self.assertTrue(ensure_ticket_code_column(self.db_path, "other_table"))
        self.assertFalse(ensure_ticket_code_column(self.db_path, "other_table"))

    def test_load_recipients(self):
        recipients = load_recipients(self.db_path, self.table_name, require_ticket=True)
        self.assertEqual(len(recipients), 2)
        self.assertEqual(recipients[0].name, "Alice")
        self.assertEqual(recipients[0].email, "alice@example.com")
        self.assertEqual(recipients[0].team_name, "TeamA")
        self.assertEqual(recipients[0].ticket_id, "TCK-1")
        self.assertFalse(recipients[0].is_solo)

        self.assertEqual(recipients[1].name, "Bob")
        self.assertEqual(recipients[1].ticket_id, "TCK-2")
        self.assertTrue(recipients[1].is_solo)

    def test_load_recipients_missing_ticket_code_cancels(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(f"INSERT INTO {self.table_name} VALUES ('Charlie', 'charlie@example.com', 'TeamC', '')")
            conn.commit()

        with self.assertRaises(ValueError):
            load_recipients(self.db_path, self.table_name, require_ticket=True)

    def test_update_sent_at_for(self):
        ensure_sent_at_column(self.db_path, self.table_name)
        updated = update_sent_at_for(self.db_path, self.table_name, ["alice@example.com"])
        self.assertEqual(updated, 1)

        # Loading recipients with skip_sent=True should now only return Bob
        unsent = load_recipients(self.db_path, self.table_name, skip_sent=True)
        self.assertEqual(len(unsent), 1)
        self.assertEqual(unsent[0].email, "bob@example.com")


if __name__ == "__main__":
    unittest.main()
