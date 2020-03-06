import unittest

from application.settings import load_config


class TestSettingsLoader(unittest.TestCase):

    def testDefaultLoader(self):
        default_cfg = \
            {
                'database_config':
                    {
                        'host': 'localhost',
                        'user': 'postgres',
                        'password': 'JPYh42JS',
                        'port': 5432,
                        'database': 'CatsQMS'
                    }
            }
        self.assertDictEqual(load_config(), default_cfg)

    def testCustomLoader(self):
        custom_cfg = \
            {
                'database_config':
                    {
                        'database_uri': 'postgresql://user:password@localhost:5432/database',
                        'cfg_opt1': 'Opt1',
                        'cfg_opt2': 1234
                    }
            }
        with open("test.yaml", 'r') as f:
            self.assertDictEqual(custom_cfg, load_config(f))
