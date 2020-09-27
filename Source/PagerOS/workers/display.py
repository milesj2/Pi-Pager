from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
import time
from datetime import datetime
from PIL import ImageFont, Image
import os
# from system.menu import device_menu

from helpers.pager_menu import device_menu

from system.globals import *

TAG = "Display"

refreshing = False

_display_text_value = ""
_wifi_strength = "no"
text_pos = 0
flip = -1

CHAR_LEN = 12

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, rotate=0)

font = ImageFont.truetype(DIR_FONTS + "century.ttf", 25)
small_font = ImageFont.truetype(DIR_FONTS + "century.ttf", 20)


def handle_action(name):
    print("Got action type", name)


def exit_menu():
    global _display_text_value
    _display_text_value = STRING_EMPTY
    device_state.set_state(STATE_IDLE)


device_menu.on_menu_exit.append(exit_menu)
device_menu.on_action.append(handle_action)


def start():
    while True:
        with canvas(device) as draw:
            if device_state.get_state() == STATE_ACTIVE_ALERT:
                display_alert(draw)
                continue
            display_wifi(draw)
            display_time(draw)
            if device_state.get_state() == STATE_MENU:
                display_menu(draw)
            else:
                display_time(draw)
            time.sleep(0.2)


def display_menu(draw):
    global _display_text_value, refreshing
    _display_text_value = device_menu.get_current_menu().subitems[device_menu.current_item_index].name
    display_text(draw)
    refreshing = False


def make_font(name, size):
    font_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), name))
    print(font_path)
    return


def set_display_text(text):
    global _display_text_value, current_index
    _display_text_value = text
    current_index = 0


def clear_display_text():
    global _display_text_value, current_index
    _display_text_value = ""
    current_index = 0


def display_time(draw):
    draw.text((80, 0), datetime.now().strftime("%H:%M"), font=small_font, fill="white")


def display_text(draw):
    global text_pos
    w, h = draw.textsize(text=_display_text_value, font=font)
    if w > device.width:
        if text_pos < 0 - w:
            text_pos = device.width
        draw.text((text_pos, 40), text=_display_text_value, font=font, fill="white")
        text_pos -= 25
    else:
        draw.text((0, 40), text=_display_text_value, font=font, fill="white")
    set_refreshing(False)


def display_alert(draw):
    global flip
    if flip < 1:
        draw.rectangle((0, 0, 124, 64), fill="white")
        draw.text((16, 32), text=_display_text_value, font=font, fill="black")
    else:
        draw.text((16, 32), text=_display_text_value, font=font, fill="white")
    flip *= -1


def display_wifi(draw):
    draw_image(draw, f"{DIR_ICO}wifi_{_wifi_strength}.png", 0, 0)


def draw_image(draw, path, x, y):
    image = Image.open(path).convert("1")

    assert image.width + x <= device.width
    assert image.height + y <= device.height

    pixel_map = image.load()
    for i in range(0, image.width):
        for j in range(0, image.height):
            if pixel_map[i, j] == 255:
                draw.point((i + x, j + y), "white")


def test_action():
    print("Test action")


def is_refresh():
    return refreshing


def set_refreshing(value):
    global refreshing
    refreshing = value


if __name__ == '__main__':
    pass

