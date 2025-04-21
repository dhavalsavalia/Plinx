# HTTP Methods API

The `methods` module defines constants and helper functions for handling HTTP methods in Plinx applications. This module provides a clean way to work with HTTP methods throughout your application.

## HTTP Method Constants

::: plinx.methods.HTTPMethods
    handler: python
    rendering:
      show_source: true
      show_root_heading: true
      show_if_no_docstring: false

## Method Handling Functions

::: plinx.methods.is_valid_method
    handler: python
    rendering:
      show_source: true
      show_root_heading: true
      show_if_no_docstring: false

::: plinx.methods.get_handler_name_for_method
    handler: python
    rendering:
      show_source: true
      show_root_heading: true
      show_if_no_docstring: false

## Examples

### Checking for Valid HTTP Methods

```python
from plinx.methods import is_valid_method

# Check if a method is supported
if is_valid_method("GET"):
    print("GET is a valid HTTP method")
    
if not is_valid_method("CUSTOM"):
    print("CUSTOM is not a valid HTTP method")
```

### Working with HTTP Method Constants

```python
from plinx import Plinx
from plinx.methods import HTTPMethods

app = Plinx()

@app.route("/example")
def handler(request, response):
    if request.method == HTTPMethods.GET:
        response.text = "This is a GET request"
    elif request.method == HTTPMethods.POST:
        response.text = "This is a POST request"
    else:
        response.text = f"This is a {request.method} request"
```

### Finding Handler Method Names

```python
from plinx.methods import get_handler_name_for_method

# For class-based views, this function maps HTTP methods to method names
handler_name = get_handler_name_for_method("GET")  # Returns "get"
handler_name = get_handler_name_for_method("POST")  # Returns "post"
```

## Method Handling in Class-Based Views

In class-based views, HTTP methods are automatically mapped to methods with lowercase names:

```python
from plinx import Plinx

app = Plinx()

@app.route("/resource")
class ResourceHandler:
    def get(self, request, response):
        response.text = "Handling GET request"
        
    def post(self, request, response):
        response.text = "Handling POST request"
        
    def put(self, request, response):
        response.text = "Handling PUT request"
        
    def delete(self, request, response):
        response.text = "Handling DELETE request"
        
    def patch(self, request, response):
        response.text = "Handling PATCH request"
        
    def head(self, request, response):
        # HEAD requests don't return a body
        pass
        
    def options(self, request, response):
        response.headers["Allow"] = "GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS"
```

When a request comes in, Plinx will call the appropriate method based on the HTTP method of the request.

## Custom Method Handlers

You can implement custom method handling by overriding the default behavior:

```python
from plinx import Plinx
from plinx.methods import get_handler_name_for_method

# Custom function to map HTTP methods to handler names
def custom_method_mapper(method):
    method_map = {
        "GET": "handle_get",
        "POST": "handle_post",
        "PUT": "handle_put",
        "DELETE": "handle_delete"
    }
    return method_map.get(method, "handle_default")

app = Plinx()

@app.route("/custom")
class CustomMethodHandler:
    def handle_get(self, request, response):
        response.text = "Custom GET handler"
        
    def handle_post(self, request, response):
        response.text = "Custom POST handler"
        
    def handle_put(self, request, response):
        response.text = "Custom PUT handler"
        
    def handle_delete(self, request, response):
        response.text = "Custom DELETE handler"
        
    def handle_default(self, request, response):
        response.text = f"Default handler for {request.method}"
        
    # Override the default method handling
    def __getattr__(self, name):
        if name == get_handler_name_for_method(request.method):
            # Use our custom mapper instead
            handler_name = custom_method_mapper(request.method)
            return getattr(self, handler_name)
        raise AttributeError(f"{self.__class__.__name__} has no attribute {name}")
```

## Method Not Allowed Handling

Plinx automatically handles requests with methods not supported by your handler:

```python
from plinx import Plinx

app = Plinx()

@app.route("/limited")
class LimitedHandler:
    def get(self, request, response):
        response.text = "GET is allowed"
    
    # No other methods defined
    # POST, PUT, etc. will receive a 405 Method Not Allowed response

# For function handlers, the default behavior allows all methods
@app.route("/allow-all")
def all_methods_handler(request, response):
    response.text = f"Handling {request.method} request"
```

## Method Override

Sometimes it's useful to override the HTTP method, especially when working with HTML forms that only support GET and POST:

```python
from plinx import Plinx
from plinx.middleware import Middleware

class MethodOverrideMiddleware(Middleware):
    def process_request(self, request):
        # Check for X-HTTP-Method-Override header
        override = request.headers.get("X-HTTP-Method-Override")
        
        # Check for _method form field (common in HTML forms)
        if not override and request.method == "POST":
            override = request.POST.get("_method")
            
        # Override the method if specified
        if override and override.upper() in ["PUT", "DELETE", "PATCH"]:
            request.method = override.upper()

app = Plinx()
app.add_middleware(MethodOverrideMiddleware)
```

This allows HTML forms to simulate PUT, DELETE, and PATCH requests by including a form field named `_method` or by setting the `X-HTTP-Method-Override` header.

## Best Practices

1. **Use HTTP methods semantically**: Follow RESTful conventions (GET for retrieval, POST for creation, etc.)
2. **Handle OPTIONS requests**: Especially important for CORS support
3. **Return appropriate status codes**: 405 Method Not Allowed for unsupported methods
4. **Support idempotent methods**: GET, PUT, and DELETE should be idempotent
5. **Consider method overrides**: If supporting HTML forms that can only use GET and POST
6. **Document supported methods**: Make it clear which methods are supported by each endpoint