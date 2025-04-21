# Plinx

![purpose](https://img.shields.io/badge/purpose-learning-green.svg)
![PyPI](https://img.shields.io/pypi/v/Plinx.svg)

**Plinx** is an experimental, minimalistic, and extensible WSGI-based web framework and ORM written in Python.  
It is designed to be simple, fast, and easy to extend, making it ideal for rapid prototyping and educational purposes.

---

## Features

- 🚀 Minimal and fast web framework
- 🛣️ Intuitive routing system
- 🧩 Extensible middleware support
- 🧪 Simple, readable codebase for learning and hacking
- 📝 Type hints and modern Python best practices

---

## Installation

Install from PyPI:

```bash
pip instal Plinx
```

Install directly from the git source:

```bash
pip install git+https://github.com/dhavalsavalia/plinx.git
```

---

## Quickstart

Create a simple web application in seconds:

```python
from plinx import Plinx

app = Plinx()

@app.route("/")
def index(request, response):
    response.text = "Hello, world!"
```

Run your app (example, assuming you have an ASGI server like `uvicorn`):

```bash
uvicorn myapp:app
```

## Testing

Use [pytest](https://docs.pytest.org/en/latest/) to unit test this framework.

```bash
pytest --cov=.
```

---

## Roadmap

- [x] Web Framework
  - [x] Routing
  - [x] Explicit Routing Methods (GET, POST, etc.)
  - [x] Parameterized Routes
  - [x] Class Based Routes
  - [x] Django-like Routes
  - [x] Middleware Support
- [x] ORM

---

## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements, bug fixes, or new features.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Author & Contact

Created and maintained by [Dhaval Savalia](https://github.com/dhavalsavalia).  
For questions or opportunities, feel free to reach out via [LinkedIn](https://www.linkedin.com/in/dhavalsavalia/) or open an issue.

---
