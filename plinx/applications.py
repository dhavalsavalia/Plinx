from typing import Callable, Dict, Iterable, Tuple
from wsgiref.types import StartResponse, WSGIEnvironment

from parse import parse
from webob import Request, Response

from .utils import handle_404


class Plinx:
    def __init__(self):
        self.routes: Dict[str, Callable] = {}

    def __call__(
        self,
        environ: WSGIEnvironment,
        start_response: StartResponse,
    ) -> Iterable[bytes]:
        """
        Entrypoint for the WSGI application.
        :param environ: The WSGI environment.
        :param start_response: The WSGI callable.
        :return: The response body.
        """
        request = Request(environ)

        response = self.handle_request(request)

        return response(environ, start_response)

    def route(
        self,
        path: str,
    ):
        """
        Register a route with the given path.
        TODO: Add support for HTTP methods.
        :param path: The path to register.
        :return:
        """

        if path in self.routes:
            raise RuntimeError(f"Route '{path}' is already registered.")

        def wrapper(handler):
            self.routes[path] = handler
            return handler

        return wrapper

    def handle_request(
        self,
        request: Request,
    ) -> Response:
        """
        Handle the given request and return the response.
        :param request: The request object.
        :return: The response object.
        """
        response: Response = Response()

        handler, kwargs = self.find_handler(request, response)

        if handler is not None:
            handler(request, response, **kwargs)

        return response

    def find_handler(
        self,
        request: Request,
        response: Response,
    ) -> Tuple[Callable, dict | None] | Tuple[None, None]:
        """
        Find the handler for the given request.
        If no handler is found, set the response status code to 404
        and return None.

        :param request: The request object.
        :param response: The response object.
        :return: A tuple containing the handler and the named parameters.
        If no handler is found, return tuple[None, None].
        """
        for path, handler in self.routes.items():
            parse_result = parse(path, request.path)
            if parse_result is not None:
                return handler, parse_result.named
        
        handle_404(response)
        return None, None
