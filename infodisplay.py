import os
import signal
import time
from RPi import GPIO
from PIL import ImageFont
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas
from sensors.bmp280 import BMP280
from sensors.ds18b20 import Thermometer

class Display:

    def __init__(self):
        fontsize = 11
        font = ImageFont.truetype('DejaVuSans-Bold.ttf', fontsize)

        self.style = dict(fill='white', font=font)
        self.line = [(5, 2 * fontsize * i) for i in range(3)]
        self.disp_on = True
        self.a_screen = ssd1306(i2c(port=1, address=0x3C))
        self.b_screen = ssd1306(i2c(port=1, address=0x3D))

    def control_setup(self, disp_btn, measure_btn):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(disp_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(measure_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(disp_btn, GPIO.FALLING,
                              callback=self.turn_onoff, bouncetime=500)
        GPIO.add_event_detect(measure_btn, GPIO.FALLING,
                              callback=self.refresh, bouncetime=200)

    def turn_onoff(self, channel):
        if self.disp_on:
            self.a_screen.hide()
            self.b_screen.hide()
        else:
            self.a_screen.show()
            self.b_screen.show()
        self.disp_on = not self.disp_on

    def weather(self, t, p):
        with canvas(self.a_screen) as draw:
            draw.text(self.line[0], 'WEATHER', **self.style)
            draw.text(self.line[1], 't = {:.2f} °C'.format(t), **self.style)
            draw.text(self.line[2], 'p = {:.2f} hPa'.format(p), **self.style)

    def localnet(self, ifnet, ip, mac):
        with canvas(self.b_screen) as draw:
            draw.text(self.line[0], 'Ethernet - {}'.format(ifnet),
                      **self.style)
            draw.text(self.line[1], ip, **self.style)
            draw.text(self.line[2], mac, **self.style)

    def refresh(self, channel):
        t = Thermometer()
        p = BMP280()
        p.measure()

        h = 150
        ip = '192.168.100.100'
        mac = 'b8:23:98:2d:1c:f3'
        interface = 'eth0'

        self.weather(t.temperature, p.mslp_pressure(h))
        self.localnet(interface, ip, mac)

display = Display()
display.control_setup(17, 27)
display.refresh(None)
signal.pause()
