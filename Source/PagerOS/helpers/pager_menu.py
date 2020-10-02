from system.classes import Event, MenuItem, Menu, KnownWifiManager
from system.constants import *
from helpers.kojin_logging import Log
from helpers.config import config


TAG = "Pager Menu"

on_view_wifi = Event()
on_toggle_wifi = Event()
on_manage_wifi = Event()
on_reset_wifi = Event()


def view_wifi():
    """ Finds current wifi information and adjusts the subitem's name below to be the info before selecting it """
    view_wifi_item = device_menu.get_current_menu().subitems[device_menu.current_item_index]
    view_wifi_item.subitems[0].name = "WIFI STATUS GOES BRRRR"
    device_menu.current_item.append(view_wifi_item)


def toggle_wifi():
    """ Switches on or off wifi in config and saves config state"""
    config.set_wifi(not config.get_wifi())
    config.save_state()


def delete_wifi():
    """ Deletes selected ssid from in memory list and overwrites wpa_supplicants.conf"""
    known_networks = KnownWifiManager()
    item = device_menu.current_item[len(device_menu.current_item) - 2]

    for ssid in known_networks.ssids:
        if item.name != ssid.ssid:
            continue
        known_networks.ssids.remove(ssid)
    known_networks.save()

    # Return to managing known networks
    device_menu.current_item.pop()
    device_menu.current_item.pop()
    manage_wifi()


def manage_wifi():
    """ Parses wpa_supplicants.conf to find stored SSIDs and passwords, then populates menu items for each one"""
    known_networks = KnownWifiManager()

    manage_wifi_item = device_menu.get_current_menu().subitems[device_menu.current_item_index]
    manage_wifi_item.subitems.clear()

    for known_network in known_networks.ssids:
        manage_wifi_item.subitems.append(MenuItem(known_network.ssid, MENU_TYPE_MENU, subitems=[
            MenuItem("Delete", MENU_TYPE_MENU, subitems=[
                MenuItem(f"Are you sure? ({known_network.ssid})", MENU_TYPE_ACTION, action=delete_wifi)
            ])
        ]))

    device_menu.current_item_index = 0
    device_menu.current_item.append(manage_wifi_item)
    del known_networks


def reset_wifi():
    pass


def view_cellular():
    """ Finds current cellular information and adjusts the subitem's name below to be the info before selecting it """
    view_cellular_item = device_menu.get_current_menu().subitems[device_menu.current_item_index]
    view_cellular_item.subitems[0].name = "CELLULAR STATUS GOES BRRRR"
    device_menu.current_item.append(view_cellular_item)


def toggle_cellular():
    """ Switches on or off cellular in config and saves config state"""
    config.set_cellular(not config.get_cellular())
    config.save_state()


def toggle_sound():
    """ Switches on or off wifi in config and saves config state"""
    config.set_sound(not config.get_sound())
    config.save_state()


def action_empty():
    """ Empty action for information only menu items """
    Log.debug(TAG, "Empty action triggered")


def action_unimplemented():
    """ Logs and throws error if unimplemented action triggered"""
    menu_stack = STRING_EMPTY
    for item in device_menu.current_item:
        menu_stack += f"    {item}\n"
    Log.error(TAG, f"Action not implemented!\n  Menu stack:\n{menu_stack}\n\n  Current item:\n    "
                   f"{device_menu.get_current_item()}")

    raise NotImplemented("Menu action not implemented!")


items = [
    MenuItem(MENU_MAIN, MENU_TYPE_MENU, subitems=[
                MenuItem(MENU_NETWORK, "MENU", subitems=[
                    MenuItem("Wifi", "MENU", subitems=[
                        MenuItem("View Wifi Status", MENU_TYPE_ACTION, action=view_wifi, subitems=[
                            MenuItem("STRING_EMPTY", MENU_TYPE_ACTION, action=action_empty)
                        ]),
                        MenuItem("Toggle Wifi", MENU_TYPE_ACTION, action=toggle_wifi),
                        MenuItem("Manage Known Networks", MENU_TYPE_ACTION, action=manage_wifi, subitems=[]),
                        MenuItem("Reset Wifi", MENU_TYPE_ACTION, action=reset_wifi)
                    ]),
                    MenuItem("Cellular/Mobile", "MENU", subitems=[
                        MenuItem("View Mobile Status", MENU_TYPE_ACTION, action=view_cellular, subitems=[
                            MenuItem("STRING_EMPTY", MENU_TYPE_ACTION, action=action_empty)
                        ]),
                        MenuItem("Toggle Mobile (LTE)", MENU_TYPE_ACTION, action=toggle_cellular),
                    ])
                ]),
                MenuItem(MENU_SOUND_VIBRATE, "MENU", subitems=[
                    MenuItem("Sound", "MENU", subitems=[
                        MenuItem("Toggle Sound", "ACTION", action=toggle_sound),
                    ]),
                    MenuItem("Vibrate", "MENU", subitems=[
                        MenuItem("Toggle Vibrate", "ACTION", action=action_unimplemented),
                    ]),
                ]),
        ])
]

device_menu = Menu(items)
