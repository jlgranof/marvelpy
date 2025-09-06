"""Utility modules for Marvelpy."""

from .auth import generate_auth_params
from .error_handling import (
    classify_http_error,
    create_marvel_error,
    format_error_message,
    handle_httpx_error,
    log_error,
    retry_with_backoff,
)
from .exceptions import (
    MarvelAPIError,
    MarvelAuthenticationError,
    MarvelNetworkError,
    MarvelNotFoundError,
    MarvelRateLimitError,
    MarvelServerError,
    MarvelValidationError,
)

__all__ = [
    # Authentication utilities
    "generate_auth_params",
    # Exception classes
    "MarvelAPIError",
    "MarvelAuthenticationError",
    "MarvelNetworkError",
    "MarvelNotFoundError",
    "MarvelRateLimitError",
    "MarvelServerError",
    "MarvelValidationError",
    # Error handling utilities
    "classify_http_error",
    "create_marvel_error",
    "format_error_message",
    "handle_httpx_error",
    "log_error",
    "retry_with_backoff",
]
