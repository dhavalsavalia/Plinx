# Write test cases for the application here using pytest
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