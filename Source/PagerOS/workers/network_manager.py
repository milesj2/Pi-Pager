import psutil
import time
import system.events
from helpers.kojin_logging import Log
from system.constants import *
from system.state import device_state
from helpers.config import config
import wifi

TAG = "network_manger"

INTERFACE_LOCAL = "lo"
ADDRESS_LOCAL = "127.0.0.1"
LAN = "eth0"


on_wifi_status_update = system.events.Event()


def start():
    """ Handles periodic checking of network connectivity status (wifi/cellular) """
    Log.info(TAG, "Starting Network Manager")
    while True:
        if device_state.get_state() == STATE_ACTIVE_ALERT or not config.get_wifi():
            Log.debug(TAG, f"Wifi disabled, skipping status check.")
            time.sleep(5)
            continue
        check_wifi()
        check_cellular()
        time.sleep(30)


def check_cellular():
    """ UNIMPLMENTED: interfaces with SIM800L to check cellular status and broadcasts result """
    pass


def check_wifi():
    """ Analyses connected wifi to see status and broadcasts result """
    interfaces = {}
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
        status = WIFI_SIGNAL_HIGH
    else:
        Log.debug(TAG, "Device has no connected interfaces!")
        status = NO_SIGNAL
    Log.debug(TAG, f"Raising event on_connection_status_update with status: {status}")
    on_wifi_status_update(status)


def get_available_wifi_networks():
    networks = []

    cells = wifi.Cell.all('wlp8s0')

    for cell in cells:
        networks.append(cell)
        print(cell.ssid)

    return networks
