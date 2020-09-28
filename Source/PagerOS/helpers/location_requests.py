from system.globals import *
from helpers.kojin_logging import Log
import requests

TAG = "Location_Requests"


class StdResponse:
    """ Deserialised class formed from default response from API"""
    def __init__(self, status, balance, lat, lon, accuracy):
        self.status = status
        self.balance = balance
        self.lat = lat
        self.lon = lon
        self.accuracy = accuracy


class ErrResponse:
    """ Deserialised class formed from default response from API"""
    status = STRING_EMPTY
    message = STRING_EMPTY

    def __init__(self, status, message, balance):
        self.status = status
        self.message = message
        self.balance = balance


def deserialize_std_response(json):
    return StdResponse(json['status'], json['balance'], json['lat'], json['lon'], json['accuracy'])


def deserialize_err_response(json):
    return ErrResponse(json['status'], json['message'], json['balance'])


def http_post(url, params):
    try:
        response = requests.post(url, json=params)
        json = response.json()
        # print(json)
        if json['status'] == "ok":
            return deserialize_std_response(json)
        else:
            deserialize_err_response(json)
    except requests.ConnectionError as e:
        Log.error(TAG, "Connection Error for request:\n" + e.request.url + "\n" + str(e.args))
    except Exception as e:
        print("Now really panic!")
        Log.error(TAG, "General http get error!\n" + str(e))

