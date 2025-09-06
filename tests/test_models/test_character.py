"""Tests for character model classes.

This module contains comprehensive tests for all character-related data models
used in Marvel API responses. These tests verify proper validation, field
handling, and data integrity for character structures.
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

from marvelpy.models.character import (
    Character,
    CharacterListResponse,
    CharacterResponse,
    ComicList,
    EventList,
    SeriesList,
    StoryList,
)
from marvelpy.models.common import (
    URL,
    ComicSummary,
    EventSummary,
    Image,
    SeriesSummary,
    StorySummary,
)


class TestComicList:
    """Test cases for ComicList class.

    This test class verifies the functionality of the ComicList class,
    which represents a collection of comics featuring a specific character.
    Tests cover creation, validation, and field handling.
    """

    def test_comic_list_creation(self):
        """Test ComicList can be created with required fields.

        This test verifies that ComicList properly validates and stores
        comic collection metadata and items. It ensures the Marvel API's
        standard comic list structure is correctly modeled.

        Expected behavior:
            - All required fields (available, returned, collection_uri, items) are accepted
            - Field values are stored and accessible as expected
            - Model can be instantiated with valid data
        """
        logger.info("Testing ComicList creation with required fields")
        comic_list: ComicList = ComicList(
            available=100,
            returned=20,
            collectionURI="http://gateway.marvel.com/v1/public/characters/1009368/comics",
            items=[
                ComicSummary(
                    resourceURI="http://gateway.marvel.com/v1/public/comics/21366",
                    name="Avengers (1963) #1",
                )
            ],
        )

        assert comic_list.available == 100
        assert comic_list.returned == 20
        assert (
            comic_list.collection_uri
            == "http://gateway.marvel.com/v1/public/characters/1009368/comics"
        )
        assert len(comic_list.items) == 1
        assert comic_list.items[0].name == "Avengers (1963) #1"

    def test_comic_list_missing_required_fields(self):
        """Test ComicList raises ValidationError for missing required fields.

        This test verifies that ComicList properly validates all required
        fields and raises appropriate ValidationError when fields are
        missing. This ensures data integrity for comic list information.

        Expected behavior:
            - ValidationError is raised when required fields are missing
            - Error message indicates which fields are missing
            - Model creation fails gracefully with clear error information
        """
        logger.info("Testing ComicList raises ValidationError for missing required fields")
        
        with pytest.raises(ValidationError):
            ComicList(available=100, returned=20)  # Missing collectionURI and items
        
        logger.info("✅ ComicList missing required fields test completed successfully")

    def test_comic_list_empty_items(self):
        """Test ComicList handles empty items list correctly.

        This test verifies that ComicList can handle edge cases where
        no comics are returned (e.g., when available=0 or when filtering
        returns no matches). This is important for robust list handling.

        Expected behavior:
            - Empty items list is accepted and stored correctly
            - Available and returned can be zero
            - Items list is accessible and empty
        """
        logger.info("Testing ComicList handles empty items list correctly")
        
        comic_list: ComicList = ComicList(
            available=0,
            returned=0,
            collectionURI="http://gateway.marvel.com/v1/public/characters/1009368/comics",
            items=[],
        )

        assert comic_list.available == 0
        assert comic_list.returned == 0
        assert comic_list.items == []
        
        logger.info("✅ ComicList empty items test completed successfully")


class TestStoryList:
    """Test cases for StoryList class.

    This test class verifies the functionality of the StoryList class,
    which represents a collection of stories featuring a specific character.
    Tests cover creation, validation, and field handling.
    """

    def test_story_list_creation(self):
        """Test StoryList can be created with required fields.

        This test verifies that StoryList properly validates and stores
        story collection metadata and items. It ensures the Marvel API's
        standard story list structure is correctly modeled.

        Expected behavior:
            - All required fields (available, returned, collection_uri, items) are accepted
            - Field values are stored and accessible as expected
            - Model can be instantiated with valid data
        """
        logger.info("Testing StoryList can be created with required fields")
        
        story_list: StoryList = StoryList(
            available=50,
            returned=10,
            collectionURI="http://gateway.marvel.com/v1/public/characters/1009368/stories",
            items=[
                StorySummary(
                    resourceURI="http://gateway.marvel.com/v1/public/stories/19947",
                    name="Cover #19947",
                    type="cover",
                )
            ],
        )

        assert story_list.available == 50
        assert story_list.returned == 10
        assert (
            story_list.collection_uri
            == "http://gateway.marvel.com/v1/public/characters/1009368/stories"
        )
        assert len(story_list.items) == 1
        assert story_list.items[0].name == "Cover #19947"
        
        logger.info("✅ StoryList creation test completed successfully")

    def test_story_list_missing_required_fields(self):
        """Test StoryList raises ValidationError for missing required fields.

        This test verifies that StoryList properly validates all required
        fields and raises appropriate ValidationError when fields are
        missing. This ensures data integrity for story list information.

        Expected behavior:
            - ValidationError is raised when required fields are missing
            - Error message indicates which fields are missing
            - Model creation fails gracefully with clear error information
        """
        logger.info("Testing StoryList raises ValidationError for missing required fields")
        
        with pytest.raises(ValidationError):
            StoryList(available=50, returned=10)  # Missing collectionURI and items
        
        logger.info("✅ StoryList missing required fields test completed successfully")


class TestEventList:
    """Test cases for EventList class.

    This test class verifies the functionality of the EventList class,
    which represents a collection of events featuring a specific character.
    Tests cover creation, validation, and field handling.
    """

    def test_event_list_creation(self):
        """Test EventList can be created with required fields.

        This test verifies that EventList properly validates and stores
        event collection metadata and items. It ensures the Marvel API's
        standard event list structure is correctly modeled.

        Expected behavior:
            - All required fields (available, returned, collection_uri, items) are accepted
            - Field values are stored and accessible as expected
            - Model can be instantiated with valid data
        """
        logger.info("Testing EventList can be created with required fields")
        
        event_list: EventList = EventList(
            available=25,
            returned=5,
            collectionURI="http://gateway.marvel.com/v1/public/characters/1009368/events",
            items=[
                EventSummary(
                    resourceURI="http://gateway.marvel.com/v1/public/events/269",
                    name="Secret Invasion",
                )
            ],
        )

        assert event_list.available == 25
        assert event_list.returned == 5
        assert (
            event_list.collection_uri
            == "http://gateway.marvel.com/v1/public/characters/1009368/events"
        )
        assert len(event_list.items) == 1
        assert event_list.items[0].name == "Secret Invasion"
        
        logger.info("✅ EventList creation test completed successfully")

    def test_event_list_missing_required_fields(self):
        """Test EventList raises ValidationError for missing required fields.

        This test verifies that EventList properly validates all required
        fields and raises appropriate ValidationError when fields are
        missing. This ensures data integrity for event list information.

        Expected behavior:
            - ValidationError is raised when required fields are missing
            - Error message indicates which fields are missing
            - Model creation fails gracefully with clear error information
        """
        logger.info("Testing EventList raises ValidationError for missing required fields")
        
        with pytest.raises(ValidationError):
            EventList(available=25, returned=5)  # Missing collectionURI and items
        
        logger.info("✅ EventList missing required fields test completed successfully")


class TestSeriesList:
    """Test cases for SeriesList class.

    This test class verifies the functionality of the SeriesList class,
    which represents a collection of series featuring a specific character.
    Tests cover creation, validation, and field handling.
    """

    def test_series_list_creation(self):
        """Test SeriesList can be created with required fields.

        This test verifies that SeriesList properly validates and stores
        series collection metadata and items. It ensures the Marvel API's
        standard series list structure is correctly modeled.

        Expected behavior:
            - All required fields (available, returned, collection_uri, items) are accepted
            - Field values are stored and accessible as expected
            - Model can be instantiated with valid data
        """
        logger.info("Testing SeriesList can be created with required fields")
        
        series_list: SeriesList = SeriesList(
            available=75,
            returned=15,
            collectionURI="http://gateway.marvel.com/v1/public/characters/1009368/series",
            items=[
                SeriesSummary(
                    resourceURI="http://gateway.marvel.com/v1/public/series/1945",
                    name="Avengers (1998 - 2004)",
                )
            ],
        )

        assert series_list.available == 75
        assert series_list.returned == 15
        assert (
            series_list.collection_uri
            == "http://gateway.marvel.com/v1/public/characters/1009368/series"
        )
        assert len(series_list.items) == 1
        assert series_list.items[0].name == "Avengers (1998 - 2004)"
        
        logger.info("✅ SeriesList creation test completed successfully")

    def test_series_list_missing_required_fields(self):
        """Test SeriesList raises ValidationError for missing required fields.

        This test verifies that SeriesList properly validates all required
        fields and raises appropriate ValidationError when fields are
        missing. This ensures data integrity for series list information.

        Expected behavior:
            - ValidationError is raised when required fields are missing
            - Error message indicates which fields are missing
            - Model creation fails gracefully with clear error information
        """
        logger.info("Testing SeriesList raises ValidationError for missing required fields")
        
        with pytest.raises(ValidationError):
            SeriesList(available=75, returned=15)  # Missing collectionURI and items
        
        logger.info("✅ SeriesList missing required fields test completed successfully")


class TestCharacter:
    """Test cases for Character class.

    This test class verifies the functionality of the Character class,
    which represents a Marvel character with all associated information.
    Tests cover creation, validation, and field handling.
    """

    def test_character_creation(self):
        """Test Character can be created with required fields.

        This test verifies that Character properly validates and stores
        all character information including basic details, description,
        images, and related resources. It ensures the Marvel API's
        standard character structure is correctly modeled.

        Expected behavior:
            - All required fields are accepted and validated
            - Field values are stored and accessible as expected
            - Model can be instantiated with valid data
        """
        logger.info("Testing Character can be created with required fields")
        
        character: Character = Character(
            id=1009368,
            name="Iron Man",
            description="Wounded, captured and forced to build a weapon by his enemies...",
            modified="2014-04-29T14:18:17-0400",
            resourceURI="http://gateway.marvel.com/v1/public/characters/1009368",
            urls=[
                URL(
                    type="detail", url="http://marvel.com/characters/9/iron_man?utm_campaign=apiRef"
                )
            ],
            thumbnail=Image(
                path="http://i.annihil.us/u/prod/marvel/i/mg/9/c0/527bb7b37ff55",
                extension="jpg",
            ),
            comics=ComicList(
                available=100,
                returned=20,
                collectionURI="http://gateway.marvel.com/v1/public/characters/1009368/comics",
                items=[],
            ),
            stories=StoryList(
                available=50,
                returned=10,
                collectionURI="http://gateway.marvel.com/v1/public/characters/1009368/stories",
                items=[],
            ),
            events=EventList(
                available=25,
                returned=5,
                collectionURI="http://gateway.marvel.com/v1/public/characters/1009368/events",
                items=[],
            ),
            series=SeriesList(
                available=75,
                returned=15,
                collectionURI="http://gateway.marvel.com/v1/public/characters/1009368/series",
                items=[],
            ),
        )

        assert character.id == 1009368
        assert character.name == "Iron Man"
        assert (
            character.description
            == "Wounded, captured and forced to build a weapon by his enemies..."
        )
        assert character.modified == "2014-04-29T14:18:17-0400"
        assert character.resource_uri == "http://gateway.marvel.com/v1/public/characters/1009368"
        assert len(character.urls) == 1
        assert character.urls[0].type == "detail"
        assert character.thumbnail is not None
        assert character.thumbnail.extension == "jpg"
        assert character.comics.available == 100
        assert character.stories.available == 50
        assert character.events.available == 25
        assert character.series.available == 75
        
        logger.info("✅ Character creation test completed successfully")

    def test_character_missing_required_fields(self):
        """Test Character raises ValidationError for missing required fields.

        This test verifies that Character properly validates all required
        fields and raises appropriate ValidationError when fields are
        missing. This ensures data integrity for character information.

        Expected behavior:
            - ValidationError is raised when required fields are missing
            - Error message indicates which fields are missing
            - Model creation fails gracefully with clear error information
        """
        logger.info("Testing Character raises ValidationError for missing required fields")
        
        with pytest.raises(ValidationError):
            Character(
                id=1009368,
                name="Iron Man",
                # Missing other required fields
            )
        
        logger.info("✅ Character missing required fields test completed successfully")

    def test_character_optional_thumbnail(self):
        """Test Character handles optional thumbnail field correctly.

        This test verifies that Character can handle cases where the
        thumbnail field is None, which can happen when no image is
        available for a character.

        Expected behavior:
            - Character can be created with thumbnail=None
            - Thumbnail field is accessible and None
            - Other fields remain unaffected
        """
        logger.info("Testing Character handles optional thumbnail field correctly")
        
        character: Character = Character(
            id=1009368,
            name="Iron Man",
            description="Test description",
            modified="2014-04-29T14:18:17-0400",
            resourceURI="http://gateway.marvel.com/v1/public/characters/1009368",
            urls=[],
            thumbnail=None,
            comics=ComicList(
                available=0,
                returned=0,
                collectionURI="http://gateway.marvel.com/v1/public/characters/1009368/comics",
                items=[],
            ),
            stories=StoryList(
                available=0,
                returned=0,
                collectionURI="http://gateway.marvel.com/v1/public/characters/1009368/stories",
                items=[],
            ),
            events=EventList(
                available=0,
                returned=0,
                collectionURI="http://gateway.marvel.com/v1/public/characters/1009368/events",
                items=[],
            ),
            series=SeriesList(
                available=0,
                returned=0,
                collectionURI="http://gateway.marvel.com/v1/public/characters/1009368/series",
                items=[],
            ),
        )

        assert character.thumbnail is None
        assert character.name == "Iron Man"
        
        logger.info("✅ Character optional thumbnail test completed successfully")

    def test_character_empty_urls(self):
        """Test Character handles empty URLs list correctly.

        This test verifies that Character can handle cases where the
        urls field is an empty list, which can happen when no external
        URLs are associated with a character.

        Expected behavior:
            - Character can be created with empty urls list
            - URLs field is accessible and empty
            - Other fields remain unaffected
        """
        logger.info("Testing Character handles empty URLs list correctly")
        
        character: Character = Character(
            id=1009368,
            name="Iron Man",
            description="Test description",
            modified="2014-04-29T14:18:17-0400",
            resourceURI="http://gateway.marvel.com/v1/public/characters/1009368",
            urls=[],
            thumbnail=None,
            comics=ComicList(
                available=0,
                returned=0,
                collectionURI="http://gateway.marvel.com/v1/public/characters/1009368/comics",
                items=[],
            ),
            stories=StoryList(
                available=0,
                returned=0,
                collectionURI="http://gateway.marvel.com/v1/public/characters/1009368/stories",
                items=[],
            ),
            events=EventList(
                available=0,
                returned=0,
                collectionURI="http://gateway.marvel.com/v1/public/characters/1009368/events",
                items=[],
            ),
            series=SeriesList(
                available=0,
                returned=0,
                collectionURI="http://gateway.marvel.com/v1/public/characters/1009368/series",
                items=[],
            ),
        )

        assert character.urls == []
        assert character.name == "Iron Man"
        
        logger.info("✅ Character empty URLs test completed successfully")


class TestCharacterResponse:
    """Test cases for CharacterResponse class.

    This test class verifies the functionality of the CharacterResponse class,
    which represents a Marvel API response containing a single character.
    Tests cover creation, validation, and field handling.
    """

    def test_character_response_creation(self):
        """Test CharacterResponse can be created with required fields.

        This test verifies that CharacterResponse properly validates and stores
        all Marvel API response metadata along with character data. It ensures
        the standard single character response structure is correctly modeled.

        Expected behavior:
            - All required fields are accepted and validated
            - Character data is properly nested in the response
            - Model can be instantiated with valid data
        """
        logger.info("Testing CharacterResponse can be created with required fields")
        
        character = Character(
            id=1009368,
            name="Iron Man",
            description="Test description",
            modified="2014-04-29T14:18:17-0400",
            resourceURI="http://gateway.marvel.com/v1/public/characters/1009368",
            urls=[],
            thumbnail=None,
            comics=ComicList(
                available=0,
                returned=0,
                collectionURI="http://gateway.marvel.com/v1/public/characters/1009368/comics",
                items=[],
            ),
            stories=StoryList(
                available=0,
                returned=0,
                collectionURI="http://gateway.marvel.com/v1/public/characters/1009368/stories",
                items=[],
            ),
            events=EventList(
                available=0,
                returned=0,
                collectionURI="http://gateway.marvel.com/v1/public/characters/1009368/events",
                items=[],
            ),
            series=SeriesList(
                available=0,
                returned=0,
                collectionURI="http://gateway.marvel.com/v1/public/characters/1009368/series",
                items=[],
            ),
        )

        response: CharacterResponse = CharacterResponse(
            code=200,
            status="Ok",
            copyright="© 2024 MARVEL",
            attributionText="Data provided by Marvel. © 2024 MARVEL",
            attributionHTML="<a href='http://marvel.com'>Data provided by Marvel. © 2024 MARVEL</a>",
            etag="etag123",
            data=character,
        )

        assert response.code == 200
        assert response.status == "Ok"
        assert response.copyright == "© 2024 MARVEL"
        assert response.data.name == "Iron Man"
        assert response.data.id == 1009368
        
        logger.info("✅ CharacterResponse creation test completed successfully")

    def test_character_response_missing_required_fields(self):
        """Test CharacterResponse raises ValidationError for missing required fields.

        This test verifies that CharacterResponse properly validates all required
        fields and raises appropriate ValidationError when fields are
        missing. This ensures data integrity for character response information.

        Expected behavior:
            - ValidationError is raised when required fields are missing
            - Error message indicates which fields are missing
            - Model creation fails gracefully with clear error information
        """
        logger.info("Testing CharacterResponse raises ValidationError for missing required fields")
        
        with pytest.raises(ValidationError):
            CharacterResponse(code=200, status="Ok")  # Missing other required fields
        
        logger.info("✅ CharacterResponse missing required fields test completed successfully")


class TestCharacterListResponse:
    """Test cases for CharacterListResponse class.

    This test class verifies the functionality of the CharacterListResponse class,
    which represents a Marvel API response containing a list of characters.
    Tests cover creation, validation, and field handling.
    """

    def test_character_list_response_creation(self):
        """Test CharacterListResponse can be created with required fields.

        This test verifies that CharacterListResponse properly validates and stores
        all Marvel API response metadata along with character list data. It ensures
        the standard character list response structure is correctly modeled.

        Expected behavior:
            - All required fields are accepted and validated
            - Character list data is properly nested in the response
            - Model can be instantiated with valid data
        """
        logger.info("Testing CharacterListResponse can be created with required fields")
        
        from marvelpy.models.base import DataContainer

        character = Character(
            id=1009368,
            name="Iron Man",
            description="Test description",
            modified="2014-04-29T14:18:17-0400",
            resourceURI="http://gateway.marvel.com/v1/public/characters/1009368",
            urls=[],
            thumbnail=None,
            comics=ComicList(
                available=0,
                returned=0,
                collectionURI="http://gateway.marvel.com/v1/public/characters/1009368/comics",
                items=[],
            ),
            stories=StoryList(
                available=0,
                returned=0,
                collectionURI="http://gateway.marvel.com/v1/public/characters/1009368/stories",
                items=[],
            ),
            events=EventList(
                available=0,
                returned=0,
                collectionURI="http://gateway.marvel.com/v1/public/characters/1009368/events",
                items=[],
            ),
            series=SeriesList(
                available=0,
                returned=0,
                collectionURI="http://gateway.marvel.com/v1/public/characters/1009368/series",
                items=[],
            ),
        )

        data_container: DataContainer[Character] = DataContainer(
            offset=0,
            limit=20,
            total=100,
            count=1,
            results=[character],
        )

        response: CharacterListResponse = CharacterListResponse(
            code=200,
            status="Ok",
            copyright="© 2024 MARVEL",
            attributionText="Data provided by Marvel. © 2024 MARVEL",
            attributionHTML="<a href='http://marvel.com'>Data provided by Marvel. © 2024 MARVEL</a>",
            etag="etag123",
            data=data_container,
        )

        assert response.code == 200
        assert response.status == "Ok"
        assert response.copyright == "© 2024 MARVEL"
        assert response.data.total == 100
        assert response.data.count == 1
        assert len(response.data.results) == 1
        assert response.data.results[0].name == "Iron Man"
        
        logger.info("✅ CharacterListResponse creation test completed successfully")

    def test_character_list_response_missing_required_fields(self):
        """Test CharacterListResponse raises ValidationError for missing required fields.

        This test verifies that CharacterListResponse properly validates all required
        fields and raises appropriate ValidationError when fields are
        missing. This ensures data integrity for character list response information.

        Expected behavior:
            - ValidationError is raised when required fields are missing
            - Error message indicates which fields are missing
            - Model creation fails gracefully with clear error information
        """
        logger.info("Testing CharacterListResponse raises ValidationError for missing required fields")
        
        with pytest.raises(ValidationError):
            CharacterListResponse(code=200, status="Ok")  # Missing other required fields
        
        logger.info("✅ CharacterListResponse missing required fields test completed successfully")
