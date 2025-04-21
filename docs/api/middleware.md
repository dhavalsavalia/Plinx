# Middleware API

The `middleware` module defines the middleware system for Plinx applications. Middleware components process requests before they reach handlers and responses before they're returned to clients.

## Middleware Class

::: plinx.middleware.Middleware
    handler: python
    selection:
      members:
        - __init__
        - __call__
        - add
        - process_request
        - process_response
        - handle_request
    rendering:
      show_source: true
      show_root_heading: true
      show_if_no_docstring: false

## Custom Middleware Examples

### Simple Logging Middleware

```python
from plinx.middleware import Middleware

class LoggingMiddleware(Middleware):
    def process_request(self, request):
        print(f"Incoming request: {request.method} {request.path}")
        
    def process_response(self, request, response):
        print(f"Outgoing response: {response.status_code}")
```

### Request Timer Middleware

```python
import time
from plinx.middleware import Middleware

class TimerMiddleware(Middleware):
    def process_request(self, request):
        request.start_time = time.time()
        
    def process_response(self, request, response):
        if hasattr(request, "start_time"):
            duration = time.time() - request.start_time
            print(f"Request took {duration:.6f} seconds")
            # Add timing header
            response.headers["X-Request-Duration"] = f"{duration:.6f}"
```

### Authentication Middleware

```python
from plinx.middleware import Middleware

class AuthMiddleware(Middleware):
    def process_request(self, request):
        request.user = None
        
        # Check for authentication header
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]
            try:
                # In a real app, you'd verify the token
                user_id = self.verify_token(token)
                request.user = {"id": user_id}
            except Exception as e:
                print(f"Auth error: {str(e)}")
                
    def verify_token(self, token):
        # Simplified demo - in reality, you'd verify with your auth system
        if token == "valid_demo_token":
            return 1
        raise Exception("Invalid token")
```

### CORS Middleware

```python
from plinx.middleware import Middleware

class CORSMiddleware(Middleware):
    def __init__(self, app, allowed_origins=None):
        super().__init__(app)
        self.allowed_origins = allowed_origins or ["*"]
        
    def process_response(self, request, response):
        origin = request.headers.get("Origin", "")
        
        # Check if the origin is allowed
        if "*" in self.allowed_origins or origin in self.allowed_origins:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
            
        # Handle preflight OPTIONS requests
        if request.method == "OPTIONS":
            response.status_code = 200
            return response
```

## Using Multiple Middleware

You can add multiple middleware components to a Plinx application:

```python
from plinx import Plinx
from plinx.middleware import Middleware

class Middleware1(Middleware):
    def process_request(self, request):
        print("Middleware 1: process_request")
        
    def process_response(self, request, response):
        print("Middleware 1: process_response")

class Middleware2(Middleware):
    def process_request(self, request):
        print("Middleware 2: process_request")
        
    def process_response(self, request, response):
        print("Middleware 2: process_response")

app = Plinx()

# Order matters! Middleware1 will be called before Middleware2 for requests,
# but after Middleware2 for responses
app.add_middleware(Middleware1)
app.add_middleware(Middleware2)
```

This will produce the following execution order for a request:
1. Middleware1.process_request
2. Middleware2.process_request
3. Handler processes the request
4. Middleware2.process_response
5. Middleware1.process_response

## Short-Circuiting Requests

A middleware can short-circuit the request processing by returning a response:

```python
from plinx.middleware import Middleware
from plinx.status_codes import StatusCodes

class AuthRequiredMiddleware(Middleware):
    def process_request(self, request):
        auth_header = request.headers.get("Authorization", "")
        
        # If no auth header, short-circuit the request
        if not auth_header:
            # Need to access the app to create a response
            response = self.app.handle_request(request)
            response.status_code = StatusCodes.UNAUTHORIZED.value
            response.json = {"error": "Authentication required"}
            return response  # Short-circuit
```

## Error Handling in Middleware

```python
from plinx.middleware import Middleware
from plinx.status_codes import StatusCodes

class ErrorCatchingMiddleware(Middleware):
    def process_request(self, request):
        try:
            # Normal request processing
            pass
        except Exception as e:
            print(f"Request error: {str(e)}")
            
    def process_response(self, request, response):
        # You can modify the response based on conditions
        if response.status_code >= 500:
            response.json = {
                "error": "An internal error occurred",
                "status_code": response.status_code
            }
            # Log the error
            print(f"Server error occurred: {response.status_code}")
```