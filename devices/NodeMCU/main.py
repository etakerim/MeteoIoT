import bmp280
import utils
import machine
import time

ID = 3
ALTITUDE = 250
AP_SSID = ''
AP_PASS = ''
LOGGER_IP = ''
LOGGER_PORT = 80
USER_AGENT = 'NodeMCU'
SLEEP = 600
WAIT_SEND = 10
     

def sensor_measurement(sensor_id):
    i2c = machine.I2C(sda=machine.Pin(4), scl=machine.Pin(5))
    weather = bmp280.BMP280(i2c)
    light = machine.ADC(0)

    lx = light.read()
    t = weather.temperature
    p = weather.pressure / ((1 - (ALTITUDE / 44330)) ** 5.255)
    
    return 'id={}&t={:.1f}&p={:.0f}&lx={}'.format(sensor_id, t, p, lx)


utils.wifi_ap_connect(AP_SSID, AP_PASS)
data = sensor_measurement(ID)
utils.http_collect(LOGGER_IP, LOGGER_PORT, USER_AGENT, data)
time.sleep_ms(WAIT_SEND * 1000)
utils.deep_sleep(SLEEP - WAIT_SEND) 
