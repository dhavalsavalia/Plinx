# Quick Start

This guide will help you create your first Plinx application in just a few minutes. We'll cover the basics of:

1. Creating a simple application
2. Adding routes
3. Handling requests and responses
4. Running your application

## Your First Plinx Application

Let's create a simple "Hello, World!" application:

```python
# app.py
from plinx import Plinx

# Create a new Plinx application
app = Plinx()

# Define a route using a decorator
@app.route("/")
def hello(request, response):
    response.text = "Hello, World!"
    
if __name__ == "__main__":
    # For development only - not for production
    from wsgiref.simple_server import make_server
    
    print("Development server starting at http://localhost:8000...")
    server = make_server('localhost', 8000, app)
    server.serve_forever()
```

Save this as `app.py` and run it:

```bash
python app.py
```

Visit http://localhost:8000/ in your browser to see "Hello, World!"

## Adding More Routes

Let's expand our application with more routes:

```python
# Text response
@app.route("/about")
def about(request, response):
    response.text = "About Plinx"
    
# JSON response
@app.route("/api/info")
def api_info(request, response):
    response.json = {
        "name": "Plinx",
        "version": "1.0.0",
        "status": "OK"
    }
    
# Dynamic URL parameters
@app.route("/hello/{name}")
def greet(request, response, name):
    response.text = f"Hello, {name}!"
```

## HTTP Methods

Plinx supports different HTTP methods through specific decorators:

```python
@app.get("/users")
def get_users(request, response):
    response.json = {"users": ["user1", "user2"]}

@app.post("/users")
def create_user(request, response):
    # Access form data or JSON body from request
    response.text = "User created successfully"
    response.status_code = 201  # Created

@app.put("/users/{user_id}")
def update_user(request, response, user_id):
    response.text = f"User {user_id} updated"

@app.delete("/users/{user_id}")
def delete_user(request, response, user_id):
    response.text = f"User {user_id} deleted"
```

## Class-Based Views

For resources that require multiple HTTP methods, you can use class-based views:

```python
@app.route("/books")
class BooksResource:
    def get(self, request, response):
        response.json = {"books": ["Book 1", "Book 2"]}
        
    def post(self, request, response):
        response.text = "Book created"
        response.status_code = 201
```

## Running in Production

For production deployment, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn app:app
```

Or with custom options:

```bash
gunicorn app:app --workers=4 --bind=0.0.0.0:8000
```

## Next Steps

- Learn about [Middleware](../user-guide/middleware.md) for request/response processing
- Explore the [ORM](../orm/introduction.md) for database operations
- Check out [error handling](../user-guide/error-handling.md) techniques
- Browse the [API Reference](../api/applications.md) for detailed documentation