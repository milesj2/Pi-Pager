import time

from helpers.kojin_requests import *
from helpers.kojin_logging import Log
from system.constants import *
from system.state import device_state
from system.classes import ALERT_EMPTY, Alert, Location
from helpers.config import config
from system import events
from helpers.device_requests import Requests

TAG = "networking.thread"

# Events
on_received_alert = events.Event()
on_update_connection_status = events.Event()


def start():
    Log.info(TAG, f"Starting networking as {config.get_access_token()}")

    while True:
        if device_state.get_state() == STATE_RESPONDING or device_state.get_state() == STATE_ACTIVE_ALERT:
            time.sleep(3)
            continue

        alert = search_for_alert()
        if alert.type == ALERT_TYPE_SHOUT or alert.type == ALERT_TYPE_TEST:
            raise_alert(alert)
        time.sleep(3)


def raise_alert(alert):
    Log.info(TAG, f"Received an alert type: {alert.type} | ID: {alert.id}")
    Log.info(TAG, f"Setting device state to " + STATE_ACTIVE_ALERT)
    on_received_alert(alert)


def search_for_alert():
    Log.debug(TAG, "Searching for alert.")
    params = {
        URL_PARAM_ACCESS_TOKEN: config.get_access_token()
    }

    api_status = True

    req = Requests()
    url = URL_KOJIN_API + URL_ROUTE_KOJIN_API_GET_ALERT.format(serial=config.get_serial())
    response = req.http_get(url, params)
    print(response)
    if response['value'] == "":
        response = req.deserialise_response(response['value'], StdResponse)
    else:
        response = req.deserialise_response(response, StdResponse)

    if response is None:
        alert = ALERT_EMPTY
        api_status = False
    elif response.status == RESPONSE_STATUS_ERROR:
        alert = ALERT_EMPTY
    elif response.message == STRING_EMPTY:
        alert = ALERT_EMPTY
    else:
        alert = req.deserialise_response(response.message[0], Alert)
    on_update_connection_status(api_status)
    return alert


def update_alert_status(alert_id, status):
    params = {
        URL_PARAM_ACCESS_TOKEN: config.get_access_token(),
        URL_PARAM_ALERT_ID: alert_id,
        URL_PARAM_STATUS: status
    }

    Log.info(TAG, f"Acknowledging shout {alert_id} as {status}.")

    url = URL_KOJIN_API + URL_ROUTE_KOJIN_API_ACKNOWLEDGE_ALERT.format(serial=config.get_serial())
    response = http_get(url, params)

    Log.info(TAG, f"Response from server (code: {response.status}): {response.message}")
    return True


def on_update_location(location: Location):
    params = {
        URL_PARAM_ACCESS_TOKEN: config.get_access_token(),
        URL_PARAM_ALERT_ID: location.gps,
        URL_PARAM_STATUS: location.wifi
    }
    Log.info(TAG, f"Updating location gps: {location.gps.long}, {location.gps.lat} | "
                  f"wifi: {location.wifi.long}, {location.wifi.lat}.")

    req = Requests()

    url = URL_KOJIN_API + URL_ROUTE_KOJIN_API_ACKNOWLEDGE_ALERT.format(config.get_serial())
    json_response = req.http_get(url, params)
    response = req.deserialise_response(json_response['value'], StdResponse)

    Log.info(TAG, f"Response from server (code: {response.status}): {response.message}")


if __name__ == '__main__':
    start()
