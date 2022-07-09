# python-config-parser
This project was created to give you the possibility of creating json and yaml/yml config files dynamically using OOP

HOW TO INSTALL
---------------------------
Use pip to install it.

```
pip install python-config-parser
```


HOW TO USE
---------------------------

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

The config.yml file
```
core:
  logging:
    format: "[%(asctime)s][%(levelname)s]: %(message)s"
    datefmt: "%d-%b-%y %H:%M:%S"
  allowed_clients:
  - ip: 192.168.0.10
    timeout: 60
  - ip: 192.168.0.11
    timeout: 100
```

The instance of Config Class:
```
from pyconfigparser import Config, ConfigException
import logging

try:
    config = Config.get_config(SCHEMA_CONFIG) # <- Here I'm using that SCHEMA_CONFIG we had declared, and the dir file default value is being used
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
    level=logging.INFO
)

#the list of object example:

for client in config.core.allowed_clients:
    print(client.ip)
    print(client.timeout)

```

Instanced the first obj, you can instance Config in other files of your project
just calling the Config without args like that:

```
from pyconfigparser import Config, ConfigException

config = Config.get_config() #At this point you already have the configuration properties in your config object
```


CONTRIBUTE
----------

Fork https://github.com/BrunoSilvaAndrade/python-config-parser/ , create commit and pull request to ``develop``.
