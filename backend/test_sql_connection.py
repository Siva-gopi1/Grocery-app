import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(__file__))
import mysql.connector
import sql_connection


class SqlConnectionTests(unittest.TestCase):
    def setUp(self):
        sql_connection.__cnx = None

    @patch('sql_connection.mysql.connector.connect')
    def test_returns_none_when_database_unavailable(self, connect_mock):
        connect_mock.side_effect = mysql.connector.Error("connection failed")

        result = sql_connection.get_sql_connection()

        self.assertIsNone(result)
        self.assertIsNone(sql_connection.__cnx)


if __name__ == '__main__':
    unittest.main()
