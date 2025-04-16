import pytest

from plinx import Plinx
from plinx.methods import HTTPMethods
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

        method, handler = app.routes["/home"]
        assert handler == home
        assert method.value == "GET"

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

    def test_method_not_allowed(self, app, client):
        @app.post("/method_not_allowed")
        def method_not_allowed(request, response):
            response.text = "Best POST method"

        response = client.get("http://testserver/method_not_allowed")
        assert response.status_code == 405
        assert response.text == "Method Not Allowed"

    def test_post_request(self, app, client):
        @app.post("/post")
        def post_handler(request, response):
            response.text = "POST request received"

        response = client.post("http://testserver/post")
        assert response.status_code == 200
        assert response.text == "POST request received"

    def test_get_request(self, app, client):
        @app.get("/get")
        def get_handler(request, response):
            response.text = "GET request received"

        response = client.get("http://testserver/get")
        assert response.status_code == 200
        assert response.text == "GET request received"

    def test_put_request(self, app, client):
        @app.put("/put")
        def put_handler(request, response):
            response.text = "PUT request received"

        response = client.put("http://testserver/put")
        assert response.status_code == 200
        assert response.text == "PUT request received"

    def test_delete_request(self, app, client):
        @app.delete("/delete")
        def delete_handler(request, response):
            response.text = "DELETE request received"

        response = client.delete("http://testserver/delete")
        assert response.status_code == 200
        assert response.text == "DELETE request received"

    def test_options_request(self, app, client):
        @app.options("/options")
        def options_handler(request, response):
            response.text = "OPTIONS request received"

        response = client.options("http://testserver/options")
        assert response.status_code == 200
        assert response.text == "OPTIONS request received"

    def test_patch_request(self, app, client):
        @app.patch("/patch")
        def patch_handler(request, response):
            response.text = "PATCH request received"

        response = client.patch("http://testserver/patch")
        assert response.status_code == 200
        assert response.text == "PATCH request received"

    def test_head_request(self, app, client):
        @app.head("/head")
        def head_handler(request, response):
            response.headers["X-TEST-HEADER"] = "Test Header"

        response = client.head("http://testserver/head")
        assert response.status_code == 200
        assert response.headers["X-TEST-HEADER"] == "Test Header"

    def test_invalid_method(self, app, client):
        with pytest.raises(RuntimeError) as excinfo:

            @app.trace("/invalid")
            def invalid_handler(request, response):
                response.text = "Invalid method"

        assert isinstance(excinfo.value, RuntimeError)
        assert "'Plinx' object has no attribute 'trace'" == str(excinfo.value)


class TestClassBasedView:
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

    def test_method_not_allowed(self, app, client):
        def home(request, response):
            response.text = "Hello, World!"

        app.add_route("/home", home, HTTPMethods.POST)

        response = client.get("http://testserver/home")
        assert response.status_code == 405
        assert response.text == "Method Not Allowed"


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


class TestCustomResponses:
    def test_json_response_helper(self, app, client):
        @app.route("/json")
        def json_response(request, response):
            response.json = {"message": "Hello, JSON!"}

        response = client.get("http://testserver/json")

        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        assert response.json() == {"message": "Hello, JSON!"}

    def test_text_response_helper(self, app, client):
        @app.route("/text")
        def text_response(request, response):
            response.text = "Hello, Text!"

        response = client.get("http://testserver/text")

        assert response.status_code == 200
        assert response.headers["Content-Type"] == "text/plain"
        assert response.text == "Hello, Text!"
    
    def test_manually_setting_body(self, app, client):
        @app.route("/manual")
        def manual_response(request, response):
            response.body = b"Hello, Manual!"
            response.content_type = "text/plain"

        response = client.get("http://testserver/manual")

        assert response.status_code == 200
        assert response.headers["Content-Type"] == "text/plain"
        assert response.text == "Hello, Manual!"
    
    def test_custom_headers(self, app, client):
        @app.route("/headers")
        def custom_headers(request, response):
            response.headers["X-Custom-Header"] = "CustomValue"
            response.text = "Hello, Headers!"

        response = client.get("http://testserver/headers")

        assert response.status_code == 200
        assert response.text == "Hello, Headers!"
        assert response.headers["X-Custom-Header"] == "CustomValue"
        assert response.headers["Content-Type"] == "text/plain"