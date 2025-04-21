# Error Handling

Proper error handling is crucial for building robust web applications. This guide explains how to handle errors in Plinx applications, from simple exception handling to more complex error management strategies.

## Built-in Error Handling

### Default Error Responses

By default, Plinx handles errors in the following way:

1. If a route handler raises an exception, Plinx catches it and:
   - Sets the response status code to 500 (Internal Server Error)
   - Sets the response text to the exception's string representation

2. If no route matches the requested URL, Plinx:
   - Sets the response status code to 404 (Not Found)
   - Sets the response text to "Not Found"

3. If a route is matched but the HTTP method is not supported, Plinx:
   - Sets the response status code to 405 (Method Not Allowed)
   - Sets the response text to "Method Not Allowed"

### Custom Exception Handler

You can override the default exception handling by registering a custom exception handler:

```python
def custom_exception_handler(request, response, exception):
    """Handle all exceptions in the application."""
    response.status_code = 500
    response.json = {
        "error": str(exception),
        "type": exception.__class__.__name__
    }
    
    # You can also log the exception
    import traceback
    print(f"Exception: {exception}")
    print(traceback.format_exc())

app = Plinx()
app.add_exception_handler(custom_exception_handler)
```

This handler will be called whenever an uncaught exception occurs in a route handler.

## Handling Specific Exceptions

To handle specific exception types differently, you can check the exception type in your handler:

```python
def exception_handler(request, response, exception):
    if isinstance(exception, ValueError):
        response.status_code = 400  # Bad Request
        response.json = {"error": "Invalid input", "details": str(exception)}
    elif isinstance(exception, PermissionError):
        response.status_code = 403  # Forbidden
        response.json = {"error": "Permission denied"}
    elif isinstance(exception, FileNotFoundError):
        response.status_code = 404  # Not Found
        response.json = {"error": "Resource not found"}
    else:
        response.status_code = 500  # Internal Server Error
        response.json = {"error": "An unexpected error occurred"}
        
    # Log the error
    print(f"Error: {exception.__class__.__name__}: {exception}")

app.add_exception_handler(exception_handler)
```

## Custom Error Classes

You can define custom error classes to make your error handling more structured:

```python
class APIError(Exception):
    """Base class for API errors."""
    status_code = 500
    
    def __init__(self, message, status_code=None, payload=None):
        super().__init__(message)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload or {}
        
    def to_dict(self):
        error_dict = dict(self.payload)
        error_dict['message'] = self.message
        error_dict['status'] = self.status_code
        return error_dict

class BadRequestError(APIError):
    """Error for invalid client requests."""
    status_code = 400

class NotFoundError(APIError):
    """Error for resources that don't exist."""
    status_code = 404
```

Then handle these custom errors in your exception handler:

```python
def api_exception_handler(request, response, exception):
    if isinstance(exception, APIError):
        response.status_code = exception.status_code
        response.json = exception.to_dict()
    else:
        response.status_code = 500
        response.json = {
            "message": "An unexpected error occurred",
            "status": 500
        }

app.add_exception_handler(api_exception_handler)
```

In your handlers, you can raise these custom errors:

```python
@app.route("/users/{user_id}")
def get_user(request, response, user_id):
    try:
        user_id = int(user_id)
    except ValueError:
        raise BadRequestError("User ID must be a number")
        
    user = get_user_from_database(user_id)
    if user is None:
        raise NotFoundError(f"User {user_id} not found")
        
    response.json = {"id": user_id, "name": user["name"]}
```

## Error Handling with Middleware

You can also use middleware for error handling, which gives you more control over the request/response cycle:

```python
from plinx.middleware import Middleware

class ErrorHandlingMiddleware(Middleware):
    def process_request(self, request):
        # You could add request validation here
        pass
        
    def process_response(self, request, response):
        # You could modify error responses here
        if response.status_code >= 400:
            response.headers["X-Error"] = "true"
            
            # For API requests, ensure JSON response
            if request.path.startswith("/api/"):
                if not isinstance(response.json, dict):
                    response.json = {"error": response.text or "An error occurred"}

app.add_middleware(ErrorHandlingMiddleware)
```

## Handling 404 Errors

To customize the 404 Not Found response, you can add a catch-all route at the end of your routes:

```python
# Add all your normal routes first

# Then add a catch-all route
@app.route("/{path}")
def not_found(request, response, path=None):
    response.status_code = 404
    response.json = {
        "error": "Not Found",
        "path": request.path
    }
```

Note: This approach works because Plinx tries routes in the order they were added, and the path parameter in this route will match any single path segment. For more complex catch-all behavior, you might need a more sophisticated approach.

## Handling Method Not Allowed

For class-based views, you can explicitly handle unsupported methods:

```python
@app.route("/resources/{id}")
class ResourceHandler:
    def get(self, request, response, id):
        response.json = {"id": id, "name": f"Resource {id}"}
        
    def put(self, request, response, id):
        response.text = f"Updated resource {id}"
        
    def options(self, request, response, id):
        # Explicitly handle OPTIONS requests
        response.headers["Allow"] = "GET, PUT, OPTIONS"
        response.status_code = 204  # No Content
```

## Logging Errors

It's a good practice to log errors for debugging and monitoring. You can integrate with Python's logging module:

```python
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log'
)
logger = logging.getLogger('plinx_app')

def exception_handler(request, response, exception):
    # Log the exception with context
    logger.exception(
        f"Error handling request {request.method} {request.path}: {exception}"
    )
    
    # Set the response
    response.status_code = 500
    response.json = {"error": "An unexpected error occurred"}

app.add_exception_handler(exception_handler)
```

## Best Practices

1. **Always handle exceptions**: Never let exceptions propagate to the user without being caught and handled properly
2. **Provide useful error messages**: Make error responses informative but be careful not to expose sensitive information
3. **Use appropriate status codes**: Choose the HTTP status code that best represents the error condition
4. **Log errors with context**: Include enough information in logs to understand and reproduce the issue
5. **Consider security implications**: Don't expose sensitive details in error messages sent to clients
6. **Be consistent**: Use a consistent error response format throughout your API