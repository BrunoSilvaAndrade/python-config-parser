import json
from os import path
from schema import Schema, SchemaError

class Config(object):
    
    __instance = None

    def __new__(cls,schema:dict = None, path_file:str = "config.json"):
        if cls.__instance is None:
            cls.__create_new_instace(schema, path_file)
        return cls.__instance

    @classmethod
    def __create_new_instace(cls,schema:dict, path_file:str):
        if not path.isfile(path_file):
            raise ConfigException("Wasn't possible find the config file: {}".format(path_file))
        
        with  open(path_file, "r") as f:
            file_buff = f.read()
            f.close()

        try:
            config = Schema(schema).validate(json.loads(file_buff))
            if type(config) is not dict:
                raise ConfigException("The first config's element should be a Map")
            cls.__instance = cls.__dict_2_obj(config)
        except json.JSONDecodeError:
            raise ConfigException("Wasn't possible to decode the json file:{}".format(path_file))
        except SchemaError as e:
            raise ConfigException(str(e))
    
    @classmethod
    def __dict_2_obj(cls, data:any):
        _type = type(data)

        if _type is dict:
            obj = object.__new__(cls)
            for key in data:
                sub_data = data[key]
                if type(sub_data) in (list, dict):
                    setattr(obj, key, cls.__dict_2_obj(sub_data))
                else:
                    setattr(obj, key, sub_data)
            return obj
        if _type is list:
            for i in range(len(data)):
                data[i] = cls.__dict_2_obj(data[i])
            return data
        else:
            return data

class ConfigException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)