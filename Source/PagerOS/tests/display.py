from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
import time
import os
from datetime import datetime
from PIL import ImageFont, Image, ImageDraw


serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, rotate=0)


_display_text_value = ""
_wifi_strength = "no"
DIR_ICO = "/home/pi/pager/res/ico/"
CHAR_LEN = 12
text_pos = 0


def make_font(name, size):

    font_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), name))
    return ImageFont.truetype(font_path, size)


font = make_font("century.ttf", 25)
font_small = make_font("century.ttf", 17)


def display_time(draw):
    text = datetime.now().strftime("%H:%M")
    w, h = draw.textsize(text=text, font=font)
    draw.text((80, 0), text, font=font_small, fill="white")


def display_text(draw):
    global text_pos
    w, h = draw.textsize(text=_display_text_value, font=font)
    if w > device.width:
        print(f"pos: {text_pos} - len: {w}")
        if text_pos < 0 - w:
            text_pos = device.width
        draw.text((text_pos, 40), text=_display_text_value, font=font, fill="white")
        text_pos -= 20
    else:
        draw.text((0, 40), text=_display_text_value, font=font, fill="white")


def display_wifi(draw):
    image = Image.open(DIR_ICO + f"wifi_{_wifi_strength}.png").convert("1")
    pixelMap = image.load()
    for i in range(0, image.width):
        for j in range(0, image.height):
            if pixelMap[i, j] == 255:
                draw.point((i, j), "white")
            else:
                pass
                #print(" 0 ", end=",")
        # print()
    # device.display(image)


if __name__ == '__main__':
    _display_text_value = "Big OLD long String"
    # device.persist = False
    while True:
        with canvas(device) as draw:
            #display_time(draw)
            display_text(draw)
            #display_wifi(draw)

            time.sleep(0.2)
