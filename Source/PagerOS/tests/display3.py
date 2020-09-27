import time
import os
from datetime import datetime
from PIL import ImageFont, Image, ImageDraw


_display_text_value = ""
_wifi_strength = "no"
DIR_ICO = "D:\\_GitWorkspace\\KojinPager\\Source\\res\\ico\\"


def make_font(name, size):

    font_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), name))
    return ImageFont.truetype(font_path, size)


font = make_font("century.ttf", 25)
font_small = make_font("century.ttf", 17)



def display_wifi():
    print(DIR_ICO + f"wifi_{_wifi_strength}.png")
    return Image.open(DIR_ICO + f"wifi_{_wifi_strength}.png").convert("1")


if __name__ == '__main__':
    display_text_value = "INIT"
    while True:

        display = Image.new(mode='1', size=(128, 64), color="white")
        pixelMap = display.load()

        for i in range(0, 128):
            for j in range(0, 64):
                if j == 64 / 2 - 1 or j == 64 - 1:
                    pixelMap[i, j] = 1
                else:
                    pixelMap[i, j] = 0
        display.paste(display_wifi())

        time.sleep(1)
        display.show()
        break

    # device.clear()
