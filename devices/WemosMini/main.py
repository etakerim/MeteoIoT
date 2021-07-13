import dht
import utils
import machine
import time

ID = 2
AP_SSID = ''
AP_PASS = ''
LOGGER_IP = ''
LOGGER_PORT = 80
USER_AGENT = 'Wemos Mini'
SLEEP = 600
WAIT_SEND = 10
     

def sensor_measurement(sensor_id):
    weather = dht.DHT22(machine.Pin(2))
    light = machine.ADC(0)
    
    weather.measure()
    lx = light.read()
    t = weather.temperature()
    h = weather.humidity()
    
    return 'id={}&t={:.1f}&h={:.0f}&lx={}'.format(sensor_id, t, h, lx)


utils.wifi_ap_connect(AP_SSID, AP_PASS)
data = sensor_measurement(ID)
utils.http_collect(LOGGER_IP, LOGGER_PORT, USER_AGENT, data)
time.sleep_ms(WAIT_SEND * 1000)
utils.deep_sleep(SLEEP - WAIT_SEND)
