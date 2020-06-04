from website.models.model import Piece, Ensemble, Event
from website.config import databaseURI
from sqlalchemy import create_engine, text
from datetime import date

engine = create_engine(databaseURI, echo=True)


def get_all_pieces():
    with engine.connect() as con:
        result = con.execute("SELECT p.composer, p.title, p.opus, p.date_played, e.ens_type FROM piece p INNER JOIN ensemble e ON p.ensemble_id = e.id;")
        pieces = []
        for row in result:
            pieces.append(Piece(**row))
    return pieces


def insert_piece(composer, title, opus, date_played: date, ensemble_id):
    with engine.connect() as con:
        con.execute(text("INSERT INTO piece (composer, title, opus, date_played, ensemble_id) VALUES (:composer, :title, :opus, :date_played, :ensemble_id);"), composer=composer, title=title, opus=opus, date_played=date_played, ensemble_id=ensemble_id)


def insert_event(location, day_time):
    with engine.connect() as con:
        con.execute(text("INSERT INTO event (location, day_time) VALUES (:location, :day_time);"), location=location, day_time=day_time)


def get_all_events():
    with engine.connect() as con:
        result = con.execute("SELECT * FROM event;")
        events = []
        for row in result:
            events.append(Event(**row))
    return events


def get_all_ensembles():
    with engine.connect() as con:
        result = con.execute("SELECT * FROM ensemble;")
        ensembles = []
        for row in result:
            ensembles.append(Ensemble(**row))
    return ensembles