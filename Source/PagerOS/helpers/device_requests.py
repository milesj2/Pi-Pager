import requests
from system.state import device_state
from system.constants import *
from helpers.kojin_logging import Log
from system.state import device_state
from system.constants import *

TAG = "Requests"


class Requests:

    def __init__(self):
        if device_state.networking.get_wifi_status() == CONNECTION_STATUS_CONNECTED:
            self._client = _WifiRequests()
        else:
            self._client = _GSMRequests()

    def http_get(self, url, params):
        return self._client.http_get(url, params)

    def http_post(self, url, params):
        self._client.http_post(url, params)

    def deserialise_response(self, json, response_object):
        new_object = response_object()
        for key in json:
            new_object.__setattr__(key, json[key])
        return new_object


class _WifiRequests:
    def http_get(self, url, params ):
        try:
            return requests.get(url, params).json()
        except requests.ConnectionError as e:
            Log.error(TAG, "Connection Error for request:\n" + e.request.url + "\n" + str(e.args))
        except Exception as e:
            print("Now really panic!")
            Log.error(TAG, "General http get error!\n" + str(e))
        return None

    def http_post(self, url, params):
        try:
            response = requests.post(url, json=params)
            return response.json()
        except requests.ConnectionError as e:
            Log.error(TAG, "Connection Error for request:\n" + e.request.url + "\n" + str(e.args))
        except Exception as e:
            print("Now really panic!")
            Log.error(TAG, "General http get error!\n" + str(e))


class _GSMRequests:
    def http_get(self, url, params):
        pass

    def http_post(self, url, params):
        pass

    def deserialise_response(self, response_object):
        pass
