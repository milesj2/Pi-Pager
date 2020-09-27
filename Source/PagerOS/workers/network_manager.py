import psutil
import time
import system.events
from helpers.kojin_logging import Log
from system.globals import *

TAG = "network_manger"

INTERFACE_LOCAL = "lo"
ADDRESS_LOCAL = "127.0.0.1"
LAN = "eth0"


on_connection_status_update = system.events.Event()


interfaces = {}


def start():
    Log.info(TAG, "Starting Network Manager")
    while True:
        if device_state.get_state() == STATE_ACTIVE_ALERT:
            time.sleep(5)
            continue
        counter = 0
        Log.debug(TAG, "Looking for connected devices")
        if_addrs = psutil.net_if_addrs()
        for interface_name, interface_addresses in if_addrs.items():
            interfaces[interface_name] = False
            Log.debug(TAG, f"Found device: {interface_name}")
            for address in interface_addresses:
                Log.debug(TAG, f"|-- {str(address.family)} | {address.address}")
                if str(address.family) != 'AddressFamily.AF_INET':
                    continue
                if address.address == ADDRESS_LOCAL:
                    continue
                counter += 1
                interfaces[interface_name] = True
        Log.debug(TAG, f"Out of {len(if_addrs.items()) - 1} interfaces, {counter} were connected.")
        if counter > 0:
            status = "high"
        else:
            Log.warn(TAG, "Device has no connected interfaces!")
            status = "no"
        Log.debug(TAG, "Raising event on_connection_status_update with status: " + status)
        on_connection_status_update(status)
        time.sleep(30)
