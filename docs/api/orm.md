# ORM API

The Plinx ORM (Object-Relational Mapping) module provides a lightweight interface for working with SQLite databases. This page documents the core classes and methods available in the ORM.

## Database Class

::: plinx.orm.orm.Database
    handler: python
    selection:
      members:
        - __init__
        - create
        - save
        - all
        - get
        - update
        - delete
        - close
        - tables
    rendering:
      show_source: true
      show_root_heading: true
      show_if_no_docstring: false

## Table Class

::: plinx.orm.orm.Table
    handler: python
    selection:
      members:
        - __init__
        - __getattribute__
        - __setattr__
        - _get_create_sql
        - _get_insert_sql
        - _get_select_all_sql
        - _get_select_where_sql
        - _get_update_sql
        - _get_delete_sql
    rendering:
      show_source: true
      show_root_heading: true
      show_if_no_docstring: false

## Column Class

::: plinx.orm.orm.Column
    handler: python
    rendering:
      show_source: true
      show_root_heading: true
      show_if_no_docstring: false

## ForeignKey Class

::: plinx.orm.orm.ForeignKey
    handler: python
    rendering:
      show_source: true
      show_root_heading: true
      show_if_no_docstring: false

## Type Mapping

The ORM maps Python types to SQLite types according to the following table:

| Python Type | SQLite Type |
|-------------|-------------|
| `str`       | TEXT        |
| `int`       | INTEGER     |
| `float`     | REAL        |
| `bool`      | INTEGER     |
| `bytes`     | BLOB        |

## Examples

### Basic ORM Usage

```python
from plinx.orm import Database, Table, Column, ForeignKey

# Connect to database
db = Database("example.db")

# Define tables
class User(Table):
    name = Column(str)
    age = Column(int)

class Post(Table):
    title = Column(str)
    content = Column(str)
    author = ForeignKey(User)

# Create tables
db.create(User)
db.create(Post)

# Create records
user = User(name="John Doe", age=30)
db.save(user)

post = Post(title="Hello World", content="This is my first post", author=user)
db.save(post)

# Query records
all_users = db.all(User)
for user in all_users:
    print(f"User: {user.name}, Age: {user.age}")

# Get a specific record
post = db.get(Post, id=1)
print(f"Post: {post.title} by {post.author.name}")

# Update a record
post.content = "Updated content"
db.update(post)

# Delete a record
db.delete(post)

# Close connection when done
db.close()
```

### Advanced Querying

```python
# Get by non-primary key field
try:
    user = db.get(User, name="John Doe")
    print(f"Found user: {user.name}")
except Exception as e:
    print(f"User not found: {e}")
```

### Table Introspection

```python
# List all tables in the database
tables = db.tables
print(f"Tables in database: {tables}")
```

### Custom Table Methods

You can add custom methods to your table classes to encapsulate business logic:

```python
class User(Table):
    name = Column(str)
    email = Column(str)
    age = Column(int)
    
    def is_adult(self):
        return self.age >= 18
    
    def get_email_domain(self):
        return self.email.split('@')[1] if '@' in self.email else None
        
# Usage
user = db.get(User, id=1)
if user.is_adult():
    print(f"{user.name} is an adult")
```

## Working with Relationships

```python
class Department(Table):
    name = Column(str)

class Employee(Table):
    name = Column(str)
    department = ForeignKey(Department)
    salary = Column(float)
    
# Create tables
db.create(Department)
db.create(Employee)

# Create related records
engineering = Department(name="Engineering")
db.save(engineering)

alice = Employee(name="Alice", department=engineering, salary=75000.0)
bob = Employee(name="Bob", department=engineering, salary=85000.0)
db.save(alice)
db.save(bob)

# Query with relationship
employee = db.get(Employee, name="Alice")
print(f"{employee.name} works in {employee.department.name}")
```

## Limitations

The current version of the Plinx ORM has the following limitations:

1. **SQLite Only**: Only supports SQLite databases
2. **Basic Querying**: No complex filtering, ordering, or joins in queries
3. **No Migrations**: No built-in support for schema migrations
4. **Eager Loading**: All relationships are eagerly loaded (no lazy loading)
5. **Simple Relationships**: Only supports one-to-many relationships via ForeignKey

These limitations are intentional to keep the ORM simple and focused while still being useful for many common scenarios.