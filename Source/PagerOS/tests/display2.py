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
_wifi_strength = "no2"
DIR_ICO = "/home/pi/pager/res/ico/"


def make_font(name, size):

    font_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), name))
    return ImageFont.truetype(font_path, size)


font = make_font("century.ttf", 25)
font_small = make_font("century.ttf", 17)


def display_time():
    draw = ImageDraw.ImageDraw(Image.new("1", ))
    text = datetime.now().strftime("%H:%M")

    w, h = ImageDraw.ImageDraw.textsize(this, text=text, font=font)
    draw.text((80, 0), text, font=font_small, fill="white")
    print(f"Device Width: {device.width} | device height: {device.height} | Text dimensions: ({w}, {h})")
    print(device.width - w, device.height - h)
    return draw


def display_text(draw):
    w, h = draw.textsize(text=display_text_value, font=font)
    draw.text((12, 40), display_text_value, font=font, fill="white")


def display_wifi():
    return Image.open(DIR_ICO + f"wifi_{_wifi_strength}.png").convert("1")


if __name__ == '__main__':
    display_text_value = "INIT"
    while True:

        display = Image.new(mode='1', size=(device.width, device.height), color="white")
        pixelMap = display.load()

        print(device.width, device.height)
        for i in range(0, device.width):
            for j in range(0, device.height):
                if j == device.height / 2 - 1 or j == device.height - 1:
                    pixelMap[i, j] = 1
                else:
                    pixelMap[i, j] = 0
        display.paste(display_wifi())
        device.display(display)

        time.sleep(10)
        break
    device.clear()
