"""Base endpoint class for Marvel API interactions.

This module provides the base endpoint class that all Marvel API endpoint
classes inherit from. It provides common functionality for making HTTP requests,
handling errors, and managing authentication.
"""

from typing import Any, Dict, Optional, Type, TypeVar, Union

import httpx

from marvelpy.models.base import BaseListResponse, BaseResponse
from marvelpy.utils.error_handling import (
    create_marvel_error,
    handle_httpx_error,
    retry_with_backoff,
)

T = TypeVar("T", bound=BaseResponse[Any])
U = TypeVar("U", bound=BaseListResponse[Any])


class BaseEndpoint:
    """Base class for all Marvel API endpoints.

    This class provides common functionality for making HTTP requests to the
    Marvel API, including authentication, error handling, and response parsing.

    Attributes:
        base_url: The base URL for the Marvel API
        public_key: The Marvel API public key
        private_key: The Marvel API private key
        timeout: Request timeout in seconds
        max_retries: Maximum number of retries for failed requests
    """

    def __init__(
        self,
        base_url: str,
        public_key: str,
        private_key: str,
        timeout: float = 30.0,
        max_retries: int = 3,
    ) -> None:
        """Initialize the base endpoint.

        Args:
            base_url: The base URL for the Marvel API
            public_key: The Marvel API public key
            private_key: The Marvel API private key
            timeout: Request timeout in seconds (default: 30.0)
            max_retries: Maximum number of retries for failed requests (default: 3)
        """
        self.base_url = base_url.rstrip("/")
        self.public_key = public_key
        self.private_key = private_key
        self.timeout = timeout
        self.max_retries = max_retries

    def _generate_auth_params(self) -> Dict[str, str]:
        """Generate authentication parameters for API requests.

        Returns:
            Dictionary containing timestamp, apikey, and hash parameters
        """
        import hashlib
        import time

        timestamp = str(int(time.time()))
        hash_string = hashlib.md5(
            f"{timestamp}{self.private_key}{self.public_key}".encode()
        ).hexdigest()

        return {
            "ts": timestamp,
            "apikey": self.public_key,
            "hash": hash_string,
        }

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        response_model: Optional[Type[Union[T, U]]] = None,
    ) -> Union[T, U, Dict[str, Any]]:
        """Make an HTTP request to the Marvel API.

        This method handles authentication, error handling, and response parsing
        for all Marvel API requests.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path (e.g., '/v1/public/characters')
            params: Query parameters to include in the request
            response_model: Pydantic model class to parse the response into

        Returns:
            Parsed response as Pydantic model or raw dictionary

        Raises:
            MarvelAPIError: For any Marvel API related errors
            httpx.HTTPError: For HTTP related errors
        """
        # Add authentication parameters
        auth_params = self._generate_auth_params()
        if params is None:
            params = {}
        params.update(auth_params)

        # Build full URL
        url = f"{self.base_url}{endpoint}"

        # Create HTTP client
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            # Define the request function for retry logic
            async def make_request() -> httpx.Response:
                response = await client.request(method, url, params=params)
                response.raise_for_status()
                return response

            # Make request with retry logic
            try:
                response = await retry_with_backoff(
                    make_request,
                    max_retries=self.max_retries,
                )
            except httpx.HTTPError as error:
                raise handle_httpx_error(error, {"url": url, "params": params}) from error
            except Exception as error:
                raise create_marvel_error(
                    status_code=0,  # Use 0 for unknown errors
                    message=str(error),
                    response_data=None,
                    request_data={"url": url, "params": params},
                    original_error=error,
                ) from error

            # Parse response
            try:
                data = response.json()
            except Exception as error:
                raise create_marvel_error(
                    status_code=response.status_code,
                    message="Failed to parse JSON response",
                    response_data=response.text,
                    request_data={"url": url, "params": params},
                    original_error=error,
                ) from error

            # Return parsed model or raw data
            if response_model:
                try:
                    return response_model(**data)
                except Exception as error:
                    raise create_marvel_error(
                        status_code=response.status_code,
                        message="Failed to parse response into model",
                        response_data=data,
                        request_data={"url": url, "params": params},
                        original_error=error,
                    ) from error
            else:
                return data  # type: ignore[no-any-return]

    async def get(
        self,
        endpoint: str,
        item_id: int,
        response_model: Type[T],
    ) -> T:
        """Get a single item by ID.

        Args:
            endpoint: API endpoint path (e.g., '/v1/public/characters')
            item_id: The ID of the item to retrieve
            response_model: Pydantic model class for the response

        Returns:
            Parsed response as Pydantic model

        Raises:
            MarvelAPIError: For any Marvel API related errors
        """
        url = f"{endpoint}/{item_id}"
        result = await self._make_request("GET", url, response_model=response_model)
        return result  # type: ignore[return-value]

    async def list(
        self,
        endpoint: str,
        response_model: Type[U],
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        **filters: Any,
    ) -> U:
        """Get a list of items with optional filtering and pagination.

        Args:
            endpoint: API endpoint path (e.g., '/v1/public/characters')
            response_model: Pydantic model class for the response
            limit: Maximum number of items to return
            offset: Number of items to skip
            **filters: Additional filter parameters

        Returns:
            Parsed response as Pydantic model

        Raises:
            MarvelAPIError: For any Marvel API related errors
        """
        params: Dict[str, Any] = {}

        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        # Add any additional filters
        params.update(filters)

        result = await self._make_request("GET", endpoint, params, response_model)
        return result  # type: ignore[return-value]

    async def get_related(
        self,
        endpoint: str,
        item_id: int,
        related_type: str,
        response_model: Type[U],
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        **filters: Any,
    ) -> U:
        """Get related items for a specific entity.

        Args:
            endpoint: Base API endpoint path (e.g., '/v1/public/characters')
            item_id: The ID of the item to get related items for
            related_type: Type of related items (e.g., 'comics', 'events')
            response_model: Pydantic model class for the response
            limit: Maximum number of items to return
            offset: Number of items to skip
            **filters: Additional filter parameters

        Returns:
            Parsed response as Pydantic model

        Raises:
            MarvelAPIError: For any Marvel API related errors
        """
        url = f"{endpoint}/{item_id}/{related_type}"

        params: Dict[str, Any] = {}

        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        # Add any additional filters
        params.update(filters)

        result = await self._make_request("GET", url, params, response_model)
        return result  # type: ignore[return-value]
