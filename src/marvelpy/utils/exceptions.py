"""Custom exceptions for Marvel API client.

This module contains custom exception classes for handling different types
of errors that can occur when interacting with the Marvel API. These exceptions
provide more specific error handling and better debugging information.
"""

from typing import Any, Dict, List, Optional


class MarvelAPIError(Exception):
    """Base exception for Marvel API errors.

    This is the base class for all Marvel API related exceptions.
    It provides common functionality for error handling and debugging.

    Attributes:
        message: Error message describing what went wrong
        status_code: HTTP status code (if applicable)
        response_data: Raw response data from the API (if available)
        request_data: Request data that caused the error (if available)

    Example:
        >>> try:
        ...     # Some Marvel API operation
        ...     pass
        ... except MarvelAPIError as e:
        ...     print(f"Marvel API Error: {e.message}")
        ...     if e.status_code:
        ...         print(f"Status Code: {e.status_code}")
    """

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
        request_data: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the Marvel API error.

        Args:
            message: Error message describing what went wrong
            status_code: HTTP status code (if applicable)
            response_data: Raw response data from the API (if available)
            request_data: Request data that caused the error (if available)
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_data = response_data
        self.request_data = request_data

    def __str__(self) -> str:
        """Return string representation of the error."""
        if self.status_code:
            return f"{self.message} (Status: {self.status_code})"
        return self.message


class MarvelAuthenticationError(MarvelAPIError):
    """Exception raised for authentication errors.

    This exception is raised when there are issues with API authentication,
    such as invalid API keys, missing authentication parameters, or
    authentication failures.

    Attributes:
        message: Error message describing the authentication issue
        status_code: HTTP status code (typically 401)
        response_data: Raw response data from the API (if available)
        request_data: Request data that caused the error (if available)

    Example:
        >>> try:
        ...     # API call with invalid credentials
        ...     pass
        ... except MarvelAuthenticationError as e:
        ...     print(f"Authentication failed: {e.message}")
        ...     print("Please check your API keys")
    """

    def __init__(
        self,
        message: str = "Authentication failed",
        status_code: int = 401,
        response_data: Optional[Dict[str, Any]] = None,
        request_data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize the authentication error.

        Args:
            message: Error message describing the authentication issue
            status_code: HTTP status code (default: 401)
            response_data: Raw response data from the API (if available)
            request_data: Request data that caused the error (if available)
        """
        super().__init__(message, status_code, response_data, request_data)


class MarvelRateLimitError(MarvelAPIError):
    """Exception raised for rate limit errors.

    This exception is raised when the Marvel API rate limits are exceeded.
    The Marvel API has specific rate limits that should be respected.

    Attributes:
        message: Error message describing the rate limit issue
        status_code: HTTP status code (typically 429)
        response_data: Raw response data from the API (if available)
        request_data: Request data that caused the error (if available)
        retry_after: Number of seconds to wait before retrying (if available)

    Example:
        >>> try:
        ...     # API call that exceeds rate limits
        ...     pass
        ... except MarvelRateLimitError as e:
        ...     print(f"Rate limit exceeded: {e.message}")
        ...     if e.retry_after:
        ...         print(f"Retry after {e.retry_after} seconds")
    """

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        status_code: int = 429,
        response_data: Optional[Dict[str, Any]] = None,
        request_data: Optional[Dict[str, Any]] = None,
        retry_after: Optional[int] = None,
    ) -> None:
        """Initialize the rate limit error.

        Args:
            message: Error message describing the rate limit issue
            status_code: HTTP status code (default: 429)
            response_data: Raw response data from the API (if available)
            request_data: Request data that caused the error (if available)
            retry_after: Number of seconds to wait before retrying (if available)
        """
        super().__init__(message, status_code, response_data, request_data)
        self.retry_after = retry_after


class MarvelNotFoundError(MarvelAPIError):
    """Exception raised when a resource is not found.

    This exception is raised when requesting a specific resource that
    doesn't exist in the Marvel API, such as a character, comic, or
    other entity that cannot be found.

    Attributes:
        message: Error message describing the not found issue
        status_code: HTTP status code (typically 404)
        response_data: Raw response data from the API (if available)
        request_data: Request data that caused the error (if available)
        resource_type: Type of resource that was not found (if known)
        resource_id: ID of the resource that was not found (if known)

    Example:
        >>> try:
        ...     # Request for non-existent character
        ...     pass
        ... except MarvelNotFoundError as e:
        ...     print(f"Resource not found: {e.message}")
        ...     if e.resource_type and e.resource_id:
        ...         print(f"{e.resource_type} with ID {e.resource_id} not found")
    """

    def __init__(
        self,
        message: str = "Resource not found",
        status_code: int = 404,
        response_data: Optional[Dict[str, Any]] = None,
        request_data: Optional[Dict[str, Any]] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
    ) -> None:
        """Initialize the not found error.

        Args:
            message: Error message describing the not found issue
            status_code: HTTP status code (default: 404)
            response_data: Raw response data from the API (if available)
            request_data: Request data that caused the error (if available)
            resource_type: Type of resource that was not found (if known)
            resource_id: ID of the resource that was not found (if known)
        """
        super().__init__(message, status_code, response_data, request_data)
        self.resource_type = resource_type
        self.resource_id = resource_id


class MarvelValidationError(MarvelAPIError):
    """Exception raised for validation errors.

    This exception is raised when there are issues with request validation,
    such as invalid parameters, malformed requests, or missing required fields.

    Attributes:
        message: Error message describing the validation issue
        status_code: HTTP status code (typically 400)
        response_data: Raw response data from the API (if available)
        request_data: Request data that caused the error (if available)
        validation_errors: List of specific validation errors (if available)

    Example:
        >>> try:
        ...     # API call with invalid parameters
        ...     pass
        ... except MarvelValidationError as e:
        ...     print(f"Validation failed: {e.message}")
        ...     if e.validation_errors:
        ...         for error in e.validation_errors:
        ...             print(f"  - {error}")
    """

    def __init__(
        self,
        message: str = "Validation failed",
        status_code: int = 400,
        response_data: Optional[Dict[str, Any]] = None,
        request_data: Optional[Dict[str, Any]] = None,
        validation_errors: Optional[List[Any]] = None,
    ) -> None:
        """Initialize the validation error.

        Args:
            message: Error message describing the validation issue
            status_code: HTTP status code (default: 400)
            response_data: Raw response data from the API (if available)
            request_data: Request data that caused the error (if available)
            validation_errors: List of specific validation errors (if available)
        """
        super().__init__(message, status_code, response_data, request_data)
        self.validation_errors = validation_errors or []


class MarvelServerError(MarvelAPIError):
    """Exception raised for server errors.

    This exception is raised when there are server-side errors from the
    Marvel API, such as internal server errors, service unavailable,
    or other 5xx status codes.

    Attributes:
        message: Error message describing the server issue
        status_code: HTTP status code (typically 5xx)
        response_data: Raw response data from the API (if available)
        request_data: Request data that caused the error (if available)

    Example:
        >>> try:
        ...     # API call that results in server error
        ...     pass
        ... except MarvelServerError as e:
        ...     print(f"Server error: {e.message}")
        ...     print("Please try again later")
    """

    def __init__(
        self,
        message: str = "Server error occurred",
        status_code: int = 500,
        response_data: Optional[Dict[str, Any]] = None,
        request_data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize the server error.

        Args:
            message: Error message describing the server issue
            status_code: HTTP status code (default: 500)
            response_data: Raw response data from the API (if available)
            request_data: Request data that caused the error (if available)
        """
        super().__init__(message, status_code, response_data, request_data)


class MarvelNetworkError(MarvelAPIError):
    """Exception raised for network-related errors.

    This exception is raised when there are network-related issues,
    such as connection timeouts, DNS resolution failures, or other
    network connectivity problems.

    Attributes:
        message: Error message describing the network issue
        status_code: HTTP status code (if applicable)
        response_data: Raw response data from the API (if available)
        request_data: Request data that caused the error (if available)
        original_error: The original network error that occurred

    Example:
        >>> try:
        ...     # API call with network issues
        ...     pass
        ... except MarvelNetworkError as e:
        ...     print(f"Network error: {e.message}")
        ...     print("Please check your internet connection")
    """

    def __init__(
        self,
        message: str = "Network error occurred",
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
        request_data: Optional[Dict[str, Any]] = None,
        original_error: Optional[Exception] = None,
    ) -> None:
        """Initialize the network error.

        Args:
            message: Error message describing the network issue
            status_code: HTTP status code (if applicable)
            response_data: Raw response data from the API (if available)
            request_data: Request data that caused the error (if available)
            original_error: The original network error that occurred
        """
        super().__init__(message, status_code, response_data, request_data)
        self.original_error = original_error
