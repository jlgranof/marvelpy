"""Tests for Event models.

This module contains comprehensive tests for the Event-related Pydantic models,
including the main Event model and all associated list structures. Tests cover
creation, validation, field access, and error handling scenarios.
"""

import logging
import pytest
from pydantic import ValidationError

# Configure logging for tests
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

from marvelpy.models.common import (
    URL,
    CharacterSummary,
    ComicSummary,
    CreatorSummary,
    EventSummary,
    Image,
)
from marvelpy.models.event import (
    CharacterList,
    ComicList,
    CreatorList,
    Event,
    EventListResponse,
    EventResponse,
    SeriesList,
    StoryList,
)


class TestCharacterList:
    """Test cases for CharacterList model.

    Tests the CharacterList model which represents a collection of characters
    involved in a specific event, including pagination metadata and character summaries.
    """

    def test_character_list_creation(self):
        """Test creating a CharacterList with valid data."""
        logger.info("Testing CharacterList creation with valid data")
        
        character_list = CharacterList(
            available=50,
            returned=20,
            collectionURI="http://gateway.marvel.com/v1/public/events/269/characters",
            items=[
                CharacterSummary(
                    resourceURI="http://gateway.marvel.com/v1/public/characters/1009368",
                    name="Iron Man",
                )
            ],
        )

        assert character_list.available == 50
        assert character_list.returned == 20
        assert (
            character_list.collection_uri
            == "http://gateway.marvel.com/v1/public/events/269/characters"
        )
        assert len(character_list.items) == 1
        assert character_list.items[0].name == "Iron Man"
        
        logger.info("✅ CharacterList creation test completed successfully")

    def test_character_list_empty_items(self):
        """Test creating a CharacterList with empty items list."""
        logger.info("Testing CharacterList creation with empty items list")
        
        character_list = CharacterList(
            available=0,
            returned=0,
            collectionURI="http://gateway.marvel.com/v1/public/events/269/characters",
            items=[],
        )

        assert character_list.available == 0
        assert character_list.returned == 0
        assert len(character_list.items) == 0
        
        logger.info("✅ CharacterList empty items test completed successfully")

    def test_character_list_missing_required_fields(self):
        """Test that CharacterList requires all mandatory fields."""
        logger.info("Testing CharacterList requires all mandatory fields")
        
        with pytest.raises(ValidationError) as exc_info:
            CharacterList(available=50)

        errors = exc_info.value.errors()
        assert len(errors) >= 2  # Should have errors for missing 'returned' and 'collectionURI'
        
        logger.info("✅ CharacterList missing required fields test completed successfully")


class TestComicList:
    """Test cases for ComicList model.

    Tests the ComicList model which represents a collection of comics that are
    part of a specific event, including pagination metadata and comic summaries.
    """

    def test_comic_list_creation(self):
        """Test creating a ComicList with valid data."""
        logger.info("Testing ComicList creation with valid data")
        
        comic_list = ComicList(
            available=100,
            returned=25,
            collectionURI="http://gateway.marvel.com/v1/public/events/269/comics",
            items=[
                ComicSummary(
                    resourceURI="http://gateway.marvel.com/v1/public/comics/12345",
                    name="Avengers (1963) #1",
                )
            ],
        )

        assert comic_list.available == 100
        assert comic_list.returned == 25
        assert comic_list.collection_uri == "http://gateway.marvel.com/v1/public/events/269/comics"
        assert len(comic_list.items) == 1
        assert comic_list.items[0].name == "Avengers (1963) #1"
        
        logger.info("✅ ComicList creation test completed successfully")

    def test_comic_list_empty_items(self):
        """Test creating a ComicList with empty items list."""
        logger.info("Testing ComicList creation with empty items list")
        
        comic_list = ComicList(
            available=0,
            returned=0,
            collectionURI="http://gateway.marvel.com/v1/public/events/269/comics",
            items=[],
        )

        assert comic_list.available == 0
        assert comic_list.returned == 0
        assert len(comic_list.items) == 0
        
        logger.info("✅ ComicList empty items test completed successfully")


class TestCreatorList:
    """Test cases for CreatorList model.

    Tests the CreatorList model which represents a collection of creators who
    worked on comics related to a specific event, including pagination metadata
    and creator summaries.
    """

    def test_creator_list_creation(self):
        """Test creating a CreatorList with valid data."""
        logger.info("Testing CreatorList creation with valid data")
        
        creator_list = CreatorList(
            available=25,
            returned=10,
            collectionURI="http://gateway.marvel.com/v1/public/events/269/creators",
            items=[
                CreatorSummary(
                    resourceURI="http://gateway.marvel.com/v1/public/creators/30",
                    name="Stan Lee",
                    role="writer",
                )
            ],
        )

        assert creator_list.available == 25
        assert creator_list.returned == 10
        assert (
            creator_list.collection_uri == "http://gateway.marvel.com/v1/public/events/269/creators"
        )
        assert len(creator_list.items) == 1
        assert creator_list.items[0].name == "Stan Lee"
        assert creator_list.items[0].role == "writer"
        
        logger.info("✅ CreatorList creation test completed successfully")

    def test_creator_list_empty_items(self):
        """Test creating a CreatorList with empty items list."""
        logger.info("Testing CreatorList creation with empty items list")
        
        creator_list = CreatorList(
            available=0,
            returned=0,
            collectionURI="http://gateway.marvel.com/v1/public/events/269/creators",
            items=[],
        )

        assert creator_list.available == 0
        assert creator_list.returned == 0
        assert len(creator_list.items) == 0
        
        logger.info("✅ CreatorList empty items test completed successfully")


class TestSeriesList:
    """Test cases for SeriesList model.

    Tests the SeriesList model which represents a collection of series that are
    part of a specific event, including pagination metadata and series summaries.
    """

    def test_series_list_creation(self):
        """Test creating a SeriesList with valid data."""
        logger.info("Testing SeriesList creation with valid data")
        
        series_list = SeriesList(
            available=15,
            returned=5,
            collectionURI="http://gateway.marvel.com/v1/public/events/269/series",
            items=[],
        )

        assert series_list.available == 15
        assert series_list.returned == 5
        assert series_list.collection_uri == "http://gateway.marvel.com/v1/public/events/269/series"
        assert len(series_list.items) == 0
        
        logger.info("✅ SeriesList creation test completed successfully")

    def test_series_list_with_items(self):
        """Test creating a SeriesList with items."""
        logger.info("Testing SeriesList creation with items")
        
        from marvelpy.models.common import SeriesSummary

        series_list = SeriesList(
            available=15,
            returned=5,
            collectionURI="http://gateway.marvel.com/v1/public/events/269/series",
            items=[
                SeriesSummary(
                    resourceURI="http://gateway.marvel.com/v1/public/series/1991",
                    name="Avengers (1998 - 2004)",
                )
            ],
        )

        assert len(series_list.items) == 1
        assert series_list.items[0].name == "Avengers (1998 - 2004)"
        
        logger.info("✅ SeriesList with items test completed successfully")


class TestStoryList:
    """Test cases for StoryList model.

    Tests the StoryList model which represents a collection of stories that are
    part of a specific event, including pagination metadata and story summaries.
    """

    def test_story_list_creation(self):
        """Test creating a StoryList with valid data."""
        logger.info("Testing StoryList creation with valid data")
        
        story_list = StoryList(
            available=200,
            returned=50,
            collectionURI="http://gateway.marvel.com/v1/public/events/269/stories",
            items=[],
        )

        assert story_list.available == 200
        assert story_list.returned == 50
        assert story_list.collection_uri == "http://gateway.marvel.com/v1/public/events/269/stories"
        assert len(story_list.items) == 0
        
        logger.info("✅ StoryList creation test completed successfully")

    def test_story_list_with_items(self):
        """Test creating a StoryList with items."""
        logger.info("Testing StoryList creation with items")
        
        from marvelpy.models.common import StorySummary

        story_list = StoryList(
            available=200,
            returned=50,
            collectionURI="http://gateway.marvel.com/v1/public/events/269/stories",
            items=[
                StorySummary(
                    resourceURI="http://gateway.marvel.com/v1/public/stories/12345",
                    name="Cover #1",
                    type="cover",
                )
            ],
        )

        assert len(story_list.items) == 1
        assert story_list.items[0].name == "Cover #1"
        assert story_list.items[0].type == "cover"
        
        logger.info("✅ StoryList with items test completed successfully")


class TestEvent:
    """Test cases for Event model.

    Tests the main Event model which represents a Marvel event with all associated
    information including basic details, description, dates, and related resources.
    """

    def test_event_creation_minimal(self):
        """Test creating an Event with minimal required data."""
        logger.info("Testing Event creation with minimal required data")
        
        event = Event(
            id=269,
            title="Secret Invasion",
            description="The shape-shifting alien race known as the Skrulls...",
            resourceURI="http://gateway.marvel.com/v1/public/events/269",
            modified="2013-11-20T17:40:18-0500",
            start="2008-04-01 00:00:00",
            end="2008-12-01 00:00:00",
            comics=ComicList(
                available=100,
                returned=25,
                collectionURI="http://gateway.marvel.com/v1/public/events/269/comics",
                items=[],
            ),
            stories=StoryList(
                available=200,
                returned=50,
                collectionURI="http://gateway.marvel.com/v1/public/events/269/stories",
                items=[],
            ),
            series=SeriesList(
                available=15,
                returned=5,
                collectionURI="http://gateway.marvel.com/v1/public/events/269/series",
                items=[],
            ),
            characters=CharacterList(
                available=50,
                returned=20,
                collectionURI="http://gateway.marvel.com/v1/public/events/269/characters",
                items=[],
            ),
            creators=CreatorList(
                available=25,
                returned=10,
                collectionURI="http://gateway.marvel.com/v1/public/events/269/creators",
                items=[],
            ),
        )

        assert event.id == 269
        assert event.title == "Secret Invasion"
        assert event.description == "The shape-shifting alien race known as the Skrulls..."
        assert event.resource_uri == "http://gateway.marvel.com/v1/public/events/269"
        assert event.modified == "2013-11-20T17:40:18-0500"
        assert event.start == "2008-04-01 00:00:00"
        assert event.end == "2008-12-01 00:00:00"
        assert event.thumbnail is None
        assert event.next is None
        assert event.previous is None
        
        logger.info("✅ Event creation minimal test completed successfully")

    def test_event_creation_with_optional_fields(self):
        """Test creating an Event with all optional fields."""
        logger.info("Testing Event creation with all optional fields")
        
        thumbnail = Image(
            path="http://i.annihil.us/u/prod/marvel/i/mg/9/c0/527bb7b37ff55", extension="jpg"
        )

        next_event = EventSummary(
            resourceURI="http://gateway.marvel.com/v1/public/events/270", name="Next Event"
        )

        previous_event = EventSummary(
            resourceURI="http://gateway.marvel.com/v1/public/events/268", name="Previous Event"
        )

        url = URL(type="detail", url="http://marvel.com/comics/events/269/secret_invasion")

        event = Event(
            id=269,
            title="Secret Invasion",
            description="The shape-shifting alien race known as the Skrulls...",
            resourceURI="http://gateway.marvel.com/v1/public/events/269",
            urls=[url],
            modified="2013-11-20T17:40:18-0500",
            start="2008-04-01 00:00:00",
            end="2008-12-01 00:00:00",
            thumbnail=thumbnail,
            comics=ComicList(
                available=100,
                returned=25,
                collectionURI="http://gateway.marvel.com/v1/public/events/269/comics",
                items=[],
            ),
            stories=StoryList(
                available=200,
                returned=50,
                collectionURI="http://gateway.marvel.com/v1/public/events/269/stories",
                items=[],
            ),
            series=SeriesList(
                available=15,
                returned=5,
                collectionURI="http://gateway.marvel.com/v1/public/events/269/series",
                items=[],
            ),
            characters=CharacterList(
                available=50,
                returned=20,
                collectionURI="http://gateway.marvel.com/v1/public/events/269/characters",
                items=[],
            ),
            creators=CreatorList(
                available=25,
                returned=10,
                collectionURI="http://gateway.marvel.com/v1/public/events/269/creators",
                items=[],
            ),
            next=next_event,
            previous=previous_event,
        )

        assert event.thumbnail is not None
        assert event.thumbnail.path == "http://i.annihil.us/u/prod/marvel/i/mg/9/c0/527bb7b37ff55"
        assert event.thumbnail.extension == "jpg"
        assert event.next is not None
        assert event.next.name == "Next Event"
        assert event.previous is not None
        assert event.previous.name == "Previous Event"
        assert len(event.urls) == 1
        assert event.urls[0].type == "detail"
        
        logger.info("✅ Event creation with optional fields test completed successfully")

    def test_event_missing_required_fields(self):
        """Test that Event requires all mandatory fields."""
        logger.info("Testing Event requires all mandatory fields")
        
        with pytest.raises(ValidationError) as exc_info:
            Event(id=269, title="Secret Invasion")

        errors = exc_info.value.errors()
        assert len(errors) >= 5  # Should have errors for missing required fields
        
        logger.info("✅ Event missing required fields test completed successfully")

    def test_event_field_access(self):
        """Test accessing Event fields after creation."""
        logger.info("Testing accessing Event fields after creation")
        
        event = Event(
            id=269,
            title="Secret Invasion",
            description="Test description",
            resourceURI="http://gateway.marvel.com/v1/public/events/269",
            modified="2013-11-20T17:40:18-0500",
            start="2008-04-01 00:00:00",
            end="2008-12-01 00:00:00",
            comics=ComicList(
                available=100,
                returned=25,
                collectionURI="http://gateway.marvel.com/v1/public/events/269/comics",
                items=[],
            ),
            stories=StoryList(
                available=200,
                returned=50,
                collectionURI="http://gateway.marvel.com/v1/public/events/269/stories",
                items=[],
            ),
            series=SeriesList(
                available=15,
                returned=5,
                collectionURI="http://gateway.marvel.com/v1/public/events/269/series",
                items=[],
            ),
            characters=CharacterList(
                available=50,
                returned=20,
                collectionURI="http://gateway.marvel.com/v1/public/events/269/characters",
                items=[],
            ),
            creators=CreatorList(
                available=25,
                returned=10,
                collectionURI="http://gateway.marvel.com/v1/public/events/269/creators",
                items=[],
            ),
        )

        # Test that all fields are accessible
        assert isinstance(event.comics, ComicList)
        assert isinstance(event.stories, StoryList)
        assert isinstance(event.series, SeriesList)
        assert isinstance(event.characters, CharacterList)
        assert isinstance(event.creators, CreatorList)
        
        logger.info("✅ Event field access test completed successfully")


class TestEventListResponse:
    """Test cases for EventListResponse model.

    Tests the EventListResponse model which represents a Marvel API response
    containing a list of events with pagination metadata.
    """

    def test_event_list_response_creation(self):
        """Test creating an EventListResponse with valid data."""
        logger.info("Testing EventListResponse creation with valid data")
        
        from marvelpy.models.base import DataContainer

        event = Event(
            id=269,
            title="Secret Invasion",
            description="Test description",
            resourceURI="http://gateway.marvel.com/v1/public/events/269",
            modified="2013-11-20T17:40:18-0500",
            start="2008-04-01 00:00:00",
            end="2008-12-01 00:00:00",
            comics=ComicList(
                available=100,
                returned=25,
                collectionURI="http://gateway.marvel.com/v1/public/events/269/comics",
                items=[],
            ),
            stories=StoryList(
                available=200,
                returned=50,
                collectionURI="http://gateway.marvel.com/v1/public/events/269/stories",
                items=[],
            ),
            series=SeriesList(
                available=15,
                returned=5,
                collectionURI="http://gateway.marvel.com/v1/public/events/269/series",
                items=[],
            ),
            characters=CharacterList(
                available=50,
                returned=20,
                collectionURI="http://gateway.marvel.com/v1/public/events/269/characters",
                items=[],
            ),
            creators=CreatorList(
                available=25,
                returned=10,
                collectionURI="http://gateway.marvel.com/v1/public/events/269/creators",
                items=[],
            ),
        )

        response = EventListResponse(
            code=200,
            status="Ok",
            copyright="© 2024 MARVEL",
            attributionText="Data provided by Marvel. © 2024 MARVEL",
            attributionHTML="<a href='http://marvel.com'>Data provided by Marvel. © 2024 MARVEL</a>",
            etag="etag123",
            data=DataContainer(offset=0, limit=20, total=50, count=1, results=[event]),
        )

        assert response.code == 200
        assert response.status == "Ok"
        assert response.data.count == 1
        assert response.data.results[0].title == "Secret Invasion"
        
        logger.info("✅ EventListResponse creation test completed successfully")

    def test_event_list_response_empty_results(self):
        """Test creating an EventListResponse with empty results."""
        logger.info("Testing EventListResponse creation with empty results")
        
        from marvelpy.models.base import DataContainer

        response = EventListResponse(
            code=200,
            status="Ok",
            copyright="© 2024 MARVEL",
            attributionText="Data provided by Marvel. © 2024 MARVEL",
            attributionHTML="<a href='http://marvel.com'>Data provided by Marvel. © 2024 MARVEL</a>",
            etag="etag123",
            data=DataContainer(offset=0, limit=20, total=0, count=0, results=[]),
        )

        assert response.data.count == 0
        assert len(response.data.results) == 0
        
        logger.info("✅ EventListResponse empty results test completed successfully")


class TestEventResponse:
    """Test cases for EventResponse model.

    Tests the EventResponse model which represents a Marvel API response
    containing a single event with full details.
    """

    def test_event_response_creation(self):
        """Test creating an EventResponse with valid data."""
        logger.info("Testing EventResponse creation with valid data")
        
        event = Event(
            id=269,
            title="Secret Invasion",
            description="Test description",
            resourceURI="http://gateway.marvel.com/v1/public/events/269",
            modified="2013-11-20T17:40:18-0500",
            start="2008-04-01 00:00:00",
            end="2008-12-01 00:00:00",
            comics=ComicList(
                available=100,
                returned=25,
                collectionURI="http://gateway.marvel.com/v1/public/events/269/comics",
                items=[],
            ),
            stories=StoryList(
                available=200,
                returned=50,
                collectionURI="http://gateway.marvel.com/v1/public/events/269/stories",
                items=[],
            ),
            series=SeriesList(
                available=15,
                returned=5,
                collectionURI="http://gateway.marvel.com/v1/public/events/269/series",
                items=[],
            ),
            characters=CharacterList(
                available=50,
                returned=20,
                collectionURI="http://gateway.marvel.com/v1/public/events/269/characters",
                items=[],
            ),
            creators=CreatorList(
                available=25,
                returned=10,
                collectionURI="http://gateway.marvel.com/v1/public/events/269/creators",
                items=[],
            ),
        )

        response = EventResponse(
            code=200,
            status="Ok",
            copyright="© 2024 MARVEL",
            attributionText="Data provided by Marvel. © 2024 MARVEL",
            attributionHTML="<a href='http://marvel.com'>Data provided by Marvel. © 2024 MARVEL</a>",
            etag="etag123",
            data=event,
        )

        assert response.code == 200
        assert response.status == "Ok"
        assert response.data.title == "Secret Invasion"
        assert response.data.id == 269
        
        logger.info("✅ EventResponse creation test completed successfully")

    def test_event_response_missing_required_fields(self):
        """Test that EventResponse requires all mandatory fields."""
        logger.info("Testing EventResponse requires all mandatory fields")
        
        with pytest.raises(ValidationError) as exc_info:
            EventResponse(code=200)

        errors = exc_info.value.errors()
        assert len(errors) >= 5  # Should have errors for missing required fields
        
        logger.info("✅ EventResponse missing required fields test completed successfully")
