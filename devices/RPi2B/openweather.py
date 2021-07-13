#!/usr/bin/env python3
import sqlite3
from pyowm.owm import OWM


BRATISLAVA = 3060972
API_KEY = 'XXX'
DB = '/home/pi/weather/weather.db'


if __name__ == '__main__':
    owm = OWM(API_KEY)
    mgr = owm.weather_manager()
    observation = mgr.weather_at_id(BRATISLAVA)
    
    if observation is not None:
        weather = observation.weather
        
        session = sqlite3.connect(DB)
        cursor = session.cursor()
        
        cursor.execute(
            'INSERT INTO openweathermap( '
            ' reference_time, sunrise_time, sunset_time, clouds, rain, '
            ' wind_speed, wind_deg, humidity, pressure, temperature, status, ' 
            ' detailed_status, weather_code, visibility_distance) '
            'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (
                weather.reference_time(timeformat='iso'),
                weather.sunrise_time(timeformat='iso'),
                weather.sunset_time(timeformat='iso'),
                weather.clouds,
                weather.rain.get('1h'),
                weather.wind().get('speed'),
                weather.wind().get('deg'),
                weather.humidity,
                weather.pressure.get('press'),
                weather.temperature('celsius').get('temp'),
                weather.status,
                weather.detailed_status,
                weather.weather_code,
                weather.visibility_distance
            )
        )
        session.commit()
        session.close()
    

# crontab -e
# */10 * * * * /home/pi/openweather.py
# sudo pip install pyowm
