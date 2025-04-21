import json
from typing import Iterable
from wsgiref.types import StartResponse, WSGIEnvironment

from webob import Response as WebObResponse


class PlinxResponse:
    """
    Response class for the Plinx web framework.

    This class provides a simple interface for constructing HTTP responses,
    with high-level helpers for common response types like JSON and plain text.
    It wraps WebOb's Response for actual WSGI compliance and output generation.

    The class provides multiple ways to set response content:

    1. Set the `text` attribute for plain text responses
    2. Set the `json` attribute for JSON responses
    3. Set the `body` attribute directly for binary data

    It also allows setting status codes, content types, and custom headers.

    Examples:
        Plain text response:
        ```python
        def handler(request, response):
            response.text = "Hello, World!"
            response.status_code = 200  # Optional, defaults to 200
        ```

        JSON response:
        ```python
        def handler(request, response):
            response.json = {"message": "Hello, World!"}
            # Content-Type will automatically be set to application/json
        ```

        Custom headers:
        ```python
        def handler(request, response):
            response.text = "Not Found"
            response.status_code = 404
            response.headers["X-Custom-Header"] = "Value"
        ```
    """

    def __init__(self):
        """
        Initialize a new response object.

        Sets up default values for the response attributes:
        - json: None (will be serialized to JSON if set)
        - text: None (will be encoded to UTF-8 if set)
        - content_type: None (will be set based on response type)
        - body: Empty bytes (raw response body)
        - status_code: 200 (OK)
        - headers: Empty dict (custom HTTP headers)
        """
        self.json = None
        self.text = None
        self.content_type = None
        self.body = b""
        self.status_code = 200
        self.headers = {}

    def __call__(
        self,
        environ: WSGIEnvironment,
        start_response: StartResponse,
    ) -> Iterable[bytes]:
        """
        WSGI callable interface for the response.

        This makes the response object act as a WSGI application,
        which is required for compatibility with WSGI servers.
        It delegates the actual WSGI handling to WebOb's Response.

        Args:
            environ: The WSGI environment dictionary
            start_response: The WSGI start_response callable

        Returns:
            An iterable of bytes representing the response body
        """

        self.set_body_and_content_type()

        response = WebObResponse(
            body=self.body,
            content_type=self.content_type,
            status=self.status_code,
            headers=self.headers,
        )
        return response(environ, start_response)

    def set_body_and_content_type(self):
        """
        Prepare the response body and content type based on the response attributes.

        This method is called automatically before the response is returned.
        It handles the conversion of high-level response attributes (`json`, `text`)
        into the raw response body and appropriate content type.

        The priority order is:
        1. If `json` is set, encode it as JSON and set content_type to application/json
        2. If `text` is set, encode it as UTF-8 and set content_type to text/plain
        3. Otherwise, use the existing `body` and `content_type`
        """
        if self.json is not None:
            self.body = json.dumps(self.json).encode("UTF-8")
            self.content_type = "application/json"
        elif self.text is not None:
            self.body = (
                self.text.encode("utf-8") if isinstance(self.text, str) else self.text
            )
            self.content_type = "text/plain"

        if self.content_type is not None:
            self.headers["Content-Type"] = self.content_type
