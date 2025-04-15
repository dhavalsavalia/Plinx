import pytest

from plinx import Plinx
from plinx.middleware import Middleware


@pytest.fixture
def app():
    return Plinx()


@pytest.fixture
def client(app):
    return app.test_session()


class TestFlaskLikeApplication:
    def test_app_object(self, app):
        assert app.routes == {}
        assert app is not None

    def test_route_decorator(self, app):
        @app.route("/home")
        def home(request, response):
            response.text = "Hello, World!"

        assert app.routes["/home"] == home

    def test_404_response(self, client):
        response = client.get("http://testserver/not-found")
        assert response.status_code == 404
        assert response.text == "Not Found"

    def test_parameterized_route(self, app, client):
        @app.route("/hello/{name}")
        def hello(request, response, name):
            response.text = f"Hello, {name}!"

        response = client.get("http://testserver/hello/Dhaval")
        assert response.status_code == 200
        assert response.text == "Hello, Dhaval!"

    def test_duplicate_route(self, app):
        @app.route("/duplicate")
        def handler1(request, response):
            response.text = "First"

        with pytest.raises(RuntimeError) as excinfo:

            @app.route("/duplicate")
            def handler2(request, response):
                response.text = "Second"

        assert isinstance(excinfo.value, RuntimeError)
        assert "Route '/duplicate' is already registered." == str(excinfo.value)

    def test_class_based_route(self, app, client):
        @app.route("/book")
        class BooksResource:
            def get(self, req, resp):
                resp.text = "Books Page"

            def post(self, req, resp):
                resp.text = "Endpoint to create a book"

        response = client.get("http://testserver/book")
        assert response.status_code == 200
        assert response.text == "Books Page"
        response = client.post("http://testserver/book")
        assert response.status_code == 200
        assert response.text == "Endpoint to create a book"

    def test_method_not_allowed(self, app, client):
        @app.route("/cbv")
        class DummyCBV:
            def get(self, req, resp):
                resp.text = "GET OK"

        response = client.post("http://testserver/cbv")
        assert response.status_code == 405
        assert response.text == "Method Not Allowed"


class TestExceptionHandling:
    def test_custom_exception_handler(self, app, client):
        def on_exception(request, response, exception):
            response.text = "AttributeErrorHappened"

        app.add_exception_handler(on_exception)

        @app.route("/exception")
        def exception_handler(request, response):
            raise AttributeError("This is a test exception")

        response = client.get("http://testserver/exception")
        assert response.text == "AttributeErrorHappened"
    
    def test_no_exception_handler(self, app, client):
        @app.route("/exception")
        def exception_handler(request, response):
            raise AttributeError("This is a test exception")

        response = client.get("http://testserver/exception")
        
        assert response.status_code == 500
        assert response.text == "This is a test exception"


class TestDjangoLikeApplication:
    def test_add_route(self, app, client):
        def home(request, response):
            response.text = "Hello, World!"

        app.add_route("/home", home)

        response = client.get("http://testserver/home")
        assert response.status_code == 200
        assert response.text == "Hello, World!"


class TestMiddleware:
    def test_middleware_functionality(self, app, client):
        process_request_called = False
        process_response_called = False

        class CallMiddlewareMethods(Middleware):
            def __init__(self, app):
                super().__init__(app)

            def process_request(self, request):
                nonlocal process_request_called
                process_request_called = True

            def process_response(self, request, response):
                nonlocal process_response_called
                process_response_called = True

        app.add_middleware(CallMiddlewareMethods)

        @app.route("/")
        def home(request, response):
            response.text = "Hello, World!"

        client.get("http://testserver/")

        assert process_request_called is True
        assert process_response_called is True
