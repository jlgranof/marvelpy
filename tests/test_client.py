"""Comprehensive tests for the enhanced MarvelClient."""

import logging
from unittest.mock import MagicMock, patch

import pytest

from marvelpy.client import MarvelClient
from marvelpy.models.character import Character, CharacterListResponse
from marvelpy.models.comic import Comic, ComicListResponse
from marvelpy.models.creator import CreatorListResponse
from marvelpy.models.event import EventListResponse
from marvelpy.models.series import SeriesListResponse
from marvelpy.models.story import StoryListResponse

# Configure logging for unit tests
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class TestMarvelClient:
    """Test cases for the enhanced MarvelClient."""

    @pytest.fixture
    def client(self):
        """Create a MarvelClient instance for testing."""
        return MarvelClient(
            public_key="test_public_key",
            private_key="test_private_key",
            timeout=5.0,
            max_retries=1,
        )

    def test_client_initialization(self, client):
        """Test MarvelClient initialization."""
        logger.info("Testing MarvelClient initialization")

        assert client.public_key == "test_public_key"
        assert client.private_key == "test_private_key"
        assert client.timeout == 5.0
        assert client.max_retries == 1
        assert client.base_url == MarvelClient.BASE_URL

        # Check that all endpoint attributes are initialized
        endpoints = ["characters", "comics", "events", "series", "stories", "creators"]
        for endpoint in endpoints:
            assert hasattr(client, endpoint), f"Missing {endpoint} endpoint"
            logger.info(f"✅ {endpoint} endpoint initialized")

        logger.info("✅ MarvelClient initialization successful")

    def test_client_initialization_with_custom_base_url(self):
        """Test MarvelClient initialization with custom base URL."""
        custom_url = "https://custom.marvel.com"
        client = MarvelClient(
            public_key="test_public_key",
            private_key="test_private_key",
            base_url=custom_url,
        )
        assert client.base_url == custom_url

    @pytest.mark.asyncio
    async def test_context_manager(self, client):
        """Test async context manager."""
        with patch.object(client, "close") as mock_close:
            async with client as ctx_client:
                assert ctx_client is client
            mock_close.assert_called_once()

    @pytest.mark.asyncio
    async def test_close(self, client):
        """Test close method (no-op since endpoints use context managers)."""
        # The close method should not raise any exceptions
        await client.close()

        # Since the close method is a no-op, we just verify it completes successfully
        assert True

    # ============================================================================
    # CHARACTER METHODS TESTS
    # ============================================================================

    @pytest.mark.asyncio
    async def test_get_character(self, client):
        """Test getting a single character by ID."""
        mock_character = MagicMock(spec=Character)
        mock_character.id = 1009368
        mock_character.name = "Iron Man"

        with patch.object(client.characters, "get_character", return_value=mock_character):
            result = await client.get_character(1009368)

            assert result == mock_character
            client.characters.get_character.assert_called_once_with(1009368)

    @pytest.mark.asyncio
    async def test_list_characters(self, client):
        """Test listing characters with filtering."""
        mock_response = MagicMock(spec=CharacterListResponse)

        with patch.object(client.characters, "list_characters", return_value=mock_response):
            result = await client.list_characters(
                limit=10, name_starts_with="Spider", comics=[123, 456]
            )

            assert result == mock_response
            client.characters.list_characters.assert_called_once_with(
                limit=10,
                offset=None,
                name=None,
                name_starts_with="Spider",
                modified_since=None,
                comics=[123, 456],
                series=None,
                events=None,
                stories=None,
                order_by=None,
            )

    @pytest.mark.asyncio
    async def test_search_characters(self, client):
        """Test searching for characters by name."""
        mock_response = MagicMock(spec=CharacterListResponse)

        with patch.object(client.characters, "list_characters", return_value=mock_response):
            result = await client.search_characters("iron man", limit=5)

            assert result == mock_response
            client.characters.list_characters.assert_called_once_with(
                name_starts_with="iron man",
                limit=5,
                offset=None,
            )

    @pytest.mark.asyncio
    async def test_get_character_comics(self, client):
        """Test getting comics for a character."""
        mock_response = MagicMock(spec=ComicListResponse)

        with patch.object(client.characters, "get_comics", return_value=mock_response):
            result = await client.get_character_comics(1009368, limit=5)

            assert result == mock_response
            client.characters.get_comics.assert_called_once_with(
                character_id=1009368,
                limit=5,
                offset=None,
                format=None,
                format_type=None,
                no_variants=None,
                date_descriptor=None,
                date_range=None,
                diamond_code=None,
                digital_id=None,
                upc=None,
                isbn=None,
                ean=None,
                issn=None,
                has_digital_issue=None,
                modified_since=None,
                creators=None,
                series=None,
                events=None,
                stories=None,
                shared_appearances=None,
                collaborators=None,
                order_by=None,
            )

    @pytest.mark.asyncio
    async def test_get_character_events(self, client):
        """Test getting events for a character."""
        mock_response = MagicMock(spec=EventListResponse)

        with patch.object(client.characters, "get_events", return_value=mock_response):
            result = await client.get_character_events(1009368, limit=3)

            assert result == mock_response
            client.characters.get_events.assert_called_once_with(
                character_id=1009368,
                limit=3,
                offset=None,
                name=None,
                name_starts_with=None,
                modified_since=None,
                creators=None,
                series=None,
                comics=None,
                stories=None,
                order_by=None,
            )

    @pytest.mark.asyncio
    async def test_get_character_series(self, client):
        """Test getting series for a character."""
        mock_response = MagicMock(spec=SeriesListResponse)

        with patch.object(client.characters, "get_series", return_value=mock_response):
            result = await client.get_character_series(1009368, limit=5)

            assert result == mock_response
            client.characters.get_series.assert_called_once_with(
                character_id=1009368,
                limit=5,
                offset=None,
                title=None,
                title_starts_with=None,
                start_year=None,
                modified_since=None,
                comics=None,
                stories=None,
                events=None,
                creators=None,
                series_type=None,
                contains=None,
                order_by=None,
            )

    @pytest.mark.asyncio
    async def test_get_character_stories(self, client):
        """Test getting stories for a character."""
        mock_response = MagicMock(spec=StoryListResponse)

        with patch.object(client.characters, "get_stories", return_value=mock_response):
            result = await client.get_character_stories(1009368, limit=5)

            assert result == mock_response
            client.characters.get_stories.assert_called_once_with(
                character_id=1009368,
                limit=5,
                offset=None,
                modified_since=None,
                comics=None,
                series=None,
                events=None,
                creators=None,
                order_by=None,
            )

    @pytest.mark.asyncio
    async def test_get_character_creators(self, client):
        """Test getting creators for a character."""
        mock_response = MagicMock(spec=CreatorListResponse)

        with patch.object(client.characters, "get_creators", return_value=mock_response):
            result = await client.get_character_creators(1009368, limit=5)

            assert result == mock_response
            client.characters.get_creators.assert_called_once_with(
                character_id=1009368,
                limit=5,
                offset=None,
                modified_since=None,
                comics=None,
                series=None,
                events=None,
                stories=None,
                order_by=None,
            )

    # ============================================================================
    # COMIC METHODS TESTS
    # ============================================================================

    @pytest.mark.asyncio
    async def test_get_comic(self, client):
        """Test getting a single comic by ID."""
        mock_comic = MagicMock(spec=Comic)
        mock_comic.id = 21366
        mock_comic.title = "Avengers (1963) #1"

        with patch.object(client.comics, "get_comic", return_value=mock_comic):
            result = await client.get_comic(21366)

            assert result == mock_comic
            client.comics.get_comic.assert_called_once_with(21366)

    @pytest.mark.asyncio
    async def test_list_comics(self, client):
        """Test listing comics with filtering."""
        mock_response = MagicMock(spec=ComicListResponse)

        with patch.object(client.comics, "list_comics", return_value=mock_response):
            result = await client.list_comics(limit=10, format="comic", characters=[1009368])

            assert result == mock_response
            client.comics.list_comics.assert_called_once_with(
                limit=10,
                offset=None,
                format="comic",
                format_type=None,
                no_variants=None,
                date_descriptor=None,
                date_range=None,
                diamond_code=None,
                digital_id=None,
                upc=None,
                isbn=None,
                ean=None,
                issn=None,
                has_digital_issue=None,
                modified_since=None,
                creators=None,
                characters=[1009368],
                series=None,
                events=None,
                stories=None,
                shared_appearances=None,
                collaborators=None,
                order_by=None,
            )

    @pytest.mark.asyncio
    async def test_search_comics(self, client):
        """Test searching for comics by title."""
        mock_response = MagicMock(spec=ComicListResponse)

        with patch.object(client.comics, "list_comics", return_value=mock_response):
            result = await client.search_comics("amazing spider-man", limit=5)

            assert result == mock_response
            client.comics.list_comics.assert_called_once_with(
                title_starts_with="amazing spider-man",
                limit=5,
                offset=None,
            )

    @pytest.mark.asyncio
    async def test_get_comic_characters(self, client):
        """Test getting characters for a comic."""
        mock_response = MagicMock(spec=CharacterListResponse)

        with patch.object(client.comics, "get_characters", return_value=mock_response):
            result = await client.get_comic_characters(21366, limit=5)

            assert result == mock_response
            client.comics.get_characters.assert_called_once_with(
                comic_id=21366,
                limit=5,
                offset=None,
                name=None,
                name_starts_with=None,
                modified_since=None,
                series=None,
                events=None,
                stories=None,
                order_by=None,
            )

    @pytest.mark.asyncio
    async def test_get_comic_creators(self, client):
        """Test getting creators for a comic."""
        mock_response = MagicMock(spec=CreatorListResponse)

        with patch.object(client.comics, "get_creators", return_value=mock_response):
            result = await client.get_comic_creators(21366, limit=5)

            assert result == mock_response
            client.comics.get_creators.assert_called_once_with(
                comic_id=21366,
                limit=5,
                offset=None,
                first_name=None,
                middle_name=None,
                last_name=None,
                suffix=None,
                name_starts_with=None,
                first_name_starts_with=None,
                middle_name_starts_with=None,
                last_name_starts_with=None,
                modified_since=None,
                comics=None,
                series=None,
                events=None,
                stories=None,
                order_by=None,
            )

    @pytest.mark.asyncio
    async def test_get_comic_events(self, client):
        """Test getting events for a comic."""
        mock_response = MagicMock(spec=EventListResponse)

        with patch.object(client.comics, "get_events", return_value=mock_response):
            result = await client.get_comic_events(21366, limit=3)

            assert result == mock_response
            client.comics.get_events.assert_called_once_with(
                comic_id=21366,
                limit=3,
                offset=None,
                name=None,
                name_starts_with=None,
                modified_since=None,
                creators=None,
                characters=None,
                series=None,
                stories=None,
                order_by=None,
            )

    @pytest.mark.asyncio
    async def test_get_comic_stories(self, client):
        """Test getting stories for a comic."""
        mock_response = MagicMock(spec=StoryListResponse)

        with patch.object(client.comics, "get_stories", return_value=mock_response):
            result = await client.get_comic_stories(21366, limit=5)

            assert result == mock_response
            client.comics.get_stories.assert_called_once_with(
                comic_id=21366,
                limit=5,
                offset=None,
                modified_since=None,
                series=None,
                events=None,
                creators=None,
                characters=None,
                order_by=None,
            )

    # ============================================================================
    # INTEGRATION TESTS
    # ============================================================================

    def test_all_methods_exist(self, client):
        """Test that all expected methods exist on the client."""
        expected_methods = [
            # Character methods
            "get_character",
            "list_characters",
            "search_characters",
            "get_character_comics",
            "get_character_events",
            "get_character_series",
            "get_character_stories",
            "get_character_creators",
            # Comic methods
            "get_comic",
            "list_comics",
            "search_comics",
            "get_comic_characters",
            "get_comic_creators",
            "get_comic_events",
            "get_comic_stories",
            # Event methods
            "get_event",
            "list_events",
            "search_events",
            "get_event_characters",
            "get_event_comics",
            "get_event_creators",
            "get_event_series",
            "get_event_stories",
            # Series methods
            "get_series",
            "list_series",
            "search_series",
            "get_series_characters",
            "get_series_comics",
            "get_series_creators",
            "get_series_events",
            "get_series_stories",
            # Story methods
            "get_story",
            "list_stories",
            "get_story_characters",
            "get_story_comics",
            "get_story_creators",
            "get_story_events",
            "get_story_series",
            # Creator methods
            "get_creator",
            "list_creators",
            "search_creators",
            "get_creator_comics",
            "get_creator_events",
            "get_creator_series",
            "get_creator_stories",
        ]

        for method_name in expected_methods:
            assert hasattr(client, method_name), f"Method {method_name} not found on client"
            method = getattr(client, method_name)
            assert callable(method), f"Method {method_name} is not callable"

    def test_endpoint_attributes_exist(self, client):
        """Test that all endpoint attributes exist and are properly initialized."""
        endpoints = ["characters", "comics", "events", "series", "stories", "creators"]

        for endpoint_name in endpoints:
            assert hasattr(client, endpoint_name), f"Endpoint {endpoint_name} not found"
            endpoint = getattr(client, endpoint_name)
            assert endpoint is not None, f"Endpoint {endpoint_name} is None"

    def test_method_count(self, client):
        """Test that we have the expected number of methods."""
        # Count public methods (excluding private methods starting with _)
        public_methods = [method for method in dir(client) if not method.startswith("_")]

        # We expect at least 58 methods (as mentioned in the client)
        # This includes all the endpoint methods plus some utility methods
        assert len(public_methods) >= 58, f"Expected at least 58 methods, got {len(public_methods)}"

        # Print the methods for debugging
        print(f"Found {len(public_methods)} public methods:")
        for method in sorted(public_methods):
            print(f"  - {method}")
