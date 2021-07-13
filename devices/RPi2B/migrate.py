# Migrácia (čas 5 minút): 
# 0. sudo apt-get install php-sqlite3 sqlite3, /etc/php/php.ini -> odkomentuj extension=sqlite3
# Restart apache
# 1. vytvor databázu a schému
# 2. spusti tento skript (vyskúšaj na prázdnej db)
# 3. vymeň ds18b20.py
# 4. vymeň web
import sqlite3

FILE = 't.csv'
DB = 'weather.db'

ses = sqlite3.connect(DB)
c = ses.cursor()

log = []
with open(FILE, 'r') as source:
    for line in source:
        dtc, t = line.split(',')
        log.append((1, dtc.replace('T', ' '), t))
    
c.executemany(
    'INSERT INTO measurements (sensor_id, measured_at, t_celsius) '
    'VALUES (?, ?, ?)', log
)
ses.commit()
ses.close()
