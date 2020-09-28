import requests
from system.constants import *
from helpers.kojin_logging import Log


TAG = "Kojin_Requests"


class StdResponse:
    """ Deserialised class formed from default response from API"""
    status = STRING_EMPTY
    message = STRING_EMPTY

    def __init__(self, status, message):
        self.status = status
        self.message = message


# deserializers
def deserialize_response(dct):
    return StdResponse(dct['status'], dct['message'])


def http_get(url, params):
    try:
        # set_state(STATE_IDLE)  # whY?
        response = requests.get(url, params)
        # TODO more handling to do.
        if 'value' in response.json():
            response = deserialize_response(response.json()['value'])
        else:
            response = deserialize_response(response.json())
        # update_connection_status(CONNECTION_STATUS_CONNECTED)
        return response
    except requests.ConnectionError as e:
        Log.error(TAG, "Connection Error for request:\n" + e.request.url + "\n" + str(e.args))
    except Exception as e:
        print("Now really panic!")
        Log.error(TAG, "General http get error!\n" + str(e))
    # update_connection_status(CONNECTION_STATUS_DISCONNECTED)
    # set_state(STATE_DISCONNECTED)
    return None



