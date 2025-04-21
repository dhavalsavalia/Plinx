# Responses

Plinx provides a flexible response system that makes it easy to return different types of content to clients. This guide explains how to work with response objects and demonstrates various response techniques.

## Response Object

The response object in Plinx is an instance of `plinx.response.PlinxResponse` that is passed to every handler. It provides methods and properties for setting response data, status codes, and headers:

```python
@app.route("/example")
def handler(request, response):
    response.text = "Hello, World!"
    response.status_code = 200
    response.headers["X-Custom-Header"] = "Value"
```

## Common Response Properties

The response object provides several properties for working with different content types:

| Property | Description |
| --- | --- |
| `response.text` | Set response body as plain text |
| `response.json` | Set response body from a JSON-serializable object |
| `response.body` | Set raw response body as bytes |
| `response.content_type` | Set the Content-Type header |
| `response.status_code` | Set the HTTP status code |
| `response.headers` | Dictionary-like object for setting HTTP headers |

## Text Responses

The simplest way to send a response is to set the `text` property:

```python
@app.route("/text")
def text_handler(request, response):
    response.text = "This is a plain text response"
    # Content-Type is automatically set to text/plain
```

## JSON Responses

Setting the `json` property automatically serializes the data and sets the appropriate content type:

```python
@app.route("/json")
def json_handler(request, response):
    response.json = {
        "message": "Success",
        "data": {
            "items": [1, 2, 3],
            "total": 3
        }
    }
    # Content-Type is automatically set to application/json
```

The JSON serialization handles various Python types:

```python
@app.route("/complex-json")
def complex_json_handler(request, response):
    from datetime import datetime
    
    response.json = {
        "string": "Hello",
        "number": 42,
        "float": 3.14,
        "boolean": True,
        "none": None,
        "list": [1, 2, 3],
        "dict": {"key": "value"},
        "date": datetime.now()  # Will be converted to ISO format string
    }
```

## Status Codes

HTTP status codes indicate the result of the request. Plinx provides a `status_codes` module with constants for common codes:

```python
from plinx import Plinx
from plinx.status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND

app = Plinx()

@app.route("/success")
def success_handler(request, response):
    response.status_code = HTTP_200_OK
    response.json = {"message": "Success"}

@app.route("/created")
def created_handler(request, response):
    response.status_code = HTTP_201_CREATED
    response.json = {"message": "Resource created"}

@app.route("/not-found")
def not_found_handler(request, response):
    response.status_code = HTTP_404_NOT_FOUND
    response.json = {"error": "Resource not found"}
```

## Setting Headers

HTTP headers provide additional information about the response:

```python
@app.route("/headers")
def headers_handler(request, response):
    response.text = "Response with custom headers"
    
    # Set individual headers
    response.headers["X-Custom-Header"] = "Value"
    response.headers["Cache-Control"] = "no-cache"
    
    # Set Content-Type explicitly
    response.content_type = "text/plain; charset=utf-8"
```

## Binary Responses

For binary data, use the `body` property with bytes:

```python
@app.route("/binary")
def binary_handler(request, response):
    # Create some binary data
    binary_data = b"\x00\x01\x02\x03\x04"
    
    response.body = binary_data
    response.content_type = "application/octet-stream"
```

## File Downloads

You can serve files for download:

```python
import os

@app.route("/download")
def download_handler(request, response):
    # Read a file
    file_path = os.path.join(os.path.dirname(__file__), "files/document.pdf")
    
    with open(file_path, "rb") as f:
        file_data = f.read()
    
    # Set response
    response.body = file_data
    response.content_type = "application/pdf"
    
    # Set headers for download
    filename = os.path.basename(file_path)
    response.headers["Content-Disposition"] = f'attachment; filename="{filename}"'
    response.headers["Content-Length"] = str(len(file_data))
```

## HTML Responses

For HTML content, set the appropriate content type:

```python
@app.route("/html")
def html_handler(request, response):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Plinx Example</title>
    </head>
    <body>
        <h1>Hello from Plinx</h1>
        <p>This is an HTML response.</p>
    </body>
    </html>
    """
    
    response.text = html
    response.content_type = "text/html"
```

## Redirects

To redirect the client to another URL:

```python
@app.route("/redirect")
def redirect_handler(request, response):
    # Set status code for redirect
    response.status_code = 302  # or 301 for permanent redirect
    
    # Set the Location header
    response.headers["Location"] = "/target-url"
    
    # Optional message
    response.text = "Redirecting..."
```

## Error Responses

For error responses, it's good practice to return a consistent format:

```python
@app.route("/error")
def error_handler(request, response):
    response.status_code = 500
    response.json = {
        "error": {
            "code": "INTERNAL_ERROR",
            "message": "An unexpected error occurred",
            "details": "Database connection failed"
        }
    }
```

## Content Negotiation

You can implement content negotiation to return different formats based on the `Accept` header:

```python
@app.route("/negotiate")
def negotiate_handler(request, response):
    data = {"name": "Example", "value": 42}
    
    # Get the Accept header
    accept = request.headers.get("Accept", "")
    
    if "application/xml" in accept:
        # Return XML
        xml = f"<data><name>{data['name']}</name><value>{data['value']}</value></data>"
        response.text = xml
        response.content_type = "application/xml"
    else:
        # Default to JSON
        response.json = data
```

## Streaming Responses

For large responses, you might want to stream the data:

```python
@app.route("/stream")
def stream_handler(request, response):
    def generate_large_data():
        for i in range(1000):
            yield f"Line {i}\n".encode()
    
    # Set streaming response
    response.body_iter = generate_large_data()
    response.content_type = "text/plain"
```

## Cookies

Setting cookies in the response:

```python
@app.route("/cookies")
def cookie_handler(request, response):
    # Set a simple cookie
    response.set_cookie("session", "abc123")
    
    # Set a cookie with additional parameters
    response.set_cookie(
        "user_id",
        "123",
        max_age=3600,  # 1 hour
        path="/",
        secure=True,
        httponly=True,
        samesite="Lax"
    )
    
    response.text = "Cookies set"
```

## CORS Headers

For cross-origin requests, you'll need to add appropriate CORS headers:

```python
@app.route("/api/data")
def cors_handler(request, response):
    # Add CORS headers
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    
    # Handle preflight OPTIONS request
    if request.method == "OPTIONS":
        response.text = ""
        return
    
    # Regular response
    response.json = {"message": "CORS-enabled endpoint"}
```

## Response Templates

For complex responses, you might want to create a helper function:

```python
def create_api_response(data=None, error=None, meta=None, status_code=200):
    """Create a consistent API response structure."""
    response_data = {
        "data": data or {},
        "error": error,
        "meta": meta or {},
        "timestamp": datetime.now().isoformat()
    }
    
    if error:
        if not status_code or status_code < 400:
            status_code = 400
    
    return response_data, status_code

@app.route("/api/users")
def users_handler(request, response):
    try:
        user_data = {"id": 1, "name": "John Doe"}
        response_data, status_code = create_api_response(
            data=user_data,
            meta={"version": "1.0"}
        )
        
        response.json = response_data
        response.status_code = status_code
        
    except Exception as e:
        response_data, status_code = create_api_response(
            error={"message": str(e), "type": type(e).__name__},
            status_code=500
        )
        
        response.json = response_data
        response.status_code = status_code
```

## Best Practices

1. **Be consistent**: Use a consistent format for your API responses
2. **Use appropriate status codes**: Follow HTTP standard conventions
3. **Set correct content types**: Make sure the Content-Type matches your content
4. **Handle errors gracefully**: Return meaningful error messages
5. **Consider content negotiation**: Support different formats based on client needs
6. **Manage response size**: Consider pagination for large data sets
7. **Document your API**: Include examples of response formats in your API documentation
8. **Follow security practices**: Set appropriate security headers and cookie flags

By following these practices, you can create clear and consistent responses in your Plinx applications.