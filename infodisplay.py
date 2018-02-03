import time
from PIL import ImageFont
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas

a_screen = ssd1306(i2c(port=1, address=0x3C))
b_screen = ssd1306(i2c(port=1, address=0x3D))
font = ImageFont.truetype("DejaVuSans-Bold.ttf", 12)
