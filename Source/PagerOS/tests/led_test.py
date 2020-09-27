import RPi.GPIO as GPIO
import time

PIN_LED_MAIN = 23
PIN_LED_ALERT = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_LED_MAIN, GPIO.OUT)
# GPIO.setup(PIN_LED_ALERT, GPIO.OUT)

print("Turning on main status led.")

GPIO.output(PIN_LED_MAIN, GPIO.HIGH)
time.sleep(0.5)
GPIO.output(PIN_LED_MAIN, GPIO.LOW)
time.sleep(0.5)
GPIO.output(PIN_LED_MAIN, GPIO.HIGH)
time.sleep(0.5)
GPIO.output(PIN_LED_MAIN, GPIO.LOW)
