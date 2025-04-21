# Response API

The `response` module provides the `PlinxResponse` class, which handles HTTP response generation in Plinx applications. This class offers a simple interface for setting response content, status codes, and headers.

## PlinxResponse Class

::: plinx.response.PlinxResponse
    handler: python
    selection:
      members:
        - __init__
        - __call__
        - set_body_and_content_type
    rendering:
      show_source: true
      show_root_heading: true
      show_if_no_docstring: false

## Examples

### Text Responses

```python
@app.route("/hello")
def hello(request, response):
    response.text = "Hello, World!"
    response.status_code = 200  # Optional, defaults to 200
```

### JSON Responses

```python
@app.route("/api/data")
def get_data(request, response):
    response.json = {
        "name": "Plinx",
        "version": "1.0.0",
        "features": ["routing", "middleware", "orm"]
    }
    # Content-Type is automatically set to application/json
```

### Custom Status Codes

```python
from plinx.status_codes import StatusCodes

@app.route("/not-found")
def not_found(request, response):
    response.text = "Resource not found"
    response.status_code = StatusCodes.NOT_FOUND.value  # 404
```

### Setting Headers

```python
@app.route("/download")
def download(request, response):
    response.text = "File content goes here"
    response.headers["Content-Type"] = "text/plain"
    response.headers["Content-Disposition"] = "attachment; filename=sample.txt"
```

### Binary Responses

```python
@app.route("/image")
def get_image(request, response):
    with open("image.png", "rb") as f:
        response.body = f.read()
    response.content_type = "image/png"
```

## Response Properties

| Property | Type | Description |
|----------|------|-------------|
| `text` | `str` | Text content of the response (sets content type to "text/plain") |
| `json` | `Any` | JSON-serializable content (sets content type to "application/json") |
| `body` | `bytes` | Raw response body as bytes |
| `content_type` | `str` | MIME type of the response (e.g., "text/html", "application/json") |
| `status_code` | `int` | HTTP status code (default: 200) |
| `headers` | `dict` | Dictionary of HTTP headers |

## Content Type Handling

The `PlinxResponse` class automatically sets the Content-Type header based on how you set the response content:

1. If you set `response.json`, the content type is set to "application/json"
2. If you set `response.text`, the content type is set to "text/plain"
3. If you set `response.body` directly, you should also set `response.content_type` manually

## Internal Workflow

When a response is being prepared to be sent back to the client:

1. The `set_body_and_content_type()` method is called to ensure the response body and headers are properly prepared
2. The response is converted to a WebOb Response object
3. The WebOb Response handles the actual WSGI response generation

## Custom Response Classes

If you need to extend the `PlinxResponse` class with additional functionality, you can create a subclass:

```python
from plinx.response import PlinxResponse

class HTMLResponse(PlinxResponse):
    def set_html(self, html_content):
        self.body = html_content.encode("utf-8")
        self.content_type = "text/html"
        
    def render_template(self, template_name, **context):
        # Simple template rendering example
        with open(f"templates/{template_name}.html") as f:
            template = f.read()
        
        # Very basic template substitution
        for key, value in context.items():
            template = template.replace(f"{{{{{key}}}}}", str(value))
            
        self.set_html(template)
```

To use your custom response class, you would need to modify your application to create instances of your class instead of the standard `PlinxResponse`.