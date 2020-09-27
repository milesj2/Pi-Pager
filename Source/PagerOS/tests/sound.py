import os
import time

file = "alerter.mp3"

while True:
    os.system("mpg123 " + file)
