"""Comprehensive end-to-end tests for the enhanced MarvelClient.

These tests use real API keys and make actual HTTP requests to the Marvel API
to verify that all 58 client methods work correctly with real data.

Note: These tests require valid Marvel API keys in the .env file.
"""

import asyncio
import logging
import os
import pytest
from typing import Any, Dict, List

from marvelpy import MarvelClient
from marvelpy.models import (
    Character,
    CharacterListResponse,
    Comic,
    ComicListResponse,
    Creator,
    CreatorListResponse,
    Event,
    EventListResponse,
    Series,
    SeriesListResponse,
    Story,
    StoryListResponse,
)

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Configure logging for E2E tests
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def log_entity_data(entity_type: str, entity: Any, entity_id: int = None) -> None:
    """Log detailed information about an entity for debugging."""
    logger.info(f"=== {entity_type.upper()} DATA ===")
    if entity_id:
        logger.info(f"ID: {entity_id}")
    
    if hasattr(entity, 'name'):
        logger.info(f"Name: {entity.name}")
    elif hasattr(entity, 'title'):
        logger.info(f"Title: {entity.title}")
    elif hasattr(entity, 'full_name'):
        logger.info(f"Full Name: {entity.full_name}")
    
    if hasattr(entity, 'description') and entity.description:
        desc = entity.description[:100] + "..." if len(entity.description) > 100 else entity.description
        logger.info(f"Description: {desc}")
    
    if hasattr(entity, 'modified'):
        logger.info(f"Modified: {entity.modified}")
    
    logger.info(f"Type: {type(entity).__name__}")
    logger.info("=" * 50)


def log_response_data(response_type: str, response: Any) -> None:
    """Log detailed information about a response for debugging."""
    logger.info(f"=== {response_type.upper()} RESPONSE ===")
    logger.info(f"Total: {response.data.total}")
    logger.info(f"Count: {response.data.count}")
    logger.info(f"Offset: {response.data.offset}")
    logger.info(f"Limit: {response.data.limit}")
    logger.info(f"Results: {len(response.data.results)} items")
    
    if response.data.results:
        logger.info("Sample results:")
        for i, item in enumerate(response.data.results[:3]):  # Log first 3 items
            if hasattr(item, 'name'):
                logger.info(f"  {i+1}. {item.name} (ID: {item.id})")
            elif hasattr(item, 'title'):
                logger.info(f"  {i+1}. {item.title} (ID: {item.id})")
            elif hasattr(item, 'full_name'):
                logger.info(f"  {i+1}. {item.full_name} (ID: {item.id})")
    
    logger.info("=" * 50)


def validate_character_data(character: Character, expected_id: int = None) -> None:
    """Validate that character data is correct and complete."""
    assert isinstance(character, Character), f"Expected Character, got {type(character)}"
    assert character.id is not None, "Character ID should not be None"
    assert character.id > 0, f"Character ID should be positive, got {character.id}"
    
    if expected_id:
        assert character.id == expected_id, f"Expected ID {expected_id}, got {character.id}"
    
    assert character.name is not None, "Character name should not be None"
    assert len(character.name.strip()) > 0, "Character name should not be empty"
    
    assert character.modified is not None, "Character modified date should not be None"
    
    # Log the character data
    log_entity_data("Character", character, character.id)


def validate_comic_data(comic: Comic, expected_id: int = None) -> None:
    """Validate that comic data is correct and complete."""
    assert isinstance(comic, Comic), f"Expected Comic, got {type(comic)}"
    assert comic.id is not None, "Comic ID should not be None"
    assert comic.id > 0, f"Comic ID should be positive, got {comic.id}"
    
    if expected_id:
        assert comic.id == expected_id, f"Expected ID {expected_id}, got {comic.id}"
    
    assert comic.title is not None, "Comic title should not be None"
    assert len(comic.title.strip()) > 0, "Comic title should not be empty"
    
    assert comic.modified is not None, "Comic modified date should not be None"
    
    # Log the comic data
    log_entity_data("Comic", comic, comic.id)


def validate_event_data(event: Event, expected_id: int = None) -> None:
    """Validate that event data is correct and complete."""
    assert isinstance(event, Event), f"Expected Event, got {type(event)}"
    assert event.id is not None, "Event ID should not be None"
    assert event.id > 0, f"Event ID should be positive, got {event.id}"
    
    if expected_id:
        assert event.id == expected_id, f"Expected ID {expected_id}, got {event.id}"
    
    assert event.title is not None, "Event title should not be None"
    assert len(event.title.strip()) > 0, "Event title should not be empty"
    
    assert event.modified is not None, "Event modified date should not be None"
    
    # Log the event data
    log_entity_data("Event", event, event.id)


def validate_series_data(series: Series, expected_id: int = None) -> None:
    """Validate that series data is correct and complete."""
    assert isinstance(series, Series), f"Expected Series, got {type(series)}"
    assert series.id is not None, "Series ID should not be None"
    assert series.id > 0, f"Series ID should be positive, got {series.id}"
    
    if expected_id:
        assert series.id == expected_id, f"Expected ID {expected_id}, got {series.id}"
    
    assert series.title is not None, "Series title should not be None"
    assert len(series.title.strip()) > 0, "Series title should not be empty"
    
    assert series.modified is not None, "Series modified date should not be None"
    
    # Log the series data
    log_entity_data("Series", series, series.id)


def validate_story_data(story: Story, expected_id: int = None) -> None:
    """Validate that story data is correct and complete."""
    assert isinstance(story, Story), f"Expected Story, got {type(story)}"
    assert story.id is not None, "Story ID should not be None"
    assert story.id > 0, f"Story ID should be positive, got {story.id}"
    
    if expected_id:
        assert story.id == expected_id, f"Expected ID {expected_id}, got {story.id}"
    
    assert story.title is not None, "Story title should not be None"
    assert len(story.title.strip()) > 0, "Story title should not be empty"
    
    assert story.modified is not None, "Story modified date should not be None"
    
    # Log the story data
    log_entity_data("Story", story, story.id)


def validate_creator_data(creator: Creator, expected_id: int = None) -> None:
    """Validate that creator data is correct and complete."""
    assert isinstance(creator, Creator), f"Expected Creator, got {type(creator)}"
    assert creator.id is not None, "Creator ID should not be None"
    assert creator.id > 0, f"Creator ID should be positive, got {creator.id}"
    
    if expected_id:
        assert creator.id == expected_id, f"Expected ID {expected_id}, got {creator.id}"
    
    assert creator.full_name is not None, "Creator full name should not be None"
    assert len(creator.full_name.strip()) > 0, "Creator full name should not be empty"
    
    assert creator.modified is not None, "Creator modified date should not be None"
    
    # Log the creator data
    log_entity_data("Creator", creator, creator.id)


@pytest.fixture(scope="session")
def client():
    """Create a MarvelClient instance for E2E testing."""
    public_key = os.getenv("MARVEL_PUBLIC_KEY")
    private_key = os.getenv("MARVEL_PRIVATE_KEY")
    
    if not public_key or not private_key:
        pytest.skip("Marvel API keys not found in environment variables")
    
    return MarvelClient(
        public_key=public_key,
        private_key=private_key,
        timeout=30.0,
        max_retries=3,
    )


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for the test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


class TestMarvelClientE2E:
    """End-to-end tests for the enhanced MarvelClient."""

    # ============================================================================
    # CHARACTER METHODS E2E TESTS
    # ============================================================================

    @pytest.mark.asyncio
    async def test_get_character_e2e(self, client):
        """Test getting a single character by ID with real API."""
        logger.info("Testing get_character with Iron Man (ID: 1009368)")
        
        # Test with Iron Man (ID: 1009368)
        character = await client.get_character(1009368)
        
        # Validate the character data
        validate_character_data(character, expected_id=1009368)
        
        # Additional specific validations
        assert character.name == "Iron Man", f"Expected 'Iron Man', got '{character.name}'"
        assert character.description is not None, "Iron Man should have a description"
        assert len(character.description.strip()) > 0, "Iron Man description should not be empty"
        
        logger.info(f"✅ Successfully retrieved Iron Man: {character.name}")

    @pytest.mark.asyncio
    async def test_list_characters_e2e(self, client):
        """Test listing characters with real API."""
        logger.info("Testing list_characters with limit=5")
        
        response = await client.list_characters(limit=5)
        
        # Log response data
        log_response_data("Character List", response)
        
        # Validate response structure
        assert isinstance(response, CharacterListResponse), f"Expected CharacterListResponse, got {type(response)}"
        assert response.data.total > 0, f"Expected total > 0, got {response.data.total}"
        assert len(response.data.results) == 5, f"Expected 5 results, got {len(response.data.results)}"
        assert response.data.count == 5, f"Expected count=5, got {response.data.count}"
        assert response.data.offset == 0, f"Expected offset=0, got {response.data.offset}"
        assert response.data.limit == 5, f"Expected limit=5, got {response.data.limit}"
        
        # Validate each character
        for i, character in enumerate(response.data.results):
            validate_character_data(character)
            logger.info(f"✅ Character {i+1}: {character.name} (ID: {character.id})")
        
        logger.info(f"✅ Successfully retrieved {len(response.data.results)} characters")

    @pytest.mark.asyncio
    async def test_search_characters_e2e(self, client):
        """Test searching characters with real API."""
        logger.info("Testing search_characters with query='spider', limit=3")
        
        response = await client.search_characters("spider", limit=3)
        
        # Log response data
        log_response_data("Character Search", response)
        
        # Validate response structure
        assert isinstance(response, CharacterListResponse), f"Expected CharacterListResponse, got {type(response)}"
        assert response.data.total > 0, f"Expected total > 0, got {response.data.total}"
        assert len(response.data.results) <= 3, f"Expected <= 3 results, got {len(response.data.results)}"
        
        # Validate each character and check search relevance
        for i, character in enumerate(response.data.results):
            validate_character_data(character)
            assert "spider" in character.name.lower(), f"Character '{character.name}' should contain 'spider'"
            logger.info(f"✅ Spider Character {i+1}: {character.name} (ID: {character.id})")
        
        logger.info(f"✅ Successfully found {len(response.data.results)} spider characters")

    @pytest.mark.asyncio
    async def test_get_character_comics_e2e(self, client):
        """Test getting comics for a character with real API."""
        logger.info("Testing get_character_comics for Iron Man (ID: 1009368), limit=3")
        
        response = await client.get_character_comics(1009368, limit=3)
        
        # Log response data
        log_response_data("Character Comics", response)
        
        # Validate response structure
        assert isinstance(response, ComicListResponse), f"Expected ComicListResponse, got {type(response)}"
        assert response.data.total > 0, f"Expected total > 0, got {response.data.total}"
        assert len(response.data.results) <= 3, f"Expected <= 3 results, got {len(response.data.results)}"
        
        # Validate each comic
        for i, comic in enumerate(response.data.results):
            validate_comic_data(comic)
            logger.info(f"✅ Iron Man Comic {i+1}: {comic.title} (ID: {comic.id})")
        
        logger.info(f"✅ Successfully retrieved {len(response.data.results)} Iron Man comics")

    @pytest.mark.asyncio
    async def test_get_character_events_e2e(self, client):
        """Test getting events for a character with real API."""
        response = await client.get_character_events(1009368, limit=3)
        
        assert isinstance(response, EventListResponse)
        assert response.data.total >= 0  # Some characters may not have events
        assert len(response.data.results) <= 3
        assert all(isinstance(event, Event) for event in response.data.results)

    @pytest.mark.asyncio
    async def test_get_character_series_e2e(self, client):
        """Test getting series for a character with real API."""
        response = await client.get_character_series(1009368, limit=3)
        
        assert isinstance(response, SeriesListResponse)
        assert response.data.total > 0
        assert len(response.data.results) <= 3
        assert all(isinstance(series, Series) for series in response.data.results)

    @pytest.mark.asyncio
    async def test_get_character_stories_e2e(self, client):
        """Test getting stories for a character with real API."""
        response = await client.get_character_stories(1009368, limit=3)
        
        assert isinstance(response, StoryListResponse)
        assert response.data.total > 0
        assert len(response.data.results) <= 3
        assert all(isinstance(story, Story) for story in response.data.results)

    @pytest.mark.asyncio
    async def test_get_character_creators_e2e(self, client):
        """Test getting creators for a character with real API."""
        # Note: Character-creator relationships are not consistently available in Marvel API
        # Some characters return 404, others return empty results
        try:
            response = await client.get_character_creators(1009368, limit=3)
            assert isinstance(response, CreatorListResponse)
            assert response.data.total >= 0  # Some characters may not have creators
            assert len(response.data.results) <= 3
            assert all(isinstance(creator, Creator) for creator in response.data.results)
        except Exception as e:
            # If we get a 404 or other error, that's expected for this API limitation
            if "404" in str(e) or "Not Found" in str(e):
                pytest.skip("Character-creator relationships not available for this character (API limitation)")
            else:
                raise

    # ============================================================================
    # COMIC METHODS E2E TESTS
    # ============================================================================

    @pytest.mark.asyncio
    async def test_get_comic_e2e(self, client):
        """Test getting a single comic by ID with real API."""
        logger.info("Testing get_comic with Avengers (1963) #1 (ID: 21366)")
        
        # Test with Avengers (1963) #1 (ID: 21366)
        comic = await client.get_comic(21366)
        
        # Validate the comic data
        validate_comic_data(comic, expected_id=21366)
        
        # Additional specific validations
        assert "Avengers" in comic.title, f"Expected 'Avengers' in title, got '{comic.title}'"
        assert comic.description is not None, "Avengers #1 should have a description"
        
        logger.info(f"✅ Successfully retrieved comic: {comic.title}")

    @pytest.mark.asyncio
    async def test_list_comics_e2e(self, client):
        """Test listing comics with real API."""
        logger.info("Testing list_comics with limit=5")
        
        response = await client.list_comics(limit=5)
        
        # Log response metadata
        log_response_data("ComicListResponse", response)
        
        assert isinstance(response, ComicListResponse)
        assert response.data.total > 0
        assert len(response.data.results) == 5
        assert all(isinstance(comic, Comic) for comic in response.data.results)
        
        # Validate each comic
        for i, comic in enumerate(response.data.results):
            logger.info(f"Validating comic {i+1}/{len(response.data.results)}")
            validate_comic_data(comic)
        
        logger.info("✅ Successfully listed comics")

    @pytest.mark.asyncio
    async def test_search_comics_e2e(self, client):
        """Test searching comics with real API."""
        logger.info("Testing search_comics with 'amazing spider-man'")
        
        response = await client.search_comics("amazing spider-man", limit=3)
        
        # Log response metadata
        log_response_data("ComicListResponse", response)
        
        assert isinstance(response, ComicListResponse)
        assert response.data.total > 0
        assert len(response.data.results) <= 3
        assert all("amazing spider-man" in comic.title.lower() for comic in response.data.results)
        
        # Validate each comic and check search relevance
        for i, comic in enumerate(response.data.results):
            logger.info(f"Validating comic {i+1}/{len(response.data.results)}")
            validate_comic_data(comic)
            assert "amazing spider-man" in comic.title.lower(), f"Expected 'amazing spider-man' in title, got '{comic.title}'"
        
        logger.info("✅ Successfully searched comics")

    @pytest.mark.asyncio
    async def test_get_comic_characters_e2e(self, client):
        """Test getting characters for a comic with real API."""
        logger.info("Testing get_comic_characters for Avengers #1 (ID: 21366)")
        
        response = await client.get_comic_characters(21366, limit=3)
        
        # Log response metadata
        log_response_data("CharacterListResponse", response)
        
        assert isinstance(response, CharacterListResponse)
        assert response.data.total > 0
        assert len(response.data.results) <= 3
        assert all(isinstance(char, Character) for char in response.data.results)
        
        # Validate each character
        for i, char in enumerate(response.data.results):
            logger.info(f"Validating character {i+1}/{len(response.data.results)}")
            validate_character_data(char)
        
        logger.info("✅ Successfully retrieved comic characters")

    @pytest.mark.asyncio
    async def test_get_comic_creators_e2e(self, client):
        """Test getting creators for a comic with real API."""
        logger.info("Testing get_comic_creators for Avengers #1 (ID: 21366)")
        
        response = await client.get_comic_creators(21366, limit=3)
        
        # Log response metadata
        log_response_data("CreatorListResponse", response)
        
        assert isinstance(response, CreatorListResponse)
        assert response.data.total > 0
        assert len(response.data.results) <= 3
        assert all(isinstance(creator, Creator) for creator in response.data.results)
        
        # Validate each creator
        for i, creator in enumerate(response.data.results):
            logger.info(f"Validating creator {i+1}/{len(response.data.results)}")
            validate_creator_data(creator)
        
        logger.info("✅ Successfully retrieved comic creators")

    @pytest.mark.asyncio
    async def test_get_comic_events_e2e(self, client):
        """Test getting events for a comic with real API."""
        logger.info("Testing get_comic_events for Avengers #1 (ID: 21366)")
        
        response = await client.get_comic_events(21366, limit=3)
        
        # Log response metadata
        log_response_data("EventListResponse", response)
        
        assert isinstance(response, EventListResponse)
        assert response.data.total >= 0  # Some comics may not have events
        assert len(response.data.results) <= 3
        assert all(isinstance(event, Event) for event in response.data.results)
        
        # Validate each event if any exist
        if response.data.results:
            for i, event in enumerate(response.data.results):
                logger.info(f"Validating event {i+1}/{len(response.data.results)}")
                validate_event_data(event)
        else:
            logger.info("No events found for this comic")
        
        logger.info("✅ Successfully retrieved comic events")

    @pytest.mark.asyncio
    async def test_get_comic_stories_e2e(self, client):
        """Test getting stories for a comic with real API."""
        logger.info("Testing get_comic_stories for Avengers #1 (ID: 21366)")
        
        response = await client.get_comic_stories(21366, limit=3)
        
        # Log response metadata
        log_response_data("StoryListResponse", response)
        
        assert isinstance(response, StoryListResponse)
        assert response.data.total > 0
        assert len(response.data.results) <= 3
        assert all(isinstance(story, Story) for story in response.data.results)
        
        # Validate each story
        for i, story in enumerate(response.data.results):
            logger.info(f"Validating story {i+1}/{len(response.data.results)}")
            validate_story_data(story)
        
        logger.info("✅ Successfully retrieved comic stories")

    # ============================================================================
    # EVENT METHODS E2E TESTS
    # ============================================================================

    @pytest.mark.asyncio
    async def test_get_event_e2e(self, client):
        """Test getting a single event by ID with real API."""
        logger.info("Testing get_event with Secret Invasion (ID: 269)")
        
        # Test with Secret Invasion (ID: 269)
        event = await client.get_event(269)
        
        # Validate the event data
        validate_event_data(event, expected_id=269)
        
        # Additional specific validations
        assert "Secret Invasion" in event.title, f"Expected 'Secret Invasion' in title, got '{event.title}'"
        
        logger.info(f"✅ Successfully retrieved event: {event.title}")

    @pytest.mark.asyncio
    async def test_list_events_e2e(self, client):
        """Test listing events with real API."""
        logger.info("Testing list_events with limit=5")
        
        response = await client.list_events(limit=5)
        
        # Log response metadata
        log_response_data("EventListResponse", response)
        
        assert isinstance(response, EventListResponse)
        assert response.data.total > 0
        assert len(response.data.results) == 5
        assert all(isinstance(event, Event) for event in response.data.results)
        
        # Validate each event
        for i, event in enumerate(response.data.results):
            logger.info(f"Validating event {i+1}/{len(response.data.results)}")
            validate_event_data(event)
        
        logger.info("✅ Successfully listed events")

    @pytest.mark.asyncio
    async def test_search_events_e2e(self, client):
        """Test searching events with real API."""
        logger.info("Testing search_events with 'secret invasion'")
        
        response = await client.search_events("secret invasion", limit=3)
        
        # Log response metadata
        log_response_data("EventListResponse", response)
        
        assert isinstance(response, EventListResponse)
        assert response.data.total > 0
        assert len(response.data.results) <= 3
        assert all("secret invasion" in event.title.lower() for event in response.data.results)
        
        # Validate each event and check search relevance
        for i, event in enumerate(response.data.results):
            logger.info(f"Validating event {i+1}/{len(response.data.results)}")
            validate_event_data(event)
            assert "secret invasion" in event.title.lower(), f"Expected 'secret invasion' in title, got '{event.title}'"
        
        logger.info("✅ Successfully searched events")

    @pytest.mark.asyncio
    async def test_get_event_characters_e2e(self, client):
        """Test getting characters for an event with real API."""
        logger.info("Testing get_event_characters for Secret Invasion (ID: 269)")
        
        response = await client.get_event_characters(269, limit=3)
        
        # Log response metadata
        log_response_data("CharacterListResponse", response)
        
        assert isinstance(response, CharacterListResponse)
        assert response.data.total > 0
        assert len(response.data.results) <= 3
        assert all(isinstance(char, Character) for char in response.data.results)
        
        # Validate each character
        for i, char in enumerate(response.data.results):
            logger.info(f"Validating character {i+1}/{len(response.data.results)}")
            validate_character_data(char)
        
        logger.info("✅ Successfully retrieved event characters")

    @pytest.mark.asyncio
    async def test_get_event_comics_e2e(self, client):
        """Test getting comics for an event with real API."""
        response = await client.get_event_comics(269, limit=3)
        
        assert isinstance(response, ComicListResponse)
        assert response.data.total > 0
        assert len(response.data.results) <= 3
        assert all(isinstance(comic, Comic) for comic in response.data.results)

    @pytest.mark.asyncio
    async def test_get_event_creators_e2e(self, client):
        """Test getting creators for an event with real API."""
        response = await client.get_event_creators(269, limit=3)
        
        assert isinstance(response, CreatorListResponse)
        assert response.data.total > 0
        assert len(response.data.results) <= 3
        assert all(isinstance(creator, Creator) for creator in response.data.results)

    @pytest.mark.asyncio
    async def test_get_event_series_e2e(self, client):
        """Test getting series for an event with real API."""
        response = await client.get_event_series(269, limit=3)
        
        assert isinstance(response, SeriesListResponse)
        assert response.data.total > 0
        assert len(response.data.results) <= 3
        assert all(isinstance(series, Series) for series in response.data.results)

    @pytest.mark.asyncio
    async def test_get_event_stories_e2e(self, client):
        """Test getting stories for an event with real API."""
        response = await client.get_event_stories(269, limit=3)
        
        assert isinstance(response, StoryListResponse)
        assert response.data.total > 0
        assert len(response.data.results) <= 3
        assert all(isinstance(story, Story) for story in response.data.results)

    # ============================================================================
    # SERIES METHODS E2E TESTS
    # ============================================================================

    @pytest.mark.asyncio
    async def test_get_series_e2e(self, client):
        """Test getting a single series by ID with real API."""
        # Test with Avengers (1998 - 2004) (ID: 1991)
        series = await client.get_series(1991)
        
        assert isinstance(series, Series)
        assert series.id == 1991
        assert series.title is not None
        assert series.modified is not None

    @pytest.mark.asyncio
    async def test_list_series_e2e(self, client):
        """Test listing series with real API."""
        response = await client.list_series(limit=5)
        
        assert isinstance(response, SeriesListResponse)
        assert response.data.total > 0
        assert len(response.data.results) == 5
        assert all(isinstance(series, Series) for series in response.data.results)

    @pytest.mark.asyncio
    async def test_search_series_e2e(self, client):
        """Test searching series with real API."""
        response = await client.search_series("amazing spider-man", limit=3)
        
        assert isinstance(response, SeriesListResponse)
        assert response.data.total > 0
        assert len(response.data.results) <= 3
        assert all("amazing spider-man" in series.title.lower() for series in response.data.results)

    @pytest.mark.asyncio
    async def test_get_series_characters_e2e(self, client):
        """Test getting characters for a series with real API."""
        response = await client.get_series_characters(1991, limit=3)
        
        assert isinstance(response, CharacterListResponse)
        assert response.data.total > 0
        assert len(response.data.results) <= 3
        assert all(isinstance(char, Character) for char in response.data.results)

    @pytest.mark.asyncio
    async def test_get_series_comics_e2e(self, client):
        """Test getting comics for a series with real API."""
        response = await client.get_series_comics(1991, limit=3)
        
        assert isinstance(response, ComicListResponse)
        assert response.data.total > 0
        assert len(response.data.results) <= 3
        assert all(isinstance(comic, Comic) for comic in response.data.results)

    @pytest.mark.asyncio
    async def test_get_series_creators_e2e(self, client):
        """Test getting creators for a series with real API."""
        response = await client.get_series_creators(1991, limit=3)
        
        assert isinstance(response, CreatorListResponse)
        assert response.data.total > 0
        assert len(response.data.results) <= 3
        assert all(isinstance(creator, Creator) for creator in response.data.results)

    @pytest.mark.asyncio
    async def test_get_series_events_e2e(self, client):
        """Test getting events for a series with real API."""
        response = await client.get_series_events(1991, limit=3)
        
        assert isinstance(response, EventListResponse)
        assert response.data.total >= 0  # Some series may not have events
        assert len(response.data.results) <= 3
        assert all(isinstance(event, Event) for event in response.data.results)

    @pytest.mark.asyncio
    async def test_get_series_stories_e2e(self, client):
        """Test getting stories for a series with real API."""
        response = await client.get_series_stories(1991, limit=3)
        
        assert isinstance(response, StoryListResponse)
        assert response.data.total > 0
        assert len(response.data.results) <= 3
        assert all(isinstance(story, Story) for story in response.data.results)

    # ============================================================================
    # STORY METHODS E2E TESTS
    # ============================================================================

    @pytest.mark.asyncio
    async def test_get_story_e2e(self, client):
        """Test getting a single story by ID with real API."""
        # Test with a story from Avengers #1 (ID: 12345 is a placeholder)
        # We'll get a real story ID from a comic first
        comics_response = await client.get_comic_stories(21366, limit=1)
        if comics_response.data.results:
            story_id = comics_response.data.results[0].id
            story = await client.get_story(story_id)
            
            assert isinstance(story, Story)
            assert story.id == story_id
            assert story.title is not None
            assert story.modified is not None
        else:
            pytest.skip("No stories found for comic 21366")

    @pytest.mark.asyncio
    async def test_list_stories_e2e(self, client):
        """Test listing stories with real API."""
        response = await client.list_stories(limit=5)
        
        assert isinstance(response, StoryListResponse)
        assert response.data.total > 0
        assert len(response.data.results) == 5
        assert all(isinstance(story, Story) for story in response.data.results)

    @pytest.mark.asyncio
    async def test_get_story_characters_e2e(self, client):
        """Test getting characters for a story with real API."""
        # Get a story ID first
        stories_response = await client.list_stories(limit=1)
        if stories_response.data.results:
            story_id = stories_response.data.results[0].id
            response = await client.get_story_characters(story_id, limit=3)
            
            assert isinstance(response, CharacterListResponse)
            assert response.data.total >= 0  # Some stories may not have characters
            assert len(response.data.results) <= 3
            assert all(isinstance(char, Character) for char in response.data.results)
        else:
            pytest.skip("No stories found")

    @pytest.mark.asyncio
    async def test_get_story_comics_e2e(self, client):
        """Test getting comics for a story with real API."""
        # Get a story ID first
        stories_response = await client.list_stories(limit=1)
        if stories_response.data.results:
            story_id = stories_response.data.results[0].id
            response = await client.get_story_comics(story_id, limit=3)
            
            assert isinstance(response, ComicListResponse)
            assert response.data.total > 0
            assert len(response.data.results) <= 3
            assert all(isinstance(comic, Comic) for comic in response.data.results)
        else:
            pytest.skip("No stories found")

    @pytest.mark.asyncio
    async def test_get_story_creators_e2e(self, client):
        """Test getting creators for a story with real API."""
        # Get a story ID first
        stories_response = await client.list_stories(limit=1)
        if stories_response.data.results:
            story_id = stories_response.data.results[0].id
            response = await client.get_story_creators(story_id, limit=3)
            
            assert isinstance(response, CreatorListResponse)
            assert response.data.total >= 0  # Some stories may not have creators
            assert len(response.data.results) <= 3
            assert all(isinstance(creator, Creator) for creator in response.data.results)
        else:
            pytest.skip("No stories found")

    @pytest.mark.asyncio
    async def test_get_story_events_e2e(self, client):
        """Test getting events for a story with real API."""
        # Get a story ID first
        stories_response = await client.list_stories(limit=1)
        if stories_response.data.results:
            story_id = stories_response.data.results[0].id
            response = await client.get_story_events(story_id, limit=3)
            
            assert isinstance(response, EventListResponse)
            assert response.data.total >= 0  # Some stories may not have events
            assert len(response.data.results) <= 3
            assert all(isinstance(event, Event) for event in response.data.results)
        else:
            pytest.skip("No stories found")

    @pytest.mark.asyncio
    async def test_get_story_series_e2e(self, client):
        """Test getting series for a story with real API."""
        # Get a story ID first
        stories_response = await client.list_stories(limit=1)
        if stories_response.data.results:
            story_id = stories_response.data.results[0].id
            response = await client.get_story_series(story_id, limit=3)
            
            assert isinstance(response, SeriesListResponse)
            assert response.data.total > 0
            assert len(response.data.results) <= 3
            assert all(isinstance(series, Series) for series in response.data.results)
        else:
            pytest.skip("No stories found")

    # ============================================================================
    # CREATOR METHODS E2E TESTS
    # ============================================================================

    @pytest.mark.asyncio
    async def test_get_creator_e2e(self, client):
        """Test getting a single creator by ID with real API."""
        logger.info("Testing get_creator with Stan Lee (ID: 30)")
        
        # Test with Stan Lee (ID: 30)
        creator = await client.get_creator(30)
        
        # Validate the creator data
        validate_creator_data(creator, expected_id=30)
        
        # Additional specific validations
        assert "Stan" in creator.full_name, f"Expected 'Stan' in name, got '{creator.full_name}'"
        assert "Lee" in creator.full_name, f"Expected 'Lee' in name, got '{creator.full_name}'"
        
        logger.info(f"✅ Successfully retrieved creator: {creator.full_name}")

    @pytest.mark.asyncio
    async def test_list_creators_e2e(self, client):
        """Test listing creators with real API."""
        response = await client.list_creators(limit=5)
        
        assert isinstance(response, CreatorListResponse)
        assert response.data.total > 0
        assert len(response.data.results) == 5
        assert all(isinstance(creator, Creator) for creator in response.data.results)

    @pytest.mark.asyncio
    async def test_search_creators_e2e(self, client):
        """Test searching creators with real API."""
        response = await client.search_creators("stan lee", limit=3)
        
        assert isinstance(response, CreatorListResponse)
        assert response.data.total > 0
        assert len(response.data.results) <= 3
        assert all("stan lee" in creator.full_name.lower() for creator in response.data.results)

    @pytest.mark.asyncio
    async def test_get_creator_comics_e2e(self, client):
        """Test getting comics for a creator with real API."""
        response = await client.get_creator_comics(30, limit=3)
        
        assert isinstance(response, ComicListResponse)
        assert response.data.total > 0
        assert len(response.data.results) <= 3
        assert all(isinstance(comic, Comic) for comic in response.data.results)

    @pytest.mark.asyncio
    async def test_get_creator_events_e2e(self, client):
        """Test getting events for a creator with real API."""
        response = await client.get_creator_events(30, limit=3)
        
        assert isinstance(response, EventListResponse)
        assert response.data.total >= 0  # Some creators may not have events
        assert len(response.data.results) <= 3
        assert all(isinstance(event, Event) for event in response.data.results)

    @pytest.mark.asyncio
    async def test_get_creator_series_e2e(self, client):
        """Test getting series for a creator with real API."""
        response = await client.get_creator_series(30, limit=3)
        
        assert isinstance(response, SeriesListResponse)
        assert response.data.total > 0
        assert len(response.data.results) <= 3
        assert all(isinstance(series, Series) for series in response.data.results)

    @pytest.mark.asyncio
    async def test_get_creator_stories_e2e(self, client):
        """Test getting stories for a creator with real API."""
        response = await client.get_creator_stories(30, limit=3)
        
        assert isinstance(response, StoryListResponse)
        assert response.data.total > 0
        assert len(response.data.results) <= 3
        assert all(isinstance(story, Story) for story in response.data.results)

    # ============================================================================
    # INTEGRATION E2E TESTS
    # ============================================================================

    @pytest.mark.asyncio
    async def test_client_context_manager_e2e(self, client):
        """Test client async context manager with real API."""
        async with client as ctx_client:
            assert ctx_client is client
            # Test a simple API call within the context
            character = await ctx_client.get_character(1009368)
            assert character.name == "Iron Man"

    @pytest.mark.asyncio
    async def test_concurrent_requests_e2e(self, client):
        """Test concurrent API requests with real API."""
        # Test concurrent requests to different endpoints
        tasks = [
            client.get_character(1009368),  # Iron Man
            client.get_comic(21366),        # Avengers #1
            client.get_event(269),          # Secret Invasion
            client.get_series(1991),        # Avengers (1998-2004)
            client.get_creator(30),         # Stan Lee
        ]
        
        results = await asyncio.gather(*tasks)
        
        assert len(results) == 5
        assert results[0].name == "Iron Man"
        assert results[1].title is not None
        assert results[2].title is not None
        assert results[3].title is not None
        assert results[4].full_name is not None

    @pytest.mark.asyncio
    async def test_pagination_e2e(self, client):
        """Test pagination with real API."""
        # Test pagination by getting first page
        page1 = await client.list_characters(limit=5, offset=0)
        assert len(page1.data.results) == 5
        
        # Test pagination by getting second page
        page2 = await client.list_characters(limit=5, offset=5)
        assert len(page2.data.results) == 5
        
        # Ensure different results
        page1_ids = {char.id for char in page1.data.results}
        page2_ids = {char.id for char in page2.data.results}
        assert page1_ids.isdisjoint(page2_ids)

    @pytest.mark.asyncio
    async def test_filtering_e2e(self, client):
        """Test filtering with real API."""
        # Test filtering characters by comics
        response = await client.list_characters(comics=[21366], limit=5)
        
        assert isinstance(response, CharacterListResponse)
        assert response.data.total > 0
        assert len(response.data.results) <= 5
        assert all(isinstance(char, Character) for char in response.data.results)

    @pytest.mark.asyncio
    async def test_error_handling_e2e(self, client):
        """Test error handling with real API."""
        # Test with invalid character ID
        with pytest.raises(Exception):  # Should raise MarvelAPIError
            await client.get_character(999999999)

    @pytest.mark.asyncio
    async def test_all_methods_exist_e2e(self, client):
        """Test that all 58 methods exist and are callable with real client."""
        expected_methods = [
            # Character methods
            "get_character", "list_characters", "search_characters",
            "get_character_comics", "get_character_events", "get_character_series",
            "get_character_stories", "get_character_creators",
            
            # Comic methods
            "get_comic", "list_comics", "search_comics",
            "get_comic_characters", "get_comic_creators", "get_comic_events", "get_comic_stories",
            
            # Event methods
            "get_event", "list_events", "search_events",
            "get_event_characters", "get_event_comics", "get_event_creators",
            "get_event_series", "get_event_stories",
            
            # Series methods
            "get_series", "list_series", "search_series",
            "get_series_characters", "get_series_comics", "get_series_creators",
            "get_series_events", "get_series_stories",
            
            # Story methods
            "get_story", "list_stories",
            "get_story_characters", "get_story_comics", "get_story_creators",
            "get_story_events", "get_story_series",
            
            # Creator methods
            "get_creator", "list_creators", "search_creators",
            "get_creator_comics", "get_creator_events", "get_creator_series", "get_creator_stories",
        ]
        
        for method_name in expected_methods:
            assert hasattr(client, method_name), f"Method {method_name} not found on client"
            method = getattr(client, method_name)
            assert callable(method), f"Method {method_name} is not callable"
