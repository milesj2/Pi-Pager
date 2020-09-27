from helpers import kojin_requests
from system import constants as c
import json


class Shout(object):
    def __init__(self, id, shout_id, pager_id, station_id, type):
        self.id = id
        self.shout_id = shout_id
        self.pager_id = pager_id
        self.station_id = station_id
        self.type = type


def derserialise_shout(dct):
    return Shout(dct['id'], dct['shoutID'], dct['pagerID'], dct['stationID'], dct['type'])


params = {
    c.URL_PARAM_ACCESS_TOKEN: "PagerTestAccess"
}


response = kojin_requests.get(c.URL_KOJIN_API + c.URL_ROUTE_KOJIN_API_GET_ALERT, params, verify=False)

print(response.content)

shout = json.loads(response.content, object_hook=derserialise_shout)[0]

print(shout.type)
