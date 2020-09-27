from system.globals import *
from system.events import *


class MenuItem:
    name = STRING_EMPTY
    subitems = []
    type = STRING_EMPTY
    action = STRING_EMPTY

    def __init__(self, name, itemType, action=None, args=None, subitems=None):
        if subitems is None:
            subitems = []
        if args is None:
            args = []
        self.name = name
        self.subitems = subitems
        self.type = itemType
        self.action = action
        self.args = args

    def __str__(self):
        if self.type == MENU_TYPE_MENU:
            return f"Menu item {self.name}; type: {self.type}; subitems: {self.subitems}"
        else:
            return f"Menu item {self.name}; type: {self.type}; action: {self.action}; args = {self.args}"


class Menu:
    on_action = Event()
    _on_action = Event()
    on_menu_exit = Event()
    current_item = []

    current_index = 0
    current_item_index = 0

    MENU_STATE_ROAMING = "ROAMING"
    MENU_STATE_DIALOGUE = "DIALOGUE"

    menu_state = MENU_STATE_DIALOGUE

    items = [
        MenuItem(MENU_MAIN, MENU_TYPE_MENU, subitems=[
            MenuItem(MENU_NETWORK, "MENU", subitems=[
                MenuItem(SUB_MENU_WIFI, "MENU", subitems=[
                    MenuItem("View Wifi Status", "ACTION", action=_on_action),
                    MenuItem("Toggle Wifi", "MENU", subitems=[
                        MenuItem("On", "ACTION", action=_on_action),
                        MenuItem("Off", "ACTION", action=_on_action),
                    ]),
                    MenuItem("Manage Known Networks", "DIALOGUE", action=_on_action),
                    MenuItem("Reset Wifi", "ACTION", action=_on_action)
                ]),
                MenuItem(SUB_MENU_MOBILE, "MENU", subitems=[
                    MenuItem("View Mobile Status", "ACTION", action=_on_action),
                    MenuItem("Toggle Mobile (LTE)", "ACTION", action=_on_action),
                ])
            ]),
            MenuItem(MENU_SOUND_VIBRATE, "MENU", subitems=[
                MenuItem("Sound", "MENU", subitems=[
                    MenuItem("Toggle Sound", "ACTION", action=_on_action),
                ]),
                MenuItem("Vibrate", "MENU", subitems=[
                    MenuItem("Toggle Vibrate", "ACTION", action=_on_action),
                ]),
            ]),
        ])

    ]

    def __init__(self):
        self._on_action.append(self.fire_action_event)

    def fire_action_event(self):
        self.on_action(self.get_current_item())

    def get_current_menu(self):
        return self.current_item[len(self.current_item) - 1]

    def get_current_item(self):
        return self.get_current_menu().subitems[self.current_item_index].name

    def select_item(self):
        current_item = self.get_current_menu()
        next_item = current_item.subitems[self.current_item_index]
        if next_item.type == MENU_TYPE_MENU:
            self.current_item.append(current_item.subitems[self.current_item_index])
            self.current_item_index = 0
        else:
            # self.on_action(next_item)
            self.fire_action_event()
            # next_item.action()

    def deselect_item(self):
        self.current_item.pop()
        self.current_item_index = 0
        if len(self.current_item) == 0:
            self.reset()
            self.on_menu_exit()

    def move_left(self):
        current_item = self.current_item[len(self.current_item) - 1]
        self.current_item_index -= 1
        if self.current_item_index < 0:
            self.current_item_index = len(current_item.subitems) - 1

    def move_right(self):
        current_item = self.current_item[len(self.current_item) - 1]
        if (len(current_item.subitems) - 1) <= self.current_item_index:
            self.current_item_index = 0
        else:
            self.current_item_index += 1

    def reset(self):
        self.current_item = [self.items[0]]
        self.current_item_index = 0


device_menu = Menu()
