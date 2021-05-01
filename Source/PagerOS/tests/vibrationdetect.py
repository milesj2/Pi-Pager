import RPi.GPIO as GPIO
import time

# GPIO SETUP
CHANNEL = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(CHANNEL, GPIO.IN)


vibrate_pattern = []

modes = ["ON", "OFF"]


def callback(channel):
    vibrate_pattern.clear()
    start_time = time.time()
    pattern_time = start_time
    up_or_down = GPIO.input(channel)
    while time.time() - start_time < 2:
        time.sleep(0.001)
        if GPIO.input(channel) == up_or_down:
            continue
        vibrate_pattern.append([up_or_down, time.time()-pattern_time])
        up_or_down = GPIO.input(channel)
        pattern_time = time.time()
    print(vibrate_pattern)

    for stuff in vibrate_pattern:
        print(modes[stuff[0]], "for", stuff[1])
    print("END")


def callback2(channel):
    start_time = time.time()
    while True:
        # time.sleep(0.0005)
        print(time.time(), GPIO.input(channel))
    print("END")



GPIO.add_event_detect(CHANNEL, GPIO.FALLING, callback=callback2, bouncetime=10000)  # let us know when the pin goes HIGH or LOW


print("Setup complete")
# infinite loop
while True:
    time.sleep(1)
