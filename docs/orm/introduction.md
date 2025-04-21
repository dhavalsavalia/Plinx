# ORM Introduction

Plinx includes a lightweight Object-Relational Mapping (ORM) system that makes it easy to interact with SQLite databases. The ORM provides a clean, Pythonic interface for defining tables and performing database operations without writing raw SQL.

## Key Features

- **Simple Table Definitions**: Define database tables as Python classes
- **Automatic Table Creation**: Create tables from class definitions
- **Intuitive CRUD Operations**: Easy methods for creating, reading, updating, and deleting records
- **Foreign Key Relationships**: Define relationships between tables
- **Type Mapping**: Python types mapped to appropriate SQLite types
- **No Raw SQL Required**: Perform common operations without writing SQL

## Basic Concepts

The Plinx ORM consists of a few core components:

- **Database**: The main class for connecting to SQLite and performing operations
- **Table**: Base class for defining database tables
- **Column**: Class for defining table columns with Python types
- **ForeignKey**: Class for defining relationships between tables

## Quick Example

Here's a quick example of how to use the Plinx ORM:

```python
from plinx.orm import Database, Table, Column, ForeignKey

# Connect to a SQLite database
db = Database("my_app.db")

# Define tables
class Author(Table):
    name = Column(str)
    bio = Column(str)

class Book(Table):
    title = Column(str)
    year = Column(int)
    author = ForeignKey(Author)

# Create tables in the database
db.create(Author)
db.create(Book)

# Create records
jk_rowling = Author(name="J.K. Rowling", bio="British author...")
db.save(jk_rowling)

harry_potter = Book(
    title="Harry Potter and the Philosopher's Stone",
    year=1997,
    author=jk_rowling
)
db.save(harry_potter)

# Query records
all_authors = db.all(Author)
for author in all_authors:
    print(f"Author: {author.name}")

all_books = db.all(Book)
for book in all_books:
    print(f"Book: {book.title} by {book.author.name}")

# Get a specific record
book = db.get(Book, id=1)
print(f"Found book: {book.title}")

# Update a record
book.year = 1998
db.update(book)

# Delete a record
db.delete(book)
```

## When to Use the Plinx ORM

The Plinx ORM is ideal for:

- Small to medium-sized applications
- Prototyping and rapid development
- Educational purposes
- Projects where a full-featured ORM would be overkill

It provides a balance between simplicity and power, allowing you to get started quickly without dealing with the complexity of larger ORMs.

## Limitations

The Plinx ORM has some limitations compared to more robust ORMs like SQLAlchemy:

- **SQLite Only**: Currently only supports SQLite databases
- **Limited Query API**: No query builder or complex filtering
- **No Migrations**: No built-in schema migration system
- **Limited Relationship Types**: Only simple foreign keys are supported
- **No Lazy Loading**: All relationships are eagerly loaded

These limitations are intentional to keep the ORM simple and focused. If you need more advanced features, consider using a more comprehensive ORM.

## Next Steps

In the next sections, we'll explore how to:

- Define tables and columns in detail
- Work with foreign key relationships
- Perform CRUD operations
- Handle common database patterns

Let's start with [Tables & Models](tables-and-models.md).