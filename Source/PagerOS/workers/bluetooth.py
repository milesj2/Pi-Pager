import time
from helpers.kojin_logging import Log


TAG = "bluetooth.thread"


def start():
    while True:
        Log.info(TAG, "Handling bluetooth stuff.")
        time.sleep(5)
