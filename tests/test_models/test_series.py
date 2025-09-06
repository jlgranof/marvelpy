"""Tests for Series models.

This module contains comprehensive tests for the Series-related Pydantic models,
including the main Series model and all associated list structures. Tests cover
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
    SeriesSummary,
)
from marvelpy.models.series import (
    CharacterList,
    ComicList,
    CreatorList,
    EventList,
    Series,
    SeriesListResponse,
    SeriesResponse,
    StoryList,
)


class TestCharacterList:
    """Test cases for CharacterList model.

    Tests the CharacterList model which represents a collection of characters
    that appear in a specific series, including pagination metadata and character summaries.
    """

    def test_character_list_creation(self):
        """Test creating a CharacterList with valid data."""
        logger.info("Testing character list creation with valid data")
        character_list = CharacterList(
            available=25,
            returned=10,
            collectionURI="http://gateway.marvel.com/v1/public/series/1991/characters",
            items=[
                CharacterSummary(
                    resourceURI="http://gateway.marvel.com/v1/public/characters/1009368",
                    name="Iron Man",
                )
            ],
        )

        assert character_list.available == 25
        assert character_list.returned == 10
        assert (
            character_list.collection_uri
            == "http://gateway.marvel.com/v1/public/series/1991/characters"
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
            collectionURI="http://gateway.marvel.com/v1/public/series/1991/characters",
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
            CharacterList(available=25)

        errors = exc_info.value.errors()
        assert len(errors) >= 2  # Should have errors for missing 'returned' and 'collectionURI'
        logger.info("✅ Character list missing required fields test completed successfully")


class TestComicList:
    """Test cases for ComicList model.

    Tests the ComicList model which represents a collection of comics that are
    part of a specific series, including pagination metadata and comic summaries.
    """

    def test_comic_list_creation(self):
        """Test creating a ComicList with valid data."""
        logger.info("Testing comic list creation with valid data")
        comic_list = ComicList(
            available=200,
            returned=50,
            collectionURI="http://gateway.marvel.com/v1/public/series/1991/comics",
            items=[
                ComicSummary(
                    resourceURI="http://gateway.marvel.com/v1/public/comics/12345",
                    name="Avengers (1998) #1",
                )
            ],
        )

        assert comic_list.available == 200
        assert comic_list.returned == 50
        assert comic_list.collection_uri == "http://gateway.marvel.com/v1/public/series/1991/comics"
        assert len(comic_list.items) == 1
        assert comic_list.items[0].name == "Avengers (1998) #1"
        logger.info("✅ Comic list creation test completed successfully")

    def test_comic_list_empty_items(self):
        """Test creating a ComicList with empty items list."""
        logger.info("Testing comic list creation with empty items list")
        comic_list = ComicList(
            available=0,
            returned=0,
            collectionURI="http://gateway.marvel.com/v1/public/series/1991/comics",
            items=[],
        )

        assert comic_list.available == 0
        assert comic_list.returned == 0
        assert len(comic_list.items) == 0
        logger.info("✅ Comic list empty items test completed successfully")


class TestCreatorList:
    """Test cases for CreatorList model.

    Tests the CreatorList model which represents a collection of creators who
    worked on comics in a specific series, including pagination metadata and creator summaries.
    """

    def test_creator_list_creation(self):
        """Test creating a CreatorList with valid data."""
        logger.info("Testing creator list creation with valid data")
        creator_list = CreatorList(
            available=15,
            returned=8,
            collectionURI="http://gateway.marvel.com/v1/public/series/1991/creators",
            items=[
                CreatorSummary(
                    resourceURI="http://gateway.marvel.com/v1/public/creators/30",
                    name="Kurt Busiek",
                    role="writer",
                )
            ],
        )

        assert creator_list.available == 15
        assert creator_list.returned == 8
        assert (
            creator_list.collection_uri
            == "http://gateway.marvel.com/v1/public/series/1991/creators"
        )
        assert len(creator_list.items) == 1
        assert creator_list.items[0].name == "Kurt Busiek"
        assert creator_list.items[0].role == "writer"
        logger.info("✅ Creator list creation test completed successfully")

    def test_creator_list_empty_items(self):
        """Test creating a CreatorList with empty items list."""
        logger.info("Testing creator list creation with empty items list")
        creator_list = CreatorList(
            available=0,
            returned=0,
            collectionURI="http://gateway.marvel.com/v1/public/series/1991/creators",
            items=[],
        )

        assert creator_list.available == 0
        assert creator_list.returned == 0
        assert len(creator_list.items) == 0
        logger.info("✅ Creator list empty items test completed successfully")


class TestEventList:
    """Test cases for EventList model.

    Tests the EventList model which represents a collection of events that are
    related to a specific series, including pagination metadata and event summaries.
    """

    def test_event_list_creation(self):
        """Test creating an EventList with valid data."""
        logger.info("Testing event list creation with valid data")
        event_list = EventList(
            available=5,
            returned=3,
            collectionURI="http://gateway.marvel.com/v1/public/series/1991/events",
            items=[
                EventSummary(
                    resourceURI="http://gateway.marvel.com/v1/public/events/269",
                    name="Secret Invasion",
                )
            ],
        )

        assert event_list.available == 5
        assert event_list.returned == 3
        assert event_list.collection_uri == "http://gateway.marvel.com/v1/public/series/1991/events"
        assert len(event_list.items) == 1
        assert event_list.items[0].name == "Secret Invasion"
        logger.info("✅ Event list creation test completed successfully")

    def test_event_list_empty_items(self):
        """Test creating an EventList with empty items list."""
        logger.info("Testing event list creation with empty items list")
        event_list = EventList(
            available=0,
            returned=0,
            collectionURI="http://gateway.marvel.com/v1/public/series/1991/events",
            items=[],
        )

        assert event_list.available == 0
        assert event_list.returned == 0
        assert len(event_list.items) == 0
        logger.info("✅ Event list empty items test completed successfully")


class TestStoryList:
    """Test cases for StoryList model.

    Tests the StoryList model which represents a collection of stories that are
    part of a specific series, including pagination metadata and story summaries.
    """

    def test_story_list_creation(self):
        """Test creating a StoryList with valid data."""
        logger.info("Testing story list creation with valid data")
        story_list = StoryList(
            available=300,
            returned=75,
            collectionURI="http://gateway.marvel.com/v1/public/series/1991/stories",
            items=[],
        )

        assert story_list.available == 300
        assert story_list.returned == 75
        assert (
            story_list.collection_uri == "http://gateway.marvel.com/v1/public/series/1991/stories"
        )
        assert len(story_list.items) == 0
        logger.info("✅ Story list creation test completed successfully")

    def test_story_list_with_items(self):
        """Test creating a StoryList with items."""
        logger.info("Testing story list creation with items")
        from marvelpy.models.common import StorySummary

        story_list = StoryList(
            available=300,
            returned=75,
            collectionURI="http://gateway.marvel.com/v1/public/series/1991/stories",
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
        logger.info("✅ Story list with items test completed successfully")


class TestSeries:
    """Test cases for Series model.

    Tests the main Series model which represents a Marvel series with all associated
    information including basic details, description, publication dates, and related resources.
    """

    def test_series_creation_minimal(self):
        """Test creating a Series with minimal required data."""
        logger.info("Testing series creation with minimal required data")
        series = Series(
            id=1991,
            title="Avengers (1998 - 2004)",
            description="The Avengers reunite to face new threats...",
            resourceURI="http://gateway.marvel.com/v1/public/series/1991",
            start_year=1998,
            end_year=2004,
            rating="",
            modified="2013-11-20T17:40:18-0500",
            comics=ComicList(
                available=200,
                returned=50,
                collectionURI="http://gateway.marvel.com/v1/public/series/1991/comics",
                items=[],
            ),
            stories=StoryList(
                available=300,
                returned=75,
                collectionURI="http://gateway.marvel.com/v1/public/series/1991/stories",
                items=[],
            ),
            events=EventList(
                available=5,
                returned=3,
                collectionURI="http://gateway.marvel.com/v1/public/series/1991/events",
                items=[],
            ),
            characters=CharacterList(
                available=25,
                returned=10,
                collectionURI="http://gateway.marvel.com/v1/public/series/1991/characters",
                items=[],
            ),
            creators=CreatorList(
                available=15,
                returned=8,
                collectionURI="http://gateway.marvel.com/v1/public/series/1991/creators",
                items=[],
            ),
        )

        assert series.id == 1991
        assert series.title == "Avengers (1998 - 2004)"
        assert series.description == "The Avengers reunite to face new threats..."
        assert series.resource_uri == "http://gateway.marvel.com/v1/public/series/1991"
        assert series.start_year == 1998
        assert series.end_year == 2004
        assert series.rating == ""
        assert series.modified == "2013-11-20T17:40:18-0500"
        assert series.thumbnail is None
        assert series.next is None
        assert series.previous is None
        logger.info("✅ Series creation minimal test completed successfully")

    def test_series_creation_with_optional_fields(self):
        """Test creating a Series with all optional fields."""
        logger.info("Testing series creation with all optional fields")
        thumbnail = Image(
            path="http://i.annihil.us/u/prod/marvel/i/mg/9/c0/527bb7b37ff55", extension="jpg"
        )

        next_series = SeriesSummary(
            resourceURI="http://gateway.marvel.com/v1/public/series/1992", name="Next Series"
        )

        previous_series = SeriesSummary(
            resourceURI="http://gateway.marvel.com/v1/public/series/1990", name="Previous Series"
        )

        url = URL(type="detail", url="http://marvel.com/comics/series/1991/avengers_1998_-_2004")

        series = Series(
            id=1991,
            title="Avengers (1998 - 2004)",
            description="The Avengers reunite to face new threats...",
            resourceURI="http://gateway.marvel.com/v1/public/series/1991",
            urls=[url],
            start_year=1998,
            end_year=2004,
            rating="T+",
            modified="2013-11-20T17:40:18-0500",
            thumbnail=thumbnail,
            comics=ComicList(
                available=200,
                returned=50,
                collectionURI="http://gateway.marvel.com/v1/public/series/1991/comics",
                items=[],
            ),
            stories=StoryList(
                available=300,
                returned=75,
                collectionURI="http://gateway.marvel.com/v1/public/series/1991/stories",
                items=[],
            ),
            events=EventList(
                available=5,
                returned=3,
                collectionURI="http://gateway.marvel.com/v1/public/series/1991/events",
                items=[],
            ),
            characters=CharacterList(
                available=25,
                returned=10,
                collectionURI="http://gateway.marvel.com/v1/public/series/1991/characters",
                items=[],
            ),
            creators=CreatorList(
                available=15,
                returned=8,
                collectionURI="http://gateway.marvel.com/v1/public/series/1991/creators",
                items=[],
            ),
            next=next_series,
            previous=previous_series,
        )

        assert series.thumbnail is not None
        assert series.thumbnail.path == "http://i.annihil.us/u/prod/marvel/i/mg/9/c0/527bb7b37ff55"
        assert series.thumbnail.extension == "jpg"
        assert series.next is not None
        assert series.next.name == "Next Series"
        assert series.previous is not None
        assert series.previous.name == "Previous Series"
        assert len(series.urls) == 1
        assert series.urls[0].type == "detail"
        assert series.rating == "T+"
        logger.info("✅ Series creation with optional fields test completed successfully")

    def test_series_ongoing_series(self):
        """Test creating a Series that is ongoing (no end_year)."""
        logger.info("Testing series creation for ongoing series (no end_year)")
        series = Series(
            id=1991,
            title="Avengers (1998 - Present)",
            description="The Avengers continue to face new threats...",
            resourceURI="http://gateway.marvel.com/v1/public/series/1991",
            start_year=1998,
            end_year=None,
            rating="",
            modified="2013-11-20T17:40:18-0500",
            comics=ComicList(
                available=200,
                returned=50,
                collectionURI="http://gateway.marvel.com/v1/public/series/1991/comics",
                items=[],
            ),
            stories=StoryList(
                available=300,
                returned=75,
                collectionURI="http://gateway.marvel.com/v1/public/series/1991/stories",
                items=[],
            ),
            events=EventList(
                available=5,
                returned=3,
                collectionURI="http://gateway.marvel.com/v1/public/series/1991/events",
                items=[],
            ),
            characters=CharacterList(
                available=25,
                returned=10,
                collectionURI="http://gateway.marvel.com/v1/public/series/1991/characters",
                items=[],
            ),
            creators=CreatorList(
                available=15,
                returned=8,
                collectionURI="http://gateway.marvel.com/v1/public/series/1991/creators",
                items=[],
            ),
        )

        assert series.end_year is None
        assert series.title == "Avengers (1998 - Present)"
        logger.info("✅ Series ongoing series test completed successfully")

    def test_series_missing_required_fields(self):
        """Test that Series requires all mandatory fields."""
        logger.info("Testing series missing required fields validation")
        with pytest.raises(ValidationError) as exc_info:
            Series(id=1991, title="Avengers (1998 - 2004)")

        errors = exc_info.value.errors()
        assert len(errors) >= 6  # Should have errors for missing required fields
        logger.info("✅ Series missing required fields test completed successfully")

    def test_series_field_access(self):
        """Test accessing Series fields after creation."""
        logger.info("Testing series field access after creation")
        series = Series(
            id=1991,
            title="Avengers (1998 - 2004)",
            description="Test description",
            resourceURI="http://gateway.marvel.com/v1/public/series/1991",
            start_year=1998,
            end_year=2004,
            rating="",
            modified="2013-11-20T17:40:18-0500",
            comics=ComicList(
                available=200,
                returned=50,
                collectionURI="http://gateway.marvel.com/v1/public/series/1991/comics",
                items=[],
            ),
            stories=StoryList(
                available=300,
                returned=75,
                collectionURI="http://gateway.marvel.com/v1/public/series/1991/stories",
                items=[],
            ),
            events=EventList(
                available=5,
                returned=3,
                collectionURI="http://gateway.marvel.com/v1/public/series/1991/events",
                items=[],
            ),
            characters=CharacterList(
                available=25,
                returned=10,
                collectionURI="http://gateway.marvel.com/v1/public/series/1991/characters",
                items=[],
            ),
            creators=CreatorList(
                available=15,
                returned=8,
                collectionURI="http://gateway.marvel.com/v1/public/series/1991/creators",
                items=[],
            ),
        )

        # Test that all fields are accessible
        assert isinstance(series.comics, ComicList)
        assert isinstance(series.stories, StoryList)
        assert isinstance(series.events, EventList)
        assert isinstance(series.characters, CharacterList)
        assert isinstance(series.creators, CreatorList)
        logger.info("✅ Series field access test completed successfully")


class TestSeriesListResponse:
    """Test cases for SeriesListResponse model.

    Tests the SeriesListResponse model which represents a Marvel API response
    containing a list of series with pagination metadata.
    """

    def test_series_list_response_creation(self):
        """Test creating a SeriesListResponse with valid data."""
        logger.info("Testing series list response creation with valid data")
        from marvelpy.models.base import DataContainer

        series = Series(
            id=1991,
            title="Avengers (1998 - 2004)",
            description="Test description",
            resourceURI="http://gateway.marvel.com/v1/public/series/1991",
            start_year=1998,
            end_year=2004,
            rating="",
            modified="2013-11-20T17:40:18-0500",
            comics=ComicList(
                available=200,
                returned=50,
                collectionURI="http://gateway.marvel.com/v1/public/series/1991/comics",
                items=[],
            ),
            stories=StoryList(
                available=300,
                returned=75,
                collectionURI="http://gateway.marvel.com/v1/public/series/1991/stories",
                items=[],
            ),
            events=EventList(
                available=5,
                returned=3,
                collectionURI="http://gateway.marvel.com/v1/public/series/1991/events",
                items=[],
            ),
            characters=CharacterList(
                available=25,
                returned=10,
                collectionURI="http://gateway.marvel.com/v1/public/series/1991/characters",
                items=[],
            ),
            creators=CreatorList(
                available=15,
                returned=8,
                collectionURI="http://gateway.marvel.com/v1/public/series/1991/creators",
                items=[],
            ),
        )

        response = SeriesListResponse(
            code=200,
            status="Ok",
            copyright="© 2024 MARVEL",
            attributionText="Data provided by Marvel. © 2024 MARVEL",
            attributionHTML="<a href='http://marvel.com'>Data provided by Marvel. © 2024 MARVEL</a>",
            etag="etag123",
            data=DataContainer(offset=0, limit=20, total=100, count=1, results=[series]),
        )

        assert response.code == 200
        assert response.status == "Ok"
        assert response.data.count == 1
        assert response.data.results[0].title == "Avengers (1998 - 2004)"
        logger.info("✅ Series list response creation test completed successfully")

    def test_series_list_response_empty_results(self):
        """Test creating a SeriesListResponse with empty results."""
        logger.info("Testing series list response creation with empty results")
        from marvelpy.models.base import DataContainer

        response = SeriesListResponse(
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
        logger.info("✅ Series list response empty results test completed successfully")


class TestSeriesResponse:
    """Test cases for SeriesResponse model.

    Tests the SeriesResponse model which represents a Marvel API response
    containing a single series with full details.
    """

    def test_series_response_creation(self):
        """Test creating a SeriesResponse with valid data."""
        logger.info("Testing series response creation with valid data")
        series = Series(
            id=1991,
            title="Avengers (1998 - 2004)",
            description="Test description",
            resourceURI="http://gateway.marvel.com/v1/public/series/1991",
            start_year=1998,
            end_year=2004,
            rating="",
            modified="2013-11-20T17:40:18-0500",
            comics=ComicList(
                available=200,
                returned=50,
                collectionURI="http://gateway.marvel.com/v1/public/series/1991/comics",
                items=[],
            ),
            stories=StoryList(
                available=300,
                returned=75,
                collectionURI="http://gateway.marvel.com/v1/public/series/1991/stories",
                items=[],
            ),
            events=EventList(
                available=5,
                returned=3,
                collectionURI="http://gateway.marvel.com/v1/public/series/1991/events",
                items=[],
            ),
            characters=CharacterList(
                available=25,
                returned=10,
                collectionURI="http://gateway.marvel.com/v1/public/series/1991/characters",
                items=[],
            ),
            creators=CreatorList(
                available=15,
                returned=8,
                collectionURI="http://gateway.marvel.com/v1/public/series/1991/creators",
                items=[],
            ),
        )

        response = SeriesResponse(
            code=200,
            status="Ok",
            copyright="© 2024 MARVEL",
            attributionText="Data provided by Marvel. © 2024 MARVEL",
            attributionHTML="<a href='http://marvel.com'>Data provided by Marvel. © 2024 MARVEL</a>",
            etag="etag123",
            data=series,
        )

        assert response.code == 200
        assert response.status == "Ok"
        assert response.data.title == "Avengers (1998 - 2004)"
        assert response.data.id == 1991
        logger.info("✅ Series response creation test completed successfully")

    def test_series_response_missing_required_fields(self):
        """Test that SeriesResponse requires all mandatory fields."""
        logger.info("Testing series response missing required fields validation")
        with pytest.raises(ValidationError) as exc_info:
            SeriesResponse(code=200)

        errors = exc_info.value.errors()
        assert len(errors) >= 5  # Should have errors for missing required fields
        logger.info("✅ Series response missing required fields test completed successfully")
