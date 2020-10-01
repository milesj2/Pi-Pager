import configparser
import os
from system.constants import *
import system.methods as glob


class Config:
    """ class to handle interfacing with config.ini

     Changes to keys are stored in memory until Config.save_state is called.
    """
    def __init__(self):
        self._config_parser = configparser.ConfigParser()
        self._config_parser.read(os.getcwd() + "/" + CONFIG_FILE)

    def save_state(self):
        with open(os.getcwd() + CONFIG_FILE, "w+") as file:
            self._config_parser.write(file)
            file.close()

    def get_graceful_exit(self):
        return glob.parse_bool(self._config_parser[INI_HEADER_PAGER][INI_KEY_GRACEFUL_EXIT])

    def set_graceful_exit(self, value):
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

    def get_sound(self):
        return glob.parse_bool(self._config_parser[INI_HEADER_DEVICE][INI_KEY_SOUND])

    def set_sound(self, value):
        self._config_parser.set(INI_HEADER_DEVICE, INI_KEY_SOUND, str(value))

    def get_vibrate(self):
        return glob.parse_bool(self._config_parser[INI_HEADER_DEVICE][INI_KEY_VIBRATE])

    def set_vibrate(self, value):
        self._config_parser.set(INI_HEADER_DEVICE, INI_KEY_VIBRATE, str(value))


config = Config()
