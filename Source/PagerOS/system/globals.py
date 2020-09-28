from system.constants import *
from system.classes import *
from system.events import Event
from system.state import DeviceState


# current_alert = ALERT_EMPTY

device_state = DeviceState()


def parse_bool(str_bool):
    """ Returns False as default or true if str_bool matches with any strings list below"""
    return str(str_bool).lower() in ("yes", "true", "t", "y", "1", "on")


