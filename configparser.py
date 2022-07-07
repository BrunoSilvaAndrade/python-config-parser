import os
import re
import yaml
import json
from os import path
from typing import Any
from schema import Schema, SchemaError


ENTITY_NAME_PATTERN = '^[\w\d_]+$'


def json_parser(file_buff):
    try:
        return json.loads(file_buff)
    except json.JSONDecodeError as e:
        raise ConfigFileDecodeError(e)


def yaml_parser(file_buff):
    try:
        return yaml.load(file_buff, yaml.FullLoader)
    except yaml.YAMLError as e:
        raise ConfigFileDecodeError(e)


DEFAULT_CONFIG_FILES = ('config.json', 'config.yaml', 'config.yml')

SUPPORTED_EXTENSIONS = {
    'json': json_parser,
    'yaml': yaml_parser,
    'yml': yaml_parser
}


class Config(object):
    __instance = None

    def __new__(cls, schema: dict = None, config_dir: str = 'config', file_name: Any = DEFAULT_CONFIG_FILES):

        if cls.__instance is None or schema is not None:
            cls.__create_new_instance(schema, config_dir, file_name)
        return cls.__instance

    @classmethod
    def __create_new_instance(cls, schema, config_dir, file_name):
        cls.__check_schema(schema)
        file_path = cls.__get_file_path(config_dir, file_name)
        parser = cls.__get_file_parser(file_path)
        file_buff = cls.__get_file_buff(file_path)

        try:
            config = Schema(schema).validate(parser(file_buff))
            cls.__instance = cls.__dict_2_obj(config)
        except SchemaError as e:
            raise ConfigFileModelError(str(e))

    @classmethod
    def __get_file_parser(cls, file_path):
        try:
            extension = file_path.split('.')[-1]
            return SUPPORTED_EXTENSIONS[extension]
        except KeyError:
            raise ConfigFileExtensionNotSupportedError(f'Supported extensions: {list(SUPPORTED_EXTENSIONS.keys())}')

    @classmethod
    def __get_file_path(cls, config_dir, file_name):
        file_path = f'{os.getcwd()}/{config_dir}/'
        if type(file_name) is str:
            file_name = [file_name]

        for f_name in file_name:
            if path.isfile(file_path + f_name):
                return file_path + f_name

        raise ConfigFileNotFoundError(f'Config file {file_path}{file_name} was not found')

    @classmethod
    def __check_schema(cls, schema):
        if schema is None:
            raise ConfigInvalidSchemaError('The schema config can not be None')
        if type(schema) is not dict:
            raise ConfigInvalidSchemaError('The first config\'s schema element should be a Map')

    @classmethod
    def __get_file_buff(cls, path_file: str):
        try:
            with open(path_file, 'r') as f:
                return f.read()
        except Exception as e:
            raise ConfigFileOpenReadError(str(e))

    @classmethod
    def __dict_2_obj(cls, data: Any):
        _type = type(data)

        if _type is dict:
            obj = object.__new__(cls)
            for key, value in data.items():
                if re.search(ENTITY_NAME_PATTERN, key) is None:
                    raise ConfigEntitiesWithWrongNameError(
                        'The entity keys only may have words, number and underscores')
                setattr(obj, key, cls.__dict_2_obj(value))
            return obj
        if _type in (list, set, tuple):
            return list(map(lambda v: cls.__dict_2_obj(v), data))
        else:
            return data


class ConfigError(Exception):
    pass


class ConfigFileModelError(ConfigError):
    pass


class ConfigFileDecodeError(ConfigError):
    pass


class ConfigSchemaModelError(ConfigError):
    pass


class ConfigInvalidSchemaError(ConfigError):
    pass


class ConfigFileOpenReadError(ConfigError):
    pass


class ConfigFileNotFoundError(ConfigError):
    pass


class ConfigFileExtensionNotSupportedError(ConfigError):
    pass


class ConfigEntitiesWithWrongNameError(ConfigError):
    pass
