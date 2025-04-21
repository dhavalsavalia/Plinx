# Release Notes

## Plinx 1.0.0 (April 2025)

We're excited to announce the release of Plinx 1.0.0! This is the first stable release of our experimental, minimalistic, and extensible WSGI-based web framework and ORM.

### Core Features

- **WSGI Application Framework**

    - Complete request/response cycle
    - Decorator-based routing system
    - Class-based views
    - HTTP method-specific route handlers
    - URL pattern matching with parameter extraction

- **Middleware System**

    - Nested middleware architecture
    - Request and response processing hooks
    - Easy extension points for cross-cutting concerns

- **Response Handling**

    - Simple API for text and JSON responses
    - Custom status codes and headers
    - Content-type negotiation

- **Lightweight ORM**

    - SQLite database support
    - Table definitions as Python classes
    - Basic CRUD operations
    - Foreign key relationships
    - Python type to SQL type mapping

- **Testing Support**

    - Test client for making requests to your application
    - No HTTP server required for testing

- **Modern Python Features**
    - Type hints throughout the codebase
    - Support for Python 3.11+
    - Clean, readable code structure

### Notable Design Decisions

- **Explicit Request/Response Model**: Unlike some frameworks that use global request objects or return values as responses, Plinx explicitly passes request and response objects to handlers.
- **Minimal Dependencies**: Plinx has very few dependencies, making it lightweight and easy to install.
- **Educational Focus**: The codebase is designed to be readable and understandable, serving as a learning resource.
- **WSGI Foundation**: Built on the proven WSGI standard for broad compatibility and simplicity.

### Installation

Plinx 1.0.0 can be installed from PyPI:

```bash
pip install Plinx
```

### Compatibility

Plinx 1.0.0 requires:

- Python 3.11 or higher
- WebOb
- parse

### Documentation

Comprehensive documentation is available at:

- [Online Documentation](https://plinx.readthedocs.io/)
- In the `docs/` directory of the source code

### Known Limitations

- **ORM Constraints**: The ORM is intentionally simple and currently only supports SQLite
- **Performance**: Optimized for clarity and simplicity rather than raw performance
- **Feature Set**: Focused on core functionality; some common web framework features are not included

### Future Roadmap

While Plinx 1.0.0 is a stable release, we have plans for future enhancements:

- Additional ORM features (more advanced queries, additional relationship types)
- Optional ASGI support
- Integration helpers for common third-party libraries
- Enhanced routing capabilities
- Template rendering integrations

### Acknowledgments

Special thanks to everyone who contributed to making this release possible, including testers, documentation writers, and early adopters who provided valuable feedback during development.
