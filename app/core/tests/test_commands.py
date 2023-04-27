"""
Test custom Django management commands.
"""

# mock behavior of database response
from unittest.mock import patch

# possible errors when connecting to db before ready
from psycopg2 import OperationalError as Psycopg2Error

# simulate calling a command
from django.core.management import call_command

# db error depending on other operational error
from django.db.utils import OperationalError

# simple test case .. do not need db setup or migration
from django.test import SimpleTestCase


# path to command to be mocked
@patch("core.management.commands.wait_for_db.Command.check")
class CommandTests(SimpleTestCase):
    """Test commands"""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""

        # when called -> return True, nothing else
        patched_check.return_value = True

        # command on commands.wait_for_db
        call_command("wait_for_db")

        # ensure mocked object is called with these parameters
        patched_check.assert_called_once_with(databases=["default"])

    # replace sleep function with a magic mock object ..
    # overriding behavior of sleep to just mock and not do
    @patch("time.sleep")
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting
        OperationalError Psycopg2Error .. simulating for real db error"""
        # raise exception instead of returning a value
        # first two times we call the mock method
        # -> Psycopg2Error, the next 3 times OperationalError
        patched_check.side_effect = (
            [Psycopg2Error] * 2 + [OperationalError] * 3 + [True]
        )

        call_command("wait_for_db")

        self.assertEqual(patched_check.call_count, 6)

        # making sure the db called with "default" as argument
        patched_check.assert_called_with(databases=["default"])
