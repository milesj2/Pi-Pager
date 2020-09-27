from system.constants import *
from system.events import Event


class Alert(object):
    """ Class object to be populated by json response"""
    def __init__(self, alert_id, shout_id, pager_id, station_id, alert_type):
        self.id = alert_id
        self.shout_id = shout_id
        self.pager_id = pager_id
        self.station_id = station_id
        self.type = alert_type


