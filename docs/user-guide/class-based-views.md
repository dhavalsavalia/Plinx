# Class-Based Views

Class-based views in Plinx provide an object-oriented approach to organizing your request handlers. This guide explains how to implement and use class-based views effectively.

## Introduction to Class-Based Views

While function-based views are simple and straightforward, class-based views offer several advantages:

1. **Organization**: Group related endpoint handlers by HTTP method
2. **Code reuse**: Share functionality through inheritance
3. **State management**: Store and access shared state across methods
4. **Cleaner structure**: Separate handlers for different HTTP methods

## Basic Usage

Creating a class-based view is simple:

```python
from plinx import Plinx

app = Plinx()

@app.route("/books")
class BookResource:
    def get(self, request, response):
        response.json = {"books": ["Book 1", "Book 2", "Book 3"]}
        
    def post(self, request, response):
        response.status_code = 201
        response.json = {"message": "Book created successfully"}
```

Plinx will automatically dispatch requests to the appropriate method based on the HTTP method:

- `GET` requests to `/books` will call the `get` method
- `POST` requests to `/books` will call the `post` method
- Requests with unsupported methods will receive a 405 Method Not Allowed response

## HTTP Method Support

Class-based views can implement handlers for any HTTP method by defining corresponding methods:

```python
@app.route("/resource")
class CompleteResource:
    def get(self, request, response):
        # Handle GET requests
        response.text = "GET request processed"
        
    def post(self, request, response):
        # Handle POST requests
        response.text = "POST request processed"
        
    def put(self, request, response):
        # Handle PUT requests
        response.text = "PUT request processed"
        
    def delete(self, request, response):
        # Handle DELETE requests
        response.text = "DELETE request processed"
        
    def patch(self, request, response):
        # Handle PATCH requests
        response.text = "PATCH request processed"
        
    def head(self, request, response):
        # Handle HEAD requests
        # Note: No body is returned for HEAD requests
        
    def options(self, request, response):
        # Handle OPTIONS requests
        response.headers["Allow"] = "GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS"
        response.text = ""
```

## URL Parameters with Class-Based Views

URL parameters work the same way as with function-based views:

```python
@app.route("/books/{book_id:d}")
class BookDetailResource:
    def get(self, request, response, book_id):
        response.json = {"book_id": book_id, "title": f"Book {book_id}"}
        
    def put(self, request, response, book_id):
        response.json = {"message": f"Book {book_id} updated"}
        
    def delete(self, request, response, book_id):
        response.json = {"message": f"Book {book_id} deleted"}
```

## Reusing Code with Inheritance

One of the major advantages of class-based views is the ability to share code through inheritance:

```python
# Base class with common functionality
class BaseResourceView:
    def get_current_user(self, request):
        auth_token = request.headers.get("Authorization", "")
        if auth_token.startswith("Bearer "):
            # Validate token and return user (implementation details omitted)
            return {"id": 123, "username": "example_user"}
        return None
    
    def check_authentication(self, request, response):
        user = self.get_current_user(request)
        if user is None:
            response.status_code = 401
            response.json = {"error": "Authentication required"}
            return False
        request.user = user
        return True

# Implement a protected resource using the base class
@app.route("/profile")
class ProfileResource(BaseResourceView):
    def get(self, request, response):
        if not self.check_authentication(request, response):
            return  # Authentication failed, response already set
        
        response.json = {
            "profile": {
                "id": request.user["id"],
                "username": request.user["username"]
            }
        }
```

## Initialization and State

Class-based views are instantiated once per request, allowing you to maintain state during the request lifecycle:

```python
@app.route("/stateful")
class StatefulResource:
    def __init__(self):
        self.start_time = time.time()
        self.operations = []
    
    def get(self, request, response):
        self.operations.append("GET")
        processing_time = time.time() - self.start_time
        
        response.json = {
            "operations": self.operations,
            "processing_time": f"{processing_time:.6f} seconds"
        }
    
    def post(self, request, response):
        self.operations.append("POST")
        # Process the request
        response.json = {"operations": self.operations}
```

## Handling Different Content Types

Class-based views can implement specialized methods for handling different content types:

```python
@app.route("/api/data")
class DataResource:
    def get(self, request, response):
        content_type = request.headers.get("Accept", "application/json")
        
        data = {"name": "Example", "value": 42}
        
        if "application/xml" in content_type:
            self.respond_with_xml(response, data)
        else:
            self.respond_with_json(response, data)
    
    def respond_with_json(self, response, data):
        response.json = data
    
    def respond_with_xml(self, response, data):
        # Convert data to XML (simplified example)
        xml = f"<data><name>{data['name']}</name><value>{data['value']}</value></data>"
        response.text = xml
        response.content_type = "application/xml"
```

## Mixins for Common Functionality

Mixins are a powerful way to compose functionality into your class-based views:

```python
# Authentication mixin
class AuthMixin:
    def authenticate(self, request, response):
        # Authentication logic
        pass

# Logging mixin
class LoggingMixin:
    def log_request(self, request):
        print(f"Request received: {request.method} {request.path}")
    
    def log_response(self, response):
        print(f"Response generated: {response.status_code}")

# Cache control mixin
class CacheControlMixin:
    def add_cache_headers(self, response, max_age=3600):
        response.headers["Cache-Control"] = f"max-age={max_age}"

# Combined resource using mixins
@app.route("/api/items")
class ItemResource(AuthMixin, LoggingMixin, CacheControlMixin):
    def get(self, request, response):
        self.log_request(request)
        
        if not self.authenticate(request, response):
            return
            
        response.json = {"items": ["Item 1", "Item 2"]}
        
        self.add_cache_headers(response, max_age=60)
        self.log_response(response)
```

## Best Practices

1. **Keep classes focused**: Each class should have a clear responsibility
2. **Use inheritance carefully**: Deep inheritance hierarchies can be hard to understand
3. **Consider mixins** for reusable, composable functionality
4. **Document method requirements**: Make it clear what each method expects and returns
5. **Be consistent with method signatures**: All handler methods should take the same parameters
6. **Use helper methods**: Extract common functionality into helper methods
7. **Remember that classes are instantiated per request**: Don't rely on state being preserved between requests

Class-based views provide a powerful way to organize your application logic. By following these best practices, you can create clean, maintainable, and reusable request handlers in your Plinx applications.