from system.globals import *
from helpers.kojin_logging import Log
from helpers.config import config


TAG = "Pager Menu"

on_view_wifi = Event()
on_toggle_wifi = Event()
on_manage_wifi = Event()
on_reset_wifi = Event()


def view_wifi():
    view_wifi_item = device_menu.get_current_menu().subitems[device_menu.current_item_index]
    view_wifi_item.subitems[0].name = "WIFI STATUS GOES BRRRR"
    device_menu.current_item.append(view_wifi_item)


def toggle_wifi():
    config.set_wifi(not config.get_wifi())
    config.save_state()


def manage_wifi():
    pass


def reset_wifi():
    pass


def view_cellular():
    view_cellular_item = device_menu.get_current_menu().subitems[device_menu.current_item_index]
    view_cellular_item.subitems[0].name = "CELLULAR STATUS GOES BRRRR"
    device_menu.current_item.append(view_cellular_item)


def toggle_cellular():
    config.set_cellular(not config.get_cellular())
    config.save_state()


def action_empty():
    Log.debug(TAG, "Empty action triggered")


def action_unimplemented():
    Log.error(TAG, "Action not implemented!")


items = [
    MenuItem(MENU_MAIN, MENU_TYPE_MENU, subitems=[
                MenuItem(MENU_NETWORK, "MENU", subitems=[
                    MenuItem("Wifi", "MENU", subitems=[
                        MenuItem("View Wifi Status", MENU_TYPE_ACTION, action=view_wifi, subitems=[
                            MenuItem("STRING_EMPTY", MENU_TYPE_ACTION, action=action_empty)
                        ]),
                        MenuItem("Toggle Wifi", MENU_TYPE_ACTION, action=toggle_wifi),
                        MenuItem("Manage Known Networks", "DIALOGUE", action=action_unimplemented),
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
                        MenuItem("Toggle Sound", "ACTION", action=action_unimplemented),
                    ]),
                    MenuItem("Vibrate", "MENU", subitems=[
                        MenuItem("Toggle Vibrate", "ACTION", action=action_unimplemented),
                    ]),
                ]),
        ])
]

device_menu = Menu(items)
