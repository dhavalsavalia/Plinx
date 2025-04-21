# Tables & Models

In the Plinx ORM, database tables are represented as Python classes that inherit from the `Table` base class. This page explains how to define tables, columns, and relationships for your database.

## Defining Tables

To define a database table, create a class that inherits from `Table`:

```python
from plinx.orm import Table, Column

class User(Table):
    name = Column(str)
    email = Column(str)
    age = Column(int)
    is_active = Column(bool)
```

This code defines a `User` table with columns for `name`, `email`, `age`, and `is_active`. Each column is defined using the `Column` class with a Python type that determines the corresponding SQLite type.

## Column Types

Plinx ORM maps Python types to SQLite types as follows:

| Python Type | SQLite Type |
|-------------|-------------|
| `str`       | TEXT        |
| `int`       | INTEGER     |
| `float`     | REAL        |
| `bool`      | INTEGER     |
| `bytes`     | BLOB        |

For example:

```python
class Product(Table):
    name = Column(str)          # TEXT
    price = Column(float)       # REAL
    stock = Column(int)         # INTEGER
    is_available = Column(bool) # INTEGER (0 or 1)
    image_data = Column(bytes)  # BLOB
```

## Creating Tables in the Database

After defining your table classes, you need to create them in the database:

```python
from plinx.orm import Database

db = Database("my_app.db")  # Connect to SQLite database

# Create tables
db.create(User)
db.create(Product)
```

The `create` method generates and executes the appropriate SQL `CREATE TABLE` statement based on your class definition. If the table already exists, it won't be recreated (Plinx uses `CREATE TABLE IF NOT EXISTS`).

## Primary Keys

Every table automatically gets an auto-incrementing integer primary key column named `id`. You don't need to define this yourself:

```python
user = User(name="John", email="john@example.com", age=30, is_active=True)
db.save(user)
print(user.id)  # Automatically assigned after saving
```

## Relationships

To define relationships between tables, use the `ForeignKey` class:

```python
from plinx.orm import Table, Column, ForeignKey

class Category(Table):
    name = Column(str)
    description = Column(str)

class Product(Table):
    name = Column(str)
    price = Column(float)
    category = ForeignKey(Category)  # Reference to Category
```

This creates a foreign key from `Product` to `Category`. Behind the scenes, Plinx creates a `category_id` column in the `Product` table that references the `id` column in the `Category` table.

When you retrieve a `Product` from the database, its `category` attribute will be a fully loaded `Category` instance:

```python
# Create a category
electronics = Category(name="Electronics", description="Electronic devices")
db.save(electronics)

# Create a product with a reference to the category
phone = Product(name="Smartphone", price=599.99, category=electronics)
db.save(phone)

# Retrieve the product
product = db.get(Product, id=1)
print(product.name)            # "Smartphone"
print(product.category.name)   # "Electronics"
```

## Creating Instances

To create a new record, instantiate your table class with keyword arguments for each column:

```python
user = User(
    name="Alice Smith",
    email="alice@example.com",
    age=25,
    is_active=True
)
```

All attributes are optional during instantiation. If not provided, they'll be set to `None`:

```python
# Partial instantiation
user = User(name="Bob Johnson")
print(user.email)  # None
```

## Attribute Access

You can access and modify attributes as normal Python properties:

```python
user = User(name="Charlie Brown")
print(user.name)  # "Charlie Brown"

user.name = "Charlie B. Brown"
user.age = 32
```

## Table Names

By default, the table name in the database is the lowercase version of your class name:

- `User` class → `user` table
- `Product` class → `product` table
- `OrderItem` class → `orderitem` table

## The Model Pattern

While the ORM doesn't enforce a strict MVC (Model-View-Controller) pattern, your `Table` classes essentially function as models. It's a good practice to include business logic related to your data in these classes:

```python
class User(Table):
    name = Column(str)
    email = Column(str)
    age = Column(int)
    
    def is_adult(self):
        return self.age >= 18
    
    def get_display_name(self):
        return self.name.split()[0]  # Return first name
```

This encapsulates behavior with data, following good object-oriented design principles.

## Best Practices

1. **Class names should be singular**: Use `User`, not `Users`
2. **Use descriptive names**: Choose clear, descriptive names for tables and columns
3. **Keep models organized**: Group related models in the same module/file
4. **Define relationships explicitly**: Use `ForeignKey` to make relationships clear
5. **Add business logic**: Include methods that encapsulate business rules

## Limitations

The current Plinx ORM implementation has a few limitations to be aware of:

- No support for composite primary keys
- No built-in schema migrations
- No support for complex SQL features like indexes, unique constraints, etc.
- No support for many-to-many relationships without an explicit join table

These limitations help keep the ORM simple and focused while still being useful for many common scenarios.

## Next Steps

Now that you understand how to define tables and models, let's look at how to perform [database operations](database-operations.md) with the Plinx ORM.