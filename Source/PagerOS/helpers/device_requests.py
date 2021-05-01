import requests
from helpers.kojin_logging import Log
from system.state import device_state
from system.constants import *
import urllib3

TAG = "Requests"


class Requests:

    def __init__(self):
        if device_state.networking.is_wifi_connected_and_enabled():
            Log.info(TAG, "Starting Wi-Fi Client")
            self._client = _WifiRequests()
        else:
            Log.info(TAG, "Starting GSM Client")
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

    urllib3.disable_warnings()

    def http_get(self, url, params):
        try:
            return requests.get(url, params).json()
        except requests.ConnectionError as e:
            Log.error(TAG, "Connection Error for request:\n" + e.request.url + "\n" + str(e.args))
        except Exception as e:
            print("General Error!")
            Log.error(TAG, "General http get error!\n" + str(e))
        return None

    def http_post(self, url, params):
        try:
            response = requests.post(url, json=params)
            return response.json()
        except requests.ConnectionError as e:
            Log.error(TAG, "Connection Error for request:\n" + e.request.url + "\n" + str(e.args))
        except Exception as e:
            print("General Error!")
            Log.error(TAG, "General http get error!\n" + str(e))


class _GSMRequests:
    def http_get(self, url, params):
        pass

    def http_post(self, url, params):
        pass

    def deserialise_response(self, response_object):
        pass
