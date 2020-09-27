from system.constants import *
from system.menu import Menu, MenuItem
from system.events import Event
from helpers.kojin_logging import Log


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
    pass


def manage_wifi():
    pass


def reset_wifi():
    pass


def action_empty():
    pass


def action_unimplemented():
    Log.error(TAG, "Action not implemented!")


items = [
    MenuItem(MENU_MAIN, MENU_TYPE_MENU, subitems=[
                MenuItem(MENU_NETWORK, "MENU", subitems=[
                    MenuItem(SUB_MENU_WIFI, "MENU", subitems=[
                        MenuItem("View Wifi Status", MENU_TYPE_ACTION, action=view_wifi, subitems=[
                            MenuItem("STRING_EMPTY", MENU_TYPE_ACTION, action=action_empty)
                        ]),
                        MenuItem("Toggle Wifi", "MENU", subitems=[
                            MenuItem("On", MENU_TYPE_ACTION, action=action_unimplemented),
                            MenuItem("Off", MENU_TYPE_ACTION, action=action_unimplemented),
                        ]),
                        MenuItem("Manage Known Networks", "DIALOGUE", action=action_unimplemented),
                        MenuItem("Reset Wifi", MENU_TYPE_ACTION, action=reset_wifi)
                    ]),
                    MenuItem(SUB_MENU_MOBILE, "MENU", subitems=[
                        MenuItem("View Mobile Status", MENU_TYPE_ACTION, action=action_unimplemented),
                        MenuItem("Toggle Mobile (LTE)", MENU_TYPE_ACTION, action=action_unimplemented),
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
