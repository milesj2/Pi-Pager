import threading
import time
import os

from system.state import device_state
from system.classes import ALERT_EMPTY
from system.constants import *
from helpers.config import config
from helpers.kojin_logging import Log
from helpers.pager_menu import device_menu
from workers import gpio, networking, network_manager, location, display

TAG = "main"

current_alert = ALERT_EMPTY


def main():
    """ Main method for pager.

    This handles all threads, assigning events and monitors threads to make sure they haven't crashed.

    """
    Log.info(TAG, "Pager Starting.")
    display.set_display_text("Initialising...")
    device_state.set_state(STATE_INITIALISING)

    if config.get_debug():
        Log.debug(TAG, "Debugging enabled.")
        Log.debugging = config.get_debug()

    if not config.get_graceful_exit():
        Log.warn(TAG, "Pager did not exit gracefully!")
        # TODO handle uploading logs to ftp server

    config.set_graceful_exit(False)
    config.save_state()

    #################################################
    # ############## handlers  ######################
    #################################################
    networking.on_received_alert.append(handle_alert)
    networking.on_update_connection_status(device_state.networking.set_api_status)

    network_manager.on_connection_status_update.append(handle_connection_status_update)

    location.on_update_location.append(networking.on_update_location)

    gpio.on_shutdown_signal_received.append(handle_shut_down)
    gpio.on_main_button_press.append(handle_main_button_press)
    gpio.on_negative_button_press.append(handle_negative_button_press)
    gpio.on_left_button_press.append(handle_left_button_press)
    gpio.on_right_button_press.append(handle_right_button_press)

    #################################################
    # ############### threads  ######################
    #################################################

    t_net = threading.Thread(target=networking.start)
    t_location = threading.Thread(target=location.start)
    t_gpio = threading.Thread(target=gpio.start)
    t_net_manager = threading.Thread(target=network_manager.start)
    t_display = threading.Thread(target=display.start)
    # t_bluetooth = threading.Thread(target=bluetooth.start)

    t_net.start()
    t_gpio.start()
    t_net_manager.start()
    t_display.start()
    t_location.start()
    # t_bluetooth.start()

    Log.info(TAG, "Finished setup.")
    device_state.set_state(STATE_IDLE)

    display.clear_display_text()

    while True:
        if not t_net.is_alive():
            Log.warn(TAG, "Networking thread has died. Restarting...")
            t_net = threading.Thread(target=networking.start)
            t_net.start()
        if not t_gpio.is_alive():
            Log.warn(TAG, "GPIO thread has died. Restarting...")
            t_gpio = threading.Thread(target=gpio.start)
            t_gpio.start()
        if not t_net_manager.is_alive():
            Log.warn(TAG, "Network manager thread has died. Restarting...")
            t_net_manager = threading.Thread(target=network_manager.start)
            t_net_manager.start()
        if not t_display.is_alive():
            Log.warn(TAG, "Display thread has died. Restarting...")
            t_display = threading.Thread(target=network_manager.start)
            t_display.start()
        if not t_location.is_alive():
            Log.warn(TAG, "Location thread has died. Restarting...")
            t_net_manager = threading.Thread(target=location.start)
            t_net_manager.start()
        time.sleep(10)


########################################
# ########## EVENTS ####################
########################################

def handle_connection_status_update(status):
    """ Gets a status update and updates display

     Args:
         status (str) : status of connection
    """
    device_state.networking.set_wifi_status(status)


def handle_main_button_press():
    """ Receives event from GPIO and performs actions based on device state """
    if device_state.get_state() == STATE_ACTIVE_ALERT:
        display.clear_display_text()
        handle_update_alert_status(ALERT_STATUS_ACKNOWLEDGE)
    elif device_state.get_state() == STATE_MENU:
        if display.refreshing:
            return
        display.refreshing = True
        device_menu.select_item()
    else:
        if display.refreshing:
            return
        display.refreshing = True
        device_menu.reset()
        display.clear_display_text()
        device_state.set_state(STATE_MENU)


def handle_negative_button_press():
    """ Receives event from GPIO and performs actions based on device state """
    if device_state.get_state() == STATE_ACTIVE_ALERT:
        handle_update_alert_status(ALERT_STATUS_DISMISSED)
    elif device_state.get_state() == STATE_MENU:
        if display.refreshing:
            return
        display.refreshing = True
        device_menu.deselect_item()
    else:
        if display.refreshing:
            return
        display.refreshing = True
        device_menu.reset()
        display.clear_display_text()


def handle_left_button_press():
    """ Receives event from GPIO and performs actions based on device state """
    if device_state.get_state() == STATE_MENU:
        if display.refreshing:
            return
        display.refreshing = True
        device_menu.move_left()


def handle_right_button_press():
    """ Receives event from GPIO and performs actions based on device state """
    if device_state.get_state() == STATE_MENU:
        if display.refreshing:
            return
        display.refreshing = True
        device_menu.move_right()


def handle_alert(alert):
    """ Event handler for receiving alert from networking

    Args:
        alert (system.classes.Alert) : alert class with all attributes of current alert

    """
    global current_alert
    current_alert = alert
    display.set_display_text(alert.type)
    if alert.type != ALERT_TYPE_SHOUT and alert.type != ALERT_TYPE_TEST:
        Log.error(TAG, "Received a shout of unknown type! -> shout_type '" + alert.type + "'")
        return
    Log.info(TAG, f"Setting device state to {STATE_ACTIVE_ALERT}.")
    device_state.set_state(STATE_ACTIVE_ALERT)
    gpio.acknowledged = False
    gpio.on_update_alert_status.append(handle_update_alert_status)
    gpio.handle_alert(alert.type)


def handle_update_alert_status(status):
    """ Event handler for receiving gpio input during alerting state

    Args:
        status (str) : acknowledged/dismissed etc to send to the api

    """
    Log.info(TAG, "Acknowledge alert.")
    # FIXME: Change this to update device state?
    gpio.acknowledged = True
    if current_alert is not None:
        networking.update_alert_status(current_alert.id, status)

    # FIXME: delete this next line?
    gpio.on_update_alert_status.clear()

    Log.info(TAG, f"Setting device state to {STATE_IDLE}.")
    device_state.set_state(STATE_IDLE)
    display.clear_display_text()


def handle_shut_down():
    """ Shuts down the pager gracefully """
    display.set_display_text("Shutting down.")
    device_state.set_state(STATE_SHUTTING_DOWN)
    config.set_graceful_exit(True)
    config.save_state()
    time.sleep(3)
    display.clear_display_text()
    os.system('sudo shutdown now')


if __name__ == '__main__':
    Log.info(TAG, "Starting pager version " + PAGER_VERSION)
    main()
