"""Tests for the StoriesEndpoint class.

This module contains comprehensive tests for the StoriesEndpoint class,
including all story-related methods and their various parameters.
"""

from typing import Any, Dict
from unittest.mock import Mock, patch

import pytest

from marvelpy.endpoints.stories import StoriesEndpoint
from marvelpy.models.character import CharacterListResponse
from marvelpy.models.comic import ComicListResponse
from marvelpy.models.creator import CreatorListResponse
from marvelpy.models.event import EventListResponse
from marvelpy.models.series import SeriesListResponse
from marvelpy.models.story import StoryListResponse


class TestStoriesEndpoint:
    """Test cases for the StoriesEndpoint class."""

    def test_init(self):
        """Test StoriesEndpoint initialization."""
        endpoint = StoriesEndpoint(
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
    async def test_get_story(self):
        """Test getting a single story by ID."""
        endpoint = StoriesEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_story = Mock()
        mock_story.id = 12345
        mock_story.title = "Cover #1"

        mock_data = Mock()
        mock_data.results = [mock_story]

        mock_response = Mock()
        mock_response.data = mock_data

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_story(12345)

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/stories/12345",
                response_model=StoryListResponse,
            )
            assert result == mock_story

    @pytest.mark.asyncio
    async def test_list_stories_basic(self):
        """Test listing stories with basic parameters."""
        endpoint = StoriesEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.list_stories(limit=10, offset=0)

            expected_params = {
                "limit": 10,
                "offset": 0,
            }

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/stories",
                expected_params,
                StoryListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_list_stories_with_filters(self):
        """Test listing stories with various filters."""
        endpoint = StoriesEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.list_stories(
                limit=20,
                offset=10,
                modified_since="2023-01-01",
                comics=[123, 456],
                series=[789],
                events=[101, 102],
                creators=[201, 202],
                characters=[303, 404],
                order_by="id",
            )

            expected_params = {
                "limit": 20,
                "offset": 10,
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
                "/v1/public/stories",
                expected_params,
                StoryListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_characters_basic(self):
        """Test getting characters for a story with basic parameters."""
        endpoint = StoriesEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_characters(12345, limit=10, offset=0)

            expected_params = {
                "limit": 10,
                "offset": 0,
            }

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/stories/12345/characters",
                expected_params,
                CharacterListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_characters_with_filters(self):
        """Test getting characters for a story with various filters."""
        endpoint = StoriesEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_characters(
                story_id=12345,
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
                "/v1/public/stories/12345/characters",
                expected_params,
                CharacterListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_comics_basic(self):
        """Test getting comics for a story with basic parameters."""
        endpoint = StoriesEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_comics(12345, limit=10, offset=0)

            expected_params = {
                "limit": 10,
                "offset": 0,
            }

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/stories/12345/comics",
                expected_params,
                ComicListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_comics_with_filters(self):
        """Test getting comics for a story with various filters."""
        endpoint = StoriesEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_comics(
                story_id=12345,
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
                "/v1/public/stories/12345/comics",
                expected_params,
                ComicListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_creators_basic(self):
        """Test getting creators for a story with basic parameters."""
        endpoint = StoriesEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_creators(12345, limit=10, offset=0)

            expected_params = {
                "limit": 10,
                "offset": 0,
            }

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/stories/12345/creators",
                expected_params,
                CreatorListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_creators_with_filters(self):
        """Test getting creators for a story with various filters."""
        endpoint = StoriesEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_creators(
                story_id=12345,
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
                "/v1/public/stories/12345/creators",
                expected_params,
                CreatorListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_events(self):
        """Test getting events for a story."""
        endpoint = StoriesEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_events(
                story_id=12345,
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
                "/v1/public/stories/12345/events",
                expected_params,
                EventListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_series(self):
        """Test getting series for a story."""
        endpoint = StoriesEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_series(
                story_id=12345,
                limit=10,
                offset=0,
                title="Avengers",
                title_starts_with="Avengers",
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
                "title": "Avengers",
                "titleStartsWith": "Avengers",
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
                "/v1/public/stories/12345/series",
                expected_params,
                SeriesListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_list_stories_no_filters(self):
        """Test listing stories with no filters (all optional parameters None)."""
        endpoint = StoriesEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.list_stories()

            expected_params: Dict[str, Any] = {}

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/stories",
                expected_params,
                StoryListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_characters_no_filters(self):
        """Test getting characters with no filters (all optional parameters None)."""
        endpoint = StoriesEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_characters(12345)

            expected_params: Dict[str, Any] = {}

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/stories/12345/characters",
                expected_params,
                CharacterListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_comics_no_filters(self):
        """Test getting comics with no filters (all optional parameters None)."""
        endpoint = StoriesEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_comics(12345)

            expected_params: Dict[str, Any] = {}

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/stories/12345/comics",
                expected_params,
                ComicListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_creators_no_filters(self):
        """Test getting creators with no filters (all optional parameters None)."""
        endpoint = StoriesEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_creators(12345)

            expected_params: Dict[str, Any] = {}

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/stories/12345/creators",
                expected_params,
                CreatorListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_events_no_filters(self):
        """Test getting events with no filters (all optional parameters None)."""
        endpoint = StoriesEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_events(12345)

            expected_params: Dict[str, Any] = {}

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/stories/12345/events",
                expected_params,
                EventListResponse,
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_series_no_filters(self):
        """Test getting series with no filters (all optional parameters None)."""
        endpoint = StoriesEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_series(12345)

            expected_params: Dict[str, Any] = {}

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/stories/12345/series",
                expected_params,
                SeriesListResponse,
            )
            assert result == mock_response
