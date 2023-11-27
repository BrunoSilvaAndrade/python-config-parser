from schema import Schema, SchemaError
from typing import Any
from os import path
import json
import yaml
import os
import re
from collections.abc import Mapping

__all__ = [
    "ConfigError",
    "ConfigFileNotFoundError",
    "Config",
    "ConfigParser",
    "configparser"
]


class ConfigError(Exception):
    pass


class ConfigFileNotFoundError(Exception):
    pass


def _json_parser(file_buff):
    try:
        return json.loads(file_buff)
    except json.JSONDecodeError as e:
        raise ConfigError('Unable to decode config file using json', e)


def _yaml_parser(file_buff):
    try:
        return yaml.safe_load(file_buff)
    except yaml.YAMLError as e:
        raise ConfigError('Unable to decode config file using yaml', e)


def _validate_schema(schema, config_obj):
    if schema is None:
        return config_obj
    elif type(schema) not in (dict, list):
        raise ConfigError('The first config\'s schema element should be a Map or a List')

    return Schema(schema).validate(config_obj)


def _get_file_buff(path_file: str):
    with open(path_file, 'r') as f:
        return f.read()


def _get_file_parser(file_path):
    try:
        extension = file_path.split('.')[-1]
        return _SUPPORTED_EXTENSIONS[extension]
    except KeyError:
        raise ConfigError(f'Supported extensions: {list(_SUPPORTED_EXTENSIONS.keys())}')


def _get_file_path(config_dir, file_name):
    file_path = f'{os.getcwd()}/{config_dir}/'
    if type(file_name) is str:
        file_name = [file_name]

    for f_name in file_name:
        if path.isfile(file_path + f_name):
            return file_path + f_name

    raise ConfigFileNotFoundError(f'Config file {file_path}{file_name} was not found')


def _is_a_valid_object_key(key):
    if re.search(_ENTITY_NAME_PATTERN, key) is None:
        raise ConfigError(f'The key {key} is invalid. The entity keys only may have words, number and underscores.')


def _is_variable(data):
    return type(data) is str and re.search(_VARIABLE_PATTERN, data) is not None


def _interpol_variable(data, ignore_unset_env_vars):
    try:
        return os.environ[_extract_env_variable_key(data)]
    except KeyError:
        if ignore_unset_env_vars:
            return None
        raise ConfigError(f'Environment variable {data} was not found')


def _extract_env_variable_key(variable):
    variable = variable[1:]
    if variable[0] == '{':
        return variable[1:-1]
    return variable


_VARIABLE_PATTERN = r'\$([a-zA-Z][\w]+|\{[a-zA-Z][\w]+\})$'
_DEFAULT_CONFIG_FILES = ('config.json', 'config.yaml', 'config.yml')
_ENTITY_NAME_PATTERN = r'^[a-zA-Z][\w]+$'
_SUPPORTED_EXTENSIONS = {
    'json': _json_parser,
    'yaml': _yaml_parser,
    'yml': _yaml_parser
}


class Config(Mapping):

    def __getitem__(self, item):
        return self.__dict__[item]

    def __iter__(self):
        return self.__dict__.keys().__iter__()

    def __len__(self):
        return len(self.__dict__)


class ConfigParser:
    def __init__(self):
        self.__instance = None
        self.__hold_an_instance = True
        self.__ignore_unset_env_vars = False

    @property
    def hold_an_instance(self):
        return self.__hold_an_instance

    @hold_an_instance.setter
    def hold_an_instance(self, value):
        if type(value) is not bool:
            raise ValueError('value must be a bool')
        self.__hold_an_instance = value

    @property
    def ignore_unset_env_vars(self):
        return self.__ignore_unset_env_vars

    @ignore_unset_env_vars.setter
    def ignore_unset_env_vars(self, value):
        if type(value) is not bool:
            raise ValueError('value must be a bool')
        self.__ignore_unset_env_vars = value

    def get_config(self, schema: dict = None, config_dir: str = 'config', file_name: Any = _DEFAULT_CONFIG_FILES):
        if self.__hold_an_instance:
            if self.__instance is None:
                self.__instance = self.__create_new_instance(schema, config_dir, file_name)
            return self.__instance
        return self.__create_new_instance(schema, config_dir, file_name)

    def __create_new_instance(self, schema, config_dir, file_name):
        file_path = _get_file_path(config_dir, file_name)
        parser = _get_file_parser(file_path)
        file_buff = _get_file_buff(file_path)

        try:
            config = _validate_schema(schema, parser(file_buff))
            return self.__dict_2_obj(config)
        except SchemaError as e:
            raise ConfigError('Schema validation error', e)

    def __dict_2_obj(self, data: Any):
        _type = type(data)

        if _type is dict:
            obj = Config()
            for key, value in data.items():
                _is_a_valid_object_key(key)
                setattr(obj, key, self.__dict_2_obj(value))
            return obj

        if _type in (list, set, tuple):
            return list(map(lambda v: self.__dict_2_obj(v), data))

        else:
            if _is_variable(data):
                return _interpol_variable(data, self.__ignore_unset_env_vars)
            return data


configparser = ConfigParser()
