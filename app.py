from plinx import Plinx


app = Plinx()


@app.route("/home")
def home(request, response):
    response.text = "Hello, World!"
