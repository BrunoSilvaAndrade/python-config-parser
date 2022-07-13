import json
import yaml


class ParseError(Exception):
    pass


def json_parser(file_buff):
    try:
        return json.loads(file_buff)
    except json.JSONDecodeError as e:
        raise ParseError('Unable to decode config file using json', e)


def yaml_parser(file_buff):
    try:
        return yaml.safe_load(file_buff)
    except yaml.YAMLError as e:
        raise ParseError('Unable to decode config file using yaml', e)
