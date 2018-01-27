import sqlite3
import datetime


class Weather:
    DB_NAME = 'weather.db'
    def __init__(self, location):
        self.table = location
        self.db = sqlite3.connect(self.DB_NAME)
        self.create_tables()

    def create_tables(self):
        c = self.db.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS {} (
                     id INTEGER PRIMARY KEY NOT NULL,
                     dtm TEXT NOT NULL,
                     temperature TEXT,
                     pressure TEXT,
                     pressure_raw TEXT)""".format(self.table))
        self.db.commit()

    def insert(self, m):
        c = self.db.cursor()
        c.execute("""INSERT INTO {}
                     (dtm, temperature, pressure, pressure_raw)
                     VALUES (?, ?, ?, ?)""".format(self.table), 
                     (m['dtm'], m['t'], m['p'], m['p_raw']))
        self.db.commit()

    def view(self, start=None, end=None):
        end = end or datetime.datetime.now()
        start = start or (end - datetime.timedelta(days=30))

        c = self.db.cursor()
        c.execute("""SELECT * FROM {} WHERE dtm > ? AND dtm < ?""".format(self.table),
                    (start.isoformat(), end.isoformat()))
        return c.fetchall()
