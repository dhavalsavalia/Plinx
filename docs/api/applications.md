# Applications API

The `applications` module contains the core `Plinx` class, which is the main entry point for creating Plinx web applications.

## Plinx Class

::: plinx.applications.Plinx
    handler: python
    selection:
      members:
        - __init__
        - __call__
        - add_route
        - route
        - handle_request
        - find_handler
        - add_exception_handler
        - add_middleware
        - test_session
    rendering:
      show_source: true
      show_root_heading: true
      show_if_no_docstring: false

## Example Usage

### Basic Application

```python
from plinx import Plinx

app = Plinx()

@app.route("/")
def home(request, response):
    response.text = "Hello, World!"
    
@app.route("/about")
def about(request, response):
    response.text = "About page"
```

### HTTP Method-Specific Routes

```python
@app.get("/api/items")
def get_items(request, response):
    response.json = {"items": ["item1", "item2"]}
    
@app.post("/api/items")
def create_item(request, response):
    response.text = "Item created"
    response.status_code = 201  # Created
```

### Dynamic Route Parameters

```python
@app.route("/users/{user_id}")
def get_user(request, response, user_id):
    response.json = {"user_id": user_id, "name": f"User {user_id}"}
```

### Class-Based Views

```python
@app.route("/resources")
class ResourceHandler:
    def get(self, request, response):
        response.json = {"resources": ["res1", "res2"]}
        
    def post(self, request, response):
        response.text = "Resource created"
        response.status_code = 201
```

### Adding Middleware

```python
from plinx.middleware import Middleware

class LoggingMiddleware(Middleware):
    def process_request(self, request):
        print(f"Request: {request.method} {request.path}")
        
    def process_response(self, request, response):
        print(f"Response: {response.status_code}")

app = Plinx()
app.add_middleware(LoggingMiddleware)
```

### Exception Handling

```python
def exception_handler(request, response, exception):
    response.status_code = 500
    response.json = {
        "error": str(exception),
        "type": exception.__class__.__name__
    }
    
app = Plinx()
app.add_exception_handler(exception_handler)
```

### Running with a WSGI Server

```python
# app.py
from plinx import Plinx

app = Plinx()

@app.route("/")
def home(request, response):
    response.text = "Hello, World!"
```

```bash
# Run with a WSGI server like Gunicorn
gunicorn app:app
```

### Testing

```python
app = Plinx()

@app.route("/")
def home(request, response):
    response.text = "Hello, World!"

# Create a test client
client = app.test_session()

# Make requests
response = client.get("/")
assert response.text == "Hello, World!"
assert response.status_code == 200
```