import db
import datetime as dt
from sqlalchemy import Date, cast, func
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def query_interval(start, finish):
    session = db.Session()
    data = (session
            .query(db.Weather)
            .filter((db.Weather.dtm <= finish) &
                    (db.Weather.dtm >= start))
            .order_by(db.Weather.dtm).all())

    return {'dates': [x.dtm for x in data],
            't': [y.temperature for y in data],
            'p': [y.pressure for y in data]}


def query_stats():
    session = db.Session()
    avgtab = (session
              .query(func.date(db.Weather.dtm).label('dtm'),
                     func.avg(db.Weather.temperature).label('avg'))
              .group_by(func.date(db.Weather.dtm)).all())

    mintab = (session
              .query(db.Weather.dtm.label('dtm'),
                    func.min(db.Weather.temperature).label('min'))
              .group_by(func.date(db.Weather.dtm)).all())

    maxtab = (session
              .query(db.Weather.dtm.label('dtm'),
                     func.max(db.Weather.temperature).label('max'))
              .group_by(func.date(db.Weather.dtm)).all())

    return {'avg': avgtab, 'min': mintab, 'max': maxtab}


def plot_quantity(ax, title, x, y, recent, period, color, hourtick):
    FONT_SIZE = 9
    WDAY_ABBR = ['Pon', 'Uto', 'Str', 'Štv', 'Pia', 'Sob', 'Ned']

    oldest = recent - period
    tick = recent.replace(hour=0, minute=0, second=0)
    while tick >= oldest:
        ax.axvline(x=tick, ls='-', color='#dddddd')
        tick -= dt.timedelta(days=1)

    ax.set_xlim(oldest, recent)
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

    tick = recent.replace(hour=0, minute=0, second=0)
    while tick >= oldest:
        wd = '{} {}'.format(WDAY_ABBR[tick.weekday()], tick.day)
        ax.text(tick, y_min, wd, fontsize=FONT_SIZE)
        tick -= dt.timedelta(days=1)


def mark_dailyrecords(ax, stats, start, finish):
    h = 4
    for temp in stats['max']:
        if temp.dtm >= start:
            linex = [temp.dtm - dt.timedelta(hours=h),
                     temp.dtm + dt.timedelta(hours=h)]
            liney = [temp.max, temp.max]
            ax.plot(linex, liney, color='r')

    for temp in stats['min']:
        if temp.dtm >= start:
            linex = [temp.dtm - dt.timedelta(hours=h),
                     temp.dtm + dt.timedelta(hours=h)]
            liney = [temp.min, temp.min]
            ax.plot(linex, liney, color='b')


def history(image, interval, hourtick, records=None):
    fig, (tg, pg) = plt.subplots(2, 1, figsize=(10,5))

    today = dt.datetime.now().replace(microsecond=0)
    oldest = today - interval
    m = query_interval(oldest, today)

    plot_quantity(tg, 'Teplota (°C)', m['dates'], m['t'],
                 today, interval, 'k', hourtick)
    plot_quantity(pg, 'Atmosferický tlak (hPa)', m['dates'], m['p'],
                 today, interval, 'b', hourtick)
    if records:
        mark_dailyrecords(tg, records, oldest, today)

    plt.subplots_adjust(left=0.07, bottom=0.07, right=0.95,
                    top=0.95, hspace=0.3)
    plt.savefig(image, dpi=100)
    plt.gcf().clear()


def mark_dailyrecords(ax, stats, start, finish):
    pass

def weather_statistics(image, stats):
    dates = dt.datetime.strptime(x.dtm, '%Y-%m-%d') for x in stats['avg']]
    avge = [y.avg for y in stats['avg'],
    mini = [y.min for y in stats['min']],
    maxi = [y.max for y in stats['max']]

    fig, ax = plt.subplots(1, 1, figsize=(10,5))

    fig.autofmt_xdate()
    ax.grid(True)
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.bar(dates, mini, color='#3f9bff')
    ax.bar(dates, maxi, color='#ff3f3f')
    ax.bar(dates, avge, color='#62ff3f')

    plt.savefig(image, dpi=100, bbox_inches='tight')
    plt.gcf().clear()


weather_history('last-3-days.png', dt.timedelta(days=3), 2)
weather_history('last-10-days.png', dt.timedelta(days=10), 6)
weather_statistics('statistics.png', query_stats())
