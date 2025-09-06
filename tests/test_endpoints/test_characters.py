"""Tests for the CharactersEndpoint class.

This module contains comprehensive tests for the CharactersEndpoint class,
including all character-related methods and their various parameters.
"""

import logging
from typing import Any, Dict
from unittest.mock import Mock, patch

import pytest

from marvelpy.endpoints.characters import CharactersEndpoint

# Configure logging for tests
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
from marvelpy.models.character import CharacterListResponse
from marvelpy.models.comic import ComicListResponse
from marvelpy.models.event import EventListResponse
from marvelpy.models.series import SeriesListResponse
from marvelpy.models.story import StoryListResponse


class TestCharactersEndpoint:
    """Test cases for the CharactersEndpoint class."""

    def test_init(self):
        """Test CharactersEndpoint initialization."""
        logger.info("Testing CharactersEndpoint initialization")
        
        endpoint = CharactersEndpoint(
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
        
        logger.info("✅ CharactersEndpoint initialization test completed successfully")

    @pytest.mark.asyncio
    async def test_get_character(self):
        """Test getting a single character by ID."""
        endpoint = CharactersEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_character = Mock()
        mock_character.id = 1011334
        mock_character.name = "Iron Man"

        mock_data = Mock()
        mock_data.results = [mock_character]

        mock_response = Mock()
        mock_response.data = mock_data

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_character(1011334)

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/characters/1011334",
                response_model=CharacterListResponse,
            )
            assert result == mock_character

    @pytest.mark.asyncio
    async def test_list_characters_basic(self):
        """Test listing characters with basic parameters."""
        endpoint = CharactersEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.list_characters(limit=10, offset=0)

            expected_params = {
                "limit": 10,
                "offset": 0,
            }

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/characters",
                expected_params,
                CharacterListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_list_characters_with_filters(self):
        """Test listing characters with various filters."""
        endpoint = CharactersEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.list_characters(
                limit=20,
                offset=10,
                name="Iron Man",
                name_starts_with="Iron",
                modified_since="2023-01-01",
                comics=[123, 456],
                series=[789],
                events=[101, 102],
                stories=[201, 202, 203],
                order_by="name",
            )

            expected_params = {
                "limit": 20,
                "offset": 10,
                "name": "Iron Man",
                "nameStartsWith": "Iron",
                "modifiedSince": "2023-01-01",
                "comics": "123,456",
                "series": "789",
                "events": "101,102",
                "stories": "201,202,203",
                "orderBy": "name",
            }

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/characters",
                expected_params,
                CharacterListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_comics_basic(self):
        """Test getting comics for a character with basic parameters."""
        endpoint = CharactersEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_comics(1011334, limit=10, offset=0)

            expected_params = {
                "limit": 10,
                "offset": 0,
            }

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/characters/1011334/comics",
                expected_params,
                ComicListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_comics_with_filters(self):
        """Test getting comics for a character with various filters."""
        endpoint = CharactersEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_comics(
                character_id=1011334,
                limit=20,
                offset=10,
                format="comic",
                format_type="comic",
                no_variants=True,
                date_descriptor="thisMonth",
                date_range=[2023, 1, 1, 2023, 12, 31],
                title="Iron Man",
                title_starts_with="Iron",
                start_year=2023,
                issue_number=1,
                diamond_code="JAN230001",
                digital_id=12345,
                upc="123456789012",
                isbn="978-1-302-90000-0",
                ean="1234567890123",
                issn="1234-5678",
                has_digital_issue=True,
                modified_since="2023-01-01",
                creators=[123, 456],
                series=[789],
                events=[101, 102],
                stories=[201, 202],
                shared_appearances=[301, 302],
                collaborators=[401, 402],
                order_by="title",
                contains="comic",
            )

            expected_params = {
                "limit": 20,
                "offset": 10,
                "format": "comic",
                "formatType": "comic",
                "noVariants": True,
                "dateDescriptor": "thisMonth",
                "dateRange": "2023,1,1,2023,12,31",
                "title": "Iron Man",
                "titleStartsWith": "Iron",
                "startYear": 2023,
                "issueNumber": 1,
                "diamondCode": "JAN230001",
                "digitalId": 12345,
                "upc": "123456789012",
                "isbn": "978-1-302-90000-0",
                "ean": "1234567890123",
                "issn": "1234-5678",
                "hasDigitalIssue": True,
                "modifiedSince": "2023-01-01",
                "creators": "123,456",
                "series": "789",
                "events": "101,102",
                "stories": "201,202",
                "sharedAppearances": "301,302",
                "collaborators": "401,402",
                "orderBy": "title",
                "contains": "comic",
            }

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/characters/1011334/comics",
                expected_params,
                ComicListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_events(self):
        """Test getting events for a character."""
        endpoint = CharactersEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_events(
                character_id=1011334,
                limit=10,
                offset=0,
                name="Civil War",
                name_starts_with="Civil",
                modified_since="2023-01-01",
                creators=[123, 456],
                series=[789],
                comics=[101, 102],
                stories=[201, 202],
                order_by="name",
            )

            expected_params = {
                "limit": 10,
                "offset": 0,
                "name": "Civil War",
                "nameStartsWith": "Civil",
                "modifiedSince": "2023-01-01",
                "creators": "123,456",
                "series": "789",
                "comics": "101,102",
                "stories": "201,202",
                "orderBy": "name",
            }

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/characters/1011334/events",
                expected_params,
                EventListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_series(self):
        """Test getting series for a character."""
        endpoint = CharactersEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_series(
                character_id=1011334,
                limit=10,
                offset=0,
                title="Iron Man",
                title_starts_with="Iron",
                start_year=2023,
                modified_since="2023-01-01",
                comics=[123, 456],
                stories=[201, 202],
                events=[101, 102],
                creators=[301, 302],
                series_type="ongoing",
                contains="comic",
                order_by="title",
            )

            expected_params = {
                "limit": 10,
                "offset": 0,
                "title": "Iron Man",
                "titleStartsWith": "Iron",
                "startYear": 2023,
                "modifiedSince": "2023-01-01",
                "comics": "123,456",
                "stories": "201,202",
                "events": "101,102",
                "creators": "301,302",
                "seriesType": "ongoing",
                "contains": "comic",
                "orderBy": "title",
            }

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/characters/1011334/series",
                expected_params,
                SeriesListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_stories(self):
        """Test getting stories for a character."""
        endpoint = CharactersEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_stories(
                character_id=1011334,
                limit=10,
                offset=0,
                modified_since="2023-01-01",
                comics=[123, 456],
                series=[789],
                events=[101, 102],
                creators=[301, 302],
                order_by="id",
            )

            expected_params = {
                "limit": 10,
                "offset": 0,
                "modifiedSince": "2023-01-01",
                "comics": "123,456",
                "series": "789",
                "events": "101,102",
                "creators": "301,302",
                "orderBy": "id",
            }

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/characters/1011334/stories",
                expected_params,
                StoryListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_list_characters_no_filters(self):
        """Test listing characters with no filters (all optional parameters None)."""
        endpoint = CharactersEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.list_characters()

            expected_params: Dict[str, Any] = {}

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/characters",
                expected_params,
                CharacterListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_comics_no_filters(self):
        """Test getting comics with no filters (all optional parameters None)."""
        endpoint = CharactersEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_comics(1011334)

            expected_params: Dict[str, Any] = {}

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/characters/1011334/comics",
                expected_params,
                ComicListResponse,
            )
            assert result == mock_response
