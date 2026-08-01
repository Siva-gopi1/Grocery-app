import os
import unittest
from unittest.mock import patch

from backend import config


class ConfigTests(unittest.TestCase):
    def test_uses_environment_overrides_for_database(self):
        with patch.dict(os.environ, {
            'DB_HOST': 'db.internal',
            'DB_PORT': '3307',
            'DB_USER': 'app_user',
            'DB_PASSWORD': 'secret',
            'DB_NAME': 'inventory',
        }, clear=False):
            db_config = config.get_db_config()
            self.assertEqual(db_config['host'], 'db.internal')
            self.assertEqual(db_config['port'], 3307)
            self.assertEqual(db_config['user'], 'app_user')
            self.assertEqual(db_config['password'], 'secret')
            self.assertEqual(db_config['database'], 'inventory')

    def test_defaults_to_local_development_values(self):
        with patch.dict(os.environ, {}, clear=True):
            db_config = config.get_db_config()
            self.assertEqual(db_config['host'], '127.0.0.1')
            self.assertEqual(db_config['port'], 3306)
            self.assertEqual(db_config['user'], 'root')
            self.assertEqual(db_config['password'], 'root')
            self.assertEqual(db_config['database'], 'grocery_store')


if __name__ == '__main__':
    unittest.main()
