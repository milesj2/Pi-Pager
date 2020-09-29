import system.constants as consts
from system.events import Event


class Alert(object):
    """ alert object to be populated by json response """
    def __init__(self, alert_id, shout_id, pager_id, station_id, alert_type):
        self.id = alert_id
        self.shout_id = shout_id
        self.pager_id = pager_id
        self.station_id = station_id
        self.type = alert_type


ALERT_EMPTY = Alert("", "", "", "", "")


class LongLat:
    """ Longitude and latitude object """
    def __init__(self, long, lat):
        self.long = long
        self.lat = lat


class Location:
    """ An object to contain gps and wifi long lat to send to api """
    def __init__(self, gps_loc: LongLat, wifi_loc: LongLat):
        self.gps = gps_loc
        self.wifi = wifi_loc


class MenuItem:
    """ Item can either be an action or submenu, use this to build a full menu within Menu.items """
    name = consts.STRING_EMPTY
    subitems = []
    type = consts.STRING_EMPTY
    action = consts.STRING_EMPTY

    def __init__(self, name, item_type, action=None, args=None, subitems=None):
        if subitems is None:
            subitems = []
        if args is None:
            args = []
        self.name = name
        self.subitems = subitems
        self.type = item_type
        self.action = action
        self.args = args

    def __str__(self):
        if self.type == consts.MENU_TYPE_MENU:
            subitems = "[ "
            for item in self.subitems:
                subitems += item.name + ", "
            subitems += " ]"
            return f"Menu item {self.name}; type: {self.type}; subitems: {subitems}"
        else:
            return f"Menu item {self.name}; type: {self.type}; action: {self.action}; args = {self.args}"


class Menu:
    on_menu_exit = Event()
    current_item = []

    current_index = 0
    current_item_index = 0

    MENU_STATE_ROAMING = "ROAMING"
    MENU_STATE_DIALOGUE = "DIALOGUE"

    menu_state = MENU_STATE_DIALOGUE

    items = []

    def __init__(self, items):
        self.items = items
        self.current_item.append(self.items[0])

    def get_current_menu(self):
        return self.current_item[len(self.current_item) - 1]

    def get_current_item(self):
        return self.get_current_menu().subitems[self.current_item_index].name

    def select_item(self):
        current_item = self.get_current_menu()
        next_item = current_item.subitems[self.current_item_index]
        if next_item.type == consts.MENU_TYPE_MENU:
            self.current_item.append(current_item.subitems[self.current_item_index])
            self.current_item_index = 0
        else:
            # self.on_action(next_item)
            # self.fire_action_event()
            next_item.action()

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



