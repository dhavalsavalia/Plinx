import sqlite3


def test_database_connection(db):
    assert db.connection is not None
    assert isinstance(db.connection, sqlite3.Connection)
    assert db.tables == []


def test_define_tables(Author, Book):
    assert Author.name.type is str
    assert Book.author.table is Author

    assert Author.name.sql_type == "TEXT"
    assert Author.age.sql_type == "INTEGER"


def test_create_tables(db, Author, Book):
    db.create(Author)
    db.create(Book)

    assert (
        Author._get_create_sql()
        == "CREATE TABLE IF NOT EXISTS author (id INTEGER PRIMARY KEY AUTOINCREMENT, age INTEGER, name TEXT);"
    )
    assert (
        Book._get_create_sql()
        == "CREATE TABLE IF NOT EXISTS book (id INTEGER PRIMARY KEY AUTOINCREMENT, author_id INTEGER, published INTEGER, title TEXT);"
    )

    for table in ("author", "book"):
        assert table in db.tables


def test_create_author_instance(db, Author):
    db.create(Author)

    john = Author(name="John Doe", age=35)

    assert john.name == "John Doe"
    assert john.age == 35
    assert john.id is None
