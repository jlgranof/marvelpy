"""Tests for Creator models.

This module contains comprehensive tests for the Creator-related Pydantic models,
including the main Creator model and all associated list structures. Tests cover
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
    EventSummary,
    Image,
    SeriesSummary,
    StorySummary,
)
from marvelpy.models.creator import (
    CharacterList,
    ComicList,
    Creator,
    CreatorListResponse,
    CreatorResponse,
    EventList,
    SeriesList,
    StoryList,
)


class TestCharacterList:
    """Test cases for CharacterList model.

    Tests the CharacterList model which represents a collection of characters
    that a specific creator has worked on, including pagination metadata and character summaries.
    """

    def test_character_list_creation(self):
        """Test creating a CharacterList with valid data."""
        logger.info("Testing CharacterList creation with valid data")
        
        character_list = CharacterList(
            available=50,
            returned=20,
            collectionURI="http://gateway.marvel.com/v1/public/creators/30/characters",
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
            == "http://gateway.marvel.com/v1/public/creators/30/characters"
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
            collectionURI="http://gateway.marvel.com/v1/public/creators/30/characters",
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

    Tests the ComicList model which represents a collection of comics that a
    specific creator has worked on, including pagination metadata and comic summaries.
    """

    def test_comic_list_creation(self):
        """Test creating a ComicList with valid data."""
        logger.info("Testing ComicList creation with valid data")
        
        comic_list = ComicList(
            available=500,
            returned=100,
            collectionURI="http://gateway.marvel.com/v1/public/creators/30/comics",
            items=[
                ComicSummary(
                    resourceURI="http://gateway.marvel.com/v1/public/comics/12345",
                    name="Amazing Spider-Man #1",
                )
            ],
        )

        assert comic_list.available == 500
        assert comic_list.returned == 100
        assert comic_list.collection_uri == "http://gateway.marvel.com/v1/public/creators/30/comics"
        assert len(comic_list.items) == 1
        assert comic_list.items[0].name == "Amazing Spider-Man #1"
        
        logger.info("✅ ComicList creation test completed successfully")

    def test_comic_list_empty_items(self):
        """Test creating a ComicList with empty items list."""
        logger.info("Testing ComicList creation with empty items list")
        
        comic_list = ComicList(
            available=0,
            returned=0,
            collectionURI="http://gateway.marvel.com/v1/public/creators/30/comics",
            items=[],
        )

        assert comic_list.available == 0
        assert comic_list.returned == 0
        assert len(comic_list.items) == 0
        
        logger.info("✅ ComicList empty items test completed successfully")


class TestEventList:
    """Test cases for EventList model.

    Tests the EventList model which represents a collection of events that a
    specific creator has worked on, including pagination metadata and event summaries.
    """

    def test_event_list_creation(self):
        """Test creating an EventList with valid data."""
        logger.info("Testing EventList creation with valid data")
        
        event_list = EventList(
            available=10,
            returned=5,
            collectionURI="http://gateway.marvel.com/v1/public/creators/30/events",
            items=[
                EventSummary(
                    resourceURI="http://gateway.marvel.com/v1/public/events/269",
                    name="Secret Invasion",
                )
            ],
        )

        assert event_list.available == 10
        assert event_list.returned == 5
        assert event_list.collection_uri == "http://gateway.marvel.com/v1/public/creators/30/events"
        assert len(event_list.items) == 1
        assert event_list.items[0].name == "Secret Invasion"
        
        logger.info("✅ EventList creation test completed successfully")

    def test_event_list_empty_items(self):
        """Test creating an EventList with empty items list."""
        logger.info("Testing EventList creation with empty items list")
        
        event_list = EventList(
            available=0,
            returned=0,
            collectionURI="http://gateway.marvel.com/v1/public/creators/30/events",
            items=[],
        )

        assert event_list.available == 0
        assert event_list.returned == 0
        assert len(event_list.items) == 0
        
        logger.info("✅ EventList empty items test completed successfully")


class TestSeriesList:
    """Test cases for SeriesList model.

    Tests the SeriesList model which represents a collection of series that a
    specific creator has worked on, including pagination metadata and series summaries.
    """

    def test_series_list_creation(self):
        """Test creating a SeriesList with valid data."""
        logger.info("Testing SeriesList creation with valid data")
        
        series_list = SeriesList(
            available=25,
            returned=10,
            collectionURI="http://gateway.marvel.com/v1/public/creators/30/series",
            items=[
                SeriesSummary(
                    resourceURI="http://gateway.marvel.com/v1/public/series/1991",
                    name="Amazing Spider-Man (1963 - 1998)",
                )
            ],
        )

        assert series_list.available == 25
        assert series_list.returned == 10
        assert (
            series_list.collection_uri == "http://gateway.marvel.com/v1/public/creators/30/series"
        )
        assert len(series_list.items) == 1
        assert series_list.items[0].name == "Amazing Spider-Man (1963 - 1998)"
        
        logger.info("✅ SeriesList creation test completed successfully")

    def test_series_list_empty_items(self):
        """Test creating a SeriesList with empty items list."""
        logger.info("Testing SeriesList creation with empty items list")
        
        series_list = SeriesList(
            available=0,
            returned=0,
            collectionURI="http://gateway.marvel.com/v1/public/creators/30/series",
            items=[],
        )

        assert series_list.available == 0
        assert series_list.returned == 0
        assert len(series_list.items) == 0
        
        logger.info("✅ SeriesList empty items test completed successfully")


class TestStoryList:
    """Test cases for StoryList model.

    Tests the StoryList model which represents a collection of stories that a
    specific creator has worked on, including pagination metadata and story summaries.
    """

    def test_story_list_creation(self):
        """Test creating a StoryList with valid data."""
        logger.info("Testing StoryList creation with valid data")
        
        story_list = StoryList(
            available=1000,
            returned=200,
            collectionURI="http://gateway.marvel.com/v1/public/creators/30/stories",
            items=[
                StorySummary(
                    resourceURI="http://gateway.marvel.com/v1/public/stories/12345",
                    name="Cover #1",
                    type="cover",
                )
            ],
        )

        assert story_list.available == 1000
        assert story_list.returned == 200
        assert (
            story_list.collection_uri == "http://gateway.marvel.com/v1/public/creators/30/stories"
        )
        assert len(story_list.items) == 1
        assert story_list.items[0].name == "Cover #1"
        assert story_list.items[0].type == "cover"
        
        logger.info("✅ StoryList creation test completed successfully")

    def test_story_list_empty_items(self):
        """Test creating a StoryList with empty items list."""
        logger.info("Testing StoryList creation with empty items list")
        
        story_list = StoryList(
            available=0,
            returned=0,
            collectionURI="http://gateway.marvel.com/v1/public/creators/30/stories",
            items=[],
        )

        assert story_list.available == 0
        assert story_list.returned == 0
        assert len(story_list.items) == 0
        
        logger.info("✅ StoryList empty items test completed successfully")


class TestCreator:
    """Test cases for Creator model.

    Tests the main Creator model which represents a Marvel creator with all associated
    information including basic details, description, and related resources.
    """

    def test_creator_creation_minimal(self):
        """Test creating a Creator with minimal required data."""
        logger.info("Testing Creator creation with minimal required data")
        
        creator = Creator(
            id=30,
            firstName="Stan",
            middleName="",
            lastName="Lee",
            suffix="",
            fullName="Stan Lee",
            modified="2013-11-20T17:40:18-0500",
            resourceURI="http://gateway.marvel.com/v1/public/creators/30",
            comics=ComicList(
                available=500,
                returned=100,
                collectionURI="http://gateway.marvel.com/v1/public/creators/30/comics",
                items=[],
            ),
            series=SeriesList(
                available=25,
                returned=10,
                collectionURI="http://gateway.marvel.com/v1/public/creators/30/series",
                items=[],
            ),
            stories=StoryList(
                available=1000,
                returned=200,
                collectionURI="http://gateway.marvel.com/v1/public/creators/30/stories",
                items=[],
            ),
            events=EventList(
                available=10,
                returned=5,
                collectionURI="http://gateway.marvel.com/v1/public/creators/30/events",
                items=[],
            ),
            characters=CharacterList(
                available=50,
                returned=20,
                collectionURI="http://gateway.marvel.com/v1/public/creators/30/characters",
                items=[],
            ),
        )

        assert creator.id == 30
        assert creator.first_name == "Stan"
        assert creator.middle_name == ""
        assert creator.last_name == "Lee"
        assert creator.suffix == ""
        assert creator.full_name == "Stan Lee"
        assert creator.resource_uri == "http://gateway.marvel.com/v1/public/creators/30"
        assert creator.modified == "2013-11-20T17:40:18-0500"
        assert creator.thumbnail is None
        assert len(creator.urls) == 0
        
        logger.info("✅ Creator creation minimal test completed successfully")

    def test_creator_creation_with_optional_fields(self):
        """Test creating a Creator with all optional fields."""
        logger.info("Testing Creator creation with all optional fields")
        
        thumbnail = Image(
            path="http://i.annihil.us/u/prod/marvel/i/mg/9/c0/527bb7b37ff55", extension="jpg"
        )

        url = URL(type="detail", url="http://marvel.com/comics/creators/30/stan_lee")

        creator = Creator(
            id=30,
            firstName="Stan",
            middleName="",
            lastName="Lee",
            suffix="",
            fullName="Stan Lee",
            modified="2013-11-20T17:40:18-0500",
            resourceURI="http://gateway.marvel.com/v1/public/creators/30",
            urls=[url],
            thumbnail=thumbnail,
            comics=ComicList(
                available=500,
                returned=100,
                collectionURI="http://gateway.marvel.com/v1/public/creators/30/comics",
                items=[],
            ),
            series=SeriesList(
                available=25,
                returned=10,
                collectionURI="http://gateway.marvel.com/v1/public/creators/30/series",
                items=[],
            ),
            stories=StoryList(
                available=1000,
                returned=200,
                collectionURI="http://gateway.marvel.com/v1/public/creators/30/stories",
                items=[],
            ),
            events=EventList(
                available=10,
                returned=5,
                collectionURI="http://gateway.marvel.com/v1/public/creators/30/events",
                items=[],
            ),
            characters=CharacterList(
                available=50,
                returned=20,
                collectionURI="http://gateway.marvel.com/v1/public/creators/30/characters",
                items=[],
            ),
        )

        assert creator.thumbnail is not None
        assert creator.thumbnail.path == "http://i.annihil.us/u/prod/marvel/i/mg/9/c0/527bb7b37ff55"
        assert creator.thumbnail.extension == "jpg"
        assert len(creator.urls) == 1
        assert creator.urls[0].type == "detail"
        
        logger.info("✅ Creator creation with optional fields test completed successfully")

    def test_creator_with_middle_name_and_suffix(self):
        """Test creating a Creator with middle name and suffix."""
        logger.info("Testing Creator creation with middle name and suffix")
        
        creator = Creator(
            id=123,
            firstName="John",
            middleName="Michael",
            lastName="Smith",
            suffix="Jr.",
            fullName="John Michael Smith Jr.",
            modified="2013-11-20T17:40:18-0500",
            resourceURI="http://gateway.marvel.com/v1/public/creators/123",
            comics=ComicList(
                available=10,
                returned=5,
                collectionURI="http://gateway.marvel.com/v1/public/creators/123/comics",
                items=[],
            ),
            series=SeriesList(
                available=5,
                returned=3,
                collectionURI="http://gateway.marvel.com/v1/public/creators/123/series",
                items=[],
            ),
            stories=StoryList(
                available=20,
                returned=10,
                collectionURI="http://gateway.marvel.com/v1/public/creators/123/stories",
                items=[],
            ),
            events=EventList(
                available=2,
                returned=1,
                collectionURI="http://gateway.marvel.com/v1/public/creators/123/events",
                items=[],
            ),
            characters=CharacterList(
                available=8,
                returned=4,
                collectionURI="http://gateway.marvel.com/v1/public/creators/123/characters",
                items=[],
            ),
        )

        assert creator.first_name == "John"
        assert creator.middle_name == "Michael"
        assert creator.last_name == "Smith"
        assert creator.suffix == "Jr."
        assert creator.full_name == "John Michael Smith Jr."
        
        logger.info("✅ Creator with middle name and suffix test completed successfully")

    def test_creator_missing_required_fields(self):
        """Test that Creator requires all mandatory fields."""
        logger.info("Testing Creator requires all mandatory fields")
        
        with pytest.raises(ValidationError) as exc_info:
            Creator(id=30, firstName="Stan")

        errors = exc_info.value.errors()
        assert len(errors) >= 6  # Should have errors for missing required fields
        
        logger.info("✅ Creator missing required fields test completed successfully")

    def test_creator_field_access(self):
        """Test accessing Creator fields after creation."""
        logger.info("Testing accessing Creator fields after creation")
        
        creator = Creator(
            id=30,
            firstName="Stan",
            middleName="",
            lastName="Lee",
            suffix="",
            fullName="Stan Lee",
            modified="2013-11-20T17:40:18-0500",
            resourceURI="http://gateway.marvel.com/v1/public/creators/30",
            comics=ComicList(
                available=500,
                returned=100,
                collectionURI="http://gateway.marvel.com/v1/public/creators/30/comics",
                items=[],
            ),
            series=SeriesList(
                available=25,
                returned=10,
                collectionURI="http://gateway.marvel.com/v1/public/creators/30/series",
                items=[],
            ),
            stories=StoryList(
                available=1000,
                returned=200,
                collectionURI="http://gateway.marvel.com/v1/public/creators/30/stories",
                items=[],
            ),
            events=EventList(
                available=10,
                returned=5,
                collectionURI="http://gateway.marvel.com/v1/public/creators/30/events",
                items=[],
            ),
            characters=CharacterList(
                available=50,
                returned=20,
                collectionURI="http://gateway.marvel.com/v1/public/creators/30/characters",
                items=[],
            ),
        )

        # Test that all fields are accessible
        assert isinstance(creator.comics, ComicList)
        assert isinstance(creator.series, SeriesList)
        assert isinstance(creator.stories, StoryList)
        assert isinstance(creator.events, EventList)
        assert isinstance(creator.characters, CharacterList)
        
        logger.info("✅ Creator field access test completed successfully")


class TestCreatorListResponse:
    """Test cases for CreatorListResponse model.

    Tests the CreatorListResponse model which represents a Marvel API response
    containing a list of creators with pagination metadata.
    """

    def test_creator_list_response_creation(self):
        """Test creating a CreatorListResponse with valid data."""
        logger.info("Testing CreatorListResponse creation with valid data")
        
        from marvelpy.models.base import DataContainer

        creator = Creator(
            id=30,
            firstName="Stan",
            middleName="",
            lastName="Lee",
            suffix="",
            fullName="Stan Lee",
            modified="2013-11-20T17:40:18-0500",
            resourceURI="http://gateway.marvel.com/v1/public/creators/30",
            comics=ComicList(
                available=500,
                returned=100,
                collectionURI="http://gateway.marvel.com/v1/public/creators/30/comics",
                items=[],
            ),
            series=SeriesList(
                available=25,
                returned=10,
                collectionURI="http://gateway.marvel.com/v1/public/creators/30/series",
                items=[],
            ),
            stories=StoryList(
                available=1000,
                returned=200,
                collectionURI="http://gateway.marvel.com/v1/public/creators/30/stories",
                items=[],
            ),
            events=EventList(
                available=10,
                returned=5,
                collectionURI="http://gateway.marvel.com/v1/public/creators/30/events",
                items=[],
            ),
            characters=CharacterList(
                available=50,
                returned=20,
                collectionURI="http://gateway.marvel.com/v1/public/creators/30/characters",
                items=[],
            ),
        )

        response = CreatorListResponse(
            code=200,
            status="Ok",
            copyright="© 2024 MARVEL",
            attributionText="Data provided by Marvel. © 2024 MARVEL",
            attributionHTML="<a href='http://marvel.com'>Data provided by Marvel. © 2024 MARVEL</a>",
            etag="etag123",
            data=DataContainer(offset=0, limit=20, total=200, count=1, results=[creator]),
        )

        assert response.code == 200
        assert response.status == "Ok"
        assert response.data.count == 1
        assert response.data.results[0].full_name == "Stan Lee"
        
        logger.info("✅ CreatorListResponse creation test completed successfully")

    def test_creator_list_response_empty_results(self):
        """Test creating a CreatorListResponse with empty results."""
        logger.info("Testing CreatorListResponse creation with empty results")
        
        from marvelpy.models.base import DataContainer

        response = CreatorListResponse(
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
        
        logger.info("✅ CreatorListResponse empty results test completed successfully")


class TestCreatorResponse:
    """Test cases for CreatorResponse model.

    Tests the CreatorResponse model which represents a Marvel API response
    containing a single creator with full details.
    """

    def test_creator_response_creation(self):
        """Test creating a CreatorResponse with valid data."""
        logger.info("Testing CreatorResponse creation with valid data")
        
        creator = Creator(
            id=30,
            firstName="Stan",
            middleName="",
            lastName="Lee",
            suffix="",
            fullName="Stan Lee",
            modified="2013-11-20T17:40:18-0500",
            resourceURI="http://gateway.marvel.com/v1/public/creators/30",
            comics=ComicList(
                available=500,
                returned=100,
                collectionURI="http://gateway.marvel.com/v1/public/creators/30/comics",
                items=[],
            ),
            series=SeriesList(
                available=25,
                returned=10,
                collectionURI="http://gateway.marvel.com/v1/public/creators/30/series",
                items=[],
            ),
            stories=StoryList(
                available=1000,
                returned=200,
                collectionURI="http://gateway.marvel.com/v1/public/creators/30/stories",
                items=[],
            ),
            events=EventList(
                available=10,
                returned=5,
                collectionURI="http://gateway.marvel.com/v1/public/creators/30/events",
                items=[],
            ),
            characters=CharacterList(
                available=50,
                returned=20,
                collectionURI="http://gateway.marvel.com/v1/public/creators/30/characters",
                items=[],
            ),
        )

        response = CreatorResponse(
            code=200,
            status="Ok",
            copyright="© 2024 MARVEL",
            attributionText="Data provided by Marvel. © 2024 MARVEL",
            attributionHTML="<a href='http://marvel.com'>Data provided by Marvel. © 2024 MARVEL</a>",
            etag="etag123",
            data=creator,
        )

        assert response.code == 200
        assert response.status == "Ok"
        assert response.data.full_name == "Stan Lee"
        assert response.data.id == 30
        
        logger.info("✅ CreatorResponse creation test completed successfully")

    def test_creator_response_missing_required_fields(self):
        """Test that CreatorResponse requires all mandatory fields."""
        logger.info("Testing CreatorResponse requires all mandatory fields")
        
        with pytest.raises(ValidationError) as exc_info:
            CreatorResponse(code=200)

        errors = exc_info.value.errors()
        assert len(errors) >= 5  # Should have errors for missing required fields
        
        logger.info("✅ CreatorResponse missing required fields test completed successfully")
