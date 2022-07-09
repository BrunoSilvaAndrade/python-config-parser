import unittest
from configparser import *
from config.schema_config_test import SIMPLE_SCHEMA_CONFIG


class ConfigTestCase(unittest.TestCase):

    def test_config_without_file(self):
        self.assertRaises(ConfigFileNotFoundError, Config.get_config, SIMPLE_SCHEMA_CONFIG, 'config', 'some_non_exists_file.json')

    def test_config_with_wrong_json_model(self):
        self.assertRaises(ConfigFileModelError, Config.get_config, SIMPLE_SCHEMA_CONFIG, 'config', 'wrong_model.json')

    def test_config_file_with_unsupported_extension(self):
        self.assertRaises(ConfigFileExtensionNotSupportedError, Config.get_config, SIMPLE_SCHEMA_CONFIG, 'config', 'config.bad_extension')

    def test_to_access_attr_from_config(self):
        config = Config.get_config(SIMPLE_SCHEMA_CONFIG)
        self.assertEqual(config.core.logging.format, 'format')
        self.assertEqual(config.core.logging.datefmt, 'datefmt')
        self.assertEqual(config.core.obj_list[0].name, 'bruno')
        self.assertEqual(config.core.obj_list[0].age, 24)

    def test_access_fake_attr(self):
        config = Config.get_config(SIMPLE_SCHEMA_CONFIG)
        self.assertRaises(AttributeError, lambda: config.fake_attr)


if __name__ == '__main__':
    unittest.main()
