import inspect
from typing import Callable, Dict, Iterable, Tuple
from wsgiref.types import StartResponse, WSGIEnvironment

from parse import parse
from requests import Session as RequestsSession
from webob import Request, Response
from wsgiadapter import WSGIAdapter as RequestsWSGIAdapter

from .methods import HTTPMethods
from .middleware import Middleware
from .status_codes import StatusCodes
from .utils import handle_404


class Plinx:
    def __init__(self):
        self.routes: Dict[str, Tuple[HTTPMethods, Callable]] = {}
        self.exception_handler = None
        self.middleware = Middleware(self)

        self._method_decorators = {}
        for method in HTTPMethods:
            self._method_decorators[method.name.lower()] = (
                self._create_method_decorator(method)
            )

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
        return self.middleware(environ, start_response)

    def add_route(
        self,
        path: str,
        handler: Callable,
        method: HTTPMethods = HTTPMethods.GET,
    ):
        """
        Add a route to the application. Django-like syntax.
        :param path: The path to register.
        :param handler: The handler to register.
        :return:
        """
        if path in self.routes:
            raise RuntimeError(f"Route '{path}' is already registered.")

        self.routes[path] = (method, handler)

    def route(
        self,
        path: str,
    ):
        """
        Register a route with the given path.
        :param path: The path to register.
        :return:
        """

        def wrapper(handler):
            self.add_route(path, handler)
            return handler

        return wrapper

    def __getattr__(
        self,
        name: str,
    ):
        """Allow access to HTTP method decorators like app.get, app.post etc."""
        if name in self._method_decorators:
            return self._method_decorators[name]
        raise RuntimeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'"
        )

    def _create_method_decorator(self, method: HTTPMethods):
        """
        Creates a decorator for registering routes with a specific HTTP method.
        :param method: The HTTP method enum value
        :return: Decorator function
        """

        def decorator(path: str):
            def wrapper(handler):
                self.add_route(path, handler, method)
                return handler

            return wrapper

        return decorator

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

        handler_definition, kwargs = self.find_handler(request, response)

        try:
            if handler_definition is not None:
                method, handler = handler_definition

                # Handle CBVs
                if inspect.isclass(handler):
                    handler = getattr(
                        handler(),
                        request.method.lower(),
                        None,
                    )
                    # only allow methods that are defined in the class
                    if handler is None:
                        response.status_code = StatusCodes.METHOD_NOT_ALLOWED.value
                        response.text = "Method Not Allowed"
                        return response

                if inspect.isfunction(handler):
                    # Handle function-based views
                    if request.method != method.value:
                        response.status_code = StatusCodes.METHOD_NOT_ALLOWED.value
                        response.text = "Method Not Allowed"
                        return response

                handler(request, response, **kwargs)

        except Exception as e:
            if self.exception_handler:
                self.exception_handler(request, response, e)
            else:
                response.status_code = StatusCodes.INTERNAL_SERVER_ERROR.value
                response.text = str(e)

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

    def add_exception_handler(
        self,
        exception_handler,
    ):
        self.exception_handler = exception_handler

    def add_middleware(
        self,
        middleware_cls: type[Middleware],
    ):
        """
        Add a middleware class to the application.
        :param middleware_cls: The middleware class to add.
        """
        self.middleware.add(middleware_cls)

    def test_session(self, base_url="http://testserver"):
        session = RequestsSession()
        session.mount(prefix=base_url, adapter=RequestsWSGIAdapter(self))
        return session
