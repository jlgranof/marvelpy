"""Tests for error handling utilities.

This module contains comprehensive tests for error handling utilities,
including error classification, error creation, and retry logic.
"""

import logging
from unittest.mock import AsyncMock, Mock, patch

import httpx
import pytest

# Configure logging for tests
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

from marvelpy.utils.error_handling import (
    classify_http_error,
    create_marvel_error,
    format_error_message,
    handle_httpx_error,
    log_error,
    retry_with_backoff,
)
from marvelpy.utils.exceptions import (
    MarvelAPIError,
    MarvelAuthenticationError,
    MarvelNetworkError,
    MarvelNotFoundError,
    MarvelRateLimitError,
    MarvelServerError,
    MarvelValidationError,
)


class TestClassifyHttpError:
    """Test cases for HTTP error classification.

    Tests the classify_http_error function to ensure it correctly
    maps HTTP status codes to appropriate exception classes.
    """

    def test_classify_authentication_error(self):
        """Test classification of authentication errors."""
        logger.info("Testing HTTP error classification for authentication errors")
        error_class = classify_http_error(401)
        assert error_class == MarvelAuthenticationError
        logger.info("✅ Authentication error classification test completed successfully")

    def test_classify_not_found_error(self):
        """Test classification of not found errors."""
        logger.info("Testing HTTP error classification for not found errors")
        error_class = classify_http_error(404)
        assert error_class == MarvelNotFoundError
        logger.info("✅ Not found error classification test completed successfully")

    def test_classify_validation_error(self):
        """Test classification of validation errors."""
        logger.info("Testing HTTP error classification for validation errors")
        error_class = classify_http_error(400)
        assert error_class == MarvelValidationError
        logger.info("✅ Validation error classification test completed successfully")

    def test_classify_rate_limit_error(self):
        """Test classification of rate limit errors."""
        logger.info("Testing HTTP error classification for rate limit errors")
        error_class = classify_http_error(429)
        assert error_class == MarvelRateLimitError
        logger.info("✅ Rate limit error classification test completed successfully")

    def test_classify_server_errors(self):
        """Test classification of server errors."""
        logger.info("Testing HTTP error classification for server errors")
        server_codes = [500, 501, 502, 503, 504]
        for code in server_codes:
            error_class = classify_http_error(code)
            assert error_class == MarvelServerError
        logger.info("✅ Server error classification test completed successfully")

    def test_classify_other_errors(self):
        """Test classification of other HTTP errors."""
        logger.info("Testing HTTP error classification for other errors")
        other_codes = [200, 201, 300, 301, 403, 405, 422]
        for code in other_codes:
            error_class = classify_http_error(code)
            assert error_class == MarvelAPIError
        logger.info("✅ Other error classification test completed successfully")

    def test_classify_with_response_data(self):
        """Test classification with response data (should not affect result)."""
        logger.info("Testing HTTP error classification with response data")
        response_data = {"error": "test"}
        error_class = classify_http_error(404, response_data=response_data)
        assert error_class == MarvelNotFoundError
        logger.info("✅ Error classification with response data test completed successfully")

    def test_classify_with_request_data(self):
        """Test classification with request data (should not affect result)."""
        logger.info("Testing HTTP error classification with request data")
        request_data = {"id": "123"}
        error_class = classify_http_error(401, request_data=request_data)
        assert error_class == MarvelAuthenticationError
        logger.info("✅ Error classification with request data test completed successfully")


class TestCreateMarvelError:
    """Test cases for Marvel error creation.

    Tests the create_marvel_error function to ensure it creates
    appropriate exception instances with correct parameters.
    """

    def test_create_authentication_error(self):
        """Test creating an authentication error."""
        logger.info("Testing Marvel error creation for authentication error")
        error = create_marvel_error(401, message="Invalid API key")

        assert isinstance(error, MarvelAuthenticationError)
        assert error.message == "Invalid API key"
        assert error.status_code == 401
        logger.info("✅ Authentication error creation test completed successfully")

    def test_create_not_found_error(self):
        """Test creating a not found error with resource info."""
        logger.info("Testing Marvel error creation for not found error")
        error = create_marvel_error(
            404, message="Character not found", resource_type="character", resource_id="12345"
        )

        assert isinstance(error, MarvelNotFoundError)
        assert error.message == "Character not found"
        assert error.status_code == 404
        assert error.resource_type == "character"
        assert error.resource_id == "12345"
        logger.info("✅ Not found error creation test completed successfully")

    def test_create_rate_limit_error(self):
        """Test creating a rate limit error with retry info."""
        logger.info("Testing Marvel error creation for rate limit error")
        error = create_marvel_error(429, retry_after=60)

        assert isinstance(error, MarvelRateLimitError)
        assert error.message == "Rate limit exceeded"
        assert error.status_code == 429
        assert error.retry_after == 60
        logger.info("✅ Rate limit error creation test completed successfully")

    def test_create_validation_error(self):
        """Test creating a validation error with validation details."""
        logger.info("Testing Marvel error creation for validation error")
        validation_errors = ["Invalid parameter", "Missing field"]
        error = create_marvel_error(
            400, message="Request validation failed", validation_errors=validation_errors
        )

        assert isinstance(error, MarvelValidationError)
        assert error.message == "Request validation failed"
        assert error.status_code == 400
        assert error.validation_errors == validation_errors
        logger.info("✅ Validation error creation test completed successfully")

    def test_create_server_error(self):
        """Test creating a server error."""
        logger.info("Testing Marvel error creation for server error")
        error = create_marvel_error(500, message="Internal server error")

        assert isinstance(error, MarvelServerError)
        assert error.message == "Internal server error"
        assert error.status_code == 500
        logger.info("✅ Server error creation test completed successfully")

    def test_create_error_with_response_data(self):
        """Test creating an error with response data."""
        logger.info("Testing Marvel error creation with response data")
        response_data = {"error": "Not found"}
        error = create_marvel_error(404, response_data=response_data)

        assert error.response_data == response_data
        logger.info("✅ Error creation with response data test completed successfully")

    def test_create_error_with_request_data(self):
        """Test creating an error with request data."""
        logger.info("Testing Marvel error creation with request data")
        request_data = {"id": "123"}
        error = create_marvel_error(400, request_data=request_data)

        assert error.request_data == request_data
        logger.info("✅ Error creation with request data test completed successfully")

    def test_create_error_default_message(self):
        """Test creating an error with default message."""
        logger.info("Testing Marvel error creation with default messages")
        error = create_marvel_error(404)
        assert error.message == "Resource not found"

        error = create_marvel_error(401)
        assert error.message == "Authentication failed"
        logger.info("✅ Error creation with default message test completed successfully")


class TestHandleHttpxError:
    """Test cases for httpx error handling.

    Tests the handle_httpx_error function to ensure it correctly
    converts httpx errors to Marvel API errors.
    """

    def test_handle_http_status_error(self):
        """Test handling HTTP status errors."""
        logger.info("Testing httpx error handling for HTTP status errors")
        response = Mock()
        response.status_code = 404
        response.reason_phrase = "Not Found"
        response.json.return_value = {"error": "Not found"}

        httpx_error = httpx.HTTPStatusError("Not found", request=Mock(), response=response)
        marvel_error = handle_httpx_error(httpx_error)

        assert isinstance(marvel_error, MarvelNotFoundError)
        assert marvel_error.status_code == 404
        assert "404 error: Not Found" in marvel_error.message
        logger.info("✅ HTTP status error handling test completed successfully")

    def test_handle_http_status_error_with_text_response(self):
        """Test handling HTTP status errors with text response."""
        logger.info("Testing httpx error handling for HTTP status errors with text response")
        response = Mock()
        response.status_code = 500
        response.reason_phrase = "Internal Server Error"
        response.json.side_effect = ValueError("Invalid JSON")
        response.text = "Internal server error"

        httpx_error = httpx.HTTPStatusError("Server error", request=Mock(), response=response)
        marvel_error = handle_httpx_error(httpx_error)

        assert isinstance(marvel_error, MarvelServerError)
        assert marvel_error.status_code == 500
        assert marvel_error.response_data == {"text": "Internal server error"}
        logger.info("✅ HTTP status error with text response handling test completed successfully")

    def test_handle_timeout_exception(self):
        """Test handling timeout exceptions."""
        logger.info("Testing httpx error handling for timeout exceptions")
        timeout_error = httpx.TimeoutException("Request timeout")
        marvel_error = handle_httpx_error(timeout_error)

        assert isinstance(marvel_error, MarvelNetworkError)
        assert "timeout" in marvel_error.message.lower()
        assert marvel_error.original_error == timeout_error
        logger.info("✅ Timeout exception handling test completed successfully")

    def test_handle_connect_error(self):
        """Test handling connection errors."""
        logger.info("Testing httpx error handling for connection errors")
        connect_error = httpx.ConnectError("Connection failed")
        marvel_error = handle_httpx_error(connect_error)

        assert isinstance(marvel_error, MarvelNetworkError)
        assert "connection error" in marvel_error.message.lower()
        assert marvel_error.original_error == connect_error
        logger.info("✅ Connection error handling test completed successfully")

    def test_handle_request_error(self):
        """Test handling other request errors."""
        logger.info("Testing httpx error handling for request errors")
        request_error = httpx.RequestError("Request failed")
        marvel_error = handle_httpx_error(request_error)

        assert isinstance(marvel_error, MarvelNetworkError)
        assert "Request error" in marvel_error.message
        assert marvel_error.original_error == request_error
        logger.info("✅ Request error handling test completed successfully")

    def test_handle_other_httpx_error(self):
        """Test handling other httpx errors."""
        logger.info("Testing httpx error handling for other httpx errors")
        other_error = httpx.HTTPError("Unknown error")
        marvel_error = handle_httpx_error(other_error)

        assert isinstance(marvel_error, MarvelNetworkError)
        assert "Network error" in marvel_error.message
        assert marvel_error.original_error == other_error
        logger.info("✅ Other httpx error handling test completed successfully")

    def test_handle_error_with_request_data(self):
        """Test handling errors with request data."""
        logger.info("Testing httpx error handling with request data")
        request_data = {"id": "123"}
        timeout_error = httpx.TimeoutException("Request timeout")
        marvel_error = handle_httpx_error(timeout_error, request_data=request_data)

        assert marvel_error.request_data == request_data
        logger.info("✅ Error handling with request data test completed successfully")


class TestRetryWithBackoff:
    """Test cases for retry with backoff functionality.

    Tests the retry_with_backoff function to ensure it correctly
    implements retry logic with exponential backoff.
    """

    @pytest.mark.asyncio
    async def test_retry_success_on_first_attempt(self):
        """Test that successful function calls return immediately."""
        logger.info("Testing retry with backoff for success on first attempt")
        func = AsyncMock(return_value="success")

        result = await retry_with_backoff(func)

        assert result == "success"
        assert func.call_count == 1
        logger.info("✅ Retry success on first attempt test completed successfully")

    @pytest.mark.asyncio
    async def test_retry_success_after_failures(self):
        """Test that retry succeeds after initial failures."""
        logger.info("Testing retry with backoff for success after failures")
        func = AsyncMock(
            side_effect=[
                MarvelServerError("Server error"),
                MarvelServerError("Server error"),
                "success",
            ]
        )

        with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
            result = await retry_with_backoff(func, max_retries=3)

            assert result == "success"
            assert func.call_count == 3
            assert mock_sleep.call_count == 2  # Sleep between retries
            logger.info("✅ Retry success after failures test completed successfully")

    @pytest.mark.asyncio
    async def test_retry_exhausted_raises_last_exception(self):
        """Test that retry raises the last exception when exhausted."""
        logger.info("Testing retry with backoff for exhausted retries")
        func = AsyncMock(side_effect=MarvelServerError("Server error"))

        with patch("asyncio.sleep", new_callable=AsyncMock), pytest.raises(
            MarvelServerError, match="Server error"
        ):
            await retry_with_backoff(func, max_retries=2)
        logger.info("✅ Retry exhausted raises last exception test completed successfully")

    @pytest.mark.asyncio
    async def test_retry_non_retryable_error_raises_immediately(self):
        """Test that non-retryable errors are raised immediately."""
        logger.info("Testing retry with backoff for non-retryable errors")
        func = AsyncMock(side_effect=MarvelValidationError("Validation error"))

        with pytest.raises(MarvelValidationError, match="Validation error"):
            await retry_with_backoff(func, max_retries=3)

        assert func.call_count == 1  # Only called once
        logger.info("✅ Retry non-retryable error raises immediately test completed successfully")

    @pytest.mark.asyncio
    async def test_retry_custom_retry_on_errors(self):
        """Test retry with custom retryable error types."""
        logger.info("Testing retry with backoff for custom retryable errors")
        func = AsyncMock(side_effect=MarvelNotFoundError("Not found"))

        with patch("asyncio.sleep", new_callable=AsyncMock):
            with pytest.raises(MarvelNotFoundError):
                await retry_with_backoff(func, max_retries=2, retry_on=[MarvelNotFoundError])

            assert func.call_count == 3  # Initial + 2 retries
            logger.info("✅ Retry custom retryable errors test completed successfully")

    @pytest.mark.asyncio
    async def test_retry_backoff_delay_calculation(self):
        """Test that backoff delay is calculated correctly."""
        logger.info("Testing retry with backoff delay calculation")
        func = AsyncMock(side_effect=MarvelServerError("Server error"))

        with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
            with pytest.raises(MarvelServerError):
                await retry_with_backoff(func, max_retries=3, base_delay=1.0, backoff_factor=2.0)

            # Check that sleep was called with increasing delays
            expected_delays = [1.0, 2.0, 4.0]  # base_delay * backoff_factor^attempt
            actual_delays = [call[0][0] for call in mock_sleep.call_args_list]
            assert actual_delays == expected_delays
            logger.info("✅ Retry backoff delay calculation test completed successfully")

    @pytest.mark.asyncio
    async def test_retry_max_delay_limit(self):
        """Test that delay is capped at max_delay."""
        logger.info("Testing retry with backoff max delay limit")
        func = AsyncMock(side_effect=MarvelServerError("Server error"))

        with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
            with pytest.raises(MarvelServerError):
                await retry_with_backoff(
                    func, max_retries=5, base_delay=1.0, backoff_factor=10.0, max_delay=5.0
                )

            # Check that delays are capped at max_delay
            actual_delays = [call[0][0] for call in mock_sleep.call_args_list]
            assert all(delay <= 5.0 for delay in actual_delays)
            logger.info("✅ Retry max delay limit test completed successfully")


class TestFormatErrorMessage:
    """Test cases for error message formatting.

    Tests the format_error_message function to ensure it creates
    user-friendly error messages with appropriate context.
    """

    def test_format_basic_error(self):
        """Test formatting a basic error message."""
        logger.info("Testing error message formatting for basic error")
        error = MarvelAPIError("Test error", status_code=500)
        message = format_error_message(error)

        assert message == "Test error (Status: 500)"
        logger.info("✅ Basic error formatting test completed successfully")

    def test_format_not_found_error_with_resource_info(self):
        """Test formatting a not found error with resource information."""
        logger.info("Testing error message formatting for not found error with resource info")
        error = MarvelNotFoundError(
            "Character not found", resource_type="character", resource_id="12345"
        )
        message = format_error_message(error)

        assert "Character not found (Status: 404)" in message
        assert "Character with ID 12345 not found" in message
        logger.info("✅ Not found error with resource info formatting test completed successfully")

    def test_format_not_found_error_with_type_only(self):
        """Test formatting a not found error with type only."""
        logger.info("Testing error message formatting for not found error with type only")
        error = MarvelNotFoundError("Comic not found", resource_type="comic")
        message = format_error_message(error)

        assert "Comic not found (Status: 404)" in message
        assert "Comic not found" in message
        logger.info("✅ Not found error with type only formatting test completed successfully")

    def test_format_rate_limit_error_with_retry_after(self):
        """Test formatting a rate limit error with retry information."""
        logger.info("Testing error message formatting for rate limit error with retry after")
        error = MarvelRateLimitError(retry_after=60)
        message = format_error_message(error)

        assert "Rate limit exceeded (Status: 429)" in message
        assert "Retry after 60 seconds" in message
        logger.info("✅ Rate limit error with retry after formatting test completed successfully")

    def test_format_rate_limit_error_without_retry_after(self):
        """Test formatting a rate limit error without retry information."""
        logger.info("Testing error message formatting for rate limit error without retry after")
        error = MarvelRateLimitError()
        message = format_error_message(error)

        assert "Rate limit exceeded (Status: 429)" in message
        assert "Please wait before making more requests" in message
        logger.info("✅ Rate limit error without retry after formatting test completed successfully")

    def test_format_validation_error_with_validation_errors(self):
        """Test formatting a validation error with validation details."""
        logger.info("Testing error message formatting for validation error with validation errors")
        validation_errors = ["Invalid parameter", "Missing field"]
        error = MarvelValidationError(validation_errors=validation_errors)
        message = format_error_message(error)

        assert "Validation failed (Status: 400)" in message
        assert "Validation errors: Invalid parameter, Missing field" in message
        logger.info("✅ Validation error with validation errors formatting test completed successfully")

    def test_format_network_error(self):
        """Test formatting a network error."""
        logger.info("Testing error message formatting for network error")
        error = MarvelNetworkError("Connection failed")
        message = format_error_message(error)

        assert "Connection failed" in message
        assert "Please check your internet connection and try again" in message
        logger.info("✅ Network error formatting test completed successfully")

    def test_format_server_error(self):
        """Test formatting a server error."""
        logger.info("Testing error message formatting for server error")
        error = MarvelServerError("Internal server error")
        message = format_error_message(error)

        assert "Internal server error (Status: 500)" in message
        assert "Please try again later" in message
        logger.info("✅ Server error formatting test completed successfully")

    def test_format_authentication_error(self):
        """Test formatting an authentication error."""
        logger.info("Testing error message formatting for authentication error")
        error = MarvelAuthenticationError("Invalid API key")
        message = format_error_message(error)

        assert "Invalid API key (Status: 401)" in message
        assert "Please check your API keys" in message
        logger.info("✅ Authentication error formatting test completed successfully")


class TestLogError:
    """Test cases for error logging.

    Tests the log_error function to ensure it logs errors
    with appropriate levels and context.
    """

    def test_log_server_error(self):
        """Test logging a server error (should use ERROR level)."""
        logger.info("Testing error logging for server error")
        error = MarvelServerError("Internal server error", status_code=500)

        with patch("logging.getLogger") as mock_get_logger:
            mock_logger = Mock()
            mock_get_logger.return_value = mock_logger

            log_error(error)

            mock_logger.log.assert_called_once()
            call_args = mock_logger.log.call_args
            assert call_args[0][0] == logging.ERROR  # Check log level
            assert "Internal server error (Status: 500)" in call_args[0][1]  # Check message
        logger.info("✅ Server error logging test completed successfully")

    def test_log_rate_limit_error(self):
        """Test logging a rate limit error (should use WARNING level)."""
        logger.info("Testing error logging for rate limit error")
        error = MarvelRateLimitError(retry_after=60)

        with patch("logging.getLogger") as mock_get_logger:
            mock_logger = Mock()
            mock_get_logger.return_value = mock_logger

            log_error(error)

            mock_logger.log.assert_called_once()
            call_args = mock_logger.log.call_args
            assert call_args[0][0] == logging.WARNING  # Check log level
            assert "Rate limit exceeded (Status: 429)" in call_args[0][1]  # Check message
        logger.info("✅ Rate limit error logging test completed successfully")

    def test_log_authentication_error(self):
        """Test logging an authentication error (should use ERROR level)."""
        logger.info("Testing error logging for authentication error")
        error = MarvelAuthenticationError("Invalid API key")

        with patch("logging.getLogger") as mock_get_logger:
            mock_logger = Mock()
            mock_get_logger.return_value = mock_logger

            log_error(error)

            mock_logger.log.assert_called_once()
            call_args = mock_logger.log.call_args
            assert call_args[0][0] == logging.ERROR  # Check log level
            assert "Invalid API key" in call_args[0][1]  # Check message
        logger.info("✅ Authentication error logging test completed successfully")

    def test_log_error_with_context(self):
        """Test logging an error with additional context."""
        logger.info("Testing error logging with additional context")
        error = MarvelNotFoundError(
            "Character not found",
            status_code=404,
            request_data={"id": "123"},
            response_data={"error": "Not found"},
        )

        with patch("logging.getLogger") as mock_get_logger:
            mock_logger = Mock()
            mock_get_logger.return_value = mock_logger

            log_error(error)

            mock_logger.log.assert_called_once()
            call_args = mock_logger.log.call_args
            assert call_args[0][0] == logging.INFO  # Check log level
            message = call_args[0][1]
            assert "status_code=404" in message
            assert "request_data={'id': '123'}" in message
            assert "response_data={'error': 'Not found'}" in message
        logger.info("✅ Error logging with context test completed successfully")

    def test_log_error_with_custom_logger(self):
        """Test logging an error with a custom logger."""
        logger.info("Testing error logging with custom logger")
        error = MarvelAPIError("Test error")
        custom_logger = Mock()

        log_error(error, logger=custom_logger)

        custom_logger.log.assert_called_once()
        call_args = custom_logger.log.call_args
        assert call_args[0][0] == logging.INFO  # Check log level
        assert "Test error" in call_args[0][1]  # Check message
        logger.info("✅ Error logging with custom logger test completed successfully")
