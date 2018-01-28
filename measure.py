import os
import db
from sensors.ds18b20 import Thermometer
from sensors.bmp280 import BMP280

LOCATION = os.environ['LOCATION_ID']
t = Thermometer()
p = BMP280()

session = db.Session()
place = session.query(db.Location).get(LOCATION)

p.measure()   # Wake up sensor after inactivity
p.measure()   # Read actual pressure
session.add(db.Weather(
                location_id=LOCATION,
                temperature=t.temperature,
                pressure=p.mslp_pressure(place.altitude))
            )
session.commit()
