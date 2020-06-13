# python-json-config-parser
This project was created to give you the possibility of creating json config files dynamicaly using OOP

HOW TO INSTALL
---------------------------
Use pip to install it.

```
pip install python-json-config-parser
```


HOW TO USE
---------------------------
The Class Config takes two arguments, the first is a Schema(https://github.com/keleshev/schema) to ensure the model of config, the second is the str path of json config file.

If you don't specify the path, the default value('config.json') will be used if one exists in the same dir where the script is running.

For example:

The model file.
```
from schema import Use, And

SCHEMA_CONFIG = {
    "core":{
        "logging":{
            "format": And(Use(str), lambda string: len(string) > 0),
            "datefmt": And(Use(str), lambda string: len(string) > 0)
        },
        "allowed_clients":[
            {
                "ip":str, # <- Here you can use regex to validate the ip format
                "timeout":int
            }
        ]
    }
}

```

The config.json file
```
{
    "core":{
        "logging":{
            "format":"[%(asctime)s][%(levelname)s]: %(message)s",
            "datefmt": "%d-%b-%y %H:%M:%S"
        },
        "allowed_clients":[
            {
                "ip":"192.168.0.10",
                "timeout":60
            },
            {
                "ip":"192.168.0.11",
                "timeout":100
            }
        ]
    }
}
```

The istance of Config Class:
```
from jsonconfigparser import Config, ConfigException
import logging

try:
    config = Config(SCHEMA_CONFIG) # <- Here I'm using that SCHEMA_CONFIG we had declared, and the dir file default value is being used
except ConfigException as e:
    print(e)
    exit()

#to access your config you need just:


fmt = config.core.logging.format #look this, at this point I'm already using the config variable
dtfmt = config.core.logging.datefmt #here again

logging.getLogger(__name__)

logging.basicConfig(
    format=fmt,
    datefmt=dtfmt
    level=20
)

#the list of object example:

for client in config.core.allowed_clients:
    print(client.ip)
    print(client.timeout)

```

Instanced the first obj, you can instance Config in other files of your project
just calling the Config without args like that:

```
from jsonconfigparser import Config, ConfigException

config = Config() #At this point you already have the configuration properties in your config object
```


CONTRIBUTE
----------

Fork https://github.com/BrunoSilvaAndrade/python-json-config-parser/ , create commit and pull request to ``develop``.
