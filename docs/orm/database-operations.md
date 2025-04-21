# Database Operations

This page explains how to perform common database operations using the Plinx ORM, including creating, retrieving, updating, and deleting records.

## Basic CRUD Operations

CRUD stands for Create, Read, Update, and Delete - the four basic database operations you'll perform with the ORM.

### Connecting to a Database

First, establish a connection to your SQLite database:

```python
from plinx.orm import Database

db = Database("my_app.db")
```

This creates a new SQLite database file if it doesn't exist, or opens an existing one.

### Creating Records

To create a new record in the database:

1. Create an instance of your Table class
2. Call the `save` method on the database

```python
from plinx.orm import Database, Table, Column

db = Database("my_app.db")

class User(Table):
    name = Column(str)
    email = Column(str)
    
db.create(User)  # Create the table if it doesn't exist

# Create a new user
user = User(name="John Doe", email="john@example.com")
db.save(user)

# The instance now has an id assigned
print(user.id)  # 1
```

### Retrieving Records

#### Get All Records

To retrieve all records from a table:

```python
users = db.all(User)

for user in users:
    print(f"User {user.id}: {user.name} ({user.email})")
```

#### Get a Single Record by ID or Criteria

To retrieve a specific record by ID or other criteria:

```python
# Get by ID
user = db.get(User, id=1)
print(user.name)  # "John Doe"

# Get by other criteria
user = db.get(User, email="john@example.com")
print(user.name)  # "John Doe"
```

If no record matches the criteria, an exception is raised.

### Updating Records

To update a record:

1. Get the record from the database
2. Modify its attributes
3. Call the `update` method

```python
# Get the record
user = db.get(User, id=1)

# Modify attributes
user.name = "John Smith"
user.email = "johnsmith@example.com"

# Save changes
db.update(user)
```

### Deleting Records

To delete a record:

```python
# Get the record
user = db.get(User, id=1)

# Delete it
db.delete(user)
```

## Working with Relationships

### Creating Related Records

When working with related records, you can create them in a natural, object-oriented way:

```python
from plinx.orm import Database, Table, Column, ForeignKey

db = Database("my_app.db")

class Author(Table):
    name = Column(str)

class Book(Table):
    title = Column(str)
    author = ForeignKey(Author)

db.create(Author)
db.create(Book)

# Create an author
author = Author(name="Jane Austen")
db.save(author)

# Create a book related to the author
book = Book(title="Pride and Prejudice", author=author)
db.save(book)
```

### Retrieving Related Records

When you retrieve a record with foreign keys, the related objects are automatically loaded:

```python
# Get the book
book = db.get(Book, id=1)

# Access the related author
print(book.title)       # "Pride and Prejudice"
print(book.author.name) # "Jane Austen"
```

### Updating Relationships

You can change relationships by assigning a different object:

```python
# Get two authors
austen = db.get(Author, name="Jane Austen")
dickens = Author(name="Charles Dickens")
db.save(dickens)

# Get the book
book = db.get(Book, id=1)

# Change the author
book.author = dickens
db.update(book)

# Verify the change
updated_book = db.get(Book, id=1)
print(updated_book.author.name)  # "Charles Dickens"
```

## Working with Multiple Tables

### Creating Multiple Tables

You can create multiple tables in sequence:

```python
from plinx.orm import Database, Table, Column, ForeignKey

db = Database("bookstore.db")

class Publisher(Table):
    name = Column(str)
    
class Author(Table):
    name = Column(str)
    bio = Column(str)
    
class Book(Table):
    title = Column(str)
    year = Column(int)
    author = ForeignKey(Author)
    publisher = ForeignKey(Publisher)

# Create all tables
db.create(Publisher)
db.create(Author)
db.create(Book)
```

### Complex Queries and Filtering

Currently, Plinx ORM supports basic filtering using the `get` method's keyword arguments:

```python
# Get a book with specific title
book = db.get(Book, title="Pride and Prejudice")

# Get a book by ID
book = db.get(Book, id=1)
```

For more complex queries, you would need to extend the ORM or use SQLite directly.

## Best Practices

### Connection Management

It's good practice to close the database connection when you're done with it:

```python
db = Database("my_app.db")
# Use the database...
db.close()  # Close the connection when done
```

In web applications, you typically create the database connection when the app starts and close it when the app shuts down.

### Exception Handling

Handle exceptions when retrieving records that might not exist:

```python
try:
    user = db.get(User, email="nonexistent@example.com")
except Exception as e:
    print(f"Error: {e}")
    # Handle the case where the user doesn't exist
```

### Batching Operations

For larger operations, you might want to batch your database calls:

```python
# Batch inserting users
users_data = [
    {"name": "User 1", "email": "user1@example.com"},
    {"name": "User 2", "email": "user2@example.com"},
    {"name": "User 3", "email": "user3@example.com"},
]

for data in users_data:
    user = User(**data)
    db.save(user)
```

## Advanced Topics

### Using Transactions

The Plinx ORM automatically handles transactions for individual operations. For custom transactions spanning multiple operations, you can use the SQLite connection directly:

```python
try:
    db.connection.execute("BEGIN TRANSACTION;")
    
    # Perform multiple operations
    author = Author(name="Leo Tolstoy")
    db.save(author)
    
    book1 = Book(title="War and Peace", author=author)
    db.save(book1)
    
    book2 = Book(title="Anna Karenina", author=author)
    db.save(book2)
    
    db.connection.execute("COMMIT;")
except Exception as e:
    db.connection.execute("ROLLBACK;")
    print(f"Transaction failed: {e}")
```

### Raw SQL Access

If you need functionality not provided by the ORM, you can execute raw SQL:

```python
# Execute a custom query
cursor = db.connection.execute(
    "SELECT book.title, author.name FROM book JOIN author ON book.author_id = author.id"
)
results = cursor.fetchall()

for title, author_name in results:
    print(f"{title} by {author_name}")
```

### Table Introspection

You can get a list of all tables in the database:

```python
tables = db.tables
print(f"Database tables: {tables}")
```

## Limitations and Future Enhancements

The current version of the Plinx ORM is intentionally minimalistic. Here are some features that might be added in future versions:

- More complex query capabilities (filtering, ordering, etc.)
- Support for table indexes and constraints
- Schema migration tools
- Lazy-loading of relationships
- Support for more database backends beyond SQLite

## Summary

The Plinx ORM provides a simple, intuitive way to interact with SQLite databases using Python objects. While it lacks some features of more comprehensive ORMs, it offers a clean interface for basic CRUD operations and relationships that is perfect for small to medium-sized applications and educational purposes.