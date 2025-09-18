import unittest
from unittest.mock import patch, MagicMock
#from core.Mysqlsource import ConnnectToDB

class TestConnectToDB(unittest.TestCase):
    """Unit tests for the connect method in ConnnectToDB class."""

    @patch('core.Mysqlsource.mysql.connector.connect')
    def test_connect_success(self, mock_connect):
        """Test successful connection to the database."""
        # Mock the connection and cursor
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        # Initialize the database connection object
        db = ConnnectToDB(
            host="localhost",
            port=3306,
            user="test_user",
            password="test_password",
            database="test_db"
        )

        # Call the connect method
        connection, cursor = db.connect()

        # Assertions
        mock_connect.assert_called_once_with(
            host="localhost",
            port=3306,
            user="test_user",
            password="test_password",
            database="test_db"
        )
        self.assertIsNotNone(connection)
        self.assertIsNotNone(cursor)
        self.assertEqual(connection, mock_connection)
        self.assertEqual(cursor, mock_cursor)

    @patch('core.Mysqlsource.mysql.connector.connect')
    def test_connect_failure(self, mock_connect):
        """Test failed connection to the database."""
        # Simulate a connection error
        mock_connect.side_effect = mysql.connector.Error("Connection failed")

        # Initialize the database connection object
        db = ConnnectToDB(
            host="localhost",
            port=3306,
            user="test_user",
            password="test_password",
            database="test_db"
        )

        # Call the connect method
        connection, cursor = db.connect()

        # Assertions
        mock_connect.assert_called_once_with(
            host="localhost",
            port=3306,
            user="test_user",
            password="test_password",
            database="test_db"
        )
        self.assertIsNone(connection)
        self.assertIsNone(cursor)

if __name__ == "__main__":
    unittest.main()