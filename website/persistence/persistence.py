from website.models.model import Piece, Event, Performance  # , Ensemble
from website.config import databaseURI, test_databaseURI
from sqlalchemy import create_engine, text


# engine = create_engine(databaseURI, echo=True)
engine = create_engine(test_databaseURI, echo=True)


def get_all_pieces():
    with engine.connect() as con:
        # result = con.execute("SELECT c.name, p.title, p.opus, e.ens_type FROM piece p INNER JOIN ensemble e ON p.ensemble_id = e.id INNER JOIN composer c ON p.composer_id = c.id;")

    #     result = con.execute("SELECT c.name, p.title FROM piece p INNER JOIN composer c ON p.composer_id = c.id;")
    #     pieces = []
    #     for row in result:
    #         pieces.append(Piece(**row))
    # return pieces

        res = con.execute("SELECT c.name, p.title FROM performance pf INNER JOIN piece p ON pf.piece_id = p.id INNER JOIN composer c ON p.composer_id = c.id;")

        repertoire = []
        for row in res:
            repertoire.append(Piece(**row))
    return repertoire


def get_all_performances():
    with engine.connect() as con:
        result = con.execute("SELECT c.name, p.title, pf.notes FROM performance pf INNER JOIN piece p ON pf.piece_id = p.id INNER JOIN composer c ON p.composer_id = c.id;")
        repertoire = []
        for row in result:
            repertoire.append(Performance(**row))
    return repertoire


def insert_piece(name, title):  # , opus, ensemble_id):
    with engine.connect() as con:
        # con.execute(text("INSERT INTO piece (composer, title, opus, ensemble_id) VALUES (:composer, :title, :opus, :ensemble_id);"), composer=composer, title=title, opus=opus, ensemble_id=ensemble_id)
        con.execute(text("INSERT INTO piece (name, title) VALUES (:name, :title);"), name=name, title=title)


def insert_event(location, day_time):  # TO BE EDITED
    with engine.connect() as con:
        con.execute(text("INSERT INTO event (location, day_time) VALUES (:location, :day_time);"), location=location, day_time=day_time)


def get_event(event_id):
    with engine.connect() as con:
        result = con.execute(text("SELECT e.id, v.name, e.day_time FROM event e INNER JOIN venue v ON e.venue_id = v.id WHERE e.id = :event_id;"), event_id=event_id)
        for row in result:
            event = Event(**row)
    return event


def get_all_events():
    with engine.connect() as con:
        result = con.execute("SELECT e.id, v.name, e.day_time FROM event e INNER JOIN venue v ON e.venue_id = v.id;")
        events = []
        for row in result:
            events.append(Event(**row))
    return events


# def get_all_ensembles():
#     with engine.connect() as con:
#         result = con.execute("SELECT * FROM ensemble;")
#         ensembles = []
#         for row in result:
#             ensembles.append(Ensemble(**row))
#     return ensembles
