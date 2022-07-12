from pyconfigparser import Config, ConfigError, ConfigFileNotFoundError, ParseException
from config.schemas import SIMPLE_SCHEMA_CONFIG, UNSUPPORTED_OBJECT_KEYS_SCHEMA
import unittest
import os

DT_FMT_TEST = '%Y-%m-%dT%H:%M:%SZ'
VAR_LOG_LEVEL_INFO = 'INFO'


class ConfigTestCase(unittest.TestCase):
    def setUp(self) -> None:
        Config.set_hold_an_instance(False)
        os.environ['DATE_FORMAT_TEST'] = DT_FMT_TEST
        os.environ['LOG_LEVEL_TEST'] = VAR_LOG_LEVEL_INFO

    def test_new(self):
        self.assertRaises(RuntimeError, Config)

    def test_schema_checking(self):
        self.assertRaises(ConfigError, Config.get_config, 1)

    def test_config_without_file(self):
        self.assertRaises(ConfigFileNotFoundError, Config.get_config, SIMPLE_SCHEMA_CONFIG,
                          'config',
                          'some_non_exists_file.json')

    def test_undefined_env_var(self):
        try:
            Config.get_config(file_name='config.yaml')
        except Exception as e:
            self.assertIn('Environment', str(e))

    def test_to_access_attr_from_config(self):
        config = Config.get_config(SIMPLE_SCHEMA_CONFIG)
        self.assertEqual(VAR_LOG_LEVEL_INFO, config.core.logging.level)
        self.assertEqual(DT_FMT_TEST, config.core.logging.datefmt)
        self.assertEqual('format', config.core.logging.format)
        self.assertEqual(24, config.core.obj_list[0].age)
        self.assertEqual('Mike', config.core.obj_list[0]['name'])  # <- using subscriptable access

    def test_access_fake_attr(self):
        config = Config.get_config(SIMPLE_SCHEMA_CONFIG)
        self.assertRaises(AttributeError, lambda: config.fake_attr)

    def test_unsupported_object_key(self):
        self.assertRaises(ConfigError, Config.get_config, UNSUPPORTED_OBJECT_KEYS_SCHEMA,
                          file_name='unsupported_object_key.json')

    def test_set_hold_an_invalid_instance(self):
        self.assertRaises(ValueError, Config.set_hold_an_instance, [])

    def test_config_with_wrong_json_model(self):
        self.assertRaises(ConfigError, Config.get_config, SIMPLE_SCHEMA_CONFIG, file_name='wrong_model.json')

    def test_config_file_with_unsupported_extension(self):
        self.assertRaises(ConfigError, Config.get_config, SIMPLE_SCHEMA_CONFIG, file_name='config.bad_extension')

    def test_bad_decoder_error(self):
        self.assertRaises(ParseException, Config.get_config, SIMPLE_SCHEMA_CONFIG, file_name='bad_content.json')
        self.assertRaises(ParseException, Config.get_config, SIMPLE_SCHEMA_CONFIG, file_name='bad_content.yaml')


if __name__ == '__main__':
    unittest.main()
