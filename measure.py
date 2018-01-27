from datetime import datetime
from sensors.ds18b20 import Thermometer
from sensors.bmp280 import BMP280

ALTITUDE = 150
t = Thermometer()
p = BMP280()

p.measure()
date = datetime.now().replace(microsecond=0)

measurement = {
        'dtm': date.isoformat(),
        't': t.temperature,
        'p': p.mslp_pressure(ALTITUDE),
        'p_raw': p.pressure
    }
print(measurement)
