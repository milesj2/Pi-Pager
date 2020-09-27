from system.classes import *

PAGER_VERSION = "v0.1_ALPHA"

DIR_RES = "/home/pi/pager/res/"
DIR_FONTS = DIR_RES + "fonts/"
DIR_ICO = DIR_RES + "ico/"

ENVIR_GRACEFUL_EXIT = "graceful_exit"

CONFIG_FILE = "/config.ini"

INI_HEADER_PAGER = "pager"
INI_HEADER_KOJIN_API = "kojin_api"
INI_HEADER_USER = "user"
INI_HEADER_LOGGING = "logging"

INI_KEY_SERIAL = "serial"
INI_KEY_GRACEFUL_EXIT = "graceful_exit"
INI_KEY_ACCESS_TOKEN = "access_token"
INI_KEY_NAME = "name"
INI_KEY_STATION = "station"
INI_KEY_LOGGING_LEVEL = "logging_level"
INI_KEY_GPIO_WARNINGS = "gpio_warnings"
INI_KEY_DEBUG = "debug"

URL_PARAM_ACCESS_TOKEN = "accessToken"
URL_PARAM_ALERT_ID = "alertID"
URL_PARAM_STATION = "station"
URL_PARAM_STATUS = "status"

LOGGING_LEVEL_VERBOSE = "VERBOSE"
LOGGING_LEVEL_STRICT = "STRICT"
LOGGING_LEVEL_OFF = "OFF"

URL_KOJIN_API = "https://firepager.meinserver.ga/"
# URL_KOJIN_API = "https://BADURL/"

URL_ROUTE_KOJIN_API_GET_ALERT = "api/shouts/pager"
URL_ROUTE_KOJIN_API_ACKNOWLEDGE_ALERT = "api/shouts/pager/status"

RESPONSE_STATUS_ERROR = "error"
RESPONSE_STATUS_SUCCESS = "success"

ALERT_TYPE_SHOUT = "SHOUT"
ALERT_TYPE_TEST = "TEST"
ALERT_TYPE_BLANK = "BLANK"

ALERT_STATUS_RECEIVED = "Received"
ALERT_STATUS_ACKNOWLEDGE = "Acknowledged"
ALERT_STATUS_DISMISSED = "Dismissed"
ALERT_STATUS_TIMED_OUT = "TimeOut"

ALERTER_TIMEOUT = 25

STRING_EMPTY = ""
ALERT_EMPTY = Alert("", "", "", "", "")

STATE_INITIALISING = "INITIALISING"
STATE_DISCONNECTED = "DISCONNECTED"
STATE_CONNECTED = "CONNECTED"
STATE_IDLE = "IDLE"
STATE_ACTIVE_ALERT = "ACTIVE_ALERT"
STATE_RESPONDING = "RESPONDING"
STATE_MENU = "MENU"

CONNECTION_STATUS_CONNECTED = "CONNECTED"
CONNECTION_STATUS_DISCONNECTED = "DISCONNECTED"

MENU_TYPE_MENU = "MENU"
MENU_TYPE_ACTION = "ACTION"

MENU_MAIN = "Main"
MENU_NETWORK = "Network"
MENU_SOUND_VIBRATE = "Sound & Vibrate"
MENU_RESET = "Reset"

SUB_MENU_WIFI = MENU_NETWORK + "_WIFI"
SUB_MENU_MOBILE = MENU_NETWORK + "_MOBILE"
