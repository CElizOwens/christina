from collections import namedtuple

Piece = namedtuple('Piece', ['composer', 'title', 'opus', 'ens_type'])
Ensemble = namedtuple('Ensemble', ['id', 'ens_type', 'size'])
Event = namedtuple('Event', ['id', 'location', 'day_time'])
