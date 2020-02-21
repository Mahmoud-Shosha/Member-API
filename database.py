from flask import g
import psycopg2
from psycopg2.extras import DictCursor


def connect_db():
    """Return a new connection to the DB"""

    connection = psycopg2.connect(host="localhost", database="learning",
                                  user="postgres", password="192168-Water",
                                  cursor_factory=DictCursor)

    return connection


def get_db():
    """Return the current connection to the DB"""
    if not hasattr(g, 'db'):
        g.db = connect_db()

    return g.db
