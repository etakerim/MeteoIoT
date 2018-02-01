import db
import datetime as dt
from sqlalchemy import DateTime, cast, func
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


class MeteoGraphs:
    def __init__(self, temp_title, press_title):
        self.temp_title = temp_title
        self.press_title = press_title
