import time
import datetime
import RPi.GPIO as GPIO
from system.globals import *
from helpers.config import config
from helpers.kojin_logging import Log
from system.events import Event


TAG = "gpio.thread"
PIN_NEGATIVE_BUTTON = 17
PIN_BUZZER = 18
PIN_LED_ALERT = 23
PIN_MAIN_BUTTON = 24
PIN_LED_POWER = 25
PIN_LEFT_BUTTON = 27
PIN_RIGHT_BUTTON = 22

FREQUENCY_HIGH = 0.0011
FREQUENCY_LOW = 0.001
NOTE_LENGTH = 200


on_shutdown_signal_received = Event()
on_update_alert_status = Event()

on_main_button_press = Event()
on_negative_button_press = Event()
on_left_button_press = Event()
on_right_button_press = Event()

acknowledged = False


def start():
    Log.info(TAG, f"Show GPIO warnings set to {config.get_gpio_warnings_enabled()}.")
    GPIO.setwarnings(config.get_gpio_warnings_enabled())
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(PIN_BUZZER, GPIO.OUT)
    GPIO.setup(PIN_LED_POWER, GPIO.OUT)
    GPIO.setup(PIN_LED_ALERT, GPIO.OUT)

    GPIO.setup(PIN_MAIN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PIN_NEGATIVE_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PIN_LEFT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PIN_RIGHT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    Log.info(TAG, "Turning on main status led.")
    GPIO.output(PIN_LED_POWER, GPIO.HIGH)

    # Add main button listener
    GPIO.add_event_detect(PIN_MAIN_BUTTON, GPIO.RISING, callback=handle_button_press)
    GPIO.add_event_detect(PIN_NEGATIVE_BUTTON, GPIO.RISING, callback=handle_button_press)
    GPIO.add_event_detect(PIN_LEFT_BUTTON, GPIO.RISING, callback=handle_button_press)
    GPIO.add_event_detect(PIN_RIGHT_BUTTON, GPIO.RISING, callback=handle_button_press)

    Log.info(TAG, "Listening to inputs!")
    while True:
        time.sleep(0.5)


def handle_button_press(channel):
    """ Event handler for when any button is pressed"""
    Log.debug(TAG, "Button pressed - " + str(channel))
    if channel == PIN_MAIN_BUTTON:
        on_main_button_press()
    elif channel == PIN_NEGATIVE_BUTTON:
        on_negative_button_press()
    elif channel == PIN_LEFT_BUTTON:
        on_left_button_press()
    else:
        on_right_button_press()
    time.sleep(0.2)


def play_note(length, frequency):
    for i in range(0, length):
        GPIO.output(PIN_BUZZER, GPIO.HIGH)
        time.sleep(frequency)
        GPIO.output(PIN_BUZZER, GPIO.LOW)
        time.sleep(frequency)


def handle_alert(shout_type):
    """ Event handler for when pager receives an alert """
    if shout_type == ALERT_TYPE_SHOUT:
        handle_shout()
    else:
        handle_test()


def handle_shout():
    """ All io for alerting user there is a shout is handled here """
    global acknowledged
    acknowledged = False
    Log.info(TAG, "Setting off alert for a shout!")
    time_started = datetime.time
    for i in range(0, ALERTER_TIMEOUT):
        if acknowledged:
            time_finished = datetime.time
            Log.info(TAG, f"Alert acknowledged. Stopping alerter after {i} seconds.")
            break
        play_note(NOTE_LENGTH, FREQUENCY_LOW)
        GPIO.output(PIN_LED_ALERT, GPIO.HIGH)
        play_note(NOTE_LENGTH, FREQUENCY_HIGH)
        GPIO.output(PIN_LED_ALERT, GPIO.LOW)
    if not acknowledged:
        Log.info(TAG, "Alert timed out.")
        on_update_alert_status(ALERT_STATUS_TIMED_OUT)


def handle_test():
    """ All io for alerting user there is a test alert is handled here """
    global acknowledged
    acknowledged = False
    Log.info(TAG, "Setting off alert for a test!")

    for i in range(0, ALERTER_TIMEOUT):
        if device_state.get_state() != STATE_ACTIVE_ALERT:
            Log.info(TAG, f"Alert acknowledged. Stopping alerter after {i} seconds.")
            break
        play_note(100, FREQUENCY_HIGH)
        GPIO.output(PIN_LED_ALERT, GPIO.HIGH)
        time.sleep(0.1)
        play_note(100, FREQUENCY_HIGH)
        GPIO.output(PIN_LED_ALERT, GPIO.LOW)
        time.sleep(0.1)
    # if not acknowledged:
    # If it has not been acknowledged and still in active alert state
    if device_state.get_state() == STATE_ACTIVE_ALERT:
        Log.info(TAG, "Alert timed out.")
        on_update_alert_status(ALERT_STATUS_TIMED_OUT)


if __name__ == '__main__':
    start()
