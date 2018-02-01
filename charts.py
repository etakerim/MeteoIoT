import db
import datetime as dt
from sqlalchemy import DateTime, cast, func
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


class MeteoGraphs:
    def __init__(self, temp_title, press_title):
        self.temp_title = temp_title
        self.press_title = press_title

    def query_interval(self, start, finish):
        session = db.Session()
        data = (session
                .query(db.Weather)
                .filter((cast(db.Weather.dtm, DateTime) <=
                         cast(finish, DateTime)) &
                        (cast(db.Weather.dtm, DateTime) >=
                         cast(start, DateTime)))
                .order_by(db.Weather.dtm).all())

        return {'dates': [x.dtm for x in data],
                't': [y.temperature for y in data]
                'p': [y.pressure for y in data]}
