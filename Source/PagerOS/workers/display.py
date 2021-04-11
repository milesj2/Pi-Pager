from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
import time
from datetime import datetime
from PIL import ImageFont, Image
import os
# from system.menu import device_menu
from helpers.config import config
from helpers.pager_menu import device_menu
from system.constants import *
from system.state import device_state

from system.methods import *

TAG = "Display"

COLOUR_WHITE = 255
COLOUR_BLACK = 0

refreshing = False

_display_text_value = ""
text_pos = 0
flip = -1

CHAR_LEN = 12

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, rotate=0)

DEFAULT_FONT = ImageFont.truetype(DIR_FONTS + "century.ttf", 25)
SMALL_FONT = ImageFont.truetype(DIR_FONTS + "century.ttf", 20)


def exit_menu():
    """ Resets device state on exiting menu state """
    set_refreshing(False)
    clear_display_text()
    device_state.set_state(STATE_IDLE)


device_menu.on_menu_exit.append(exit_menu)


def start():
    """ Starts continuous drawing/refresh of screen

    This has to be continuous refresh as when a new draw object is created the screen is wiped.
    """
    while True:
        with canvas(device) as draw:
            # Handle full screen states
            if device_state.get_state() == STATE_SHUTTING_DOWN:
                display_text(draw)
                time.sleep(0.2)
                continue
            if device_state.get_state() == STATE_ACTIVE_ALERT:
                display_alert(draw)
                continue
            # Draw system status icons
            display_wifi(draw)
            display_time(draw)
            display_cellular(draw)

            if device_state.get_state() == STATE_MENU:
                display_menu(draw)
            else:
                display_text(draw)
            time.sleep(0.2)


def display_menu(draw):
    """ Gets current menu item name and sets the display text as that.

    Args:
         draw (PIL.ImageDraw.ImageDraw): display canvas object
     """
    current_menu_text = device_menu.get_current_menu().subitems[device_menu.current_item_index].name
    if current_menu_text != _display_text_value:
        set_display_text(current_menu_text)
    display_text(draw)
    set_refreshing(False)


def set_display_text(text):
    """ Sets script variable _display_text_value and resets the scroll value

    Args:
        text (str): new display text value

    """
    global _display_text_value, text_pos
    _display_text_value = text
    text_pos = 0


def clear_display_text():
    """ resets script variable _display_text_value and the scroll value """
    global _display_text_value, text_pos
    _display_text_value = ""
    text_pos = 0


def clear_display():
    with canvas(device) as draw:
        draw.rectangle((0, 0, 124, 64), fill="black")


def display_time(draw):
    """ Draws current time in 24hr format top right of screen

    Args:
         draw (PIL.ImageDraw.ImageDraw): display canvas object
     """
    draw.text((80, 0), datetime.now().strftime("%H:%M"), font=SMALL_FONT, fill="white")


def display_text(draw):
    """ Draws and scrolls text in bottom half of screen """
    global text_pos
    w, h = draw.textsize(text=_display_text_value, font=DEFAULT_FONT)
    if w > device.width:
        if text_pos < 0 - w:
            text_pos = device.width
        draw.text((text_pos, 40), text=_display_text_value, font=DEFAULT_FONT, fill="white")
        text_pos -= 25
    else:
        draw.text((0, 40), text=_display_text_value, font=DEFAULT_FONT, fill="white")
    set_refreshing(False)


def display_alert(draw):
    """ Either displays black text on a white background or white text on the whole screen.

    No status indicators are shown.

    Args:
         draw (PIL.ImageDraw.ImageDraw): display canvas object
    """
    global flip
    if flip < 1:
        draw.rectangle((0, 0, 124, 64), fill="white")
        draw.text((16, 32), text=_display_text_value, font=DEFAULT_FONT, fill="black")
    else:
        draw.text((16, 32), text=_display_text_value, font=DEFAULT_FONT, fill="white")
    flip *= -1
    time.sleep(0.2)


def display_wifi(draw):
    """ Displays wifi strength symbol on top bar

    Args:
         draw (PIL.ImageDraw.ImageDraw): display canvas object
    """
    if config.get_wifi():
        status = device_state.networking.get_wifi_status()
    else:
        status = DISABLED
    im = f"{DIR_ICO}wifi_{status}.png"
    # FIXME: try/except statement only in to prevent status returning blank and image not being found.
    #       This makes no sense.
    try:
        draw_image(draw, im, 0, 0)
    except:
        print("ERROR:", im, status)


def display_cellular(draw):
    """ Displays cellular strength symbol on top bar

    Args:
         draw (PIL.ImageDraw.ImageDraw): display canvas object
    """
    if config.get_cellular():
        status = device_state.networking.get_cellular_status()
    else:
        status = DISABLED
    draw_image(draw, f"{DIR_ICO}cellular_{status}.png", 24, 0)


def draw_image(draw, path, x, y):
    """ Generic method to display an image on the screen

     Args:
         draw (PIL.ImageDraw.ImageDraw): display canvas object
         path (str): absolute path to image
         x (int): x coord
         y (int): y coord
     """
    image = Image.open(path).convert("1")

    assert image.width + x <= device.width
    assert image.height + y <= device.height

    pixel_map = image.load()
    for i in range(0, image.width):
        for j in range(0, image.height):
            if pixel_map[i, j] == COLOUR_WHITE:
                draw.point((i + x, j + y), "white")


def is_refresh():
    """ returns refreshing variable """
    return refreshing


def set_refreshing(value):
    """ sets refreshing variable """
    global refreshing
    refreshing = value


if __name__ == '__main__':
    pass

