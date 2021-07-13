#!/usr/bin/env python3
import glob
import sqlite3
from datetime import datetime, timezone


ID = 1
DB_FILENAME = '/home/pi/weather/weather.db'


class Thermometer:
    def __init__(self):
        device = glob.glob('/sys/bus/w1/devices/28-*/w1_slave')
        self.device = device[0] if len(device) > 0 else None
        self.temp = ''

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
    sensor = Thermometer()
    session = sqlite3.connect(DB_FILENAME)
    cursor = session.cursor()
    
    temperature = sensor.temperature()
    cursor.execute(
        'INSERT INTO measurements(sensor_id, t_celsius) '
        'VALUES (?, ?)', (ID, f'{temperature:.2f}')
    )
    session.commit()
    session.close()

# crontab -e
# */10 * * * * /home/pi/ds18b20.py
#
# dtc = (datetime.now(timezone.utc).astimezone().isoformat('T', 'seconds'))
