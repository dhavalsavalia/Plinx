import os

import pytest

from plinx import Plinx
from plinx.orm import Column, Database, ForeignKey, Table


# Application fixtures
@pytest.fixture
def app():
    return Plinx()


@pytest.fixture
def client(app):
    return app.test_session()


# ORM fixtures
@pytest.fixture
def db():
    DB_PATH = "./test.db"
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    db = Database(DB_PATH)
    yield db
    db.close()
    return db


@pytest.fixture
def Author():
    class Author(Table):
        name = Column(str)
        age = Column(int)

    return Author


@pytest.fixture
def Book(Author):
    class Book(Table):
        title = Column(str)
        published = Column(bool)
        author = ForeignKey(Author)

    return Book
