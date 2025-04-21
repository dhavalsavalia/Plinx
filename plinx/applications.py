import inspect
from typing import Callable, Dict, Iterable, Tuple
from wsgiref.types import StartResponse, WSGIEnvironment

from parse import parse
from requests import Session as RequestsSession
from webob import Request
from wsgiadapter import WSGIAdapter as RequestsWSGIAdapter

from .methods import HTTPMethods
from .middleware import Middleware
from .response import PlinxResponse as Response
from .status_codes import StatusCodes
from .utils import handle_404


class Plinx:
    """
    The main application class for the Plinx web framework.

    This class serves as the WSGI application entry point and manages routes,
    middleware, and request handling. It provides a Flask-like decorator syntax
    for adding routes and Django-like method for explicitly registering them.

    Examples:
        Creating a simple app with a route:

        ```python
        from plinx import Plinx

        app = Plinx()

        @app.route("/")
        def home(request, response):
            response.text = "Hello, World!"
        ```

        Using HTTP method-specific decorators:

        ```python
        @app.get("/users")
        def list_users(request, response):
            response.json = {"users": ["user1", "user2"]}

        @app.post("/users")
        def create_user(request, response):
            response.text = "User created"
        ```

        Using class-based views:

        ```python
        @app.route("/books")
        class BooksResource:
            def get(self, request, response):
                response.text = "List of books"

            def post(self, request, response):
                response.text = "Book created"
        ```
    """

    def __init__(self):
        """
        Initialize a new Plinx application instance.

        Sets up the routing table, middleware stack, and
        dynamically generates HTTP method-specific decorators.
        """
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
        WSGI entry point for the application.

        This method makes the Plinx instance callable as required by the WSGI spec,
        allowing it to be used directly with WSGI servers like Gunicorn or uWSGI.

        Args:
            environ: The WSGI environment dictionary containing request information
            start_response: The WSGI start_response callable

        Returns:
            An iterable of bytes representing the response body
        """
        return self.middleware(environ, start_response)

    def add_route(
        self,
        path: str,
        handler: Callable,
        method: HTTPMethods = HTTPMethods.GET,
    ):
        """
        Explicitly register a route with the application.

        This provides a Django-like syntax for registering routes,
        as an alternative to the decorator approach.

        Args:
            path: URL pattern to match (may contain parameters)
            handler: Function or class to handle matching requests
            method: HTTP method to match (defaults to GET)

        Raises:
            RuntimeError: If the path is already registered

        Example:
            ```python
            def home(request, response):
                response.text = "Hello, World!"

            app.add_route("/home", home)
            ```
        """
        if path in self.routes:
            raise RuntimeError(f"Route '{path}' is already registered.")

        self.routes[path] = (method, handler)

    def route(
        self,
        path: str,
    ):
        """
        Register a route via decorator syntax.

        This implements Flask-like syntax for registering routes. It can be used
        with both function-based handlers and class-based handlers.

        Args:
            path: URL pattern to match (may contain parameters)

        Returns:
            A decorator function that registers the handler

        Example:
            ```python
            @app.route("/home")
            def home(request, response):
                response.text = "Hello, World!"
            ```

            For class-based views:

            ```python
            @app.route("/books")
            class BooksResource:
                def get(self, request, response):
                    response.text = "List of books"
            ```
        """

        def wrapper(handler):
            self.add_route(path, handler)
            return handler

        return wrapper

    def __getattr__(
        self,
        name: str,
    ):
        """
        Enable HTTP method-specific decorators like app.get, app.post, etc.

        This magic method is called when an attribute lookup fails, allowing
        us to dynamically provide HTTP method decorators.

        Args:
            name: The attribute name being looked up

        Returns:
            A method-specific decorator function if name matches a HTTP method

        Raises:
            RuntimeError: If the attribute doesn't match a known HTTP method
        """
        if name in self._method_decorators:
            return self._method_decorators[name]
        raise RuntimeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'"
        )

    def _create_method_decorator(self, method: HTTPMethods):
        """
        Create a decorator for a specific HTTP method.

        This internal method generates the decorators used for HTTP method-specific
        route registration like @app.get(), @app.post(), etc.

        Args:
            method: The HTTP method enum value

        Returns:
            A decorator function for the specified HTTP method
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
        Process an incoming request and generate a response.

        This is the core request handling logic that finds a matching route handler,
        executes it, and handles any exceptions.

        Args:
            request: The incoming WebOb Request object

        Returns:
            A Response object containing the response data
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
    ) -> Tuple[Tuple[HTTPMethods, Callable] | None, dict | None]:
        """
        Find the appropriate handler for a request based on URL path matching.

        This method iterates through registered routes and uses the parse library
        to match URL patterns and extract parameters.

        Args:
            request: The incoming WebOb Request object
            response: The Response object being built

        Returns:
            A tuple containing:
                - The handler definition (method, handler) if found, or None
                - A dictionary of extracted URL parameters, or None
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
        """
        Register a global exception handler for the application.

        The exception handler will be called whenever an uncaught exception
        occurs during request handling.

        Args:
            exception_handler: Callable that takes (request, response, exception)

        Example:
            ```python
            def handle_exceptions(request, response, exception):
                response.status_code = 500
                response.text = f"Error: {str(exception)}"

            app.add_exception_handler(handle_exceptions)
            ```
        """
        self.exception_handler = exception_handler

    def add_middleware(
        self,
        middleware_cls: type[Middleware],
    ):
        """
        Add a middleware class to the application's middleware stack.

        Middleware classes must inherit from the Middleware base class and can
        process requests before they reach handlers and responses before they're returned.

        Args:
            middleware_cls: A class inheriting from Middleware

        Example:
            ```python
            class SimpleMiddleware(Middleware):
                def process_request(self, request):
                    print("Processing request")

                def process_response(self, request, response):
                    print("Processing response")

            app.add_middleware(SimpleMiddleware)
            ```
        """
        self.middleware.add(middleware_cls)

    def test_session(self, base_url="http://testserver"):
        """
        Create a test client session for this application.

        This provides an interface similar to the requests library for testing
        your application without making actual HTTP calls.

        Args:
            base_url: Base URL to use for requests (default: "http://testserver")

        Returns:
            A requests.Session object configured to call this application

        Example:
            ```python
            client = app.test_session()
            response = client.get("/home")
            assert response.status_code == 200
            ```
        """
        session = RequestsSession()
        session.mount(prefix=base_url, adapter=RequestsWSGIAdapter(self))
        return session
