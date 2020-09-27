from system.constants import *
from system import events


class DeviceState:
    _on_new_state = events.Event()
    _state = STRING_EMPTY

    networking = STRING_EMPTY

    class _Networking:

        _status = STRING_EMPTY
        _api_status = STRING_EMPTY

        def get_network_status(self):
            pass

        def get_current_wifi(self):
            pass

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




