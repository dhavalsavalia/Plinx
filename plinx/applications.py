from typing import Callable, Union

from webob import Request, Response

from .utils import handle_404


class Plinx:
    def __init__(self):
        self.routes = {}

    def __call__(self, environ, start_response):
        request = Request(environ)

        response = self.handle_request(request)

        return response(environ, start_response)

    def route(self, path: str):
        """
        Register a route with the given path.
        TODO: Add support for HTTP methods.
        :param path: The path to register.
        :return:
        """
        def wrapper(handler):
            self.routes[path] = handler
            return handler

        return wrapper

    def handle_request(self, request: Request):
        """
        Handle the given request and return the response.
        :param request: The request object.
        :return: The response object.
        """
        response: Response = Response()

        handler = self.find_handler(request, response)

        if handler:
            handler(request, response)

        return response

    def find_handler(
            self,
            request: Request,
            response: Response
    ) -> Union[Callable, None]:
        """
        Find the handler for the given request.
        If no handler is found, set the response status code to 404
        and return None.

        :param request: The request object.
        :param response: The response object.
        :return: The handler for the given request.
        """
        for path, handler in self.routes.items():
            if path == request.path:
                return handler

        handle_404(response)
