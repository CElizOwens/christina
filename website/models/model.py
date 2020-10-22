from collections import namedtuple

Piece = namedtuple('Piece', ['name', 'title']) # , 'opus', 'ens_type'])
# Ensemble = namedtuple('Ensemble', ['id', 'ens_type', 'size'])
Event = namedtuple('Event', ['id', 'name', 'day_time'])

Performance = namedtuple('Performance', ['name', 'title', 'notes'])
