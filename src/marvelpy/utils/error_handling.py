"""Error handling utilities for Marvel API client.

This module provides utilities for handling errors from the Marvel API,
including error classification, retry logic, and error formatting.
"""

import asyncio
import logging
from typing import Any, Awaitable, Callable, Dict, List, Optional, Type

import httpx

from .exceptions import (
    MarvelAPIError,
    MarvelAuthenticationError,
    MarvelNetworkError,
    MarvelNotFoundError,
    MarvelRateLimitError,
    MarvelServerError,
    MarvelValidationError,
)

logger = logging.getLogger(__name__)


def classify_http_error(
    status_code: int,
    response_data: Optional[Dict[str, Any]] = None,  # noqa: ARG001
    request_data: Optional[Dict[str, Any]] = None,  # noqa: ARG001
) -> Type[MarvelAPIError]:
    """Classify HTTP status codes into appropriate Marvel API exceptions.

    This function maps HTTP status codes to the appropriate Marvel API
    exception class for better error handling and debugging.

    Args:
        status_code: HTTP status code from the response
        response_data: Raw response data from the API (if available)
        request_data: Request data that caused the error (if available)

    Returns:
        The appropriate Marvel API exception class for the status code

    Example:
        >>> error_class = classify_http_error(404)
        >>> print(error_class.__name__)  # MarvelNotFoundError
        >>>
        >>> error_class = classify_http_error(401)
        >>> print(error_class.__name__)  # MarvelAuthenticationError
    """
    if status_code == 401:
        return MarvelAuthenticationError
    elif status_code == 404:
        return MarvelNotFoundError
    elif status_code == 400:
        return MarvelValidationError
    elif status_code == 429:
        return MarvelRateLimitError
    elif 500 <= status_code < 600:
        return MarvelServerError
    else:
        return MarvelAPIError


def create_marvel_error(
    status_code: int,
    message: Optional[str] = None,
    response_data: Optional[Dict[str, Any]] = None,
    request_data: Optional[Dict[str, Any]] = None,
    **kwargs: Any,
) -> MarvelAPIError:
    """Create an appropriate Marvel API error from HTTP response data.

    This function creates the appropriate Marvel API exception instance
    based on the HTTP status code and response data.

    Args:
        status_code: HTTP status code from the response
        message: Custom error message (if not provided, uses default)
        response_data: Raw response data from the API (if available)
        request_data: Request data that caused the error (if available)
        **kwargs: Additional keyword arguments for specific error types

    Returns:
        An instance of the appropriate Marvel API exception

    Example:
        >>> error = create_marvel_error(
        ...     404,
        ...     message="Character not found",
        ...     resource_type="character",
        ...     resource_id="12345"
        ... )
        >>> print(type(error))  # <class 'MarvelNotFoundError'>
        >>> print(error.resource_type)  # character
    """
    error_class = classify_http_error(status_code, response_data, request_data)

    # Use default message if none provided
    if message is None:
        if error_class == MarvelAuthenticationError:
            message = "Authentication failed"
        elif error_class == MarvelNotFoundError:
            message = "Resource not found"
        elif error_class == MarvelValidationError:
            message = "Validation failed"
        elif error_class == MarvelRateLimitError:
            message = "Rate limit exceeded"
        elif error_class == MarvelServerError:
            message = "Server error occurred"
        else:
            message = "Marvel API error occurred"

    return error_class(
        message=message,
        status_code=status_code,
        response_data=response_data,
        request_data=request_data,
        **kwargs,
    )


def handle_httpx_error(
    error: httpx.HTTPError,
    request_data: Optional[Dict[str, Any]] = None,
) -> MarvelAPIError:
    """Handle httpx errors and convert them to Marvel API errors.

    This function handles various types of httpx errors and converts them
    to appropriate Marvel API exceptions for consistent error handling.

    Args:
        error: The httpx error that occurred
        request_data: Request data that caused the error (if available)

    Returns:
        An appropriate Marvel API exception

    Example:
        >>> try:
        ...     # Some httpx operation
        ...     pass
        ... except httpx.HTTPError as e:
        ...     marvel_error = handle_httpx_error(e)
        ...     print(f"Marvel API Error: {marvel_error}")
    """
    if isinstance(error, httpx.HTTPStatusError):
        # Handle HTTP status errors
        status_code = error.response.status_code
        try:
            response_data = error.response.json()
        except Exception:
            response_data = {"text": error.response.text}

        return create_marvel_error(
            status_code=status_code,
            message=f"HTTP {status_code} error: {error.response.reason_phrase}",
            response_data=response_data,
            request_data=request_data,
        )

    elif isinstance(error, httpx.TimeoutException):
        # Handle timeout errors
        return MarvelNetworkError(
            message="Request timeout - the Marvel API did not respond in time",
            request_data=request_data,
            original_error=error,
        )

    elif isinstance(error, httpx.ConnectError):
        # Handle connection errors
        return MarvelNetworkError(
            message="Connection error - unable to connect to the Marvel API",
            request_data=request_data,
            original_error=error,
        )

    elif isinstance(error, httpx.RequestError):
        # Handle other request errors
        return MarvelNetworkError(
            message=f"Request error: {error!s}",
            request_data=request_data,
            original_error=error,
        )

    else:
        # Handle any other httpx errors
        return MarvelNetworkError(
            message=f"Network error: {error!s}",
            request_data=request_data,
            original_error=error,
        )


async def retry_with_backoff(
    func: Callable[..., Awaitable[Any]],
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    backoff_factor: float = 2.0,
    retry_on: Optional[List[Type[Exception]]] = None,
) -> Any:
    """Retry a function with exponential backoff.

    This function implements retry logic with exponential backoff for
    handling transient errors from the Marvel API.

    Args:
        func: The async function to retry
        max_retries: Maximum number of retry attempts (default: 3)
        base_delay: Base delay in seconds for the first retry (default: 1.0)
        max_delay: Maximum delay in seconds between retries (default: 60.0)
        backoff_factor: Factor to multiply delay by for each retry (default: 2.0)
        retry_on: List of exception types to retry on (default: server errors)

    Returns:
        The result of the function call

    Raises:
        The last exception if all retries are exhausted

    Example:
        >>> async def api_call():
        ...     # Some API operation that might fail
        ...     pass
        >>>
        >>> result = await retry_with_backoff(
        ...     api_call,
        ...     max_retries=3,
        ...     base_delay=1.0
        ... )
    """
    if retry_on is None:
        retry_on = [MarvelServerError, MarvelRateLimitError, MarvelNetworkError]

    last_exception = None
    delay = base_delay

    for attempt in range(max_retries + 1):
        try:
            return await func()
        except Exception as e:
            last_exception = e

            # Check if this is a retryable error
            if not any(isinstance(e, error_type) for error_type in retry_on):
                raise e

            # If this is the last attempt, raise the exception
            if attempt == max_retries:
                logger.warning(f"All {max_retries} retry attempts exhausted")
                raise e

            # Log the retry attempt
            logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay:.1f}s...")

            # Wait before retrying
            await asyncio.sleep(delay)

            # Calculate next delay with exponential backoff
            delay = min(delay * backoff_factor, max_delay)

    # This should never be reached, but just in case
    if last_exception is not None:
        raise last_exception
    else:
        raise RuntimeError("Retry failed without any exceptions")


def format_error_message(error: MarvelAPIError) -> str:
    """Format a Marvel API error into a user-friendly message.

    This function creates a formatted, user-friendly error message
    from a Marvel API exception.

    Args:
        error: The Marvel API error to format

    Returns:
        A formatted error message string

    Example:
        >>> error = MarvelNotFoundError(
        ...     "Character not found",
        ...     resource_type="character",
        ...     resource_id="12345"
        ... )
        >>> message = format_error_message(error)
        >>> print(message)  # "Character not found (Status: 404)"
    """
    message = str(error)

    # Add additional context for specific error types
    if isinstance(error, MarvelNotFoundError):
        if error.resource_type and error.resource_id:
            message += f" - {error.resource_type.title()} with ID {error.resource_id} not found"
        elif error.resource_type:
            message += f" - {error.resource_type.title()} not found"

    elif isinstance(error, MarvelRateLimitError):
        if error.retry_after:
            message += f" - Retry after {error.retry_after} seconds"
        else:
            message += " - Please wait before making more requests"

    elif isinstance(error, MarvelValidationError):
        if error.validation_errors:
            message += f" - Validation errors: {', '.join(error.validation_errors)}"

    elif isinstance(error, MarvelNetworkError):
        message += " - Please check your internet connection and try again"

    elif isinstance(error, MarvelServerError):
        message += " - Please try again later"

    elif isinstance(error, MarvelAuthenticationError):
        message += " - Please check your API keys"

    return message


def log_error(error: MarvelAPIError, logger: Optional[logging.Logger] = None) -> None:
    """Log a Marvel API error with appropriate level and context.

    This function logs Marvel API errors with appropriate log levels
    and contextual information for debugging.

    Args:
        error: The Marvel API error to log
        logger: Logger instance to use (defaults to module logger)

    Example:
        >>> error = MarvelServerError("Internal server error", status_code=500)
        >>> log_error(error)  # Logs with WARNING level
    """
    if logger is None:
        logger = logging.getLogger(__name__)

    # Determine log level based on error type
    if isinstance(error, MarvelServerError):
        log_level = logging.ERROR
    elif isinstance(error, (MarvelRateLimitError, MarvelNetworkError)):
        log_level = logging.WARNING
    elif isinstance(error, MarvelAuthenticationError):
        log_level = logging.ERROR
    else:
        log_level = logging.INFO

    # Create log message with context
    message = format_error_message(error)

    # Add additional context for debugging
    context = []
    if error.status_code:
        context.append(f"status_code={error.status_code}")
    if error.request_data:
        context.append(f"request_data={error.request_data}")
    if error.response_data:
        context.append(f"response_data={error.response_data}")

    if context:
        message += f" ({', '.join(context)})"

    logger.log(log_level, message)
