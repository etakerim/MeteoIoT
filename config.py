import os

LOCATION_ID = 1

PATH = os.path.dirname(os.path.realpath(__file__))

GRAPH_PATHS = [{'name': 'Počasie za posledné 3 dni',
                'path': 'last-3-days.png'},
               {'name': 'Počasie za posledných 10 dní',
                'path': 'last-10-days.png'},
               {'name': 'Štatistika za celé obdobie',
                 'path': 'statistics.png'}]
