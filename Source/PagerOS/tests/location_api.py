import requests


LOCATION_API_KEY = "39b1f9fa418376"

URL_KOJIN_API = "https://firepager.meinserver.ga/"
# URL_KOJIN_API = "https://BADURL/"
URL_LOCATION_API = "https://eu1.unwiredlabs.com/v2/"

URL_ROUTE_KOJIN_API_GET_ALERT = "api/shouts/pager"
URL_ROUTE_KOJIN_API_ACKNOWLEDGE_ALERT = "api/shouts/pager/status"
URL_ROUTE_KOJIN_API_UPDATE_LOCATION = "api/pager/location/update"

URL_ROUTE_LOCATION_API_LOCATION = "process.php"


def http_post(url, params):
    try:
        response = requests.post(url, json=params)
        print(response.json())
    except requests.ConnectionError as e:
        print("Connection Error for request:\n" + e.request.url + "\n" + str(e.args))
    except Exception as e:
        print("Now really panic!")
        print("General http get error!\n" + str(e))


def get_wifi_location():
    params = {
        "token": LOCATION_API_KEY,
        "wifi": [{
            "bssid": "ac:3b:77:ee:1e:b6",
            "channel": 11,
            "frequency": 2462,
            "signal": -64
        }, {
            "bssid": "78:44:76:d3:42:30"
        }]
    }

    http_post(URL_LOCATION_API + URL_ROUTE_LOCATION_API_LOCATION, params)



test = get_wifi_location()
