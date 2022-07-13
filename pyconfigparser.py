from parsers import ParseError, json_parser, yaml_parser
from schema import Schema, SchemaError
from typing import Any
from os import path
import os
import re

VARIABLE_PATTERN = r'\$([a-zA-Z][\w]+|\{[a-zA-Z][\w]+\})$'
DEFAULT_CONFIG_FILES = ('config.json', 'config.yaml', 'config.yml')
ENTITY_NAME_PATTERN = r'^[a-zA-Z][\w]+$'
SUPPORTED_EXTENSIONS = {
    'json': json_parser,
    'yaml': yaml_parser,
    'yml': yaml_parser
}


class ConfigError(Exception):
    pass


class ConfigFileNotFoundError(ConfigError):
    pass


class Config:

    def __getitem__(self, item):
        return self.__dict__[item]

    def __iter__(self):
        return self.__dict__.keys().__iter__()

    def __len__(self):
        return len(self.__dict__)

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()


class configparser:
    def __init__(self):
        self.__instance = None
        self.__hold_an_instance = True

    @property
    def hold_an_instance(self):
        return self.__hold_an_instance

    @hold_an_instance.setter
    def hold_an_instance(self, value):
        if type(value) is not bool:
            raise ValueError('value must be a bool')
        self.__hold_an_instance = value

    def get_config(self, schema: dict = None, config_dir: str = 'config', file_name: Any = DEFAULT_CONFIG_FILES):

        if self.__instance is None:
            instance = self.__create_new_instance(schema, config_dir, file_name)
            if self.__hold_an_instance:
                self.__instance = instance
            else:
                return instance
        return self.__instance

    def __create_new_instance(self, schema, config_dir, file_name):
        file_path = self.__get_file_path(config_dir, file_name)
        parser = self.__get_file_parser(file_path)
        file_buff = self.__get_file_buff(file_path)

        try:
            config = self.__validate_schema(schema, parser(file_buff))
            return self.__dict_2_obj(config)
        except ParseError as e:
            raise ConfigError(e)
        except SchemaError as e:
            raise ConfigError('Schema validation error', e)

    def __get_file_parser(self, file_path):
        try:
            extension = file_path.split('.')[-1]
            return SUPPORTED_EXTENSIONS[extension]
        except KeyError:
            raise ConfigError(f'Supported extensions: {list(SUPPORTED_EXTENSIONS.keys())}')

    def __get_file_path(self, config_dir, file_name):
        file_path = f'{os.getcwd()}/{config_dir}/'
        if type(file_name) is str:
            file_name = [file_name]

        for f_name in file_name:
            if path.isfile(file_path + f_name):
                return file_path + f_name

        raise ConfigFileNotFoundError(f'Config file {file_path}{file_name} was not found')

    def __validate_schema(self, schema, config_obj):
        if schema is None:
            return config_obj
        elif type(schema) not in (dict, list):
            raise ConfigError('The first config\'s schema element should be a Map or a List')

        return Schema(schema).validate(config_obj)

    def __get_file_buff(self, path_file: str):
        with open(path_file, 'r') as f:
            return f.read()

    def __dict_2_obj(self, data: Any):
        _type = type(data)

        if _type is dict:
            obj = Config()
            for key, value in data.items():
                self.__is_a_valid_object_key(key)
                setattr(obj, key, self.__dict_2_obj(value))
            return obj
        if _type in (list, set, tuple):
            return list(map(lambda v: self.__dict_2_obj(v), data))
        else:
            if self.__is_variable(data):
                return self.__interpol_variable(data)
            return data

    def __is_a_valid_object_key(self, key):
        if re.search(ENTITY_NAME_PATTERN, key) is None:
            raise ConfigError(f'The key {key} is invalid. The entity keys only may have words, number and underscores.')

    def __is_variable(self, data):
        return type(data) is str and re.search(VARIABLE_PATTERN, data) is not None

    def __interpol_variable(self, data):
        try:
            return os.environ[self.__extract_env_variable_key(data)]
        except KeyError:
            raise ConfigError(f'Environment variable {data} was not found')

    def __extract_env_variable_key(self, variable):
        variable = variable[1:]
        if variable[0] == '{':
            return variable[1:-1]
        return variable


configparser = configparser()
