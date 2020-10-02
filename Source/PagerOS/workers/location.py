import time
import serial
from system.classes import Location, LongLat
from system.constants import *
from system.state import device_state
from system.events import Event
from helpers.kojin_logging import Log
from helpers.config import config
import helpers.location_requests as k_requests


TAG = "location.thread"

ser = serial.Serial("/dev/ttyAMA0")
gpgga_info = "$GPGGA"
GPGGA_buffer = 0
NMEA_buff = 0

on_update_location = Event()


def start():
    """ Handles periodic location updates. """
    while True:
        Log.info(TAG, "Searching for location.")
        wifi = LongLat(-1, -1)
        if config.get_wifi():
            wifi = get_wifi_location()
        gps = get_gps_location()
        loc = Location(gps, wifi)
        on_update_location(loc)
        if device_state.get_state() != STATE_ACTIVE_ALERT:
            # Sleep for 5 minutes, or until there is a an alert.
            for i in range(0, 60):
                if device_state.get_state() == STATE_ACTIVE_ALERT:
                    break
                time.sleep(5)
        else:
            time.sleep(5)


def get_wifi_location():
    """ Sends nearby BSSIDs to location api and returns approx location

    returns:
        (LongLat): (-1, -1) if request error, or real data.
    """
    # TODO get wifi stats
    bssids = ["ac:3b:77:ee:1e:b6", "78:44:76:d3:42:30"]

    Log.info(TAG, "Finding location via WIFI.")

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
        return LongLat(-1, -1)


def get_gps_location():
    """ Parses serial output of neo-6m GPS module and extract long/lat from data buffer

    Modified code from source:
    https://www.engineersgarage.com/microcontroller-projects/articles-raspberry-pi-neo-6m-gps-module-interfacing/

    returns:
        gps_loc (LongLat): (-1, -1) if no GPS signal, or real data.

    """
    gps_loc = LongLat(-1, -1)
    Log.info(TAG, f"Waiting for GPS data input.")
    received_data = []
    for i in range(0, 10):
        received_data = ser.readline().decode().split(",")
        if received_data[0] == gpgga_info:
            break
        time.sleep(1)
    if len(received_data) == 0:
        return gps_loc
    Log.info(TAG, f"Processing GPS data.")
    nmea_buff = received_data[1:]
    nmea_latitude = nmea_buff[1]
    nmea_latitude_direction = nmea_buff[2]
    nmea_longitude = nmea_buff[3]
    nmea_longitude_direction = nmea_buff[4]
    if nmea_latitude != STRING_EMPTY or nmea_longitude != STRING_EMPTY:
        gps_loc.lat = convert_to_degrees(nmea_latitude, nmea_latitude_direction)
        gps_loc.long = convert_to_degrees(nmea_longitude, nmea_longitude_direction)
        Log.info(TAG, f"NMEA Latitude: {gps_loc.lat} | NMEA Longitude: {gps_loc.long}")
    return gps_loc


def convert_to_degrees(raw_value, direction):
    """ Takes raw data and compass direction and converts it to degrees

    Modified from:
    https://www.engineersgarage.com/microcontroller-projects/articles-raspberry-pi-neo-6m-gps-module-interfacing/

    args:
        raw_value (str): Latitude or longitude position
        direction (char): First letter of compass direction (N, S, E, W)
    return:
        position (float): degrees
    """
    raw_value = float(raw_value)
    if direction == "S" or direction == "W":
        raw_value = - raw_value
    decimal_value = raw_value / 100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value - int(decimal_value)) / 0.6
    position = degrees + mm_mmmm
    return "%.8f" % position




if __name__ == '__main__':
    Log.debug(TAG, "Starting test")
    # loc = get_wifi_location()
    # print(loc.long, loc.lat)

