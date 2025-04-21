# Core Concepts

This page explains the fundamental concepts and design principles behind Plinx.

## Architecture Overview

Plinx follows the WSGI (Web Server Gateway Interface) standard, which defines a simple and universal interface between web servers and Python web applications. The architecture consists of:

- **WSGI Application**: The `Plinx` class implements the WSGI callable interface
- **Request Handling**: Converts raw WSGI environment to convenient request objects
- **Routing**: Maps URL patterns to handler functions or classes
- **Middleware**: Processes requests/responses before/after handler execution
- **Response Generation**: Converts handler output to proper HTTP responses

## The Request-Response Cycle

Here's how a typical request flows through Plinx:

1. The WSGI server calls the Plinx application with environment and start_response
2. Middleware processes the incoming request
3. The router finds the appropriate handler for the URL path
4. The handler function/method is executed with the request and response objects
5. Middleware processes the response
6. The response is returned to the WSGI server

## Routing System

The routing system in Plinx maps URL patterns to handler functions or classes. Key features include:

- **Path Parameters**: Routes can include parameters in braces like `/users/{id}`
- **Method-Specific Routes**: Decorate handlers with `@app.get()`, `@app.post()`, etc.
- **Class-Based Views**: Route to classes with methods named after HTTP methods

## Function-Based vs. Class-Based Handlers

### Function-Based Handlers

```python
@app.route("/hello")
def hello_handler(request, response):
    response.text = "Hello, World!"
```

Function-based handlers are simple and straightforward. They're ideal for:
- Simple endpoints with a single HTTP method
- Quick prototyping
- Stateless request processing

### Class-Based Handlers

```python
@app.route("/users")
class UserResource:
    def get(self, request, response):
        response.text = "List users"
        
    def post(self, request, response):
        response.text = "Create user"
```

Class-based handlers are powerful for:
- Resources that respond to multiple HTTP methods
- Organizing related endpoints
- Reusing common functionality

## Response Building

Plinx provides a clean interface for building responses:

- **Text responses**: `response.text = "Hello, World!"`
- **JSON responses**: `response.json = {"key": "value"}`
- **Status codes**: `response.status_code = 200`
- **Custom headers**: `response.headers["X-Custom"] = "Value"`

## Middleware

Middleware allows you to process requests and responses globally:

```python
class SimpleMiddleware(Middleware):
    def process_request(self, request):
        # Process before request reaches handler
        request.middleware_was_here = True
        
    def process_response(self, request, response):
        # Process after handler generates response
        response.headers["X-Processed-By"] = "SimpleMiddleware"
```

Common middleware use cases:
- Authentication and authorization
- Logging
- CORS handling
- Request/response transformation

## Design Principles

Plinx was built with the following principles in mind:

1. **Simplicity**: Clean API without unnecessary complexity
2. **Explicitness**: Clear and readable code with minimal "magic"
3. **Lightweight**: Small core with minimal dependencies
4. **Extensibility**: Easy to extend and customize
5. **Educational Value**: Clear implementation for learning purposes

These principles guide the development of Plinx and inform its design decisions.