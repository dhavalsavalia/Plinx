# Routing

Routing is a fundamental part of any web framework, mapping URL paths to handler functions or classes. Plinx provides a flexible routing system with support for both function and class-based handlers, dynamic URL parameters, and HTTP method constraints.

## Basic Routing

The most basic way to define a route in Plinx is using the `@app.route()` decorator:

```python
from plinx import Plinx

app = Plinx()

@app.route("/hello")
def hello(request, response):
    response.text = "Hello, World!"
```

This registers the `hello` function to handle requests to the `/hello` URL path. By default, this route will only respond to GET requests.

## HTTP Method-Specific Routes

Plinx provides method-specific decorators for all standard HTTP methods:

```python
@app.get("/users")
def get_users(request, response):
    response.json = {"users": ["user1", "user2"]}

@app.post("/users")
def create_user(request, response):
    response.text = "User created"
    response.status_code = 201  # Created

@app.put("/users/{id}")
def update_user(request, response, id):
    response.text = f"Updated user {id}"

@app.delete("/users/{id}")
def delete_user(request, response, id):
    response.text = f"Deleted user {id}"

@app.patch("/users/{id}")
def patch_user(request, response, id):
    response.text = f"Partially updated user {id}"

@app.options("/users")
def options_users(request, response):
    response.headers["Allow"] = "GET, POST, PUT, DELETE, PATCH, OPTIONS"
    response.status_code = 204  # No Content
```

These decorators make your code more explicit about which HTTP methods are expected and handled.

## Dynamic URL Parameters

Plinx supports dynamic URL parameters using the `{param_name}` syntax from the `parse` library:

```python
@app.route("/posts/{post_id}")
def get_post(request, response, post_id):
    response.json = {"post_id": post_id, "title": f"Post {post_id}"}
```

When a request is made to `/posts/123`, the `post_id` parameter will be passed to the handler function with the value `"123"`.

You can use multiple parameters in a single URL:

```python
@app.route("/users/{user_id}/posts/{post_id}")
def get_user_post(request, response, user_id, post_id):
    response.json = {
        "user_id": user_id,
        "post_id": post_id,
        "title": f"Post {post_id} by User {user_id}"
    }
```

## Parameter Types

Currently, URL parameters are passed to handlers as strings. For type conversion, you'll need to handle it in your handler function:

```python
@app.route("/products/{product_id}")
def get_product(request, response, product_id):
    # Convert string to integer
    product_id = int(product_id)
    # Rest of the handler code...
    response.text = f"Product ID: {product_id}"
```

## Class-Based Handlers

For resources that respond to multiple HTTP methods, class-based handlers are more convenient:

```python
@app.route("/api/books")
class BookResource:
    def get(self, request, response):
        response.json = {"books": ["Book 1", "Book 2"]}
        
    def post(self, request, response):
        response.text = "Book created"
        response.status_code = 201
```

When a request is made to `/api/books`, Plinx will:

1. Instantiate the `BookResource` class
2. Look for a method matching the HTTP method name (lowercase)
3. Call that method with the request and response objects

Class-based handlers also support URL parameters:

```python
@app.route("/api/books/{book_id}")
class BookDetailResource:
    def get(self, request, response, book_id):
        response.json = {"id": book_id, "title": f"Book {book_id}"}
        
    def put(self, request, response, book_id):
        response.text = f"Updated book {book_id}"
        
    def delete(self, request, response, book_id):
        response.text = f"Deleted book {book_id}"
```

## Manual Route Registration

If you prefer not to use decorators, you can register routes manually using the `add_route` method:

```python
def user_profile(request, response, user_id):
    response.text = f"Profile for user {user_id}"
    
app.add_route("/users/{user_id}/profile", user_profile)
```

For class-based handlers:

```python
class ProductResource:
    def get(self, request, response):
        response.json = {"products": ["Product 1", "Product 2"]}
        
app.add_route("/products", ProductResource)
```

To specify an HTTP method other than GET:

```python
from plinx.methods import HTTPMethods

def create_category(request, response):
    response.text = "Category created"
    
app.add_route("/categories", create_category, method=HTTPMethods.POST)
```

## Method Not Allowed Handling

If a request is made with an HTTP method that's not supported by the route:

- For function-based handlers: Plinx returns a 405 Method Not Allowed response
- For class-based handlers: If the class doesn't have a method matching the HTTP method, Plinx returns a 405 Method Not Allowed response

## 404 Not Found Handling

If no route matches the requested URL path, Plinx returns a 404 Not Found response.

You can customize this behavior by adding a custom exception handler:

```python
def custom_404_handler(request, response, exception):
    response.status_code = 404
    response.text = "Sorry, the page you're looking for doesn't exist."
    
app.add_exception_handler(custom_404_handler)
```

## Route Organization

For larger applications, you might want to organize your routes into modules. Here's one approach:

```python
# routes/users.py
def register_routes(app):
    @app.route("/users")
    class UserResource:
        def get(self, request, response):
            response.json = {"users": ["user1", "user2"]}
            
        def post(self, request, response):
            response.text = "User created"

# routes/posts.py
def register_routes(app):
    @app.route("/posts")
    def get_posts(request, response):
        response.json = {"posts": ["post1", "post2"]}

# main.py
from plinx import Plinx
from routes import users, posts

app = Plinx()
users.register_routes(app)
posts.register_routes(app)
```

This approach helps keep your code organized and maintainable as your application grows.