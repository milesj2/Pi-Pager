import requests
from system.constants import *
from helpers.kojin_logging import Log


TAG = "Kojin_Requests"


class StdResponse:
    """ Deserialised class formed from default response from API """
    status = STRING_EMPTY
    message = STRING_EMPTY

    def __init__(self, status, message):
        self.status = status
        self.message = message


# deserializers
def deserialize_response(dct):
    """ Deserializes the standard response

     Args:
        dct (dictionary): response json
    Return:
        (StdResponse): class made from json
     """
    return StdResponse(dct['status'], dct['message'])


def http_get(url, params):
    """ Sends get request to Kojin Pager Api and deserializes the standard response

    Args:
        url (str): base api url + endpoint route
        params (dictionary): key and value pairs to convert to get parameters

    Returns:
        response (StdResponse): deserialized json response
    """
    try:
        response = requests.get(url, params)
        # TODO more error handling to do.
        if 'value' in response.json():
            response = deserialize_response(response.json()['value'])
        else:
            response = deserialize_response(response.json())
        return response
    except requests.ConnectionError as e:
        Log.error(TAG, "Connection Error for request:\n" + e.request.url + "\n" + str(e.args))
    except Exception as e:
        print("Now really panic!")
        Log.error(TAG, "General http get error!\n" + str(e))
    return None



