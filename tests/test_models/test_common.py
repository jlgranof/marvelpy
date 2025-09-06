"""Tests for common model classes.

This module contains comprehensive tests for all common data models used
across Marvel API endpoints. These tests verify proper validation, field
handling, and data integrity for shared structures.
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
    Date,
    EventSummary,
    Image,
    Price,
    SeriesSummary,
    StorySummary,
    TextObject,
)


class TestImage:
    """Test cases for Image class.

    This test class verifies the functionality of the Image class,
    which represents image information for Marvel API resources.
    Tests cover creation, validation, and field handling.
    """

    def test_image_creation(self):
        """Test Image can be created with required fields.

        This test verifies that Image properly validates and stores
        image path and extension information. It ensures the Marvel
        API's standard image structure is correctly modeled.

        Expected behavior:
            - Both path and extension fields are required
            - Field values are stored and accessible as expected
            - Model can be instantiated with valid data
        """
        logger.info("Testing Image creation with required fields")
        image: Image = Image(
            path="http://i.annihil.us/u/prod/marvel/i/mg/9/c0/527bb7b37ff55", extension="jpg"
        )

        assert image.path == "http://i.annihil.us/u/prod/marvel/i/mg/9/c0/527bb7b37ff55"
        assert image.extension == "jpg"
        logger.info("✅ Image creation test completed successfully")

    def test_image_missing_required_fields(self):
        """Test Image raises ValidationError for missing required fields.

        This test verifies that Image properly validates all required
        fields and raises appropriate ValidationError when fields are
        missing. This ensures data integrity for image information.

        Expected behavior:
            - ValidationError is raised when required fields are missing
            - Error message indicates which fields are missing
            - Model creation fails gracefully with clear error information
        """
        logger.info("Testing image missing required fields validation")
        with pytest.raises(ValidationError):
            Image(path="http://example.com/image")  # Missing extension

        with pytest.raises(ValidationError):
            Image(extension="jpg")  # Missing path
        logger.info("✅ Image missing required fields test completed successfully")

    def test_image_full_url_construction(self):
        """Test Image can be used to construct full image URLs.

        This test verifies that Image fields can be combined to create
        full image URLs, which is a common use case for displaying
        images in applications.

        Expected behavior:
            - Path and extension can be combined to form full URL
            - Full URL construction works correctly
            - Image data is suitable for URL generation
        """
        logger.info("Testing image full URL construction")
        image: Image = Image(
            path="http://i.annihil.us/u/prod/marvel/i/mg/9/c0/527bb7b37ff55", extension="jpg"
        )

        full_url = f"{image.path}.{image.extension}"
        expected_url = "http://i.annihil.us/u/prod/marvel/i/mg/9/c0/527bb7b37ff55.jpg"

        assert full_url == expected_url
        logger.info("✅ Image full URL construction test completed successfully")


class TestURL:
    """Test cases for URL class.

    This test class verifies the functionality of the URL class,
    which represents external URLs associated with Marvel API resources.
    Tests cover creation, validation, and field handling.
    """

    def test_url_creation(self):
        """Test URL can be created with required fields.

        This test verifies that URL properly validates and stores
        URL type and value information. It ensures the Marvel API's
        standard URL structure is correctly modeled.

        Expected behavior:
            - Both type and url fields are required
            - Field values are stored and accessible as expected
            - Model can be instantiated with valid data
        """
        logger.info("Testing URL creation with required fields")
        url: URL = URL(
            type="detail", url="http://marvel.com/characters/9/iron_man?utm_campaign=apiRef"
        )

        assert url.type == "detail"
        assert url.url == "http://marvel.com/characters/9/iron_man?utm_campaign=apiRef"
        logger.info("✅ URL creation test completed successfully")

    def test_url_missing_required_fields(self):
        """Test URL raises ValidationError for missing required fields.

        This test verifies that URL properly validates all required
        fields and raises appropriate ValidationError when fields are
        missing. This ensures data integrity for URL information.

        Expected behavior:
            - ValidationError is raised when required fields are missing
            - Error message indicates which fields are missing
            - Model creation fails gracefully with clear error information
        """
        logger.info("Testing URL missing required fields validation")
        with pytest.raises(ValidationError):
            URL(type="detail")  # Missing url

        with pytest.raises(ValidationError):
            URL(url="http://example.com")  # Missing type
        logger.info("✅ URL missing required fields test completed successfully")

    def test_url_different_types(self):
        """Test URL handles different URL types correctly.

        This test verifies that URL can handle various URL types
        that appear in Marvel API responses, such as detail pages,
        wiki links, and purchase links.

        Expected behavior:
            - Different URL types are accepted and stored correctly
            - URL values are preserved regardless of type
            - Model handles various URL formats appropriately
        """
        logger.info("Testing URL different types handling")
        url_types = ["detail", "wiki", "comiclink", "purchase"]
        base_url = "http://marvel.com/test"

        for url_type in url_types:
            url: URL = URL(type=url_type, url=base_url)
            assert url.type == url_type
            assert url.url == base_url
        logger.info("✅ URL different types test completed successfully")


class TestTextObject:
    """Test cases for TextObject class.

    This test class verifies the functionality of the TextObject class,
    which represents text content associated with Marvel API resources.
    Tests cover creation, validation, and field handling.
    """

    def test_text_object_creation(self):
        """Test TextObject can be created with required fields.

        This test verifies that TextObject properly validates and stores
        text type, language, and content information. It ensures the
        Marvel API's standard text structure is correctly modeled.

        Expected behavior:
            - All required fields (type, language, text) are accepted
            - Field values are stored and accessible as expected
            - Model can be instantiated with valid data
        """
        logger.info("Testing text object creation with required fields")
        text_obj: TextObject = TextObject(
            type="description",
            language="en-us",
            text="Wounded, captured and forced to build a weapon by his enemies...",
        )

        assert text_obj.type == "description"
        assert text_obj.language == "en-us"
        assert text_obj.text == "Wounded, captured and forced to build a weapon by his enemies..."
        logger.info("✅ Text object creation test completed successfully")

    def test_text_object_missing_required_fields(self):
        """Test TextObject raises ValidationError for missing required fields.

        This test verifies that TextObject properly validates all required
        fields and raises appropriate ValidationError when fields are
        missing. This ensures data integrity for text information.

        Expected behavior:
            - ValidationError is raised when required fields are missing
            - Error message indicates which fields are missing
            - Model creation fails gracefully with clear error information
        """
        logger.info("Testing text object missing required fields validation")
        with pytest.raises(ValidationError):
            TextObject(type="description", language="en-us")  # Missing text

        with pytest.raises(ValidationError):
            TextObject(type="description", text="Some text")  # Missing language

        with pytest.raises(ValidationError):
            TextObject(language="en-us", text="Some text")  # Missing type
        logger.info("✅ Text object missing required fields test completed successfully")

    def test_text_object_different_languages(self):
        """Test TextObject handles different languages correctly.

        This test verifies that TextObject can handle various language
        codes that may appear in Marvel API responses, ensuring
        internationalization support.

        Expected behavior:
            - Different language codes are accepted and stored correctly
            - Text content is preserved regardless of language
            - Model handles various language formats appropriately
        """
        logger.info("Testing text object different languages handling")
        languages = ["en-us", "es", "fr", "de", "ja"]
        text_content = "Test description"

        for language in languages:
            text_obj: TextObject = TextObject(
                type="description", language=language, text=text_content
            )
            assert text_obj.language == language
            assert text_obj.text == text_content
        logger.info("✅ Text object different languages test completed successfully")


class TestDate:
    """Test cases for Date class.

    This test class verifies the functionality of the Date class,
    which represents date information associated with Marvel API resources.
    Tests cover creation, validation, and field handling.
    """

    def test_date_creation(self):
        """Test Date can be created with required fields.

        This test verifies that Date properly validates and stores
        date type and value information. It ensures the Marvel API's
        standard date structure is correctly modeled.

        Expected behavior:
            - Both type and date fields are required
            - Field values are stored and accessible as expected
            - Model can be instantiated with valid data
        """
        logger.info("Testing date creation with required fields")
        date_obj: Date = Date(type="onsaleDate", date="2014-04-29T00:00:00-0400")

        assert date_obj.type == "onsaleDate"
        assert date_obj.date == "2014-04-29T00:00:00-0400"
        logger.info("✅ Date creation test completed successfully")

    def test_date_missing_required_fields(self):
        """Test Date raises ValidationError for missing required fields.

        This test verifies that Date properly validates all required
        fields and raises appropriate ValidationError when fields are
        missing. This ensures data integrity for date information.

        Expected behavior:
            - ValidationError is raised when required fields are missing
            - Error message indicates which fields are missing
            - Model creation fails gracefully with clear error information
        """
        logger.info("Testing date missing required fields validation")
        with pytest.raises(ValidationError):
            Date(type="onsaleDate")  # Missing date

        with pytest.raises(ValidationError):
            Date(date="2014-04-29T00:00:00-0400")  # Missing type
        logger.info("✅ Date missing required fields test completed successfully")

    def test_date_different_types(self):
        """Test Date handles different date types correctly.

        This test verifies that Date can handle various date types
        that appear in Marvel API responses, such as on-sale dates,
        focus dates, and unlimited dates.

        Expected behavior:
            - Different date types are accepted and stored correctly
            - Date values are preserved regardless of type
            - Model handles various date formats appropriately
        """
        logger.info("Testing date different types handling")
        date_types = ["onsaleDate", "focDate", "unlimitedDate"]
        date_value = "2014-04-29T00:00:00-0400"

        for date_type in date_types:
            date_obj: Date = Date(type=date_type, date=date_value)
            assert date_obj.type == date_type
            assert date_obj.date == date_value
        logger.info("✅ Date different types test completed successfully")


class TestPrice:
    """Test cases for Price class.

    This test class verifies the functionality of the Price class,
    which represents pricing information for Marvel API resources.
    Tests cover creation, validation, and field handling.
    """

    def test_price_creation(self):
        """Test Price can be created with required fields.

        This test verifies that Price properly validates and stores
        price type and value information. It ensures the Marvel API's
        standard price structure is correctly modeled.

        Expected behavior:
            - Both type and price fields are required
            - Field values are stored and accessible as expected
            - Model can be instantiated with valid data
        """
        logger.info("Testing price creation with required fields")
        price_obj: Price = Price(type="printPrice", price=3.99)

        assert price_obj.type == "printPrice"
        assert price_obj.price == 3.99
        logger.info("✅ Price creation test completed successfully")

    def test_price_missing_required_fields(self):
        """Test Price raises ValidationError for missing required fields.

        This test verifies that Price properly validates all required
        fields and raises appropriate ValidationError when fields are
        missing. This ensures data integrity for price information.

        Expected behavior:
            - ValidationError is raised when required fields are missing
            - Error message indicates which fields are missing
            - Model creation fails gracefully with clear error information
        """
        logger.info("Testing price missing required fields validation")
        with pytest.raises(ValidationError):
            Price(type="printPrice")  # Missing price

        with pytest.raises(ValidationError):
            Price(price=3.99)  # Missing type
        logger.info("✅ Price missing required fields test completed successfully")

    def test_price_different_values(self):
        """Test Price handles different price values correctly.

        This test verifies that Price can handle various price values
        including zero prices and high values, ensuring proper
        numeric handling.

        Expected behavior:
            - Different price values are accepted and stored correctly
            - Price values are preserved as floats
            - Model handles various numeric formats appropriately
        """
        logger.info("Testing price different values handling")
        price_values = [0.0, 1.99, 3.99, 9.99, 99.99]

        for price_value in price_values:
            price_obj: Price = Price(type="printPrice", price=price_value)
            assert price_obj.price == price_value
            assert isinstance(price_obj.price, float)
        logger.info("✅ Price different values test completed successfully")


class TestSummaryModels:
    """Test cases for summary model classes.

    This test class verifies the functionality of all summary model
    classes (CreatorSummary, CharacterSummary, etc.), which represent
    lightweight versions of full Marvel API resources.
    Tests cover creation, validation, and field handling.
    """

    def test_creator_summary_creation(self):
        """Test CreatorSummary can be created with required fields.

        This test verifies that CreatorSummary properly validates and stores
        creator resource URI, name, and role information. It ensures the
        Marvel API's standard creator summary structure is correctly modeled.

        Expected behavior:
            - All required fields (resource_uri, name, role) are accepted
            - Field values are stored and accessible as expected
            - Model can be instantiated with valid data
        """
        logger.info("Testing creator summary creation with required fields")
        creator: CreatorSummary = CreatorSummary(
            resourceURI="http://gateway.marvel.com/v1/public/creators/30",
            name="Stan Lee",
            role="writer",
        )

        assert creator.resource_uri == "http://gateway.marvel.com/v1/public/creators/30"
        assert creator.name == "Stan Lee"
        assert creator.role == "writer"
        logger.info("✅ Creator summary creation test completed successfully")

    def test_character_summary_creation(self):
        """Test CharacterSummary can be created with required fields.

        This test verifies that CharacterSummary properly validates and stores
        character resource URI and name information. It ensures the
        Marvel API's standard character summary structure is correctly modeled.

        Expected behavior:
            - Both required fields (resource_uri, name) are accepted
            - Field values are stored and accessible as expected
            - Model can be instantiated with valid data
        """
        logger.info("Testing character summary creation with required fields")
        character: CharacterSummary = CharacterSummary(
            resourceURI="http://gateway.marvel.com/v1/public/characters/1009368", name="Iron Man"
        )

        assert character.resource_uri == "http://gateway.marvel.com/v1/public/characters/1009368"
        assert character.name == "Iron Man"
        logger.info("✅ Character summary creation test completed successfully")

    def test_story_summary_creation(self):
        """Test StorySummary can be created with required fields.

        This test verifies that StorySummary properly validates and stores
        story resource URI, name, and type information. It ensures the
        Marvel API's standard story summary structure is correctly modeled.

        Expected behavior:
            - All required fields (resource_uri, name, type) are accepted
            - Field values are stored and accessible as expected
            - Model can be instantiated with valid data
        """
        logger.info("Testing story summary creation with required fields")
        story: StorySummary = StorySummary(
            resourceURI="http://gateway.marvel.com/v1/public/stories/19947",
            name="Cover #19947",
            type="cover",
        )

        assert story.resource_uri == "http://gateway.marvel.com/v1/public/stories/19947"
        assert story.name == "Cover #19947"
        assert story.type == "cover"
        logger.info("✅ Story summary creation test completed successfully")

    def test_event_summary_creation(self):
        """Test EventSummary can be created with required fields.

        This test verifies that EventSummary properly validates and stores
        event resource URI and name information. It ensures the
        Marvel API's standard event summary structure is correctly modeled.

        Expected behavior:
            - Both required fields (resource_uri, name) are accepted
            - Field values are stored and accessible as expected
            - Model can be instantiated with valid data
        """
        logger.info("Testing event summary creation with required fields")
        event: EventSummary = EventSummary(
            resourceURI="http://gateway.marvel.com/v1/public/events/269", name="Secret Invasion"
        )

        assert event.resource_uri == "http://gateway.marvel.com/v1/public/events/269"
        assert event.name == "Secret Invasion"
        logger.info("✅ Event summary creation test completed successfully")

    def test_series_summary_creation(self):
        """Test SeriesSummary can be created with required fields.

        This test verifies that SeriesSummary properly validates and stores
        series resource URI and name information. It ensures the
        Marvel API's standard series summary structure is correctly modeled.

        Expected behavior:
            - Both required fields (resource_uri, name) are accepted
            - Field values are stored and accessible as expected
            - Model can be instantiated with valid data
        """
        logger.info("Testing series summary creation with required fields")
        series: SeriesSummary = SeriesSummary(
            resourceURI="http://gateway.marvel.com/v1/public/series/1945",
            name="Avengers (1998 - 2004)",
        )

        assert series.resource_uri == "http://gateway.marvel.com/v1/public/series/1945"
        assert series.name == "Avengers (1998 - 2004)"
        logger.info("✅ Series summary creation test completed successfully")

    def test_comic_summary_creation(self):
        """Test ComicSummary can be created with required fields.

        This test verifies that ComicSummary properly validates and stores
        comic resource URI and name information. It ensures the
        Marvel API's standard comic summary structure is correctly modeled.

        Expected behavior:
            - Both required fields (resource_uri, name) are accepted
            - Field values are stored and accessible as expected
            - Model can be instantiated with valid data
        """
        logger.info("Testing comic summary creation with required fields")
        comic: ComicSummary = ComicSummary(
            resourceURI="http://gateway.marvel.com/v1/public/comics/21366",
            name="Avengers (1963) #1",
        )

        assert comic.resource_uri == "http://gateway.marvel.com/v1/public/comics/21366"
        assert comic.name == "Avengers (1963) #1"
        logger.info("✅ Comic summary creation test completed successfully")

    def test_summary_models_missing_required_fields(self):
        """Test summary models raise ValidationError for missing required fields.

        This test verifies that all summary models properly validate
        required fields and raise appropriate ValidationError when
        fields are missing. This ensures data integrity for summary information.

        Expected behavior:
            - ValidationError is raised when required fields are missing
            - Error message indicates which fields are missing
            - Model creation fails gracefully with clear error information
        """
        logger.info("Testing summary models missing required fields validation")
        # Test CreatorSummary missing fields
        with pytest.raises(ValidationError):
            CreatorSummary(name="Stan Lee", role="writer")  # Missing resourceURI

        # Test CharacterSummary missing fields
        with pytest.raises(ValidationError):
            CharacterSummary(name="Iron Man")  # Missing resourceURI

        # Test StorySummary missing fields
        with pytest.raises(ValidationError):
            StorySummary(name="Cover #19947", type="cover")  # Missing resourceURI

        # Test EventSummary missing fields
        with pytest.raises(ValidationError):
            EventSummary(name="Secret Invasion")  # Missing resourceURI

        # Test SeriesSummary missing fields
        with pytest.raises(ValidationError):
            SeriesSummary(name="Avengers (1998 - 2004)")  # Missing resourceURI

        # Test ComicSummary missing fields
        with pytest.raises(ValidationError):
            ComicSummary(name="Avengers (1963) #1")  # Missing resourceURI
        logger.info("✅ Summary models missing required fields test completed successfully")
