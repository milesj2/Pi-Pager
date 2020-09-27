from system import state
from system.constants import *


# current_alert = ALERT_EMPTY

device_state = state.DeviceState()


def parse_bool(str_bool):
    """ Returns False as default or if str_bool does match with list below"""
    return str_bool.lower() in ("yes", "true", "t", "y", "1", "on")


