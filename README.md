# Plinx

Plinx is an experimental, minimalistic, and extensible web framework and ORM written in Python.

## Installation

Install from git source:
```bash
$ pip install git+https://github.com/dhavalsavalia/plinx.git
```

## Usage

### Web Framework

```python
from plinx import Plinx

app = Plinx()

@app.route("/")
def index(request, response):
    response.text = "Hello, world!"
```

# Roadmap

- [ ] Web Framework
  - [x] Routing
  - [ ] Explicit Routing Methods
  - [ ] Parameterized Routes
- [ ] ORM
