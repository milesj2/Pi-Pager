import time
from datetime import datetime
import RPi.GPIO as GPIO
from system.constants import *
from system.events import Event
from system.state import device_state
from helpers.config import config
from helpers.kojin_logging import Log
import threading


TAG = "gpio.thread"

PIN_NEGATIVE_BUTTON = 17
PIN_BUZZER = 18
PIN_LED_ALERT = 23
PIN_MAIN_BUTTON = 24
PIN_VIBRATE = 25
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
    GPIO.setup(PIN_VIBRATE, GPIO.OUT)
    GPIO.setup(PIN_LED_ALERT, GPIO.OUT)

    GPIO.setup(PIN_MAIN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PIN_NEGATIVE_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PIN_LEFT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PIN_RIGHT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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
    """ Plays a note given the length and frequency

    Args:
        length (int): How long the note should last
        frequency (int): affects oscillation. The larger the number, the lower the note.
    """
    for i in range(0, length):
        GPIO.output(PIN_BUZZER, GPIO.HIGH)
        time.sleep(frequency)
        GPIO.output(PIN_BUZZER, GPIO.LOW)
        time.sleep(frequency)


def vibrate(length, rest):
    """ Activates vibrate module

    Args:
        length (int): length of time the vibrate module will be on
        rest (int): length of time in between vibrations
    """
    GPIO.output(PIN_VIBRATE, GPIO.HIGH)
    time.sleep(length)
    GPIO.output(PIN_VIBRATE, GPIO.LOW)
    time.sleep(rest)


def handle_alert(shout_type):
    """ Event handler for when pager receives an alert """
    if shout_type == ALERT_TYPE_SHOUT:
        handle_shout()
    else:
        handle_test()


def alert_sound(note_length):
    """ Loops while in alert state and continually plays two notes

    Args:
        note_length (int): length of each note
    """
    while device_state.get_state() == STATE_ACTIVE_ALERT:
        play_note(note_length, FREQUENCY_HIGH)
        play_note(note_length, FREQUENCY_LOW)


def alert_vibrate(vibrate_length, rest):
    """ Loops while in alert state and continually toggles vibrate

    Args:
        vibrate_length (int): length of time the vibrate module will be on
        rest (int): length of time in between vibrations
    """
    while device_state.get_state() == STATE_ACTIVE_ALERT:
        vibrate(vibrate_length, rest)


def alert_led(flashes):
    """ Loops while in alert state and flashes led in accordance to given sequence

    Args:
        flashes (list): list of lists of two values.
                        - Position one either GPIO.HIGH or GPIO.LOW,
                        - Position two is sleep length
                        e.g. [ [GPIO.HIGH, 0.1], [GPIO.LOW, 0.9] ]
    """
    while device_state.get_state() == STATE_ACTIVE_ALERT:
        for flash in flashes:
            GPIO.output(PIN_LED_ALERT, flash[0])
            time.sleep(flash[1])


def handle_shout():
    """ All io for alerting user there is a shout is handled here """
    Log.info(TAG, "Setting off alert for a shout!")
    time_started = datetime.now()

    led_flash_sequence = [
        [GPIO.HIGH, 0.1],
        [GPIO.LOW, 0.1],
        [GPIO.HIGH, 0.1],
        [GPIO.LOW, 0.7]
    ]

    t_vibrate = threading.Thread(target=alert_vibrate, args=(0.5, 0.25,))
    t_sound = threading.Thread(target=alert_sound, args=(NOTE_FULL_LENGTH,))
    t_led = threading.Thread(target=alert_led, args=(led_flash_sequence,))

    if config.get_sound():
        t_sound.start()
    if config.get_vibrate():
        t_vibrate.start()
    t_led.start()

    for i in range(0, ALERTER_TIMEOUT):
        if acknowledged:
            time_taken = datetime.now() - time_started
            Log.info(TAG, f"Alert acknowledged. Stopping alerter after {time_taken.seconds} seconds.")
            break
        time.sleep(1)
    time_taken = datetime.now() - time_started
    if time_taken.seconds > ALERTER_TIMEOUT:
        Log.info(TAG, "Alert timed out.")
        on_update_alert_status(ALERT_STATUS_TIMED_OUT)


def handle_test():
    """ All io for alerting user there is a test alert is handled here """
    Log.info(TAG, "Setting off alert for a test!")

    led_flash_sequence = [
        [GPIO.HIGH, 0.5],
        [GPIO.LOW, 0.5],
    ]

    t_vibrate = threading.Thread(target=alert_vibrate, args=(0.25, 0.25,))
    t_sound = threading.Thread(target=alert_sound, args=(NOTE_HALF_LENGTH,))
    t_led = threading.Thread(target=alert_led, args=(led_flash_sequence,))

    if config.get_sound():
        t_sound.start()
    if config.get_vibrate():
        t_vibrate.start()
    t_led.start()

    time_started = datetime.now()
    for i in range(0, ALERTER_TIMEOUT):
        if device_state.get_state() != STATE_ACTIVE_ALERT:
            time_taken = datetime.now() - time_started
            Log.info(TAG, f"Alert acknowledged. Stopping alerter after {time_taken.seconds} seconds.")
            break
        time.sleep(1)
    time_taken = datetime.now() - time_started
    if time_taken.seconds > ALERTER_TIMEOUT:
        Log.info(TAG, "Alert timed out.")
        on_update_alert_status(ALERT_STATUS_TIMED_OUT)


if __name__ == '__main__':
    start()
