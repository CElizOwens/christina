from collections import namedtuple

Piece = namedtuple('Piece', ['last_name', 'title', 'opus', 'ens_type'])
# ['last_name', 'first_inits', 'title', 'opus', ens_type']
Ensemble = namedtuple('Ensemble', ['id', 'ens_type', 'size'])
Event = namedtuple('Event', ['id', 'location', 'day_time'])
