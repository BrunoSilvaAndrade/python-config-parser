SIMPLE_SCHEMA_CONFIG = {
    'core': {
        'logging': {
            'format': str,
            'datefmt': str,
            'level': str
        },
        'obj_list': [{'name': str, 'age': int}]
    }
}

UNSUPPORTED_OBJECT_KEYS_SCHEMA = {
    'testeWith-': int
}
