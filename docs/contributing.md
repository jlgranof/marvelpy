# Contributing

Thank you for your interest in contributing to Marvelpy! We welcome contributions from the community.

## Development Setup

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/marvelpy.git
   cd marvelpy
   ```

3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install in development mode**:
   ```bash
   pip install -e ".[dev]"
   ```

5. **Install pre-commit hooks**:
   ```bash
   pre-commit install
   ```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=marvelpy --cov-report=html

# Run specific test file
pytest tests/test_hello.py
```

## Code Quality

We use several tools to maintain code quality:

- **Ruff** - Fast Python linter and formatter
- **MyPy** - Static type checking
- **Pre-commit** - Git hooks for code quality

Run these manually:
```bash
ruff check src tests
ruff format src tests
mypy src
```

## Documentation

Documentation is built with MkDocs:

```bash
# Install docs dependencies
pip install -e ".[docs]"

# Serve docs locally
mkdocs serve

# Build docs
mkdocs build
```

## Pull Request Process

1. **Create a feature branch** from `main`
2. **Make your changes** with tests
3. **Ensure all tests pass** and code quality checks pass
4. **Update documentation** if needed
5. **Submit a pull request** with a clear description

## Code Style

- Follow PEP 8 style guidelines
- Use type hints for all functions
- Write docstrings for all public functions
- Keep functions small and focused
- Write tests for new functionality

## Reporting Issues

When reporting issues, please include:

- Python version
- Marvelpy version
- Steps to reproduce
- Expected vs actual behavior
- Any error messages or stack traces

## Questions?

Feel free to open an issue for questions or discussions!
