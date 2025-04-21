import inspect
import sqlite3
from typing import Generic, TypeVar

from .utils import SQLITE_TYPE_MAP

T = TypeVar("T")


class Database:
    """
    SQLite database wrapper that provides a simple ORM interface.

    The Database class is the main entry point for ORM operations in Plinx.
    It handles database connections, table creation, and provides methods for
    basic CRUD operations (Create, Read, Update, Delete) on Table objects.

    This class uses SQLite as the underlying database engine and provides
    a simplified interface that avoids writing raw SQL in most cases.

    Examples:
        Creating a database and defining models:

        ```python
        from plinx.orm import Database, Table, Column, ForeignKey

        db = Database("app.db")

        class User(Table):
            name = Column(str)
            age = Column(int)

        db.create(User)

        # Create a new user
        john = User(name="John Doe", age=30)
        db.save(john)

        # Query users
        all_users = db.all(User)
        john = db.get(User, id=1)

        # Update a user
        john.age = 31
        db.update(john)

        # Delete a user
        db.delete(john)
        ```
    """

    def __init__(self, path: str):
        """
        Initialize a new database connection.

        Args:
            path: Path to the SQLite database file. If the file doesn't exist,
                 it will be created.
        """
        self.connection = sqlite3.Connection(path)

    def create(self, table: "Table"):
        """
        Create a database table based on a Table subclass definition.

        This method creates a table in the database with columns corresponding
        to the Column and ForeignKey attributes defined on the Table subclass.
        If the table already exists, this method does nothing.

        Args:
            table: A Table subclass with Column and/or ForeignKey attributes

        Example:
            ```python
            class User(Table):
                name = Column(str)
                age = Column(int)

            db.create(User)
            ```
        """
        self.connection.execute(table._get_create_sql())

    def save(self, instance: "Table"):
        """
        Save a Table instance to the database.

        This method inserts a new row into the corresponding database table.
        It automatically sets the instance's id attribute to the new row's ID.

        Args:
            instance: A Table instance to save

        Example:
            ```python
            user = User(name="John Doe", age=30)
            db.save(user)  # user.id is now set to the new row's ID
            ```
        """
        sql, values = instance._get_insert_sql()
        cursor = self.connection.execute(sql, values)
        instance._data["id"] = cursor.lastrowid
        self.connection.commit()

    def all(self, table: "Table"):
        """
        Retrieve all rows from a table.

        This method selects all rows from the table corresponding to the given
        Table subclass. It returns a list of instances of that class, with
        attributes set to the values from the database.

        Args:
            table: A Table subclass to query

        Returns:
            List of Table instances, one for each row in the table

        Example:
            ```python
            all_users = db.all(User)
            for user in all_users:
                print(f"{user.name} is {user.age} years old")
            ```
        """
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
        """
        Retrieve a single row from a table by specified criteria.

        This method selects a row from the database where the specified columns
        match the given values. It returns an instance of the Table subclass with
        attributes set to the values from the database.

        Args:
            table: A Table subclass to query
            **kwargs: Column-value pairs to filter by

        Returns:
            A Table instance corresponding to the matched row

        Raises:
            Exception: If no row matches the criteria

        Example:
            ```python
            # Get user by ID
            user = db.get(User, id=1)

            # Get user by name
            user = db.get(User, name="John Doe")
            ```
        """
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

    def update(self, instance: "Table"):
        """
        Update an existing row in the database.

        This method updates the row corresponding to the given instance with the
        current values of the instance's attributes.

        Args:
            instance: A Table instance to update. Must have an id attribute.

        Example:
            ```python
            user = db.get(User, id=1)
            user.name = "Jane Doe"
            db.update(user)
            ```
        """
        sql, values = instance._get_update_sql()
        self.connection.execute(sql, values)
        self.connection.commit()

    def delete(self, instance: "Table"):
        """
        Delete a row from the database.

        This method deletes the row corresponding to the given instance.

        Args:
            instance: A Table instance to delete. Must have an id attribute.

        Example:
            ```python
            user = db.get(User, id=1)
            db.delete(user)
            ```
        """
        sql, values = instance._get_delete_sql()
        self.connection.execute(sql, values)
        self.connection.commit()

    def close(self):
        """
        Close the database connection.

        This method closes the SQLite connection when the database is no longer
        needed. It's good practice to call this method when you're done using
        the database, especially in longer-running applications.
        """
        if self.connection:
            self.connection.close()
        self.connection = None

    @property
    def tables(self):
        """
        Get a list of all tables in the database.

        Returns:
            List of table names as strings
        """
        SELECT_TABLES_SQL = "SELECT name FROM sqlite_master WHERE type = 'table';"
        return [x[0] for x in self.connection.execute(SELECT_TABLES_SQL).fetchall()]


class Column:
    """
    Define a column in a database table.

    This class represents a column definition for a Table class. It stores
    the column's type and can generate the corresponding SQL type.

    Examples:
        ```python
        class User(Table):
            name = Column(str)  # TEXT column
            age = Column(int)   # INTEGER column
            active = Column(bool)  # INTEGER column (0=False, 1=True)
        ```
    """

    def __init__(self, type: Generic[T]):
        """
        Initialize a new column.

        Args:
            type: Python type for the column (str, int, float, bool, bytes)
        """
        self.type = type

    @property
    def sql_type(self):
        """
        Get the SQL type corresponding to this column's Python type.

        Returns:
            SQL type string (e.g., "TEXT", "INTEGER", "REAL")
        """
        return SQLITE_TYPE_MAP[self.type]


class ForeignKey:
    """
    Define a foreign key relationship between tables.

    This class represents a foreign key constraint in a database schema,
    linking one Table class to another.

    Examples:
        ```python
        class Author(Table):
            name = Column(str)

        class Book(Table):
            title = Column(str)
            author = ForeignKey(Author)  # Creates author_id column
        ```
    """

    def __init__(self, table):
        """
        Initialize a new foreign key.

        Args:
            table: The Table subclass that this foreign key references
        """
        self.table = table


class Table:
    """
    Base class for ORM models in Plinx.

    This class is used as a base class for defining database tables.
    Subclasses should define class attributes using Column and ForeignKey
    to describe the table schema.

    The Table class provides methods for generating SQL statements for
    CRUD operations, which are used by the Database class.

    Examples:
        ```python
        class User(Table):
            name = Column(str)
            age = Column(int)

        class Post(Table):
            title = Column(str)
            content = Column(str)
            author = ForeignKey(User)
        ```
    """

    def __init__(self, **kwargs):
        """
        Initialize a new record.

        Args:
            **kwargs: Column values to initialize with
        """
        self._data = {"id": None}

        for key, value in kwargs.items():
            self._data[key] = value

    def __getattribute__(self, key):
        """
        Custom attribute access for Table instances.

        This method allows Table instances to access column values as attributes,
        rather than accessing self._data directly.

        Args:
            key: Attribute name to access

        Returns:
            The attribute value
        """
        # Why use super().__getattribute__ instead of self._data[key]?
        # Because otherwise it will create an infinite loop since __getattribute__ will call itself
        # and will never return the value
        _data = super().__getattribute__("_data")
        if key in _data:
            return _data[key]
        return super().__getattribute__(key)

    def __setattr__(self, key, value):
        """
        Custom attribute assignment for Table instances.

        This method ensures that when setting an attribute that corresponds to
        a column, the value is stored in self._data.

        Args:
            key: Attribute name to set
            value: Value to assign
        """
        super().__setattr__(key, value)
        if key in self._data:
            self._data[key] = value

    @classmethod
    def _get_create_sql(cls):
        """
        Generate SQL for creating the table.

        Returns:
            SQL string for creating the table
        """
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
        """
        Generate SQL for inserting a record.

        Returns:
            Tuple of (SQL string, parameter values list)
        """
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
        """
        Generate SQL for selecting all records.

        Returns:
            Tuple of (SQL string, field names list)
        """
        SELECT_ALL_SQL = "SELECT {fields} FROM {name};"

        fields = ["id"]

        for name, field in inspect.getmembers(cls):
            if isinstance(field, Column):
                fields.append(name)
            elif isinstance(field, ForeignKey):
                fields.append(name + "_id")

        return (
            SELECT_ALL_SQL.format(
                fields=", ".join(fields),
                name=cls.__name__.lower(),
            ),
            fields,
        )

    @classmethod
    def _get_select_where_sql(cls, **kwargs):
        """
        Generate SQL for selecting records by criteria.

        Args:
            **kwargs: Column-value pairs to filter by

        Returns:
            Tuple of (SQL string, field names list, parameter values list)
        """
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

    def _get_update_sql(self):
        """
        Generate SQL for updating a record.

        Returns:
            Tuple of (SQL string, parameter values list)
        """
        UPDATE_SQL = "UPDATE {name} SET {fields} WHERE id = ?;"

        cls = self.__class__
        fields = []
        values = []

        for name, field in inspect.getmembers(cls):
            if isinstance(field, Column):
                fields.append(name)
                values.append(getattr(self, name))
            elif isinstance(field, ForeignKey):
                fields.append(name + "_id")
                values.append(getattr(self, name).id)

        values.append(getattr(self, "id"))

        return (
            UPDATE_SQL.format(
                name=cls.__name__.lower(),
                fields=", ".join([f"{field} = ?" for field in fields]),
            ),
            values,
        )

    def _get_delete_sql(self):
        """
        Generate SQL for deleting a record.

        Returns:
            Tuple of (SQL string, parameter values list)
        """
        DELETE_SQL = "DELETE FROM {name} WHERE id = ?;"

        return DELETE_SQL.format(name=self.__class__.__name__.lower()), [
            getattr(self, "id")
        ]
