# Handling Requests

Plinx provides a flexible and intuitive way to handle HTTP requests. This guide explains how request handling works and shows various techniques for working with requests and responses.

## Request Flow

When a request arrives at your Plinx application, it goes through the following flow:

1. The WSGI server passes the request to the Plinx application
2. The request passes through any configured middleware (see [Middleware](middleware.md))
3. Plinx tries to match the request path with registered routes
4. If a matching route is found, the appropriate handler is called
5. The handler generates a response
6. The response passes back through middleware
7. The response is returned to the client

## Request Object

The request object is an instance of `webob.Request` and provides access to all the information about the incoming HTTP request:

```python
@app.route("/example")
def handler(request, response):
    # Access request properties
    method = request.method  # GET, POST, etc.
    path = request.path      # /example
    query = request.GET      # Query parameters
    form = request.POST      # Form data
    json = request.json      # JSON body (if Content-Type is application/json)
    headers = request.headers  # Headers dictionary
```

### Common Request Properties

| Property | Description |
| --- | --- |
| `request.method` | HTTP method (GET, POST, etc.) |
| `request.path` | Request path |
| `request.GET` | Dictionary-like object containing query parameters |
| `request.POST` | Dictionary-like object containing form data |
| `request.json` | Parsed JSON body (if Content-Type is application/json) |
| `request.headers` | Dictionary-like object containing HTTP headers |
| `request.cookies` | Dictionary-like object containing cookies |
| `request.body` | Raw request body as bytes |

## Response Object

The response object is an instance of `plinx.response.PlinxResponse` and allows you to set the response data:

```python
@app.route("/example")
def handler(request, response):
    # Set response properties
    response.text = "Hello, World!"  # Plain text response
    response.status_code = 200       # HTTP status code
    response.headers["X-Custom"] = "Value"  # Custom header
```

### Response Helpers

Plinx provides several helper properties to make setting responses easier:

#### Text Response

```python
@app.route("/text")
def text_handler(request, response):
    response.text = "Hello, Text!"
    # Content-Type will be automatically set to text/plain
```

#### JSON Response

```python
@app.route("/json")
def json_handler(request, response):
    response.json = {"message": "Hello, JSON!"}
    # Content-Type will be automatically set to application/json
```

#### Custom Response Body

```python
@app.route("/custom")
def custom_handler(request, response):
    response.body = b"Hello, World as bytes!"
    response.content_type = "text/plain"
```

## Class-Based Views

Plinx supports class-based views for organizing handlers by HTTP method:

```python
@app.route("/books")
class BooksResource:
    def get(self, req, resp):
        resp.text = "Get all books"
        
    def post(self, req, resp):
        resp.text = "Create a new book"
        
    def put(self, req, resp):
        resp.text = "Update a book"
        
    def delete(self, req, resp):
        resp.text = "Delete a book"
```

Class-based views automatically map HTTP methods to corresponding method names. If a method is not defined, a 405 Method Not Allowed response will be returned.

## URL Parameters

Plinx supports dynamic URL parameters with type conversion:

```python
@app.route("/users/{user_id:d}")  # :d converts to integer
def user_detail(request, response, user_id):
    response.text = f"User ID: {user_id} (type: {type(user_id).__name__})"
    
@app.route("/posts/{slug}")  # String parameter (default)
def post_detail(request, response, slug):
    response.text = f"Post slug: {slug}"

@app.route("/math/{operation}/{num_1:d}/{num_2:d}")  # Multiple parameters
def calculate(request, response, operation, num_1, num_2):
    if operation == "add":
        result = num_1 + num_2
    # ... other operations
    response.text = f"Result: {result}"
```

## Error Handling

Plinx provides a mechanism for handling exceptions at the application level:

```python
def custom_exception_handler(request, response, exception_cls):
    response.text = f"Error: {str(exception_cls)}"
    response.status_code = 500  # Or an appropriate status code

app.add_exception_handler(custom_exception_handler)

@app.route("/error")
def error_handler(request, response):
    raise ValueError("Something went wrong")  # Will be handled by exception handler
```

For more details on error handling, see the [Error Handling](error-handling.md) guide.

## Best Practices

1. **Keep handlers focused**: Each handler should have a single responsibility
2. **Use class-based views** for resource-oriented endpoints
3. **Set appropriate status codes**: Use standard HTTP status codes for different situations
4. **Validate input data**: Always validate and sanitize user input
5. **Handle exceptions gracefully**: Use exception handling to provide meaningful error messages
6. **Use middleware** for cross-cutting concerns like authentication or logging
7. **Return consistent response formats**: Standardize your API response structure

By following these principles, you can build maintainable and robust request handlers in your Plinx applications.