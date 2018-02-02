import db
import config
from sensors.ds18b20 import Thermometer
from sensors.bmp280 import BMP280

t = Thermometer()
p = BMP280()

session = db.Session()
place = session.query(db.Location).get(config.LOCATION_ID)

p.measure()   # Wake up sensor after inactivity
p.measure()   # Read actual pressure
session.add(db.Weather(
                location_id=config.LOCATION_ID,
                temperature=t.temperature,
                pressure=p.mslp_pressure(place.altitude))
            )
session.commit()
