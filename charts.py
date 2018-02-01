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
                't': [y.temperature for y in data],
                'p': [y.pressure for y in data]}

    def plot_quantity(ax, title, x, y, start, finish, color, hourtick):
        FONT_SIZE = 9
        WDAY_ABBR = ['Pon', 'Uto', 'Str', 'Štv', 'Pia', 'Sob', 'Ned']

        now = start
        while now <= finish:
            ax.axvline(x=now, ls='-', color='#dddddd')
            now += dt.timedelta(days=1)

        ax.set_xlim(start, finish)
        ax.xaxis.grid(False)
        ax.yaxis.grid(True)
        ax.set_title(title)
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=hourtick))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H'))
        ax.tick_params(axis='both', which='major', labelsize=FONT_SIZE)

        ax.plot(x, y, '-', color=color)

        y_min, y_max = ax.get_ylim()
        if y_min < 0:
            ax.axhline(y=0, color='y')

        now = start
        while now <= finish:
            wd = '{} {}'.format(WDAY_ABBR[now.weekday()], now.day)
            ax.text(now, y_min, wd, fontsize=FONT_SIZE)
            now += dt.timedelta(days=1)
