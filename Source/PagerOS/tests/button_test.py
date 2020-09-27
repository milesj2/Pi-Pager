import RPi.GPIO as GPIO
import time

PIN_MAIN_BUTTON = 24

GPIO.setmode(GPIO.BCM)

GPIO.setup(PIN_MAIN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button to GPIO23


try:
    while True:
        button_state = GPIO.input(PIN_MAIN_BUTTON)
        if not button_state:

            print('Button Pressed...')
            time.sleep(0.2)
        else:
            pass
except:
    GPIO.cleanup()
