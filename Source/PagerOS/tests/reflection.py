import requests

from system.constants import *


class StdResponse:
    status = STRING_EMPTY
    balance = STRING_EMPTY
    lat = STRING_EMPTY
    lon = STRING_EMPTY
    accuracy = STRING_EMPTY

    def __int__(self):
        pass



bssids = ["ac:3b:77:ee:1e:b6", "78:44:76:d3:42:30"]

params = {
    "token": LOCATION_API_KEY,
    "wifi": [{
        "bssid": bssids[0],
        "channel": 11,
        "frequency": 2462,
        "signal": -64
    }, {
        "bssid": bssids[1]
    }]
}

try:
    response = requests.post(URL_LOCATION_API + URL_ROUTE_LOCATION_API_LOCATION, json=params)
    json = response.json()
    if json['status'] == "ok":
        object = StdResponse()
        for key in json:
            object.__setattr__(key, json[key])
    else:
        pass
except requests.ConnectionError as e:
    print("TAG", "Connection Error for request:\n" + e.request.url + "\n" + str(e.args))
except Exception as e:
    print("Now really panic!")

