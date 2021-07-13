import machine
import network
import socket


def wifi_ap_connect(ssid, password):
    iface = network.WLAN(network.STA_IF)

    if not iface.isconnected():
        iface.active(True)
        iface.connect(ssid, password)
        while not iface.isconnected():
            pass


def http_collect(ip, port, user_agent, values):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))
    client.send((
        b'POST /meteo.php HTTP/1.1\r\n'
        b'Host: {}\r\n'
        b'User-Agent: {}\r\n'
        b'Content-Type: application/x-www-form-urlencoded\r\n'
        b'Content-Length: {}\r\n'
        b'\r\n{}\r\n\r\n').format(
            ip, user_agent, len(values), values)
    )
    client.close()
    

def deep_sleep(seconds):
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    rtc.alarm(rtc.ALARM0, seconds * 1000)
    machine.deepsleep()
