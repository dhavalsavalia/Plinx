import sqlite3


def test_database_connection(db):
    assert db.connection is not None
    assert isinstance(db.connection, sqlite3.Connection)
    assert db.tables == []