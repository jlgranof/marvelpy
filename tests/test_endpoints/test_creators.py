"""Tests for the CreatorsEndpoint class.

This module contains comprehensive tests for the CreatorsEndpoint class,
including all creator-related methods and their various parameters.
"""

from typing import Any, Dict
from unittest.mock import Mock, patch

import pytest

from marvelpy.endpoints.creators import CreatorsEndpoint
from marvelpy.models.character import CharacterListResponse
from marvelpy.models.comic import ComicListResponse
from marvelpy.models.creator import CreatorListResponse
from marvelpy.models.event import EventListResponse
from marvelpy.models.series import SeriesListResponse
from marvelpy.models.story import StoryListResponse


class TestCreatorsEndpoint:
    """Test cases for the CreatorsEndpoint class."""

    def test_init(self):
        """Test CreatorsEndpoint initialization."""
        endpoint = CreatorsEndpoint(
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
    async def test_get_creator(self):
        """Test getting a single creator by ID."""
        endpoint = CreatorsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_creator = Mock()
        mock_creator.id = 30
        mock_creator.full_name = "Stan Lee"

        mock_data = Mock()
        mock_data.results = [mock_creator]

        mock_response = Mock()
        mock_response.data = mock_data

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_creator(30)

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/creators/30",
                response_model=CreatorListResponse,
            )
            assert result == mock_creator

    @pytest.mark.asyncio
    async def test_list_creators_basic(self):
        """Test listing creators with basic parameters."""
        endpoint = CreatorsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.list_creators(limit=10, offset=0)

            expected_params = {
                "limit": 10,
                "offset": 0,
            }

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/creators",
                expected_params,
                CreatorListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_list_creators_with_filters(self):
        """Test listing creators with various filters."""
        endpoint = CreatorsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.list_creators(
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
                "/v1/public/creators",
                expected_params,
                CreatorListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_characters_basic(self):
        """Test getting characters for a creator with basic parameters."""
        endpoint = CreatorsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_characters(30, limit=10, offset=0)

            expected_params = {
                "limit": 10,
                "offset": 0,
            }

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/creators/30/characters",
                expected_params,
                CharacterListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_characters_with_filters(self):
        """Test getting characters for a creator with various filters."""
        endpoint = CreatorsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_characters(
                creator_id=30,
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
                "/v1/public/creators/30/characters",
                expected_params,
                CharacterListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_comics_basic(self):
        """Test getting comics for a creator with basic parameters."""
        endpoint = CreatorsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_comics(30, limit=10, offset=0)

            expected_params = {
                "limit": 10,
                "offset": 0,
            }

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/creators/30/comics",
                expected_params,
                ComicListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_comics_with_filters(self):
        """Test getting comics for a creator with various filters."""
        endpoint = CreatorsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_comics(
                creator_id=30,
                limit=20,
                offset=10,
                format="comic",
                format_type="comic",
                no_variants=True,
                date_descriptor="thisMonth",
                date_range=[2023, 1, 1, 2023, 12, 31],
                title="Amazing Spider-Man",
                title_starts_with="Amazing",
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
                "title": "Amazing Spider-Man",
                "titleStartsWith": "Amazing",
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
                "/v1/public/creators/30/comics",
                expected_params,
                ComicListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_events(self):
        """Test getting events for a creator."""
        endpoint = CreatorsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_events(
                creator_id=30,
                limit=10,
                offset=0,
                name="Secret Invasion",
                name_starts_with="Secret",
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
                "name": "Secret Invasion",
                "nameStartsWith": "Secret",
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
                "/v1/public/creators/30/events",
                expected_params,
                EventListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_series(self):
        """Test getting series for a creator."""
        endpoint = CreatorsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_series(
                creator_id=30,
                limit=10,
                offset=0,
                title="Amazing Spider-Man",
                title_starts_with="Amazing",
                start_year=2023,
                modified_since="2023-01-01",
                comics=[123, 456],
                stories=[201, 202],
                events=[101, 102],
                creators=[301, 302],
                characters=[303, 404],
                series_type="ongoing",
                contains="comic",
                order_by="title",
            )

            expected_params = {
                "limit": 10,
                "offset": 0,
                "title": "Amazing Spider-Man",
                "titleStartsWith": "Amazing",
                "startYear": 2023,
                "modifiedSince": "2023-01-01",
                "comics": "123,456",
                "stories": "201,202",
                "events": "101,102",
                "creators": "301,302",
                "characters": "303,404",
                "seriesType": "ongoing",
                "contains": "comic",
                "orderBy": "title",
            }

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/creators/30/series",
                expected_params,
                SeriesListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_stories(self):
        """Test getting stories for a creator."""
        endpoint = CreatorsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_stories(
                creator_id=30,
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
                "/v1/public/creators/30/stories",
                expected_params,
                StoryListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_list_creators_no_filters(self):
        """Test listing creators with no filters (all optional parameters None)."""
        endpoint = CreatorsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.list_creators()

            expected_params: Dict[str, Any] = {}

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/creators",
                expected_params,
                CreatorListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_characters_no_filters(self):
        """Test getting characters with no filters (all optional parameters None)."""
        endpoint = CreatorsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_characters(30)

            expected_params: Dict[str, Any] = {}

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/creators/30/characters",
                expected_params,
                CharacterListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_comics_no_filters(self):
        """Test getting comics with no filters (all optional parameters None)."""
        endpoint = CreatorsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_comics(30)

            expected_params: Dict[str, Any] = {}

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/creators/30/comics",
                expected_params,
                ComicListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_events_no_filters(self):
        """Test getting events with no filters (all optional parameters None)."""
        endpoint = CreatorsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_events(30)

            expected_params: Dict[str, Any] = {}

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/creators/30/events",
                expected_params,
                EventListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_series_no_filters(self):
        """Test getting series with no filters (all optional parameters None)."""
        endpoint = CreatorsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_series(30)

            expected_params: Dict[str, Any] = {}

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/creators/30/series",
                expected_params,
                SeriesListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_stories_no_filters(self):
        """Test getting stories with no filters (all optional parameters None)."""
        endpoint = CreatorsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_stories(30)

            expected_params: Dict[str, Any] = {}

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/creators/30/stories",
                expected_params,
                StoryListResponse,
            )
            assert result == mock_response
