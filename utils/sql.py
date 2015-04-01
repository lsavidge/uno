import sqlite3

from flask import g


# to init database: > sqlite3 uno.db < schema.sql
def connect_db(db_path):
    """
    Connect to the sqlite database at db_path.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def query_db(query, args=(), one=False):
    """
    Query the database and return results as a list of
    dictionaries (or as a single dictionary if one=True).
    :return eg [{k1:v1, k2:v2}, {k1:v1, k2:v2} ...]
    """
    cur = g.db.execute(query, args)
    rv = cur.fetchall()
    rv = [dict(item) for item in rv]
    return (rv[0] if rv else None) if one else rv
