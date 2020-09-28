import time
from system.classes import Location, LongLat
from system.constants import *
from system.globals import device_state
from system.events import Event
from helpers.kojin_logging import Log
from helpers.config import Config
import helpers.location_requests as k_requests


TAG = "location.thread"

on_update_location = Event()


def start():
    while True:
        Log.info(TAG, "Handling location stuff.")
        wifi = LongLat("", "")
        # if device_state.networking.get_wifi_status() != DISABLED:
        if Config.get_wifi():
            wifi = get_wifi_location()
        gps = get_gps_location()
        loc = Location(gps, wifi)
        on_update_location(loc)
        if device_state.get_state() != STATE_ACTIVE_ALERT:
            time.sleep(300)
        else:
            time.sleep(5)


def get_wifi_location():
    # TODO get wifi stats
    bssids = ["ac:3b:77:ee:1e:b6", "78:44:76:d3:42:30"]

    params = {
        "token": LOCATION_API_KEY,
        "wifi": [{
            "bssid": bssids[0],
            "channel": 11,
            "frequency": 2462,
            "signal": -64
        }, {
            "bssid": bssids[1]
        }]
    }

    wifi_loc = k_requests.http_post(URL_LOCATION_API + URL_ROUTE_LOCATION_API_LOCATION, params)
    if wifi_loc.status == "ok":
        return LongLat(wifi_loc.lon, wifi_loc.lat)
    else:
        return LongLat("", "")


def get_gps_location():
    # interace with gpio
    return LongLat("", "")


if __name__ == '__main__':
    Log.debug(TAG, "Starting test")
    # loc = get_wifi_location()
    # print(loc.long, loc.lat)

