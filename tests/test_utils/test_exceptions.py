"""Tests for Marvel API exception classes.

This module contains comprehensive tests for all Marvel API exception classes,
including base exception functionality and specific exception types.
"""


from marvelpy.utils.exceptions import (
    MarvelAPIError,
    MarvelAuthenticationError,
    MarvelNetworkError,
    MarvelNotFoundError,
    MarvelRateLimitError,
    MarvelServerError,
    MarvelValidationError,
)


class TestMarvelAPIError:
    """Test cases for the base MarvelAPIError class.

    Tests the base exception class functionality including initialization,
    string representation, and attribute access.
    """

    def test_marvel_api_error_creation(self):
        """Test creating a MarvelAPIError with basic parameters."""
        error = MarvelAPIError("Test error message")

        assert str(error) == "Test error message"
        assert error.message == "Test error message"
        assert error.status_code is None
        assert error.response_data is None
        assert error.request_data is None

    def test_marvel_api_error_with_status_code(self):
        """Test creating a MarvelAPIError with status code."""
        error = MarvelAPIError("Test error", status_code=404)

        assert str(error) == "Test error (Status: 404)"
        assert error.message == "Test error"
        assert error.status_code == 404

    def test_marvel_api_error_with_all_parameters(self):
        """Test creating a MarvelAPIError with all parameters."""
        response_data = {"error": "Not found"}
        request_data = {"id": "12345"}

        error = MarvelAPIError(
            "Test error", status_code=404, response_data=response_data, request_data=request_data
        )

        assert error.message == "Test error"
        assert error.status_code == 404
        assert error.response_data == response_data
        assert error.request_data == request_data

    def test_marvel_api_error_inheritance(self):
        """Test that MarvelAPIError inherits from Exception."""
        error = MarvelAPIError("Test error")
        assert isinstance(error, Exception)


class TestMarvelAuthenticationError:
    """Test cases for MarvelAuthenticationError class.

    Tests authentication-specific error handling and default values.
    """

    def test_authentication_error_default_values(self):
        """Test MarvelAuthenticationError with default values."""
        error = MarvelAuthenticationError()

        assert error.message == "Authentication failed"
        assert error.status_code == 401
        assert error.response_data is None
        assert error.request_data is None

    def test_authentication_error_custom_message(self):
        """Test MarvelAuthenticationError with custom message."""
        error = MarvelAuthenticationError("Invalid API key")

        assert error.message == "Invalid API key"
        assert error.status_code == 401

    def test_authentication_error_with_data(self):
        """Test MarvelAuthenticationError with response and request data."""
        response_data = {"error": "Invalid credentials"}
        request_data = {"apikey": "invalid_key"}

        error = MarvelAuthenticationError(
            "Invalid API key", response_data=response_data, request_data=request_data
        )

        assert error.message == "Invalid API key"
        assert error.status_code == 401
        assert error.response_data == response_data
        assert error.request_data == request_data

    def test_authentication_error_inheritance(self):
        """Test that MarvelAuthenticationError inherits from MarvelAPIError."""
        error = MarvelAuthenticationError()
        assert isinstance(error, MarvelAPIError)
        assert isinstance(error, Exception)


class TestMarvelRateLimitError:
    """Test cases for MarvelRateLimitError class.

    Tests rate limit-specific error handling and retry information.
    """

    def test_rate_limit_error_default_values(self):
        """Test MarvelRateLimitError with default values."""
        error = MarvelRateLimitError()

        assert error.message == "Rate limit exceeded"
        assert error.status_code == 429
        assert error.retry_after is None

    def test_rate_limit_error_with_retry_after(self):
        """Test MarvelRateLimitError with retry_after information."""
        error = MarvelRateLimitError(retry_after=60)

        assert error.message == "Rate limit exceeded"
        assert error.status_code == 429
        assert error.retry_after == 60

    def test_rate_limit_error_custom_message(self):
        """Test MarvelRateLimitError with custom message."""
        error = MarvelRateLimitError("Too many requests", retry_after=30)

        assert error.message == "Too many requests"
        assert error.status_code == 429
        assert error.retry_after == 30

    def test_rate_limit_error_inheritance(self):
        """Test that MarvelRateLimitError inherits from MarvelAPIError."""
        error = MarvelRateLimitError()
        assert isinstance(error, MarvelAPIError)
        assert isinstance(error, Exception)


class TestMarvelNotFoundError:
    """Test cases for MarvelNotFoundError class.

    Tests not found-specific error handling and resource information.
    """

    def test_not_found_error_default_values(self):
        """Test MarvelNotFoundError with default values."""
        error = MarvelNotFoundError()

        assert error.message == "Resource not found"
        assert error.status_code == 404
        assert error.resource_type is None
        assert error.resource_id is None

    def test_not_found_error_with_resource_info(self):
        """Test MarvelNotFoundError with resource information."""
        error = MarvelNotFoundError(
            "Character not found", resource_type="character", resource_id="12345"
        )

        assert error.message == "Character not found"
        assert error.status_code == 404
        assert error.resource_type == "character"
        assert error.resource_id == "12345"

    def test_not_found_error_partial_resource_info(self):
        """Test MarvelNotFoundError with partial resource information."""
        error = MarvelNotFoundError("Comic not found", resource_type="comic")

        assert error.message == "Comic not found"
        assert error.status_code == 404
        assert error.resource_type == "comic"
        assert error.resource_id is None

    def test_not_found_error_inheritance(self):
        """Test that MarvelNotFoundError inherits from MarvelAPIError."""
        error = MarvelNotFoundError()
        assert isinstance(error, MarvelAPIError)
        assert isinstance(error, Exception)


class TestMarvelValidationError:
    """Test cases for MarvelValidationError class.

    Tests validation-specific error handling and validation details.
    """

    def test_validation_error_default_values(self):
        """Test MarvelValidationError with default values."""
        error = MarvelValidationError()

        assert error.message == "Validation failed"
        assert error.status_code == 400
        assert error.validation_errors == []

    def test_validation_error_with_validation_errors(self):
        """Test MarvelValidationError with validation errors."""
        validation_errors = ["Invalid parameter", "Missing required field"]
        error = MarvelValidationError(
            "Request validation failed", validation_errors=validation_errors
        )

        assert error.message == "Request validation failed"
        assert error.status_code == 400
        assert error.validation_errors == validation_errors

    def test_validation_error_empty_validation_errors(self):
        """Test MarvelValidationError with empty validation errors list."""
        error = MarvelValidationError(validation_errors=[])

        assert error.validation_errors == []

    def test_validation_error_inheritance(self):
        """Test that MarvelValidationError inherits from MarvelAPIError."""
        error = MarvelValidationError()
        assert isinstance(error, MarvelAPIError)
        assert isinstance(error, Exception)


class TestMarvelServerError:
    """Test cases for MarvelServerError class.

    Tests server-specific error handling and default values.
    """

    def test_server_error_default_values(self):
        """Test MarvelServerError with default values."""
        error = MarvelServerError()

        assert error.message == "Server error occurred"
        assert error.status_code == 500

    def test_server_error_custom_message(self):
        """Test MarvelServerError with custom message."""
        error = MarvelServerError("Internal server error", status_code=503)

        assert error.message == "Internal server error"
        assert error.status_code == 503

    def test_server_error_inheritance(self):
        """Test that MarvelServerError inherits from MarvelAPIError."""
        error = MarvelServerError()
        assert isinstance(error, MarvelAPIError)
        assert isinstance(error, Exception)


class TestMarvelNetworkError:
    """Test cases for MarvelNetworkError class.

    Tests network-specific error handling and original error information.
    """

    def test_network_error_default_values(self):
        """Test MarvelNetworkError with default values."""
        error = MarvelNetworkError()

        assert error.message == "Network error occurred"
        assert error.status_code is None
        assert error.original_error is None

    def test_network_error_with_original_error(self):
        """Test MarvelNetworkError with original error."""
        original_error = ConnectionError("Connection failed")
        error = MarvelNetworkError("Network connection failed", original_error=original_error)

        assert error.message == "Network connection failed"
        assert error.original_error == original_error

    def test_network_error_with_status_code(self):
        """Test MarvelNetworkError with status code."""
        error = MarvelNetworkError("Timeout error", status_code=408)

        assert error.message == "Timeout error"
        assert error.status_code == 408

    def test_network_error_inheritance(self):
        """Test that MarvelNetworkError inherits from MarvelAPIError."""
        error = MarvelNetworkError()
        assert isinstance(error, MarvelAPIError)
        assert isinstance(error, Exception)


class TestExceptionHierarchy:
    """Test cases for exception class hierarchy and relationships.

    Tests that all exception classes properly inherit from the base class
    and maintain correct relationships.
    """

    def test_all_exceptions_inherit_from_marvel_api_error(self):
        """Test that all Marvel API exceptions inherit from MarvelAPIError."""
        exceptions = [
            MarvelAuthenticationError(),
            MarvelRateLimitError(),
            MarvelNotFoundError(),
            MarvelValidationError(),
            MarvelServerError(),
            MarvelNetworkError(),
        ]

        for exception in exceptions:
            assert isinstance(exception, MarvelAPIError)
            assert isinstance(exception, Exception)

    def test_exception_type_checking(self):
        """Test that exception type checking works correctly."""
        auth_error = MarvelAuthenticationError()
        rate_limit_error = MarvelRateLimitError()
        not_found_error = MarvelNotFoundError()

        assert isinstance(auth_error, MarvelAuthenticationError)
        assert not isinstance(auth_error, MarvelRateLimitError)
        assert not isinstance(auth_error, MarvelNotFoundError)

        assert isinstance(rate_limit_error, MarvelRateLimitError)
        assert not isinstance(rate_limit_error, MarvelAuthenticationError)

        assert isinstance(not_found_error, MarvelNotFoundError)
        assert not isinstance(not_found_error, MarvelAuthenticationError)

    def test_exception_string_representations(self):
        """Test that all exceptions have proper string representations."""
        exceptions_with_status = [
            (MarvelAuthenticationError(), "Authentication failed (Status: 401)"),
            (MarvelRateLimitError(), "Rate limit exceeded (Status: 429)"),
            (MarvelNotFoundError(), "Resource not found (Status: 404)"),
            (MarvelValidationError(), "Validation failed (Status: 400)"),
            (MarvelServerError(), "Server error occurred (Status: 500)"),
        ]

        for exception, expected in exceptions_with_status:
            assert str(exception) == expected

        # Network error without status code
        network_error = MarvelNetworkError()
        assert str(network_error) == "Network error occurred"
