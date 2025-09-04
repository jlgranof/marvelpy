# Installation

## Requirements

- Python 3.8 or higher
- pip (Python package installer)

## Install from PyPI

The easiest way to install Marvelpy is using pip:

```bash
pip install marvelpy
```

## Install from Source

If you want to install the latest development version:

```bash
git clone https://github.com/jlgranof/marvelpy.git
cd marvelpy
pip install -e .
```

## Install with Development Dependencies

For development and testing:

```bash
pip install -e ".[dev]"
```

This will install:
- Testing tools (pytest, pytest-cov, pytest-mock)
- Linting tools (ruff, mypy)
- Documentation tools (mkdocs-material)
- Pre-commit hooks

## Verify Installation

You can verify the installation by importing the package:

```python
import marvelpy
print(marvelpy.__version__)
```

## Dependencies

Marvelpy has the following core dependencies:

- `httpx>=0.23.0` - Modern HTTP client for async requests
- `pydantic>=1.10.0` - Data validation and settings management
- `typing-extensions>=4.9.0` - Extended typing support
- `click>=8.1.0` - Command-line interface framework

## Virtual Environment (Recommended)

It's recommended to use a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install marvelpy
pip install marvelpy
```
