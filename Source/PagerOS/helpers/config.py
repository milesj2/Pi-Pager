import configparser
import os
from system.constants import *
import system.globals as glob


class Config:
    def __init__(self):
        self._config_parser = configparser.ConfigParser()
        self._config_parser.read(os.getcwd() + "/" + CONFIG_FILE)

    def save_state(self):
        with open(os.getcwd() + CONFIG_FILE, "w+") as file:
            self._config_parser.write(file)
            file.close()

    def graceful_exit(self, value=STRING_EMPTY):
        if value == STRING_EMPTY:
            return glob.parse_bool(self._config_parser[INI_HEADER_PAGER][INI_KEY_GRACEFUL_EXIT])
        else:
            self._config_parser.set(INI_HEADER_PAGER, INI_KEY_GRACEFUL_EXIT, str(value))

    def get_user_name(self):
        return self._config_parser[INI_HEADER_USER][INI_KEY_NAME]

    def get_user_station(self):
        return self._config_parser[INI_HEADER_USER][INI_KEY_STATION]

    def get_access_token(self):
        return self._config_parser[INI_HEADER_KOJIN_API][INI_KEY_ACCESS_TOKEN]

    def get_logging_level(self):
        return self._config_parser[INI_HEADER_LOGGING][INI_KEY_LOGGING_LEVEL]

    def get_gpio_warnings_enabled(self):
        return glob.parse_bool(self._config_parser[INI_HEADER_LOGGING][INI_KEY_GPIO_WARNINGS])

    def get_debug(self):
        return glob.parse_bool(self._config_parser[INI_HEADER_LOGGING][INI_KEY_DEBUG])

    def get_wifi(self):
        return glob.parse_bool(self._config_parser[INI_HEADER_DEVICE][INI_KEY_WIFI])

    def set_wifi(self, value):
        self._config_parser.set(INI_HEADER_DEVICE, INI_KEY_WIFI, str(value))

    def get_cellular(self):
        return glob.parse_bool(self._config_parser[INI_HEADER_DEVICE][INI_KEY_CELLULAR])

    def set_cellular(self, value):
        self._config_parser.set(INI_HEADER_DEVICE, INI_KEY_CELLULAR, str(value))

    def get_bluetooth(self):
        return glob.parse_bool(self._config_parser[INI_HEADER_DEVICE][INI_KEY_BLUETOOTH])

    def set_bluetooth(self, value):
        self._config_parser.set(INI_HEADER_DEVICE, INI_KEY_BLUETOOTH, str(value))



config = Config()
