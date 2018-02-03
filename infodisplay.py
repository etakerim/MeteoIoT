import time
from RPi import GPIO
from PIL import ImageFont
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas


a_screen = ssd1306(i2c(port=1, address=0x3C))
b_screen = ssd1306(i2c(port=1, address=0x3D))
fontsize = 11
font = ImageFont.truetype('DejaVuSans-Bold.ttf', fontsize)

def off(channel):
    global a_screen
    a_screen.hide()

def on(channel):
    global a_screen
    a_screen.show()

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(17, GPIO.FALLING, callback=off, bouncetime=200)
GPIO.add_event_detect(27, GPIO.FALLING, callback=on, bouncetime=200)


line = [(5, 2 * fontsize * i) for i in range(3)]
t = 23.345
p = 1015.45
interface = 'eth0'
ip = '192.168.100.100'
mac = 'b8:23:98:2d:1c:f3'

style = dict(fill='white', font=font)
with canvas(a_screen) as draw:
    draw.text(line[0], 'WEATHER', **style)
    draw.text(line[1], 't = {:.2f} °C'.format(t), **style)
    draw.text(line[2], 'p = {:.2f} hPa'.format(p), **style)

with canvas(b_screen) as draw:
    draw.text(line[0], 'Ethernet - {}'.format(interface), **style)
    draw.text(line[1], ip, **style)
    draw.text(line[2], mac, **style)

while True:
    time.sleep(1)
