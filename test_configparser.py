from pyconfigparser import ConfigParser, ConfigError, ConfigFileNotFoundError, _is_variable
from config.schemas import SIMPLE_SCHEMA_CONFIG, UNSUPPORTED_OBJECT_KEYS_SCHEMA
import unittest
import os

DT_FMT_TEST = '%Y-%m-%dT%H:%M:%SZ'
VAR_LOG_LEVEL_INFO = 'INFO'


class ConfigTestCase(unittest.TestCase):
    def setUp(self) -> None:
        os.environ['DATE_FORMAT_TEST'] = DT_FMT_TEST
        os.environ['LOG_LEVEL_TEST'] = VAR_LOG_LEVEL_INFO

    def test_schema_checking(self):
        configparser = ConfigParser()
        self.assertRaises(ConfigError, configparser.get_config, 1)

    def test_config_without_file(self):
        configparser = ConfigParser()
        self.assertRaises(ConfigFileNotFoundError, configparser.get_config, SIMPLE_SCHEMA_CONFIG,
                          'config',
                          'some_non_exists_file.json')

    def test_undefined_env_var(self):
        try:
            configparser = ConfigParser()
            configparser.get_config(file_name='config.yaml')
        except Exception as e:
            self.assertIn('Environment', str(e))

        configparser = ConfigParser()
        configparser.ignore_unset_env_vars = True
        configparser.get_config(file_name='config.yaml')

    def test_to_access_attr_from_config(self):
        configparser = ConfigParser()
        config = configparser.get_config(SIMPLE_SCHEMA_CONFIG)
        self.assertEqual(VAR_LOG_LEVEL_INFO, config.core.logging.level)
        self.assertEqual(DT_FMT_TEST, config.core.logging.datefmt)
        self.assertEqual('format', config.core.logging.format)
        self.assertEqual(24, config.core.obj_list[0].age)
        self.assertEqual('Mike', config.core.obj_list[0]['name'])  # <- using subscriptable access

    def test_access_fake_attr(self):
        configparser = ConfigParser()
        config = configparser.get_config(SIMPLE_SCHEMA_CONFIG)
        self.assertRaises(AttributeError, lambda: config.fake_attr)

    def test_unsupported_object_key(self):
        configparser = ConfigParser()
        self.assertRaises(ConfigError, configparser.get_config, UNSUPPORTED_OBJECT_KEYS_SCHEMA,
                          file_name='unsupported_object_key.json')

    def test_config_with_wrong_json_model(self):
        configparser = ConfigParser()
        self.assertRaises(ConfigError, configparser.get_config, SIMPLE_SCHEMA_CONFIG, file_name='wrong_model.json')

    def test_config_file_with_unsupported_extension(self):
        configparser = ConfigParser()
        self.assertRaises(ConfigError, configparser.get_config, SIMPLE_SCHEMA_CONFIG, file_name='config.bad_extension')

    def test_bad_decoder_error(self):
        configparser = ConfigParser()
        self.assertRaises(ConfigError, configparser.get_config, SIMPLE_SCHEMA_CONFIG, file_name='bad_content.json')
        self.assertRaises(ConfigError, configparser.get_config, SIMPLE_SCHEMA_CONFIG, file_name='bad_content.yaml')

    def test_caching_instance(self):
        configparser = ConfigParser()
        config1 = configparser.get_config()
        config2 = configparser.get_config()
        self.assertIs(config1, config2)
        configparser.hold_an_instance = False

        config2 = configparser.get_config()
        self.assertIsNot(config1, config2)

    def test_configparser_config_switches(self):
        configparser = ConfigParser()

        def assign_a_bad_type_hold_an_instance():
            configparser.hold_an_instance = []

        def assign_a_bad_type_ignore_unsetted_env_vars():
            configparser.ignore_unset_env_vars = []

        self.assertRaises(ValueError, assign_a_bad_type_hold_an_instance)
        self.assertRaises(ValueError, assign_a_bad_type_ignore_unsetted_env_vars)
        configparser.hold_an_instance = False
        configparser.ignore_unset_env_vars = True
        self.assertIs(configparser.hold_an_instance, False)
        self.assertIs(configparser.ignore_unset_env_vars, True)
        self.assertIsInstance(configparser.ignore_unset_env_vars, bool)

    def test_variable_pattern_matching(self) -> None:
        """Test the regex pattern for environment variable matching."""

        valid_env_vars = [
            "$FOO",
            "${FOO}",
            "$My_Var123"
        ]

        invalid_env_vars = [
            "FOO",                   # no $
            "$",                     # missing name
            "${}",                   # empty braces
            "$1VAR",                 # starts with number
            "${1VAR}",               # starts with number in braces
            "foo$VAR",               # not at start
            "<L/f\\U<Uj2{.S95@^$Rx"  # random password
        ]

        for var in valid_env_vars:
            with self.subTest(var=var):
                self.assertTrue(_is_variable(var), f"{var} should match")

        for var in invalid_env_vars:
            with self.subTest(var=var):
                self.assertFalse(_is_variable(var), f"{var} should not match")


if __name__ == '__main__':
    unittest.main()
