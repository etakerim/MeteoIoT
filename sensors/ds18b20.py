# dt-overlay=w1-gpio,pullup=1 (,gpiopin=4)
import glob

class Thermometer:
    def __init__(self):
        device = glob.glob('/sys/bus/w1/devices/28-*/w1_slave')
        if len(device) > 0:
            self.device = device[0]
        else:
            self.device = None
        self.temp = None  # 0.0

    def farenheit(self, temp):
        return ((temp * 9) / 5) + 32

    @property
    def temperature(self):
        if self.device is None:
            return self.temp

        with open(self.device, 'r') as f:
            lines = f.readlines()

        if len(lines) >= 2:
            if lines[0].find('YES') != -1:
                p = lines[1].find('t=')
                if p != -1:
                    self.temp = float(lines[1][p+2:]) / 1000

        return self.temp


if __name__ == '__main__':
    import time

    senzor = Thermometer()
    while True:
        t = senzor.temperature
        print("{:.2f}°C = {:.2f}°F".format(t, senzor.farenheit(t)))
        time.sleep(1)
