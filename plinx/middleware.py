from webob import Request, Response


class Middleware:
    """
    Middleware base class for all middleware classes.
    This class is used to create middleware for the Plinx application.
    Middleware classes should inherit from this class and implement the
    `process_request` and `process_response` methods.
    """

    def __init__(
        self,
        app,
    ):
        """
        Middleware base class for all middleware classes.
        :param app: The WSGI application.
        """
        self.app = app

    def __call__(
        self,
        environ: dict,
        start_response: callable,
    ):
        """
        Entrypoint for the WSGI middleware since it is now entrypoint for the WSGI application.
        :param environ: The WSGI environment.
        :param start_response: The WSGI callable.
        :return: The response body.
        """
        request = Request(environ)

        response = self.app.handle_request(request)

        return response(environ, start_response)

    def add(
        self,
        middleware_cls,
    ):
        """
        Add a middleware class to the application.
        :param middleware_cls: The middleware class to add.
        """
        self.app = middleware_cls(self.app)

    def process_request(
        self,
        request: Request,
    ):
        """
        Process the request before it is passed to the application.
        :param request: The request object.
        """
        pass

    def process_response(
        self,
        request: Request,
        response: Response,
    ):
        """
        Process the response after it is passed to the application.
        :param request: The request object.
        :param response: The response object.
        """
        pass

    def handle_request(self, request: Request):
        """
        Handle the incoming request.
        :param request: The request object.
        :return: The response object.
        """
        self.process_request(request)
        response = self.app.handle_request(request)
        self.process_response(request, response)

        return response
