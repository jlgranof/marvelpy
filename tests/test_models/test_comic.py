"""Tests for comic model classes.

This module contains comprehensive tests for all comic-related data models
used in Marvel API responses. These tests verify proper validation, field
handling, and data integrity for comic structures.
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

from marvelpy.models.comic import (
    CharacterList,
    Comic,
    ComicListResponse,
    ComicResponse,
    CreatorList,
    EventList,
    StoryList,
)
from marvelpy.models.common import (
    URL,
    CharacterSummary,
    CreatorSummary,
    Date,
    EventSummary,
    Image,
    Price,
    SeriesSummary,
    StorySummary,
    TextObject,
)


class TestCharacterList:
    """Test cases for CharacterList class.

    This test class verifies the functionality of the CharacterList class,
    which represents a collection of characters appearing in a specific comic.
    Tests cover creation, validation, and field handling.
    """

    def test_character_list_creation(self):
        """Test CharacterList can be created with required fields.

        This test verifies that CharacterList properly validates and stores
        character collection metadata and items. It ensures the Marvel API's
        standard character list structure is correctly modeled.

        Expected behavior:
            - All required fields (available, returned, collection_uri, items) are accepted
            - Field values are stored and accessible as expected
            - Model can be instantiated with valid data
        """
        logger.info("Testing CharacterList creation with required fields")
        character_list: CharacterList = CharacterList(
            available=10,
            returned=5,
            collectionURI="http://gateway.marvel.com/v1/public/comics/21366/characters",
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
            == "http://gateway.marvel.com/v1/public/comics/21366/characters"
        )
        assert len(character_list.items) == 1
        assert character_list.items[0].name == "Iron Man"

    def test_character_list_missing_required_fields(self):
        """Test CharacterList raises ValidationError for missing required fields.

        This test verifies that CharacterList properly validates all required
        fields and raises appropriate ValidationError when fields are
        missing. This ensures data integrity for character list information.

        Expected behavior:
            - ValidationError is raised when required fields are missing
            - Error message indicates which fields are missing
            - Model creation fails gracefully with clear error information
        """
        logger.info("Testing CharacterList raises ValidationError for missing required fields")
        
        with pytest.raises(ValidationError):
            CharacterList(available=10, returned=5)  # Missing collectionURI and items
        
        logger.info("✅ CharacterList missing required fields test completed successfully")


class TestCreatorList:
    """Test cases for CreatorList class.

    This test class verifies the functionality of the CreatorList class,
    which represents a collection of creators who worked on a specific comic.
    Tests cover creation, validation, and field handling.
    """

    def test_creator_list_creation(self):
        """Test CreatorList can be created with required fields.

        This test verifies that CreatorList properly validates and stores
        creator collection metadata and items. It ensures the Marvel API's
        standard creator list structure is correctly modeled.

        Expected behavior:
            - All required fields (available, returned, collection_uri, items) are accepted
            - Field values are stored and accessible as expected
            - Model can be instantiated with valid data
        """
        logger.info("Testing CreatorList can be created with required fields")
        
        creator_list: CreatorList = CreatorList(
            available=5,
            returned=3,
            collectionURI="http://gateway.marvel.com/v1/public/comics/21366/creators",
            items=[
                CreatorSummary(
                    resourceURI="http://gateway.marvel.com/v1/public/creators/30",
                    name="Stan Lee",
                    role="writer",
                )
            ],
        )

        assert creator_list.available == 5
        assert creator_list.returned == 3
        assert (
            creator_list.collection_uri
            == "http://gateway.marvel.com/v1/public/comics/21366/creators"
        )
        assert len(creator_list.items) == 1
        assert creator_list.items[0].name == "Stan Lee"
        
        logger.info("✅ CreatorList creation test completed successfully")

    def test_creator_list_missing_required_fields(self):
        """Test CreatorList raises ValidationError for missing required fields.

        This test verifies that CreatorList properly validates all required
        fields and raises appropriate ValidationError when fields are
        missing. This ensures data integrity for creator list information.

        Expected behavior:
            - ValidationError is raised when required fields are missing
            - Error message indicates which fields are missing
            - Model creation fails gracefully with clear error information
        """
        logger.info("Testing CreatorList raises ValidationError for missing required fields")
        
        with pytest.raises(ValidationError):
            CreatorList(available=5, returned=3)  # Missing collectionURI and items
        
        logger.info("✅ CreatorList missing required fields test completed successfully")


class TestStoryList:
    """Test cases for StoryList class.

    This test class verifies the functionality of the StoryList class,
    which represents a collection of stories contained in a specific comic.
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
            available=3,
            returned=2,
            collectionURI="http://gateway.marvel.com/v1/public/comics/21366/stories",
            items=[
                StorySummary(
                    resourceURI="http://gateway.marvel.com/v1/public/stories/19947",
                    name="Cover #1",
                    type="cover",
                )
            ],
        )

        assert story_list.available == 3
        assert story_list.returned == 2
        assert (
            story_list.collection_uri == "http://gateway.marvel.com/v1/public/comics/21366/stories"
        )
        assert len(story_list.items) == 1
        assert story_list.items[0].name == "Cover #1"
        
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
            StoryList(available=3, returned=2)  # Missing collectionURI and items
        
        logger.info("✅ StoryList missing required fields test completed successfully")


class TestEventList:
    """Test cases for EventList class.

    This test class verifies the functionality of the EventList class,
    which represents a collection of events that a specific comic is part of.
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
            available=2,
            returned=1,
            collectionURI="http://gateway.marvel.com/v1/public/comics/21366/events",
            items=[
                EventSummary(
                    resourceURI="http://gateway.marvel.com/v1/public/events/269",
                    name="Secret Invasion",
                )
            ],
        )

        assert event_list.available == 2
        assert event_list.returned == 1
        assert (
            event_list.collection_uri == "http://gateway.marvel.com/v1/public/comics/21366/events"
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
            EventList(available=2, returned=1)  # Missing collectionURI and items
        
        logger.info("✅ EventList missing required fields test completed successfully")


class TestComic:
    """Test cases for Comic class.

    This test class verifies the functionality of the Comic class,
    which represents a Marvel comic with all associated information.
    Tests cover creation, validation, and field handling.
    """

    def test_comic_creation(self):
        """Test Comic can be created with required fields.

        This test verifies that Comic properly validates and stores
        all comic information including publication details, creators,
        characters, stories, and related resources. It ensures the
        Marvel API's standard comic structure is correctly modeled.

        Expected behavior:
            - All required fields are accepted and validated
            - Field values are stored and accessible as expected
            - Model can be instantiated with valid data
        """
        logger.info("Testing Comic can be created with required fields")
        
        comic: Comic = Comic(
            id=21366,
            digitalId=0,
            title="Avengers (1963) #1",
            issueNumber=1,
            variantDescription="",
            description="The Avengers are born!",
            modified="2014-04-29T14:18:17-0400",
            isbn="",
            upc="",
            diamondCode="",
            ean="",
            issn="",
            format="Comic",
            pageCount=32,
            textObjects=[],
            resourceURI="http://gateway.marvel.com/v1/public/comics/21366",
            urls=[],
            series=SeriesSummary(
                resourceURI="http://gateway.marvel.com/v1/public/series/1945",
                name="Avengers (1963 - 1996)",
            ),
            variants=[],
            collections=[],
            collectedIssues=[],
            dates=[],
            prices=[],
            thumbnail=None,
            images=[],
            creators=CreatorList(
                available=0,
                returned=0,
                collectionURI="http://gateway.marvel.com/v1/public/comics/21366/creators",
                items=[],
            ),
            characters=CharacterList(
                available=0,
                returned=0,
                collectionURI="http://gateway.marvel.com/v1/public/comics/21366/characters",
                items=[],
            ),
            stories=StoryList(
                available=0,
                returned=0,
                collectionURI="http://gateway.marvel.com/v1/public/comics/21366/stories",
                items=[],
            ),
            events=EventList(
                available=0,
                returned=0,
                collectionURI="http://gateway.marvel.com/v1/public/comics/21366/events",
                items=[],
            ),
        )

        assert comic.id == 21366
        assert comic.digital_id == 0
        assert comic.title == "Avengers (1963) #1"
        assert comic.issue_number == 1
        assert comic.variant_description == ""
        assert comic.description == "The Avengers are born!"
        assert comic.modified == "2014-04-29T14:18:17-0400"
        assert comic.isbn == ""
        assert comic.upc == ""
        assert comic.diamond_code == ""
        assert comic.ean == ""
        assert comic.issn == ""
        assert comic.format == "Comic"
        assert comic.page_count == 32
        assert comic.text_objects == []
        assert comic.resource_uri == "http://gateway.marvel.com/v1/public/comics/21366"
        assert comic.urls == []
        assert comic.series.name == "Avengers (1963 - 1996)"
        assert comic.variants == []
        assert comic.collections == []
        assert comic.collected_issues == []
        assert comic.dates == []
        assert comic.prices == []
        assert comic.thumbnail is None
        assert comic.images == []
        assert comic.creators.available == 0
        assert comic.characters.available == 0
        assert comic.stories.available == 0
        assert comic.events.available == 0
        
        logger.info("✅ Comic creation test completed successfully")

    def test_comic_missing_required_fields(self):
        """Test Comic raises ValidationError for missing required fields.

        This test verifies that Comic properly validates all required
        fields and raises appropriate ValidationError when fields are
        missing. This ensures data integrity for comic information.

        Expected behavior:
            - ValidationError is raised when required fields are missing
            - Error message indicates which fields are missing
            - Model creation fails gracefully with clear error information
        """
        logger.info("Testing Comic raises ValidationError for missing required fields")
        
        with pytest.raises(ValidationError):
            Comic(
                id=21366,
                title="Avengers (1963) #1",
                # Missing other required fields
            )
        
        logger.info("✅ Comic missing required fields test completed successfully")

    def test_comic_with_optional_fields(self):
        """Test Comic handles optional fields correctly.

        This test verifies that Comic can handle optional fields like
        thumbnail, images, dates, and prices. This is important for
        comprehensive comic data representation.

        Expected behavior:
            - Optional fields can be populated with data
            - Field values are stored and accessible as expected
            - Model handles various data types appropriately
        """
        logger.info("Testing Comic handles optional fields correctly")
        
        comic: Comic = Comic(
            id=21366,
            digitalId=0,
            title="Avengers (1963) #1",
            issueNumber=1,
            variantDescription="",
            description="The Avengers are born!",
            modified="2014-04-29T14:18:17-0400",
            isbn="",
            upc="",
            diamondCode="",
            ean="",
            issn="",
            format="Comic",
            pageCount=32,
            textObjects=[
                TextObject(
                    type="description",
                    language="en-us",
                    text="The Avengers are born!",
                )
            ],
            resourceURI="http://gateway.marvel.com/v1/public/comics/21366",
            urls=[
                URL(
                    type="detail",
                    url="http://marvel.com/comics/issue/21366/avengers_1963_1",
                )
            ],
            series=SeriesSummary(
                resourceURI="http://gateway.marvel.com/v1/public/series/1945",
                name="Avengers (1963 - 1996)",
            ),
            variants=[],
            collections=[],
            collectedIssues=[],
            dates=[
                Date(type="onsaleDate", date="1963-09-01T00:00:00-0400"),
                Date(type="focDate", date="1963-08-15T00:00:00-0400"),
            ],
            prices=[
                Price(type="printPrice", price=0.12),
                Price(type="digitalPrice", price=1.99),
            ],
            thumbnail=Image(
                path="http://i.annihil.us/u/prod/marvel/i/mg/9/c0/527bb7b37ff55",
                extension="jpg",
            ),
            images=[
                Image(
                    path="http://i.annihil.us/u/prod/marvel/i/mg/9/c0/527bb7b37ff55",
                    extension="jpg",
                )
            ],
            creators=CreatorList(
                available=0,
                returned=0,
                collectionURI="http://gateway.marvel.com/v1/public/comics/21366/creators",
                items=[],
            ),
            characters=CharacterList(
                available=0,
                returned=0,
                collectionURI="http://gateway.marvel.com/v1/public/comics/21366/characters",
                items=[],
            ),
            stories=StoryList(
                available=0,
                returned=0,
                collectionURI="http://gateway.marvel.com/v1/public/comics/21366/stories",
                items=[],
            ),
            events=EventList(
                available=0,
                returned=0,
                collectionURI="http://gateway.marvel.com/v1/public/comics/21366/events",
                items=[],
            ),
        )

        assert len(comic.text_objects) == 1
        assert comic.text_objects[0].text == "The Avengers are born!"
        assert len(comic.urls) == 1
        assert comic.urls[0].type == "detail"
        assert len(comic.dates) == 2
        assert comic.dates[0].type == "onsaleDate"
        assert len(comic.prices) == 2
        assert comic.prices[0].type == "printPrice"
        assert comic.thumbnail is not None
        assert comic.thumbnail.extension == "jpg"
        assert len(comic.images) == 1
        assert comic.images[0].extension == "jpg"
        
        logger.info("✅ Comic with optional fields test completed successfully")


class TestComicResponse:
    """Test cases for ComicResponse class.

    This test class verifies the functionality of the ComicResponse class,
    which represents a Marvel API response containing a single comic.
    Tests cover creation, validation, and field handling.
    """

    def test_comic_response_creation(self):
        """Test ComicResponse can be created with required fields.

        This test verifies that ComicResponse properly validates and stores
        all Marvel API response metadata along with comic data. It ensures
        the standard single comic response structure is correctly modeled.

        Expected behavior:
            - All required fields are accepted and validated
            - Comic data is properly nested in the response
            - Model can be instantiated with valid data
        """
        logger.info("Testing ComicResponse can be created with required fields")
        
        comic = Comic(
            id=21366,
            digitalId=0,
            title="Avengers (1963) #1",
            issueNumber=1,
            variantDescription="",
            description="The Avengers are born!",
            modified="2014-04-29T14:18:17-0400",
            isbn="",
            upc="",
            diamondCode="",
            ean="",
            issn="",
            format="Comic",
            pageCount=32,
            textObjects=[],
            resourceURI="http://gateway.marvel.com/v1/public/comics/21366",
            urls=[],
            series=SeriesSummary(
                resourceURI="http://gateway.marvel.com/v1/public/series/1945",
                name="Avengers (1963 - 1996)",
            ),
            variants=[],
            collections=[],
            collectedIssues=[],
            dates=[],
            prices=[],
            thumbnail=None,
            images=[],
            creators=CreatorList(
                available=0,
                returned=0,
                collectionURI="http://gateway.marvel.com/v1/public/comics/21366/creators",
                items=[],
            ),
            characters=CharacterList(
                available=0,
                returned=0,
                collectionURI="http://gateway.marvel.com/v1/public/comics/21366/characters",
                items=[],
            ),
            stories=StoryList(
                available=0,
                returned=0,
                collectionURI="http://gateway.marvel.com/v1/public/comics/21366/stories",
                items=[],
            ),
            events=EventList(
                available=0,
                returned=0,
                collectionURI="http://gateway.marvel.com/v1/public/comics/21366/events",
                items=[],
            ),
        )

        response: ComicResponse = ComicResponse(
            code=200,
            status="Ok",
            copyright="© 2024 MARVEL",
            attributionText="Data provided by Marvel. © 2024 MARVEL",
            attributionHTML="<a href='http://marvel.com'>Data provided by Marvel. © 2024 MARVEL</a>",
            etag="etag123",
            data=comic,
        )

        assert response.code == 200
        assert response.status == "Ok"
        assert response.copyright == "© 2024 MARVEL"
        assert response.data.title == "Avengers (1963) #1"
        assert response.data.id == 21366
        
        logger.info("✅ ComicResponse creation test completed successfully")

    def test_comic_response_missing_required_fields(self):
        """Test ComicResponse raises ValidationError for missing required fields.

        This test verifies that ComicResponse properly validates all required
        fields and raises appropriate ValidationError when fields are
        missing. This ensures data integrity for comic response information.

        Expected behavior:
            - ValidationError is raised when required fields are missing
            - Error message indicates which fields are missing
            - Model creation fails gracefully with clear error information
        """
        logger.info("Testing ComicResponse raises ValidationError for missing required fields")
        
        with pytest.raises(ValidationError):
            ComicResponse(code=200, status="Ok")  # Missing other required fields
        
        logger.info("✅ ComicResponse missing required fields test completed successfully")


class TestComicListResponse:
    """Test cases for ComicListResponse class.

    This test class verifies the functionality of the ComicListResponse class,
    which represents a Marvel API response containing a list of comics.
    Tests cover creation, validation, and field handling.
    """

    def test_comic_list_response_creation(self):
        """Test ComicListResponse can be created with required fields.

        This test verifies that ComicListResponse properly validates and stores
        all Marvel API response metadata along with comic list data. It ensures
        the standard comic list response structure is correctly modeled.

        Expected behavior:
            - All required fields are accepted and validated
            - Comic list data is properly nested in the response
            - Model can be instantiated with valid data
        """
        logger.info("Testing ComicListResponse can be created with required fields")
        
        from marvelpy.models.base import DataContainer

        comic = Comic(
            id=21366,
            digitalId=0,
            title="Avengers (1963) #1",
            issueNumber=1,
            variantDescription="",
            description="The Avengers are born!",
            modified="2014-04-29T14:18:17-0400",
            isbn="",
            upc="",
            diamondCode="",
            ean="",
            issn="",
            format="Comic",
            pageCount=32,
            textObjects=[],
            resourceURI="http://gateway.marvel.com/v1/public/comics/21366",
            urls=[],
            series=SeriesSummary(
                resourceURI="http://gateway.marvel.com/v1/public/series/1945",
                name="Avengers (1963 - 1996)",
            ),
            variants=[],
            collections=[],
            collectedIssues=[],
            dates=[],
            prices=[],
            thumbnail=None,
            images=[],
            creators=CreatorList(
                available=0,
                returned=0,
                collectionURI="http://gateway.marvel.com/v1/public/comics/21366/creators",
                items=[],
            ),
            characters=CharacterList(
                available=0,
                returned=0,
                collectionURI="http://gateway.marvel.com/v1/public/comics/21366/characters",
                items=[],
            ),
            stories=StoryList(
                available=0,
                returned=0,
                collectionURI="http://gateway.marvel.com/v1/public/comics/21366/stories",
                items=[],
            ),
            events=EventList(
                available=0,
                returned=0,
                collectionURI="http://gateway.marvel.com/v1/public/comics/21366/events",
                items=[],
            ),
        )

        data_container: DataContainer[Comic] = DataContainer(
            offset=0,
            limit=20,
            total=100,
            count=1,
            results=[comic],
        )

        response: ComicListResponse = ComicListResponse(
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
        assert response.data.results[0].title == "Avengers (1963) #1"
        
        logger.info("✅ ComicListResponse creation test completed successfully")

    def test_comic_list_response_missing_required_fields(self):
        """Test ComicListResponse raises ValidationError for missing required fields.

        This test verifies that ComicListResponse properly validates all required
        fields and raises appropriate ValidationError when fields are
        missing. This ensures data integrity for comic list response information.

        Expected behavior:
            - ValidationError is raised when required fields are missing
            - Error message indicates which fields are missing
            - Model creation fails gracefully with clear error information
        """
        logger.info("Testing ComicListResponse raises ValidationError for missing required fields")
        
        with pytest.raises(ValidationError):
            ComicListResponse(code=200, status="Ok")  # Missing other required fields
        
        logger.info("✅ ComicListResponse missing required fields test completed successfully")
