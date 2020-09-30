import time
from datetime import datetime
import RPi.GPIO as GPIO
from system.constants import *
from system.events import Event
from system.state import device_state
from helpers.config import config
from helpers.kojin_logging import Log

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
NOTE_FULL_LENGTH = 200
NOTE_HALF_LENGTH = 100


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
    GPIO.add_event_detect(PIN_MAIN_BUTTON, GPIO.FALLING, callback=handle_button_press, bouncetime=500)
    GPIO.add_event_detect(PIN_NEGATIVE_BUTTON, GPIO.FALLING, callback=handle_button_press)
    GPIO.add_event_detect(PIN_LEFT_BUTTON, GPIO.FALLING, callback=handle_button_press)
    GPIO.add_event_detect(PIN_RIGHT_BUTTON, GPIO.FALLING, callback=handle_button_press)

    Log.info(TAG, "Listening to inputs!")
    while True:
        time.sleep(0.5)


def handle_button_press(channel):
    """ Event handler for when any button is pressed"""
    Log.debug(TAG, "Button pressed - " + str(channel))
    start_time = time.time()
    while GPIO.input(channel) == 0:  # Wait for the button up
        pass
    button_time = time.time() - start_time
    Log.debug(TAG, f"Button released - {channel} after {button_time}")
    if channel == PIN_MAIN_BUTTON:
        on_main_button_press()
    elif channel == PIN_NEGATIVE_BUTTON:
        if button_time > 3:
            print("shutting down")
            on_shutdown_signal_received()
        else:
            on_negative_button_press()
    elif channel == PIN_LEFT_BUTTON:
        on_left_button_press()
    else:
        on_right_button_press()
    time.sleep(0.2)


def play_note(length, frequency):
    if not config.get_sound():
        time.sleep(length * frequency * 2)
        return
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
    Log.info(TAG, "Setting off alert for a shout!")
    time_started = datetime.now()
    for i in range(0, ALERTER_TIMEOUT):
        if acknowledged:
            time_taken = datetime.now() - time_started
            Log.info(TAG, f"Alert acknowledged. Stopping alerter after {time_taken.seconds} seconds.")
            break
        play_note(NOTE_FULL_LENGTH, FREQUENCY_LOW)
        GPIO.output(PIN_LED_ALERT, GPIO.HIGH)
        play_note(NOTE_FULL_LENGTH, FREQUENCY_HIGH)
        GPIO.output(PIN_LED_ALERT, GPIO.LOW)
    time_taken = datetime.now() - time_started
    if time_taken.seconds > ALERTER_TIMEOUT:
        Log.info(TAG, "Alert timed out.")
        on_update_alert_status(ALERT_STATUS_TIMED_OUT)


def handle_test():
    """ All io for alerting user there is a test alert is handled here """
    Log.info(TAG, "Setting off alert for a test!")
    time_started = datetime.now()
    for i in range(0, ALERTER_TIMEOUT):
        if device_state.get_state() != STATE_ACTIVE_ALERT:
            time_taken = datetime.now() - time_started
            Log.info(TAG, f"Alert acknowledged. Stopping alerter after {time_taken.seconds} seconds.")
            break
        play_note(NOTE_HALF_LENGTH, FREQUENCY_HIGH)
        GPIO.output(PIN_LED_ALERT, GPIO.HIGH)
        time.sleep(0.1)
        play_note(NOTE_HALF_LENGTH, FREQUENCY_HIGH)
        GPIO.output(PIN_LED_ALERT, GPIO.LOW)
        time.sleep(0.1)
    time_taken = datetime.now() - time_started
    if time_taken.seconds > ALERTER_TIMEOUT:
        Log.info(TAG, "Alert timed out.")
        on_update_alert_status(ALERT_STATUS_TIMED_OUT)


if __name__ == '__main__':
    start()
