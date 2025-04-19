import inspect
import sqlite3
from typing import Generic, TypeVar

from .utils import SQLITE_TYPE_MAP

T = TypeVar("T")


class Database:
    def __init__(self, path: str):
        self.connection = sqlite3.Connection(path)

    def create(self, table: "Table"):
        self.connection.execute(table._get_create_sql())

    def close(self):
        if self.connection:
            self.connection.close()
        self.connection = None

    @property
    def tables(self):
        SELECT_TABLES_SQL = "SELECT name FROM sqlite_master WHERE type = 'table';"
        return [x[0] for x in self.connection.execute(SELECT_TABLES_SQL).fetchall()]


class Column:
    def __init__(self, type: Generic[T]):
        self.type = type

    @property
    def sql_type(self):
        return SQLITE_TYPE_MAP[self.type]


class ForeignKey:
    def __init__(self, table):
        self.table = table


class Table:
    @classmethod
    def _get_create_sql(cls):
        CREATE_TABLE_SQL = "CREATE TABLE IF NOT EXISTS {name} ({fields});"
        fields = [
            "id INTEGER PRIMARY KEY AUTOINCREMENT",
        ]

        for name, field in inspect.getmembers(cls):
            if isinstance(field, Column):
                fields.append(f"{name} {field.sql_type}")
            elif isinstance(field, ForeignKey):
                fields.append(f"{name}_id INTEGER")

        fields = ", ".join(fields)
        name = cls.__name__.lower()
        return CREATE_TABLE_SQL.format(name=name, fields=fields)
