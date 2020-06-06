# python-json-config-parser
Project created to given the possibility of create dynamics Json config files and use that using oriented object paradigm


HOW IT WORKS
---------------------------
The Class Config takes two arguments, The first is a Schema(https://github.com/keleshev/schema) to secure the model of config, 
the second is the str path of json config file.
If the second argument didn't take, the default value('./config.json') is used when you call Config Class trying find this file in the same dir file where you call this Class.

For example:

The model file.
```
SCHEMA_CONFIG = {
    "core":{
        "logging":{
            "format": And(Use(str), lambda string: len(string) > 0),
            "datefmt": And(Use(str), lambda string: len(string) > 0)
        },
        "allowed_clients":[
            {
                "ip":str, # <- Here you can use regex to valid the ip format
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
logging.getLogger(__name__)
logging.basicConfig(format=config.core.logging.format, datefmt=config.core.logging.datefmt, level=20)# look this, at this point I'm already using the config variable

#the list of object example:

for client in config.core.allowed_clients:
    print(client.ip)
    print(client.timeout)

```

After of create the fist obj you don't need to pass the args again, you can instance of Config in other files of your project
just calling the Config without args like that:

```
from jsonconfigparser import Config, ConfigException

config = Config() #At this point you already have the configuration properties in your config object
```


CONTRIBUTE
----------

Fork https://github.com/BrunoSilvaAndrade/python-json-config-parser/ , create commit and pull request to ``develop``.
