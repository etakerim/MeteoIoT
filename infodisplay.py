import time
from PIL import ImageFont
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas


a_screen = ssd1306(i2c(port=1, address=0x3C))
b_screen = ssd1306(i2c(port=1, address=0x3D))
fontsize = 10
font = ImageFont.truetype('DejaVuSans-Bold.ttf', fontsize)

line = ((10, 1.5 * fontsize), (10,  1.5 * fontsize * 2), (10, 1.5 * fontsize * 3))
area = 'Bratislava-Rača'
t = 23.345
p = 1015.45
interface = 'eth0'
ip = '192.168.100.100'
mac = 'b8:23:98:2d:1c:f3'

with canvas(a_screen) as draw:
    draw.text(line[0], 'POĆASIE ({})'.format(area), fill='white', font=font)
    draw.text(line[1], 't = {:.2f} °C'.format(t), fill='white', font=font)
    draw.text(line[2], 'p = {:.2f} hPa'.format(p), fill='white', font=font)

with canvas(b_screen) as draw:
    draw.text(line[0], 'Ethernet - {}'.format(interface), fill='white', font=font)
    draw.text(line[1], ip, fill='white', font=font)
    draw.text(line[2], mac, fill='white', font=font)

while True:
    time.sleep(1)
