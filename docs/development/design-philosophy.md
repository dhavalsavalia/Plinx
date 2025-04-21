# Design Philosophy

This page outlines the core design principles that guided the development of Plinx 1.0.0. Understanding these principles provides insight into why certain design choices were made.

## Core Principles

### 1. Simplicity Over Complexity

Plinx prioritizes simplicity in its API and implementation. We believe that a framework should be easy to understand, both for users and for developers who want to learn from the code. This means:

- Favoring explicit code over "magic" behaviors
- Keeping the API surface area small and focused
- Minimizing indirection and abstraction layers
- Making the common case easy and the complex case possible

Simplicity doesn't mean lack of power—it means thoughtfully designing interfaces that expose the right level of abstraction for the task at hand.

### 2. Educational Value

Plinx was designed partly as an educational tool. The codebase should be readable and approachable enough that someone can learn web framework design by studying it. This influenced decisions like:

- Clear, well-documented code with minimal "cleverness"
- Straightforward implementations that prioritize readability
- Thorough docstrings explaining not just what code does, but why
- A codebase small enough to be understood as a whole

We want Plinx to be a framework that helps developers understand how web frameworks and ORMs work under the hood.

### 3. Minimal Dependencies

Plinx aims to have as few external dependencies as possible. This makes the framework:

- Easier to install and deploy
- More stable across environments
- Less susceptible to security issues in dependencies
- More maintainable over time

The core dependencies (WebOb, parse) were chosen carefully for their stability, simplicity, and focused purpose.

### 4. Pythonic Design

The framework embraces Python's strengths and conventions:

- Using decorators for route registration (`@app.route("/path")`)
- Providing a clean, object-oriented interface
- Following PEP 8 style conventions
- Leveraging Python's dynamic nature where appropriate
- Using type hints to improve developer experience

### 5. Extensibility

While keeping the core simple, Plinx is designed to be extended and customized:

- The middleware system allows for flexible request/response processing
- Class-based views support inheritance and composition
- The ORM can be extended with custom methods and properties
- Core components are designed to be subclassed when needed

## Design Decisions

### WSGI Foundation

Plinx is built on the WSGI standard rather than newer async frameworks (like ASGI) for several reasons:

1. WSGI is simpler and more straightforward to understand
2. It has wider support across servers and platforms
3. It's sufficient for many web applications
4. It provides a solid foundation for learning web framework concepts

### Explicit Request and Response Objects

Unlike some frameworks that use global request objects or return values as responses, Plinx explicitly passes request and response objects to handlers:

```python
@app.route("/")
def home(request, response):
    response.text = "Hello, World!"
```

This design:

- Makes the flow of data more obvious
- Avoids hidden state and global variables
- Makes testing easier
- Simplifies understanding how requests and responses work

### Lightweight ORM

The ORM in Plinx is intentionally lightweight:

- It focuses on the core CRUD operations
- It uses Python classes to define tables
- It provides a natural way to work with relationships
- It avoids complex query building or lazy loading

This approach makes the ORM easy to learn and use, while still being useful for many applications.

### Middleware Pattern

The middleware system follows a nested pattern instead of a linear chain. This design:

- Makes the request/response flow easy to understand
- Allows middleware to completely short-circuit the request if needed
- Provides symmetrical processing of requests and responses
- Follows established patterns in the Python web ecosystem

## Tradeoffs

Every design involves tradeoffs. Some conscious tradeoffs in Plinx include:

### Performance vs. Clarity

In some cases, we've chosen more readable code over maximum performance optimizations. For example:

- The ORM prioritizes a clean API over raw SQL performance
- The routing system uses pattern matching for flexibility rather than fastest possible lookups
- The middleware chain is simple rather than highly optimized

### Features vs. Focus

We've deliberately left out many features that larger frameworks provide:

- No built-in template rendering
- No form processing helpers
- No authentication/authorization system
- No admin interface
- Limited ORM query capabilities

These omissions keep the framework focused and learnable, while allowing users to integrate third-party libraries when needed.

### Flexibility vs. Convention

Plinx provides less "convention over configuration" than some frameworks:

- No enforced project structure
- Minimal automatic configuration
- Few built-in defaults

This gives users more freedom but requires more explicit choices.

## Future Direction

While maintaining the core principles, future versions of Plinx may explore:

- Optional ASGI support
- More sophisticated routing
- Enhanced ORM capabilities
- Minimal template integration
- Additional helper utilities

However, any additions will be measured against the core principles to ensure Plinx remains true to its design philosophy.