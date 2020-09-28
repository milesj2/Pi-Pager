from system.constants import *
from system import events
from helpers.config import Config


class DeviceState:
    _on_new_state = events.Event()
    _state = STRING_EMPTY

    networking = STRING_EMPTY

    class _Networking:

        _wifi_status = NO_SIGNAL
        _cellular_status = NO_SIGNAL
        _bluetooth = NO_SIGNAL
        _api_status = STRING_EMPTY

        def __init__(self):
            pass

        def get_wifi_status(self):
            return self._wifi_status

        def set_wifi_status(self, status):
            self._wifi_status = status

        def get_current_wifi(self):
            pass

        def get_cellular_status(self):
            return self._cellular_status

        def set_cellular_status(self, status):
            self._cellular_status = status

        def set_api_status(self, status):
            self._api_status = status

        def get_api_status(self,):
            return self._api_status

    def __init__(self):
        self.networking = self._Networking()

    def get_state(self):
        return self._state

    def set_state(self, state):
        if self._state != state:
            self._on_new_state(state)
            print(f"{__name__} | New device state {self._state} => {state}")
        self._state = state

    def add_handler_on_new_state(self, handler):
        self._on_new_state.append(handler)




