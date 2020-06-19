import json
from os import path
from typing import Any
from schema import Schema, SchemaError

class Config(object):
    
    __instance = None

    def __new__(cls, schema:dict = None, path_file:str = "config.json"):
        if cls.__instance is None or schema is not None:
            cls.__create_new_instace(schema, path_file)
        return cls.__instance

    @classmethod
    def __create_new_instace(cls, schema, path_file:str):
        if type(schema) is not dict:
            raise ConfigError("The first config's element should be a Map")

        file_buff = cls.__get_file_buff(path_file)

        try:
            config = Schema(schema).validate(json.loads(file_buff))
            cls.__instance = cls.__dict_2_obj(config)
        except json.JSONDecodeError:
            raise ConfigFileDecodeError("Wasn't possible to decode the json file:{}".format(path_file))
        except SchemaError as e:
            raise ConfigFileModelError(str(e))

    @classmethod
    def __get_file_buff(cls, path_file:str):
        if not path.isfile(path_file):
            raise ConfigFileNotFoundError("Wasn't find the config file: {}".format(path_file))

        try:
            with  open(path_file, "r") as f:
                return f.read()
        except Exception as e:
            raise ConfigFileOpenReadError(str(e))
    
    @classmethod
    def __dict_2_obj(cls, data: Any):
        _type = type(data)

        if _type is dict:
            obj = object.__new__(cls)
            for key, value in data.items():
                setattr(obj, key, cls.__dict_2_obj(value))
            return obj
        if _type in (list, set, tuple):
            return list(map(lambda value: cls.__dict_2_obj(value), data))
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

class ConfigFileOpenReadError(ConfigError):
    pass

class ConfigFileNotFoundError(ConfigError):
    pass
