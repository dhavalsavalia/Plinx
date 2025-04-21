# Contributing to Plinx

Thank you for considering contributing to Plinx! This document provides guidelines and information to make the contribution process smooth and effective.

## Getting Started

### Fork and Clone

First, fork the repository on GitHub, then clone your fork locally:

```bash
git clone https://github.com/your-username/Plinx.git
cd Plinx
```

### Set Up Development Environment

We recommend using a virtual environment:

```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install dev dependencies
pip install pytest pytest-cov flake8 black twine mkdocs mkdocs-material mkdocstrings mkdocstrings-python
```

## Development Workflow

### Branch Naming

Use descriptive branch names that reflect the changes you're making:

- `feature/description` for new features
- `bugfix/description` for bug fixes
- `docs/description` for documentation changes
- `refactor/description` for code refactoring

### Coding Standards

We follow standard Python conventions:

- Use [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Add docstrings following the Google style
- Include type hints where appropriate
- Keep functions focused and relatively short

You can check your code with flake8:

```bash
flake8 plinx tests
```

And format it with black:

```bash
black plinx tests
```

### Writing Tests

All new features should include tests. We use pytest for testing:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=plinx

# Run specific test file
pytest tests/test_specific.py
```

## Pull Request Process

1. Update your fork to the latest main branch
2. Create a new branch for your changes
3. Make your changes and write tests
4. Run the test suite to ensure everything passes
5. Update documentation if necessary
6. Submit a pull request with a clear description of the changes

### PR Description Template

```
## Description
[Describe the changes you've made]

## Related Issue
[Link to any related issues]

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Other (please describe)

## How Has This Been Tested?
[Describe the tests you ran]

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have added tests that prove my fix/feature works
- [ ] All tests pass locally
- [ ] I have updated the documentation accordingly
```

## Documentation

### Updating Documentation

If your changes affect user-facing functionality, update the documentation:

1. Update in-code docstrings
2. Update or add Markdown files in the `docs/` directory if needed
3. Build and check the documentation locally:

```bash
mkdocs serve
# View at http://localhost:8000
```

## Release Process

The release process is handled by maintainers, but here's the general workflow:

1. Update version in `VERSION` file
2. Update documentation if needed
3. Create a new GitHub release with release notes
4. Build and publish to PyPI

## Code of Conduct

### Our Pledge

We are committed to providing a friendly, safe, and welcoming environment for all contributors.

### Our Standards

- Be respectful and inclusive
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards other community members

### Enforcement

Violations of our code of conduct may result in temporary or permanent exclusion from project participation. Incidents can be reported to the project maintainers.

## Getting Help

If you need help with contributing, you can:

- Open an issue with questions
- Reach out to maintainers directly
- Check the documentation

Thank you for contributing to Plinx! Your time and expertise help make this project better for everyone.