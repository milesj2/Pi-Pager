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


def start():
    interfaces = {}
    Log.info(TAG, "Starting Network Manager")
    while True:
        # FIXME: should this skip?
        if device_state.get_state() == STATE_ACTIVE_ALERT or device_state.networking.get_wifi_status() == DISABLED:
            Log.debug(TAG, f"Wifi disabled, skipping status check.")
            time.sleep(5)
            continue
        connected_interfaces = 0
        Log.debug(TAG, "Looking for connected devices")
        if_addrs = psutil.net_if_addrs()
        for interface_name, interface_addresses in if_addrs.items():
            Log.debug(TAG, f"Found device: {interface_name}")
            interfaces[interface_name] = False
            for address in interface_addresses:
                Log.debug(TAG, f"|-- {str(address.family)} | {address.address}")
                if str(address.family) != 'AddressFamily.AF_INET':
                    continue
                if address.address == ADDRESS_LOCAL:
                    continue
                connected_interfaces += 1
                interfaces[interface_name] = True
        Log.debug(TAG, f"Out of {len(if_addrs.items()) - 1} interfaces, {connected_interfaces} were connected.")
        if connected_interfaces > 0:
            # TODO: get wifi strength
            status = 3
        else:
            Log.debug(TAG, "Device has no connected interfaces!")
            status = 0
        Log.debug(TAG, f"Raising event on_connection_status_update with status: {status}")
        on_connection_status_update(status)
        time.sleep(30)
