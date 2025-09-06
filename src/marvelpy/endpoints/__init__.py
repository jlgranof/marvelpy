"""Marvel API endpoint classes.

This package contains endpoint classes for interacting with the Marvel API.
Each endpoint provides type-safe methods for accessing specific Marvel API resources.
"""

from .base import BaseEndpoint
from .characters import CharactersEndpoint

__all__ = [
    "BaseEndpoint",
    "CharactersEndpoint",
]
