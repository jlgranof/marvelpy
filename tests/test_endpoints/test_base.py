"""Tests for the base endpoint class.

This module contains comprehensive tests for the BaseEndpoint class,
including authentication, error handling, and request functionality.
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from marvelpy.endpoints.base import BaseEndpoint


class TestBaseEndpoint:
    """Test cases for the BaseEndpoint class."""

    def test_init(self):
        """Test BaseEndpoint initialization."""
        endpoint = BaseEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
            timeout=30.0,
            max_retries=3,
        )

        assert endpoint.base_url == "https://gateway.marvel.com"
        assert endpoint.public_key == "test_public_key"
        assert endpoint.private_key == "test_private_key"
        assert endpoint.timeout == 30.0
        assert endpoint.max_retries == 3

    def test_init_strips_trailing_slash(self):
        """Test that BaseEndpoint strips trailing slash from base_url."""
        endpoint = BaseEndpoint(
            base_url="https://gateway.marvel.com/",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        assert endpoint.base_url == "https://gateway.marvel.com"

    def test_generate_auth_params(self):
        """Test authentication parameter generation."""
        endpoint = BaseEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        with patch("time.time", return_value=1234567890), patch("hashlib.md5") as mock_md5:
            mock_hash = Mock()
            mock_hash.hexdigest.return_value = "test_hash"
            mock_md5.return_value = mock_hash

            params = endpoint._generate_auth_params()

            assert "ts" in params
            assert "apikey" in params
            assert "hash" in params
            assert params["ts"] == "1234567890"
            assert params["apikey"] == "test_public_key"
            assert params["hash"] == "test_hash"

    @pytest.mark.asyncio
    async def test_make_request_success(self):
        """Test successful request with response model."""
        endpoint = BaseEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()
        mock_response.json.return_value = {"code": 200, "data": {"id": 1}}
        mock_response.status_code = 200

        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.request = AsyncMock(
                return_value=mock_response
            )

            with patch.object(
                endpoint,
                "_generate_auth_params",
                return_value={"ts": "123", "apikey": "test", "hash": "hash"},
            ), patch(
                "marvelpy.utils.error_handling.retry_with_backoff", return_value=mock_response
            ):
                result = await endpoint._make_request(
                    "GET",
                    "/v1/public/characters/1",
                    response_model=Mock,
                )

                assert result is not None

    @pytest.mark.asyncio
    async def test_make_request_without_response_model(self):
        """Test request without response model returns raw data."""
        endpoint = BaseEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()
        mock_response.json.return_value = {"code": 200, "data": {"id": 1}}
        mock_response.status_code = 200

        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.request = AsyncMock(
                return_value=mock_response
            )

            with patch.object(
                endpoint,
                "_generate_auth_params",
                return_value={"ts": "123", "apikey": "test", "hash": "hash"},
            ), patch(
                "marvelpy.utils.error_handling.retry_with_backoff", return_value=mock_response
            ):
                result = await endpoint._make_request(
                    "GET",
                    "/v1/public/characters/1",
                )

                assert result == {"code": 200, "data": {"id": 1}}

    @pytest.mark.asyncio
    async def test_get_method(self):
        """Test the get method."""
        endpoint = BaseEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        with patch.object(endpoint, "_make_request", return_value=Mock()) as mock_make_request:
            await endpoint.get("/v1/public/characters", 1, Mock)

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/characters/1",
                response_model=Mock,
            )

    @pytest.mark.asyncio
    async def test_list_method(self):
        """Test the list method."""
        endpoint = BaseEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        with patch.object(endpoint, "_make_request", return_value=Mock()) as mock_make_request:
            await endpoint.list(
                "/v1/public/characters",
                Mock,
                limit=10,
                offset=0,
                name="Iron Man",
            )

            expected_params = {
                "limit": 10,
                "offset": 0,
                "name": "Iron Man",
            }

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/characters",
                expected_params,
                Mock,
            )

    @pytest.mark.asyncio
    async def test_get_related_method(self):
        """Test the get_related method."""
        endpoint = BaseEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        with patch.object(endpoint, "_make_request", return_value=Mock()) as mock_make_request:
            await endpoint.get_related(
                "/v1/public/characters",
                1,
                "comics",
                Mock,
                limit=10,
                offset=0,
            )

            expected_params = {
                "limit": 10,
                "offset": 0,
            }

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/characters/1/comics",
                expected_params,
                Mock,
            )
