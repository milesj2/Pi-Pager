import configparser
import os
from system.globals import *


_config_parser = configparser.ConfigParser()
_config_parser.read(os.getcwd() + "/" + CONFIG_FILE)


class Config:

    @staticmethod
    def save_state():
        file = open(os.getcwd() + "/" + CONFIG_FILE, "w")
        _config_parser.write(file)
        file.close()

    @staticmethod
    def graceful_exit(value=STRING_EMPTY):
        if value == STRING_EMPTY:
            return parse_bool(_config_parser[INI_HEADER_PAGER][INI_KEY_GRACEFUL_EXIT])
        else:
            _config_parser.set(INI_HEADER_PAGER, INI_KEY_GRACEFUL_EXIT, str(value))

    @staticmethod
    def get_user_name():
        return _config_parser[INI_HEADER_USER][INI_KEY_NAME]

    @staticmethod
    def get_user_station():
        return _config_parser[INI_HEADER_USER][INI_KEY_STATION]

    @staticmethod
    def get_access_token():
        return _config_parser[INI_HEADER_KOJIN_API][INI_KEY_ACCESS_TOKEN]

    @staticmethod
    def get_logging_level():
        return _config_parser[INI_HEADER_LOGGING][INI_KEY_LOGGING_LEVEL]

    @staticmethod
    def get_gpio_warnings_enabled():
        return parse_bool(_config_parser[INI_HEADER_LOGGING][INI_KEY_GPIO_WARNINGS])

    @staticmethod
    def get_debug():
        return parse_bool(_config_parser[INI_HEADER_LOGGING][INI_KEY_DEBUG])

