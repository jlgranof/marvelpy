"""Tests for the EventsEndpoint class.

This module contains comprehensive tests for the EventsEndpoint class,
including all event-related methods and their various parameters.
"""

import logging
from typing import Any, Dict
from unittest.mock import Mock, patch

import pytest

# Configure logging for tests
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

from marvelpy.endpoints.events import EventsEndpoint
from marvelpy.models.character import CharacterListResponse
from marvelpy.models.comic import ComicListResponse
from marvelpy.models.creator import CreatorListResponse
from marvelpy.models.event import EventListResponse
from marvelpy.models.series import SeriesListResponse
from marvelpy.models.story import StoryListResponse


class TestEventsEndpoint:
    """Test cases for the EventsEndpoint class."""

    def test_init(self):
        """Test EventsEndpoint initialization."""
        logger.info("Testing EventsEndpoint initialization")
        
        endpoint = EventsEndpoint(
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
        
        logger.info("✅ EventsEndpoint initialization test completed successfully")

    @pytest.mark.asyncio
    async def test_get_event(self):
        """Test getting a single event by ID."""
        logger.info("Testing getting a single event by ID")
        
        endpoint = EventsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_event = Mock()
        mock_event.id = 269
        mock_event.title = "Secret Invasion"

        mock_data = Mock()
        mock_data.results = [mock_event]

        mock_response = Mock()
        mock_response.data = mock_data

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_event(269)

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/events/269",
                response_model=EventListResponse,
            )
            assert result == mock_event
            
            logger.info("✅ Get event test completed successfully")

    @pytest.mark.asyncio
    async def test_list_events_basic(self):
        """Test listing events with basic parameters."""
        logger.info("Testing listing events with basic parameters")
        
        endpoint = EventsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.list_events(limit=10, offset=0)

            expected_params = {
                "limit": 10,
                "offset": 0,
            }

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/events",
                expected_params,
                EventListResponse,
            )
            assert result == mock_response
            
            logger.info("✅ List events basic test completed successfully")

    @pytest.mark.asyncio
    async def test_list_events_with_filters(self):
        """Test listing events with various filters."""
        logger.info("Testing listing events with various filters")
        
        endpoint = EventsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.list_events(
                limit=20,
                offset=10,
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
                "limit": 20,
                "offset": 10,
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
                "/v1/public/events",
                expected_params,
                EventListResponse,
            )
            assert result == mock_response
            
            logger.info("✅ List events with filters test completed successfully")

    @pytest.mark.asyncio
    async def test_get_characters_basic(self):
        """Test getting characters for an event with basic parameters."""
        logger.info("Testing getting characters for an event with basic parameters")
        
        endpoint = EventsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_characters(269, limit=10, offset=0)

            expected_params = {
                "limit": 10,
                "offset": 0,
            }

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/events/269/characters",
                expected_params,
                CharacterListResponse,
            )
            assert result == mock_response
            
            logger.info("✅ Get characters basic test completed successfully")

    @pytest.mark.asyncio
    async def test_get_characters_with_filters(self):
        """Test getting characters for an event with various filters."""
        logger.info("Testing getting characters for an event with various filters")
        
        endpoint = EventsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_characters(
                event_id=269,
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
                "/v1/public/events/269/characters",
                expected_params,
                CharacterListResponse,
            )
            assert result == mock_response
            
            logger.info("✅ Get characters with filters test completed successfully")

    @pytest.mark.asyncio
    async def test_get_comics_basic(self):
        """Test getting comics for an event with basic parameters."""
        logger.info("Testing getting comics for an event with basic parameters")
        
        endpoint = EventsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_comics(269, limit=10, offset=0)

            expected_params = {
                "limit": 10,
                "offset": 0,
            }

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/events/269/comics",
                expected_params,
                ComicListResponse,
            )
            assert result == mock_response
            
            logger.info("✅ Get comics basic test completed successfully")

    @pytest.mark.asyncio
    async def test_get_comics_with_filters(self):
        """Test getting comics for an event with various filters."""
        logger.info("Testing getting comics for an event with various filters")
        
        endpoint = EventsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_comics(
                event_id=269,
                limit=20,
                offset=10,
                format="comic",
                format_type="comic",
                no_variants=True,
                date_descriptor="thisMonth",
                date_range=[2023, 1, 1, 2023, 12, 31],
                title="Secret Invasion",
                title_starts_with="Secret",
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
                "title": "Secret Invasion",
                "titleStartsWith": "Secret",
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
                "/v1/public/events/269/comics",
                expected_params,
                ComicListResponse,
            )
            assert result == mock_response
            
            logger.info("✅ Get comics with filters test completed successfully")

    @pytest.mark.asyncio
    async def test_get_creators_basic(self):
        """Test getting creators for an event with basic parameters."""
        logger.info("Testing getting creators for an event with basic parameters")
        
        endpoint = EventsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_creators(269, limit=10, offset=0)

            expected_params = {
                "limit": 10,
                "offset": 0,
            }

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/events/269/creators",
                expected_params,
                CreatorListResponse,
            )
            assert result == mock_response
            
            logger.info("✅ Get creators basic test completed successfully")

    @pytest.mark.asyncio
    async def test_get_creators_with_filters(self):
        """Test getting creators for an event with various filters."""
        logger.info("Testing getting creators for an event with various filters")
        
        endpoint = EventsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_creators(
                event_id=269,
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
                "/v1/public/events/269/creators",
                expected_params,
                CreatorListResponse,
            )
            assert result == mock_response
            
            logger.info("✅ Get creators with filters test completed successfully")

    @pytest.mark.asyncio
    async def test_get_series(self):
        """Test getting series for an event."""
        logger.info("Testing getting series for an event")
        
        endpoint = EventsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_series(
                event_id=269,
                limit=10,
                offset=0,
                title="Secret Invasion",
                title_starts_with="Secret",
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
                "title": "Secret Invasion",
                "titleStartsWith": "Secret",
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
                "/v1/public/events/269/series",
                expected_params,
                SeriesListResponse,
            )
            assert result == mock_response
            
            logger.info("✅ Get series test completed successfully")

    @pytest.mark.asyncio
    async def test_get_stories(self):
        """Test getting stories for an event."""
        logger.info("Testing getting stories for an event")
        
        endpoint = EventsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_stories(
                event_id=269,
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
                "/v1/public/events/269/stories",
                expected_params,
                StoryListResponse,
            )
            assert result == mock_response
            
            logger.info("✅ Get stories test completed successfully")

    @pytest.mark.asyncio
    async def test_list_events_no_filters(self):
        """Test listing events with no filters (all optional parameters None)."""
        logger.info("Testing listing events with no filters")
        
        endpoint = EventsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.list_events()

            expected_params: Dict[str, Any] = {}

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/events",
                expected_params,
                EventListResponse,
            )
            assert result == mock_response
            
            logger.info("✅ List events no filters test completed successfully")

    @pytest.mark.asyncio
    async def test_get_characters_no_filters(self):
        """Test getting characters with no filters (all optional parameters None)."""
        logger.info("Testing getting characters with no filters")
        
        endpoint = EventsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_characters(269)

            expected_params: Dict[str, Any] = {}

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/events/269/characters",
                expected_params,
                CharacterListResponse,
            )
            assert result == mock_response
            
            logger.info("✅ Get characters no filters test completed successfully")

    @pytest.mark.asyncio
    async def test_get_comics_no_filters(self):
        """Test getting comics with no filters (all optional parameters None)."""
        logger.info("Testing getting comics with no filters")
        
        endpoint = EventsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_comics(269)

            expected_params: Dict[str, Any] = {}

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/events/269/comics",
                expected_params,
                ComicListResponse,
            )
            assert result == mock_response
            
            logger.info("✅ Get comics no filters test completed successfully")

    @pytest.mark.asyncio
    async def test_get_creators_no_filters(self):
        """Test getting creators with no filters (all optional parameters None)."""
        logger.info("Testing getting creators with no filters")
        
        endpoint = EventsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_creators(269)

            expected_params: Dict[str, Any] = {}

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/events/269/creators",
                expected_params,
                CreatorListResponse,
            )
            assert result == mock_response
            
            logger.info("✅ Get creators no filters test completed successfully")

    @pytest.mark.asyncio
    async def test_get_series_no_filters(self):
        """Test getting series with no filters (all optional parameters None)."""
        logger.info("Testing getting series with no filters")
        
        endpoint = EventsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_series(269)

            expected_params: Dict[str, Any] = {}

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/events/269/series",
                expected_params,
                SeriesListResponse,
            )
            assert result == mock_response
            
            logger.info("✅ Get series no filters test completed successfully")

    @pytest.mark.asyncio
    async def test_get_stories_no_filters(self):
        """Test getting stories with no filters (all optional parameters None)."""
        logger.info("Testing getting stories with no filters")
        
        endpoint = EventsEndpoint(
            base_url="https://gateway.marvel.com",
            public_key="test_public_key",
            private_key="test_private_key",
        )

        mock_response = Mock()

        with patch.object(
            endpoint, "_make_request", return_value=mock_response
        ) as mock_make_request:
            result = await endpoint.get_stories(269)

            expected_params: Dict[str, Any] = {}

            mock_make_request.assert_called_once_with(
                "GET",
                "/v1/public/events/269/stories",
                expected_params,
                StoryListResponse,
            )
            assert result == mock_response
