from plinx import Plinx
from plinx.middleware import Middleware

app = Plinx()


@app.route("/home")
def home(request, response):
    response.text = "Hello, World!"


@app.route("/hello/{name}")
def hello(request, response, name):
    response.text = f"Hello, {name}!"


@app.post("/math/{operation}/{num_1:d}/{num_2:d}")
def calculate_math(request, response, operation, num_1, num_2):
    if operation == "add":
        response.text = f"{num_1} + {num_2} = {num_1 + num_2}"
    elif operation == "subtract":
        response.text = f"{num_1} - {num_2} = {num_1 - num_2}"
    elif operation == "multiply":
        response.text = f"{num_1} * {num_2} = {num_1 * num_2}"
    elif operation == "divide" and num_2 != 0:
        response.text = f"{num_1} / {num_2} = {num_1 / num_2}"
    elif operation == "divide" and num_2 == 0:
        response.status_code = 400
        response.text = "Cannot divide by zero"
    else:
        response.status_code = 400
        response.text = "Invalid operation"


@app.route("/book")
class BooksResource:
    def get(self, req, resp):
        resp.text = "Books Page"

    def post(self, req, resp):
        resp.text = "Endpoint to create a book"


def django_like_route(request, response):
    response.text = "Django-like route response"
app.add_route("/django-like", django_like_route)

def custom_exception_handler(request, response, exception_cls):
    response.text = str(exception_cls)

app.add_exception_handler(custom_exception_handler)

@app.route("/exception")
def exception_handler(request, response):
    raise AttributeError("This is a test exception")

class CustomMiddleware(Middleware):
    def process_request(self, request):
        print("Processing request in middleware", request.path)

    def process_response(self, request, response):
        print("Processing response in middleware", response.text)

class SecondMiddleware(Middleware):
    def process_request(self, request):
        print("Processing request in SecondMiddleware", request.path)

    def process_response(self, request, response):
        print("Processing response in SecondMiddleware", response.text)
        response.text += " - Modified by SecondMiddleware"
        return response

app.add_middleware(SecondMiddleware)
app.add_middleware(CustomMiddleware)