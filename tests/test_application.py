# Write test cases for the application here using pytest
import pytest
from webob import Request, Response

from plinx import Plinx


class TestApplication:
    app = Plinx()

    def test_app_object(self, app=app):
        assert app.routes == {}
        assert app is not None

    def test_route_decorator(self, app=app):
        @app.route("/home")
        def home(request, response):
            response.text = "Hello, World!"

        assert app.routes["/home"] == home

    def test_404_response(self, app=app):
        request = Request.blank("/not-found")
        response = Response()
        handler, kwargs = app.find_handler(request, response)
        assert handler is None, None
        assert response.status_code == 404
        assert response.text == "Not Found"

    def test_parameterized_route(self, app=app):
        @app.route("/hello/{name}")
        def hello(request, response, name):
            response.text = f"Hello, {name}!"

        request = Request.blank("/hello/Dhaval")
        response = app.handle_request(request)
        assert response.status_code == 200
        assert response.text == "Hello, Dhaval!"

    def test_duplicate_route(self, app=app):
        @app.route("/duplicate")
        def handler1(request, response):
            response.text = "First"

        with pytest.raises(RuntimeError) as excinfo:

            @app.route("/duplicate")
            def handler2(request, response):
                response.text = "Second"

        assert isinstance(excinfo.value, RuntimeError)
        assert "Route '/duplicate' is already registered." == str(excinfo.value)

    def test_class_based_route(self, app=app):
        @app.route("/book")
        class BooksResource:
            def get(self, req, resp):
                resp.text = "Books Page"

            def post(self, req, resp):
                resp.text = "Endpoint to create a book"

        request = Request.blank("/book")
        response = app.handle_request(request)
        assert response.status_code == 200
        assert response.text == "Books Page"
        request = Request.blank("/book", method="POST")
        response = app.handle_request(request)
        assert response.status_code == 200
        assert response.text == "Endpoint to create a book"

    def test_method_not_allowed(self, app=app):
        @app.route("/cbv")
        class DummyCBV:
            def get(self, req, resp):
                resp.text = "GET OK"

        request = Request.blank("/cbv", method="POST")
        response = app.handle_request(request)
        assert response.status_code == 405
        assert response.text == "Method Not Allowed"
