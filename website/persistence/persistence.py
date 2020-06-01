from website.models.model import Piece
from website.config import databaseURI
from sqlalchemy import create_engine, text

engine = create_engine(databaseURI, echo=True)


def get_all_pieces():
    with engine.connect() as con:
        result = con.execute("SELECT * FROM piece;")
        pieces = []
        for row in result:
            pieces.append(Piece(**row))
    return pieces


def insert_piece(composer, title, opus, date_played):
    with engine.connect() as con:
        con.execute(text('INSERT INTO piece (composer, title, opus, date_played) VALUES (:composer, :title, :opus, :date_played);'), composer=composer, title=title, opus=opus, date_played=date_played)
