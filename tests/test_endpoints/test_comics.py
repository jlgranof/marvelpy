"""Tests for the ComicsEndpoint class.

This module contains comprehensive tests for the ComicsEndpoint class,
including all comic-related methods and their various parameters.
"""

from typing import Any, Dict
from unittest.mock import Mock, patch

import pytest

from marvelpy.endpoints.comics import ComicsEndpoint
from marvelpy.models.character import CharacterListResponse
from marvelpy.models.comic import ComicListResponse, ComicResponse
from marvelpy.models.creator import CreatorListResponse
from marvelpy.models.event import EventListResponse
from marvelpy.models.story import StoryListResponse


class TestComicsEndpoint:
    """Test cases for the ComicsEndpoint class."""

    def test_init(self):
        """Test ComicsEndpoint initialization."""
        endpoint = ComicsEndpoint(
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

    @pytest.mark.asyncio
    async def test_get_comic(self):
        """Test getting a single comic by ID."""
        endpoint = ComicsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_comic = Mock()
        mock_comic.id = 21366
        mock_comic.title = "Avengers (1963) #1"

        mock_response = Mock()
        mock_response.data = mock_comic

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_comic(21366)

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/comics/21366",
                response_model=ComicResponse,
            )
            assert result == mock_comic

    @pytest.mark.asyncio
    async def test_list_comics_basic(self):
        """Test listing comics with basic parameters."""
        endpoint = ComicsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.list_comics(limit=10, offset=0)

            expected_params = {
                "limit": 10,
                "offset": 0,
            }

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/comics",
                expected_params,
                ComicListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_list_comics_with_filters(self):
        """Test listing comics with various filters."""
        endpoint = ComicsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.list_comics(
                limit=20,
                offset=10,
                format="comic",
                format_type="comic",
                no_variants=True,
                date_descriptor="thisMonth",
                date_range=[2023, 1, 1, 2023, 12, 31],
                title="Avengers",
                title_starts_with="Avengers",
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
                characters=[789, 101],
                series=[202, 303],
                events=[404, 505],
                stories=[606, 707],
                shared_appearances=[808, 909],
                collaborators=[101, 202],
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
                "title": "Avengers",
                "titleStartsWith": "Avengers",
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
                "characters": "789,101",
                "series": "202,303",
                "events": "404,505",
                "stories": "606,707",
                "sharedAppearances": "808,909",
                "collaborators": "101,202",
                "orderBy": "title",
                "contains": "comic",
            }

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/comics",
                expected_params,
                ComicListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_characters_basic(self):
        """Test getting characters for a comic with basic parameters."""
        endpoint = ComicsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_characters(21366, limit=10, offset=0)

            expected_params = {
                "limit": 10,
                "offset": 0,
            }

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/comics/21366/characters",
                expected_params,
                CharacterListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_characters_with_filters(self):
        """Test getting characters for a comic with various filters."""
        endpoint = ComicsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_characters(
                comic_id=21366,
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
                "/v1/public/comics/21366/characters",
                expected_params,
                CharacterListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_creators_basic(self):
        """Test getting creators for a comic with basic parameters."""
        endpoint = ComicsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_creators(21366, limit=10, offset=0)

            expected_params = {
                "limit": 10,
                "offset": 0,
            }

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/comics/21366/creators",
                expected_params,
                CreatorListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_creators_with_filters(self):
        """Test getting creators for a comic with various filters."""
        endpoint = ComicsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_creators(
                comic_id=21366,
                limit=20,
                offset=10,
                first_name="Stan",
                middle_name="Lee",
                last_name="Lee",
                suffix="Jr.",
                name_starts_with="Stan",
                first_name_starts_with="Stan",
                middle_name_starts_with="Lee",
                last_name_starts_with="Lee",
                modified_since="2023-01-01",
                comics=[123, 456],
                series=[789],
                events=[101, 102],
                stories=[201, 202],
                order_by="firstName",
            )

            expected_params = {
                "limit": 20,
                "offset": 10,
                "firstName": "Stan",
                "middleName": "Lee",
                "lastName": "Lee",
                "suffix": "Jr.",
                "nameStartsWith": "Stan",
                "firstNameStartsWith": "Stan",
                "middleNameStartsWith": "Lee",
                "lastNameStartsWith": "Lee",
                "modifiedSince": "2023-01-01",
                "comics": "123,456",
                "series": "789",
                "events": "101,102",
                "stories": "201,202",
                "orderBy": "firstName",
            }

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/comics/21366/creators",
                expected_params,
                CreatorListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_events(self):
        """Test getting events for a comic."""
        endpoint = ComicsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_events(
                comic_id=21366,
                limit=10,
                offset=0,
                name="Civil War",
                name_starts_with="Civil",
                modified_since="2023-01-01",
                creators=[123, 456],
                characters=[789, 101],
                series=[202, 303],
                comics=[404, 505],
                stories=[606, 707],
                order_by="name",
            )

            expected_params = {
                "limit": 10,
                "offset": 0,
                "name": "Civil War",
                "nameStartsWith": "Civil",
                "modifiedSince": "2023-01-01",
                "creators": "123,456",
                "characters": "789,101",
                "series": "202,303",
                "comics": "404,505",
                "stories": "606,707",
                "orderBy": "name",
            }

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/comics/21366/events",
                expected_params,
                EventListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_stories(self):
        """Test getting stories for a comic."""
        endpoint = ComicsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_stories(
                comic_id=21366,
                limit=10,
                offset=0,
                modified_since="2023-01-01",
                comics=[123, 456],
                series=[789],
                events=[101, 102],
                creators=[201, 202],
                characters=[303, 404],
                order_by="id",
            )

            expected_params = {
                "limit": 10,
                "offset": 0,
                "modifiedSince": "2023-01-01",
                "comics": "123,456",
                "series": "789",
                "events": "101,102",
                "creators": "201,202",
                "characters": "303,404",
                "orderBy": "id",
            }

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/comics/21366/stories",
                expected_params,
                StoryListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_list_comics_no_filters(self):
        """Test listing comics with no filters (all optional parameters None)."""
        endpoint = ComicsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.list_comics()

            expected_params: Dict[str, Any] = {}

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/comics",
                expected_params,
                ComicListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_characters_no_filters(self):
        """Test getting characters with no filters (all optional parameters None)."""
        endpoint = ComicsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_characters(21366)

            expected_params: Dict[str, Any] = {}

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/comics/21366/characters",
                expected_params,
                CharacterListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_creators_no_filters(self):
        """Test getting creators with no filters (all optional parameters None)."""
        endpoint = ComicsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_creators(21366)

            expected_params: Dict[str, Any] = {}

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/comics/21366/creators",
                expected_params,
                CreatorListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_events_no_filters(self):
        """Test getting events with no filters (all optional parameters None)."""
        endpoint = ComicsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_events(21366)

            expected_params: Dict[str, Any] = {}

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/comics/21366/events",
                expected_params,
                EventListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_stories_no_filters(self):
        """Test getting stories with no filters (all optional parameters None)."""
        endpoint = ComicsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_stories(21366)

            expected_params: Dict[str, Any] = {}

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/comics/21366/stories",
                expected_params,
                StoryListResponse,
            )
            assert result == mock_response
