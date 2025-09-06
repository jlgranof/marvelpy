"""Tests for Story models.

This module contains comprehensive tests for the Story-related Pydantic models,
including the main Story model and all associated list structures. Tests cover
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
    CharacterSummary,
    ComicSummary,
    CreatorSummary,
    EventSummary,
    Image,
    SeriesSummary,
)
from marvelpy.models.story import (
    CharacterList,
    ComicList,
    CreatorList,
    EventList,
    SeriesList,
    Story,
    StoryListResponse,
    StoryResponse,
)


class TestCharacterList:
    """Test cases for CharacterList model.

    Tests the CharacterList model which represents a collection of characters
    that appear in a specific story, including pagination metadata and character summaries.
    """

    def test_character_list_creation(self):
        """Test creating a CharacterList with valid data."""
        logger.info("Testing character list creation with valid data")
        character_list = CharacterList(
            available=10,
            returned=5,
            collectionURI="http://gateway.marvel.com/v1/public/stories/12345/characters",
            items=[
                CharacterSummary(
                    resourceURI="http://gateway.marvel.com/v1/public/characters/1009368",
                    name="Iron Man",
                )
            ],
        )

        assert character_list.available == 10
        assert character_list.returned == 5
        assert (
            character_list.collection_uri
            == "http://gateway.marvel.com/v1/public/stories/12345/characters"
        )
        assert len(character_list.items) == 1
        assert character_list.items[0].name == "Iron Man"
        logger.info("✅ Character list creation test completed successfully")

    def test_character_list_empty_items(self):
        """Test creating a CharacterList with empty items list."""
        logger.info("Testing character list creation with empty items list")
        character_list = CharacterList(
            available=0,
            returned=0,
            collectionURI="http://gateway.marvel.com/v1/public/stories/12345/characters",
            items=[],
        )

        assert character_list.available == 0
        assert character_list.returned == 0
        assert len(character_list.items) == 0
        logger.info("✅ Character list empty items test completed successfully")

    def test_character_list_missing_required_fields(self):
        """Test that CharacterList requires all mandatory fields."""
        logger.info("Testing character list missing required fields validation")
        with pytest.raises(ValidationError) as exc_info:
            CharacterList(available=10)

        errors = exc_info.value.errors()
        assert len(errors) >= 2  # Should have errors for missing 'returned' and 'collectionURI'
        logger.info("✅ Character list missing required fields test completed successfully")


class TestComicList:
    """Test cases for ComicList model.

    Tests the ComicList model which represents a collection of comics that contain
    a specific story, including pagination metadata and comic summaries.
    """

    def test_comic_list_creation(self):
        """Test creating a ComicList with valid data."""
        logger.info("Testing comic list creation with valid data")
        comic_list = ComicList(
            available=5,
            returned=3,
            collectionURI="http://gateway.marvel.com/v1/public/stories/12345/comics",
            items=[
                ComicSummary(
                    resourceURI="http://gateway.marvel.com/v1/public/comics/12345",
                    name="Avengers (1963) #1",
                )
            ],
        )

        assert comic_list.available == 5
        assert comic_list.returned == 3
        assert (
            comic_list.collection_uri == "http://gateway.marvel.com/v1/public/stories/12345/comics"
        )
        assert len(comic_list.items) == 1
        assert comic_list.items[0].name == "Avengers (1963) #1"
        logger.info("✅ Comic list creation test completed successfully")

    def test_comic_list_empty_items(self):
        """Test creating a ComicList with empty items list."""
        logger.info("Testing comic list creation with empty items list")
        comic_list = ComicList(
            available=0,
            returned=0,
            collectionURI="http://gateway.marvel.com/v1/public/stories/12345/comics",
            items=[],
        )

        assert comic_list.available == 0
        assert comic_list.returned == 0
        assert len(comic_list.items) == 0
        logger.info("✅ Comic list empty items test completed successfully")


class TestCreatorList:
    """Test cases for CreatorList model.

    Tests the CreatorList model which represents a collection of creators who
    worked on a specific story, including pagination metadata and creator summaries.
    """

    def test_creator_list_creation(self):
        """Test creating a CreatorList with valid data."""
        logger.info("Testing creator list creation with valid data")
        creator_list = CreatorList(
            available=8,
            returned=4,
            collectionURI="http://gateway.marvel.com/v1/public/stories/12345/creators",
            items=[
                CreatorSummary(
                    resourceURI="http://gateway.marvel.com/v1/public/creators/30",
                    name="Stan Lee",
                    role="writer",
                )
            ],
        )

        assert creator_list.available == 8
        assert creator_list.returned == 4
        assert (
            creator_list.collection_uri
            == "http://gateway.marvel.com/v1/public/stories/12345/creators"
        )
        assert len(creator_list.items) == 1
        assert creator_list.items[0].name == "Stan Lee"
        assert creator_list.items[0].role == "writer"
        logger.info("✅ Creator list creation test completed successfully")

    def test_creator_list_empty_items(self):
        """Test creating a CreatorList with empty items list."""
        logger.info("Testing creator list creation with empty items list")
        creator_list = CreatorList(
            available=0,
            returned=0,
            collectionURI="http://gateway.marvel.com/v1/public/stories/12345/creators",
            items=[],
        )

        assert creator_list.available == 0
        assert creator_list.returned == 0
        assert len(creator_list.items) == 0
        logger.info("✅ Creator list empty items test completed successfully")


class TestEventList:
    """Test cases for EventList model.

    Tests the EventList model which represents a collection of events that are
    related to a specific story, including pagination metadata and event summaries.
    """

    def test_event_list_creation(self):
        """Test creating an EventList with valid data."""
        logger.info("Testing event list creation with valid data")
        event_list = EventList(
            available=3,
            returned=2,
            collectionURI="http://gateway.marvel.com/v1/public/stories/12345/events",
            items=[
                EventSummary(
                    resourceURI="http://gateway.marvel.com/v1/public/events/269",
                    name="Secret Invasion",
                )
            ],
        )

        assert event_list.available == 3
        assert event_list.returned == 2
        assert (
            event_list.collection_uri == "http://gateway.marvel.com/v1/public/stories/12345/events"
        )
        assert len(event_list.items) == 1
        assert event_list.items[0].name == "Secret Invasion"
        logger.info("✅ Event list creation test completed successfully")

    def test_event_list_empty_items(self):
        """Test creating an EventList with empty items list."""
        logger.info("Testing event list creation with empty items list")
        event_list = EventList(
            available=0,
            returned=0,
            collectionURI="http://gateway.marvel.com/v1/public/stories/12345/events",
            items=[],
        )

        assert event_list.available == 0
        assert event_list.returned == 0
        assert len(event_list.items) == 0
        logger.info("✅ Event list empty items test completed successfully")


class TestSeriesList:
    """Test cases for SeriesList model.

    Tests the SeriesList model which represents a collection of series that contain
    a specific story, including pagination metadata and series summaries.
    """

    def test_series_list_creation(self):
        """Test creating a SeriesList with valid data."""
        logger.info("Testing series list creation with valid data")
        series_list = SeriesList(
            available=2,
            returned=1,
            collectionURI="http://gateway.marvel.com/v1/public/stories/12345/series",
            items=[
                SeriesSummary(
                    resourceURI="http://gateway.marvel.com/v1/public/series/1991",
                    name="Avengers (1998 - 2004)",
                )
            ],
        )

        assert series_list.available == 2
        assert series_list.returned == 1
        assert (
            series_list.collection_uri == "http://gateway.marvel.com/v1/public/stories/12345/series"
        )
        assert len(series_list.items) == 1
        assert series_list.items[0].name == "Avengers (1998 - 2004)"
        logger.info("✅ Series list creation test completed successfully")

    def test_series_list_empty_items(self):
        """Test creating a SeriesList with empty items list."""
        logger.info("Testing series list creation with empty items list")
        series_list = SeriesList(
            available=0,
            returned=0,
            collectionURI="http://gateway.marvel.com/v1/public/stories/12345/series",
            items=[],
        )

        assert series_list.available == 0
        assert series_list.returned == 0
        assert len(series_list.items) == 0
        logger.info("✅ Series list empty items test completed successfully")


class TestStory:
    """Test cases for Story model.

    Tests the main Story model which represents a Marvel story with all associated
    information including basic details, description, type, and related resources.
    """

    def test_story_creation_minimal(self):
        """Test creating a Story with minimal required data."""
        logger.info("Testing story creation with minimal required data")
        story = Story(
            id=12345,
            title="Cover #1",
            description="Cover story for Avengers #1",
            resourceURI="http://gateway.marvel.com/v1/public/stories/12345",
            type="cover",
            modified="2013-11-20T17:40:18-0500",
            comics=ComicList(
                available=5,
                returned=3,
                collectionURI="http://gateway.marvel.com/v1/public/stories/12345/comics",
                items=[],
            ),
            series=SeriesList(
                available=2,
                returned=1,
                collectionURI="http://gateway.marvel.com/v1/public/stories/12345/series",
                items=[],
            ),
            events=EventList(
                available=3,
                returned=2,
                collectionURI="http://gateway.marvel.com/v1/public/stories/12345/events",
                items=[],
            ),
            characters=CharacterList(
                available=10,
                returned=5,
                collectionURI="http://gateway.marvel.com/v1/public/stories/12345/characters",
                items=[],
            ),
            creators=CreatorList(
                available=8,
                returned=4,
                collectionURI="http://gateway.marvel.com/v1/public/stories/12345/creators",
                items=[],
            ),
        )

        assert story.id == 12345
        assert story.title == "Cover #1"
        assert story.description == "Cover story for Avengers #1"
        assert story.resource_uri == "http://gateway.marvel.com/v1/public/stories/12345"
        assert story.type == "cover"
        assert story.modified == "2013-11-20T17:40:18-0500"
        assert story.thumbnail is None
        assert story.original_issue is None
        logger.info("✅ Story creation minimal test completed successfully")

    def test_story_creation_with_optional_fields(self):
        """Test creating a Story with all optional fields."""
        logger.info("Testing story creation with all optional fields")
        thumbnail = Image(
            path="http://i.annihil.us/u/prod/marvel/i/mg/9/c0/527bb7b37ff55", extension="jpg"
        )

        original_issue = ComicSummary(
            resourceURI="http://gateway.marvel.com/v1/public/comics/12345",
            name="Avengers (1963) #1",
        )

        story = Story(
            id=12345,
            title="Cover #1",
            description="Cover story for Avengers #1",
            resourceURI="http://gateway.marvel.com/v1/public/stories/12345",
            type="cover",
            modified="2013-11-20T17:40:18-0500",
            thumbnail=thumbnail,
            comics=ComicList(
                available=5,
                returned=3,
                collectionURI="http://gateway.marvel.com/v1/public/stories/12345/comics",
                items=[],
            ),
            series=SeriesList(
                available=2,
                returned=1,
                collectionURI="http://gateway.marvel.com/v1/public/stories/12345/series",
                items=[],
            ),
            events=EventList(
                available=3,
                returned=2,
                collectionURI="http://gateway.marvel.com/v1/public/stories/12345/events",
                items=[],
            ),
            characters=CharacterList(
                available=10,
                returned=5,
                collectionURI="http://gateway.marvel.com/v1/public/stories/12345/characters",
                items=[],
            ),
            creators=CreatorList(
                available=8,
                returned=4,
                collectionURI="http://gateway.marvel.com/v1/public/stories/12345/creators",
                items=[],
            ),
            original_issue=original_issue,
        )

        assert story.thumbnail is not None
        assert story.thumbnail.path == "http://i.annihil.us/u/prod/marvel/i/mg/9/c0/527bb7b37ff55"
        assert story.thumbnail.extension == "jpg"
        assert story.original_issue is not None
        assert story.original_issue.name == "Avengers (1963) #1"
        logger.info("✅ Story creation with optional fields test completed successfully")

    def test_story_different_types(self):
        """Test creating Stories with different types."""
        logger.info("Testing story creation with different types")
        # Test interior story
        interior_story = Story(
            id=12346,
            title="The Coming of the Avengers",
            description="The Avengers first adventure",
            resourceURI="http://gateway.marvel.com/v1/public/stories/12346",
            type="interiorStory",
            modified="2013-11-20T17:40:18-0500",
            comics=ComicList(
                available=1,
                returned=1,
                collectionURI="http://gateway.marvel.com/v1/public/stories/12346/comics",
                items=[],
            ),
            series=SeriesList(
                available=1,
                returned=1,
                collectionURI="http://gateway.marvel.com/v1/public/stories/12346/series",
                items=[],
            ),
            events=EventList(
                available=0,
                returned=0,
                collectionURI="http://gateway.marvel.com/v1/public/stories/12346/events",
                items=[],
            ),
            characters=CharacterList(
                available=5,
                returned=5,
                collectionURI="http://gateway.marvel.com/v1/public/stories/12346/characters",
                items=[],
            ),
            creators=CreatorList(
                available=3,
                returned=3,
                collectionURI="http://gateway.marvel.com/v1/public/stories/12346/creators",
                items=[],
            ),
        )

        assert interior_story.type == "interiorStory"
        assert interior_story.title == "The Coming of the Avengers"

        # Test promo story
        promo_story = Story(
            id=12347,
            title="Promo Story",
            description="Promotional content",
            resourceURI="http://gateway.marvel.com/v1/public/stories/12347",
            type="promo",
            modified="2013-11-20T17:40:18-0500",
            comics=ComicList(
                available=1,
                returned=1,
                collectionURI="http://gateway.marvel.com/v1/public/stories/12347/comics",
                items=[],
            ),
            series=SeriesList(
                available=1,
                returned=1,
                collectionURI="http://gateway.marvel.com/v1/public/stories/12347/series",
                items=[],
            ),
            events=EventList(
                available=0,
                returned=0,
                collectionURI="http://gateway.marvel.com/v1/public/stories/12347/events",
                items=[],
            ),
            characters=CharacterList(
                available=0,
                returned=0,
                collectionURI="http://gateway.marvel.com/v1/public/stories/12347/characters",
                items=[],
            ),
            creators=CreatorList(
                available=1,
                returned=1,
                collectionURI="http://gateway.marvel.com/v1/public/stories/12347/creators",
                items=[],
            ),
        )

        assert promo_story.type == "promo"
        assert promo_story.title == "Promo Story"
        logger.info("✅ Story different types test completed successfully")

    def test_story_missing_required_fields(self):
        """Test that Story requires all mandatory fields."""
        logger.info("Testing story missing required fields validation")
        with pytest.raises(ValidationError) as exc_info:
            Story(id=12345, title="Cover #1")

        errors = exc_info.value.errors()
        assert len(errors) >= 6  # Should have errors for missing required fields
        logger.info("✅ Story missing required fields test completed successfully")

    def test_story_field_access(self):
        """Test accessing Story fields after creation."""
        logger.info("Testing story field access after creation")
        story = Story(
            id=12345,
            title="Cover #1",
            description="Test description",
            resourceURI="http://gateway.marvel.com/v1/public/stories/12345",
            type="cover",
            modified="2013-11-20T17:40:18-0500",
            comics=ComicList(
                available=5,
                returned=3,
                collectionURI="http://gateway.marvel.com/v1/public/stories/12345/comics",
                items=[],
            ),
            series=SeriesList(
                available=2,
                returned=1,
                collectionURI="http://gateway.marvel.com/v1/public/stories/12345/series",
                items=[],
            ),
            events=EventList(
                available=3,
                returned=2,
                collectionURI="http://gateway.marvel.com/v1/public/stories/12345/events",
                items=[],
            ),
            characters=CharacterList(
                available=10,
                returned=5,
                collectionURI="http://gateway.marvel.com/v1/public/stories/12345/characters",
                items=[],
            ),
            creators=CreatorList(
                available=8,
                returned=4,
                collectionURI="http://gateway.marvel.com/v1/public/stories/12345/creators",
                items=[],
            ),
        )

        # Test that all fields are accessible
        assert isinstance(story.comics, ComicList)
        assert isinstance(story.series, SeriesList)
        assert isinstance(story.events, EventList)
        assert isinstance(story.characters, CharacterList)
        assert isinstance(story.creators, CreatorList)
        logger.info("✅ Story field access test completed successfully")


class TestStoryListResponse:
    """Test cases for StoryListResponse model.

    Tests the StoryListResponse model which represents a Marvel API response
    containing a list of stories with pagination metadata.
    """

    def test_story_list_response_creation(self):
        """Test creating a StoryListResponse with valid data."""
        logger.info("Testing story list response creation with valid data")
        from marvelpy.models.base import DataContainer

        story = Story(
            id=12345,
            title="Cover #1",
            description="Test description",
            resourceURI="http://gateway.marvel.com/v1/public/stories/12345",
            type="cover",
            modified="2013-11-20T17:40:18-0500",
            comics=ComicList(
                available=5,
                returned=3,
                collectionURI="http://gateway.marvel.com/v1/public/stories/12345/comics",
                items=[],
            ),
            series=SeriesList(
                available=2,
                returned=1,
                collectionURI="http://gateway.marvel.com/v1/public/stories/12345/series",
                items=[],
            ),
            events=EventList(
                available=3,
                returned=2,
                collectionURI="http://gateway.marvel.com/v1/public/stories/12345/events",
                items=[],
            ),
            characters=CharacterList(
                available=10,
                returned=5,
                collectionURI="http://gateway.marvel.com/v1/public/stories/12345/characters",
                items=[],
            ),
            creators=CreatorList(
                available=8,
                returned=4,
                collectionURI="http://gateway.marvel.com/v1/public/stories/12345/creators",
                items=[],
            ),
        )

        response = StoryListResponse(
            code=200,
            status="Ok",
            copyright="© 2024 MARVEL",
            attributionText="Data provided by Marvel. © 2024 MARVEL",
            attributionHTML="<a href='http://marvel.com'>Data provided by Marvel. © 2024 MARVEL</a>",
            etag="etag123",
            data=DataContainer(offset=0, limit=20, total=500, count=1, results=[story]),
        )

        assert response.code == 200
        assert response.status == "Ok"
        assert response.data.count == 1
        assert response.data.results[0].title == "Cover #1"
        logger.info("✅ Story list response creation test completed successfully")

    def test_story_list_response_empty_results(self):
        """Test creating a StoryListResponse with empty results."""
        logger.info("Testing story list response creation with empty results")
        from marvelpy.models.base import DataContainer

        response = StoryListResponse(
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
        logger.info("✅ Story list response empty results test completed successfully")


class TestStoryResponse:
    """Test cases for StoryResponse model.

    Tests the StoryResponse model which represents a Marvel API response
    containing a single story with full details.
    """

    def test_story_response_creation(self):
        """Test creating a StoryResponse with valid data."""
        logger.info("Testing story response creation with valid data")
        story = Story(
            id=12345,
            title="Cover #1",
            description="Test description",
            resourceURI="http://gateway.marvel.com/v1/public/stories/12345",
            type="cover",
            modified="2013-11-20T17:40:18-0500",
            comics=ComicList(
                available=5,
                returned=3,
                collectionURI="http://gateway.marvel.com/v1/public/stories/12345/comics",
                items=[],
            ),
            series=SeriesList(
                available=2,
                returned=1,
                collectionURI="http://gateway.marvel.com/v1/public/stories/12345/series",
                items=[],
            ),
            events=EventList(
                available=3,
                returned=2,
                collectionURI="http://gateway.marvel.com/v1/public/stories/12345/events",
                items=[],
            ),
            characters=CharacterList(
                available=10,
                returned=5,
                collectionURI="http://gateway.marvel.com/v1/public/stories/12345/characters",
                items=[],
            ),
            creators=CreatorList(
                available=8,
                returned=4,
                collectionURI="http://gateway.marvel.com/v1/public/stories/12345/creators",
                items=[],
            ),
        )

        response = StoryResponse(
            code=200,
            status="Ok",
            copyright="© 2024 MARVEL",
            attributionText="Data provided by Marvel. © 2024 MARVEL",
            attributionHTML="<a href='http://marvel.com'>Data provided by Marvel. © 2024 MARVEL</a>",
            etag="etag123",
            data=story,
        )

        assert response.code == 200
        assert response.status == "Ok"
        assert response.data.title == "Cover #1"
        assert response.data.id == 12345
        logger.info("✅ Story response creation test completed successfully")

    def test_story_response_missing_required_fields(self):
        """Test that StoryResponse requires all mandatory fields."""
        logger.info("Testing story response missing required fields validation")
        with pytest.raises(ValidationError) as exc_info:
            StoryResponse(code=200)

        errors = exc_info.value.errors()
        assert len(errors) >= 5  # Should have errors for missing required fields
        logger.info("✅ Story response missing required fields test completed successfully")
