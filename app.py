from plinx import Plinx

app = Plinx()


@app.route("/home")
def home(request, response):
    response.text = "Hello, World!"


@app.route("/hello/{name}")
def hello(request, response, name):
    response.text = f"Hello, {name}!"


@app.route("/math/{operation}/{num_1:d}/{num_2:d}")
def sum(request, response, operation, num_1, num_2):
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