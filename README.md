Python-config-parser
===
This project was created to give you the possibility
of creating runtime configuration objects using json or yaml files.

MAIN FEATURES
===
---
* Declarative configurations without using .ini files
* Access OOP or subscriptable, which means that you can iterate the config object items
* Runtime validation using [schema](https://github.com/keleshev/schema)
* Automatic environment variables interpolation
* Automatic parser selecting by config file extension

HOW TO INSTALL
===
---
Use pip to install it.

```shell
pip install python-config-parser
```

HOW TO USE
===
---
First of all the config file will look for default config files if you do not pass your own config file for this.

The default config directory is ./config(if you do not pass the config directory of your preference) assuming your current directory.

The default config files names are -> (config.json, config.yaml, config.yml)




The Schema validation.
---

You may use or not schema validation, if you want to use it, it will validate your whole config object before returning it.

If you don't want to use it, it won't validate the config object before returning that, and it may generate runtime access inconsistencies.

How to use schema

```python
from schema import Use, And

SCHEMA_CONFIG = {
    'core': {
        'logging': {
            'format': And(Use(str), lambda string: len(string) > 0),
            'date_fmt': And(Use(str), lambda string: len(string) > 0),
            'random_env_variable': str
        },
        'allowed_clients': [{
                'ip': str, # <- Here you can use regex to validate the ip format
                'timeout': int
            }
        ]
    }
}

```

The config.yml file
```yaml
core:
  random_env_variable: ${RANDOM_ENV_VARIABLE}
  logging:
    format: "[%(asctime)s][%(levelname)s]: %(message)s"
    date_fmt: "%d-%b-%y %H:%M:%S"
  allowed_clients:
  - ip: 192.168.0.10
    timeout: 60
  - ip: 192.168.0.11
    timeout: 100
```
This config file as a json would be something like:

```json
{
  "core": {
    "random_env_variable": "${RANDOM_ENV_VARIABLE}",
    "logging": {
      "format": "[%(asctime)s][%(levelname)s]: %(message)s",
      "date_fmt": "%d-%b-%y %H:%M:%S"
    },
    "allowed_clients": [
      {
        "ip": "192.168.0.10",
        "timeout": 60
      },
      {
        "ip": "192.168.0.11",
        "timeout": 100
      }
    ]
  }
}
```

The instance of Config Class:
```python
from pyconfigparser import Config, ConfigError
import logging

try:
    config = Config.get_config(SCHEMA_CONFIG) # <- Here I'm using that SCHEMA_CONFIG we had declared, and the dir file default value is being used
except ConfigError as e:
    print(e)
    exit()

#to access your config you need just:


fmt = config.core.logging.format #look this, at this point I'm already using the config variable
date_fmt = config['core']['logging']['date_fmt'] #here subscriptable access

logging.getLogger(__name__)

logging.basicConfig(
    format=fmt,
    datefmt=date_fmt,
    level=logging.INFO
)

#the list of object example:

for client in config.core.allowed_clients:
    print(client.ip)
    print(client.timeout)

    
#The config object's parts which is not a list can also be itered but, it'll give you the attribute's names
#So you can access the values by subscriptale access
for logging_section_attr_key in config.core.logging:
    print(config.core.logging[logging_section_attr_key])

#Accessing the environment variable already resolved
print(config.random_env_variable)

```
Since you've already created the first Config's instance this instance will be cached inside Config class,
so after this first creation you can just invoke Config.get_config()

```python
from pyconfigparser import Config

config = Config.get_config() #At this point you already have the configuration properties in your config object
```

You can also disable the action to cache the instance config


```python
from pyconfigparser import Config

Config.set_hold_an_instance(False)
```


CONTRIBUTE
---
---

Fork https://github.com/BrunoSilvaAndrade/python-config-parser/ , create commit and pull request to ``develop``.
