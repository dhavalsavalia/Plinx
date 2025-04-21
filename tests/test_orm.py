import sqlite3

import pytest


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


def test_save_author_instances(db, Author):
    db.create(Author)

    john = Author(name="John Doe", age=23)
    db.save(john)
    assert john._get_insert_sql() == (
        "INSERT INTO author (age, name) VALUES (?, ?);",
        [23, "John Doe"],
    )
    assert john.id == 1

    man = Author(name="Man Harsh", age=28)
    db.save(man)
    assert man.id == 2

    vik = Author(name="Vik Star", age=43)
    db.save(vik)
    assert vik.id == 3

    jack = Author(name="Jack Ma", age=39)
    db.save(jack)
    assert jack.id == 4


def test_save_book_instance(db, Author, Book):
    db.create(Author)
    db.create(Book)

    john = Author(name="John Doe", age=23)
    db.save(john)

    book = Book(
        title="Test Book",
        published=True,
        author=john,
    )
    db.save(book)

    assert book._get_insert_sql() == (
        "INSERT INTO book (author_id, published, title) VALUES (?, ?, ?);",
        [1, True, "Test Book"],
    )
    assert book.id == 1


def test_query_all_authors(db, Author):
    db.create(Author)
    john = Author(name="John Doe", age=23)
    vik = Author(name="Vik Star", age=43)
    db.save(john)
    db.save(vik)

    authors = db.all(Author)

    assert Author._get_select_all_sql() == (
        "SELECT id, age, name FROM author;",
        ["id", "age", "name"],
    )
    assert len(authors) == 2
    assert type(authors[0]) is Author
    assert {a.age for a in authors} == {23, 43}
    assert {a.name for a in authors} == {"John Doe", "Vik Star"}


def test_query_all_books(db, Author, Book):
    db.create(Author)
    db.create(Book)

    john = Author(name="John Doe", age=23)
    db.save(john)

    book = Book(
        title="Test Book",
        published=True,
        author=john,
    )
    db.save(book)

    books = db.all(Book)

    assert Book._get_select_all_sql() == (
        "SELECT id, author_id, published, title FROM book;",
        ["id", "author_id", "published", "title"],
    )
    assert len(books) == 1
    assert type(books[0]) is Book
    assert {b.title for b in books} == {"Test Book"}
    assert books[0].author.name == "John Doe"
    assert books[0].author.age == 23


def test_get_author(db, Author):
    db.create(Author)
    john_srow = Author(name="John Doe", age=43)  # get it? John Snow
    db.save(john_srow)

    john_from_db = db.get(Author, id=1)

    assert Author._get_select_where_sql(id=1) == (
        "SELECT id, age, name FROM author WHERE id = ?;",
        ["id", "age", "name"],
        [1],
    )
    assert type(john_from_db) is Author
    assert john_from_db.age == 43
    assert john_from_db.name == "John Doe"
    assert john_from_db.id == 1


def test_get_book(db, Author, Book):
    db.create(Author)
    db.create(Book)

    john = Author(name="John Doe", age=23)
    db.save(john)

    book = Book(
        title="Test Book",
        published=True,
        author=john,
    )
    db.save(book)

    book_from_db = db.get(Book, title="Test Book")
    assert Book._get_select_where_sql(title="Test Book") == (
        "SELECT id, author_id, published, title FROM book WHERE title = ?;",
        ["id", "author_id", "published", "title"],
        ["Test Book"],
    )
    assert type(book_from_db) is Book
    assert book_from_db.id == 1
    assert book_from_db.title == "Test Book"
    assert book_from_db.author.name == "John Doe"
    assert book_from_db.author.age == 23


def test_get_invalid_book(db, Author, Book):
    db.create(Author)
    db.create(Book)

    john = Author(name="John Doe", age=23)
    db.save(john)

    book = Book(
        title="Test Book",
        published=True,
        author=john,
    )
    db.save(book)

    
    with pytest.raises(Exception) as excinfo:
        db.get(Book, id=2)

        assert isinstance(excinfo.value, Exception)
        assert "Book instance with {'id': 2} does not exist" == str(excinfo.value)


def test_update_author(db, Author):
    db.create(Author)
    john = Author(name="John Doe", age=23)
    db.save(john)

    john.age = 43
    john.name = "John Snow"
    db.update(john)

    assert john._get_update_sql() == (
        "UPDATE author SET age = ?, name = ? WHERE id = ?;",
        [43, "John Snow", 1],
    )

    john_from_db = db.get(Author, id=john.id)

    assert john_from_db.age == 43
    assert john_from_db.name == "John Snow"
    assert john_from_db.id == 1


def test_update_book(db, Author, Book):
    db.create(Author)
    db.create(Book)

    john = Author(name="John Doe", age=23)
    db.save(john)

    book = Book(
        title="Test Book",
        published=1,
        author=john,
    )
    db.save(book)

    book.title = "Updated Book"
    book.published = False
    db.update(book)

    assert book._get_update_sql() == (
        "UPDATE book SET author_id = ?, published = ?, title = ? WHERE id = ?;",
        [1, False, "Updated Book", 1],
    )

    book_from_db = db.get(Book, id=book.id)

    assert book_from_db.title == "Updated Book"
    assert book_from_db.id == 1
    assert book_from_db.published == False # noqa 0 is False 
