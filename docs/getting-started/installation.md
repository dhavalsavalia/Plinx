# Installation

Getting started with Plinx is simple, as it has minimal dependencies and can be installed in multiple ways.

## Requirements

Plinx requires:

- Python 3.11 or newer
- A few core dependencies (automatically installed):
    - `webob`: For WSGI request/response handling
    - `parse`: For URL pattern matching

## Installation Methods

### From PyPI (Recommended)

The simplest way to install Plinx is via pip:

```bash
pip install Plinx
```

### From Source

If you want the latest code or wish to contribute to Plinx, you can install directly from the source repository:

```bash
pip install git+https://github.com/dhavalsavalia/Plinx.git
```

### Development Installation

For development purposes, clone the repository and install in development mode:

```bash
git clone https://github.com/dhavalsavalia/Plinx.git
cd Plinx
pip install -e .
```

This will install the package in "editable" mode, meaning changes to the source code will be immediately reflected without needing to reinstall.

## Verifying Installation

You can verify that Plinx has been installed correctly by running:

```python
import plinx
print(plinx.__version__)  # Should print the current version
```

## Optional Dependencies

For development and testing, you may want to install additional packages:

```bash
# Install dev dependencies for testing, documentation, etc.
pip install requests requests-wsgi-adapter pytest pytest-cov flake8 twine mkdocs mkdocs-material mkdocstrings mkdocstrings-python
```

Or if you use pipenv:

```bash
pipenv install --dev
```

## Running with a WSGI Server

Plinx is a WSGI framework, so you'll need a WSGI server to run it in production. Gunicorn is a good choice:

```bash
pip install gunicorn
gunicorn myapp:app
```

Where `myapp` is the module containing your Plinx application instance named `app`.