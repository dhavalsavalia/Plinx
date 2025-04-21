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

    def save(self, instance: "Table"):
        sql, values = instance._get_insert_sql()
        cursor = self.connection.execute(sql, values)
        instance._data["id"] = cursor.lastrowid
        self.connection.commit()

    def all(self, table: "Table"):
        sql, fields = table._get_select_all_sql()
        rows = self.connection.execute(sql).fetchall()

        result = []

        for row in rows:
            properties = {}
            for field, value in zip(fields, row):
                if field.endswith("_id"):
                    foreign_key = field[:-3]
                    foreign_table = getattr(table, foreign_key).table
                    properties[foreign_key] = self.get(foreign_table, id=value)
                else:
                    properties[field] = value
            result.append(table(**properties))

        return result

    def get(self, table: "Table", **kwargs):
        sql, fields, params = table._get_select_where_sql(**kwargs)
        row = self.connection.execute(sql, params).fetchone()

        if row is None:
            raise Exception(f"{table.__name__} instance with {kwargs} does not exist")

        properties = {}

        for field, value in zip(fields, row):
            if field.endswith("_id"):
                foreign_key = field[:-3]
                foreign_table = getattr(table, foreign_key).table
                properties[foreign_key] = self.get(foreign_table, id=value)
            else:
                properties[field] = value

        return table(**properties)

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
    def __init__(self, **kwargs):
        self._data = {"id": None}

        for key, value in kwargs.items():
            self._data[key] = value

    def __getattribute__(self, key):
        """
        Values to be access are in `self._data`
        Accessing without __getattribute__ will return Column or ForeignKey and not the actual value
        """
        # Why use super().__getattribute__ instead of self._data[key]?
        # Because otherwise it will create an infinite loop since __getattribute__ will call itself
        # and will never return the value
        _data = super().__getattribute__("_data")
        if key in _data:
            return _data[key]
        return super().__getattribute__(key)

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

    def _get_insert_sql(self):
        INSERT_SQL = "INSERT INTO {name} ({fields}) VALUES ({placeholders});"

        cls = self.__class__
        fields = []
        placeholders = []
        values = []

        for name, field in inspect.getmembers(cls):
            if isinstance(field, Column):
                fields.append(name)
                values.append(getattr(self, name))
                placeholders.append("?")
            elif isinstance(field, ForeignKey):
                fields.append(name + "_id")
                values.append(getattr(self, name).id)
                placeholders.append("?")

        fields = ", ".join(fields)
        placeholders = ", ".join(placeholders)

        sql = INSERT_SQL.format(
            name=cls.__name__.lower(), fields=fields, placeholders=placeholders
        )

        return sql, values

    @classmethod
    def _get_select_all_sql(cls):
        SELECT_ALL_SQL = "SELECT {fields} FROM {name};"

        fields = ["id"]

        for name, field in inspect.getmembers(cls):
            if isinstance(field, Column):
                fields.append(name)
            elif isinstance(field, ForeignKey):
                fields.append(name + "_id")

        return SELECT_ALL_SQL.format(
            fields=", ".join(fields),
            name=cls.__name__.lower(),
        ), fields

    @classmethod
    def _get_select_where_sql(cls, **kwargs):
        SELECT_WHERE_SQL = "SELECT {fields} FROM {name} WHERE {query};"

        fields = ["id"]
        query = []
        values = []

        for name, field in inspect.getmembers(cls):
            if isinstance(field, Column):
                fields.append(name)
            elif isinstance(field, ForeignKey):
                fields.append(name + "_id")

        for key, value in kwargs.items():
            query.append(f"{key} = ?")
            values.append(value)

        return (
            SELECT_WHERE_SQL.format(
                fields=", ".join(fields),
                name=cls.__name__.lower(),
                query=", ".join(query),
            ),
            fields,
            values,
        )
