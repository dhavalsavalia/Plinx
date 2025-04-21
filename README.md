# Plinx

![purpose](https://img.shields.io/badge/purpose-learning-green.svg)
![PyPI](https://img.shields.io/pypi/v/Plinx.svg)

**Plinx** is an experimental, minimalistic, and extensible WSGI-based web framework and ORM written in Python.  
It is designed to be simple, fast, and easy to extend, making it ideal for rapid prototyping and educational purposes.

---

## Features

- 🚀 Minimal and fast WSGI web framework
- 💾 Integrated Object-Relational Mapper (ORM)
- 🛣️ Intuitive routing system (including parameterized and class-based routes)
- 🧩 Extensible middleware support
- 🧪 Simple, readable codebase for learning and hacking
- 📝 Type hints and modern Python best practices

---

## Installation

Install from PyPI:

```bash
pip install Plinx
```

Install directly from the git source:

```bash
pip install git+https://github.com/dhavalsavalia/plinx.git
```

---

## Quickstart

Create a simple web application in seconds:

```python
# myapp.py
from plinx import Plinx

app = Plinx()

@app.route("/")
def index(request, response):
    response.text = "Hello, Plinx 1.0.0!"

# Example using the ORM (requires database setup)
# from plinx.orm import Database, Table, Column
# db = Database("my_database.db")
# class Item(Table):
#     name = Column(str)
#     count = Column(int)
# db.create(Item)
# db.save(Item(name="Example", count=1))
```

Run your app using a WSGI server (like `gunicorn`):

```bash
pip install gunicorn
gunicorn myapp:app
```

## Testing

Use [pytest](https://docs.pytest.org/en/latest/) to unit test this framework.

```bash
pytest --cov=.
```

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
