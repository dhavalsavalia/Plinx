import json
from typing import Iterable
from wsgiref.types import StartResponse, WSGIEnvironment

from webob import Response as WebObResponse


class PlinxResponse:
    def __init__(self):
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
        Entrypoint for the WSGI application.
        :param environ: The WSGI environment.
        :param start_response: The WSGI callable.
        :return: The response body produced by the middleware.
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
        if self.json is not None:
            self.body = json.dumps(self.json).encode("UTF-8")
            self.content_type = "application/json"
        elif self.text is not None:
            self.body = self.text.encode("utf-8") if isinstance(self.text, str) else self.text
            self.content_type = "text/plain"

        if self.content_type is not None:
            self.headers["Content-Type"] = self.content_type