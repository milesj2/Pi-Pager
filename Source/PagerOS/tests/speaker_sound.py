import RPi.GPIO as GPIO
import time

PIN_BUZZER = 18
PIN_VIBRATE = 25

FREQUENCY_HIGH = 0.0011
FREQUENCY_LOW = 0.001

NOTE_LENGTH = 200

GPIO.setmode(GPIO.BCM)

GPIO.setup(PIN_BUZZER, GPIO.OUT)
GPIO.setup(PIN_VIBRATE, GPIO.OUT)


def make_note(length, frequency):
    for i in range(0, length):
        GPIO.output(PIN_BUZZER, GPIO.HIGH)
        time.sleep(frequency)
        GPIO.output(PIN_BUZZER, GPIO.LOW)
        time.sleep(frequency)


GPIO.output(PIN_VIBRATE, GPIO.HIGH)
make_note(NOTE_LENGTH, 0.001)
make_note(NOTE_LENGTH, 0.0011)
GPIO.output(PIN_VIBRATE, GPIO.HIGH)
make_note(NOTE_LENGTH, 0.001)
GPIO.output(PIN_VIBRATE, GPIO.LOW)
make_note(NOTE_LENGTH, 0.0011)
GPIO.output(PIN_VIBRATE, GPIO.HIGH)
make_note(NOTE_LENGTH, 0.001)
make_note(NOTE_LENGTH, 0.0011)
GPIO.output(PIN_VIBRATE, GPIO.LOW)
make_note(NOTE_LENGTH, 0.001)
make_note(NOTE_LENGTH, 0.0011)

