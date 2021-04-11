from system.constants import *
from helpers.kojin_logging import Log
from system.state import device_state
import requests

TAG = "Location_Requests"


class StdResponse:
    """ Deserialized class formed from default response from API"""
    def __init__(self, status, balance, lat, lon, accuracy):
        self.status = status
        self.balance = balance
        self.lat = lat
        self.lon = lon
        self.accuracy = accuracy


class ErrResponse:
    """ Deserialized class formed from default response from API"""
    status = STRING_EMPTY
    message = STRING_EMPTY

    def __init__(self, status, message, balance):
        self.status = status
        self.message = message
        self.balance = balance


def deserialize_std_response(json):
    """ Deserializes the standard response

     Args:
        dct (dictionary): response json
    Return:
        (StdResponse): class made from json
     """
    return StdResponse(json['status'], json['balance'], json['lat'], json['lon'], json['accuracy'])


def deserialize_err_response(json):
    """ Deserializes the standard error response

     Args:
        dct (dictionary): response json
    Return:
        (ErrResponse): class made from json
     """
    return ErrResponse(json['status'], json['message'], json['balance'])


def wifi_post(url, params):
    """ Sends post request to location Api and deserializes the standard response

    Args:
        url (str): base api url + endpoint route
        params (dictionary): key and value pairs to convert to get parameters

    Returns:
        (StdResponse/ErrResponse): deserialized json response depending if error in request or not
    """
    try:
        response = requests.post(url, json=params)
        json = response.json()
        if json['status'] == "ok":
            return deserialize_std_response(json)
        else:
            deserialize_err_response(json)
    except requests.ConnectionError as e:
        Log.error(TAG, "Connection Error for request:\n" + e.request.url + "\n" + str(e.args))
    except Exception as e:
        print("Now really panic!")
        Log.error(TAG, "General http get error!\n" + str(e))


def gsm_post(url, params):
    pass


def http_post(url, params):
    if device_state.networking.get_wifi_status() == CONNECTED:
        wifi_post(url, params)
    else:
        gsm_post(url, params)


