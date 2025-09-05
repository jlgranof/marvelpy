"""Common data models used across Marvel API endpoints.

This module contains shared data models that are used across multiple
Marvel API entities. These models represent common structures like
images, URLs, dates, prices, and summary objects that appear in
various API responses.
"""

from pydantic import Field

from .base import BaseModel


class Image(BaseModel):
    """Image data model for Marvel API resources.

    Represents image information for characters, comics, events, and other
    Marvel API resources. Images are typically stored on Marvel's CDN and
    include both the base path and file extension.

    Attributes:
        path: Base path to the image on Marvel's CDN (without extension)
        extension: File extension for the image (e.g., 'jpg', 'png', 'gif')

    Example:
        >>> image = Image(
        ...     path="http://i.annihil.us/u/prod/marvel/i/mg/9/c0/527bb7b37ff55",
        ...     extension="jpg"
        ... )
        >>> image.path
        'http://i.annihil.us/u/prod/marvel/i/mg/9/c0/527bb7b37ff55'
        >>> image.extension
        'jpg'
        >>> # Full URL can be constructed as: f"{image.path}.{image.extension}"
    """

    path: str = Field(..., description="Base path to the image on Marvel's CDN")
    extension: str = Field(
        ..., description="File extension for the image (e.g., 'jpg', 'png', 'gif')"
    )


class URL(BaseModel):
    """URL data model for Marvel API resources.

    Represents external URLs associated with Marvel API resources, such as
    official websites, Wikipedia pages, or other related links. Each URL
    has a type that describes its purpose.

    Attributes:
        type: Type of URL (e.g., 'detail', 'wiki', 'comiclink', 'purchase')
        url: The actual URL value

    Example:
        >>> url = URL(
        ...     type="detail",
        ...     url="http://marvel.com/characters/9/iron_man?utm_campaign=apiRef&utm_source=..."
        ... )
        >>> url.type
        'detail'
        >>> url.url
        'http://marvel.com/characters/9/iron_man?utm_campaign=apiRef&utm_source=...'
    """

    type: str = Field(
        ..., description="Type of URL (e.g., 'detail', 'wiki', 'comiclink', 'purchase')"
    )
    url: str = Field(..., description="The actual URL value")


class TextObject(BaseModel):
    """Text object data model for Marvel API resources.

    Represents text content associated with Marvel API resources, such as
    descriptions, summaries, or other textual information. Text objects
    can be in different languages and have different types.

    Attributes:
        type: Type of text object (e.g., 'description', 'summary', 'full')
        language: Language code for the text (e.g., 'en-us', 'es')
        text: The actual text content

    Example:
        >>> text_obj = TextObject(
        ...     type="description",
        ...     language="en-us",
        ...     text="Wounded, captured and forced to build a weapon by his enemies..."
        ... )
        >>> text_obj.type
        'description'
        >>> text_obj.language
        'en-us'
    """

    type: str = Field(
        ..., description="Type of text object (e.g., 'description', 'summary', 'full')"
    )
    language: str = Field(..., description="Language code for the text (e.g., 'en-us', 'es')")
    text: str = Field(..., description="The actual text content")


class Date(BaseModel):
    """Date data model for Marvel API resources.

    Represents date information associated with Marvel API resources, such as
    publication dates, on-sale dates, or other temporal information. Dates
    are typically in ISO format and have a type that describes their purpose.

    Attributes:
        type: Type of date (e.g., 'onsaleDate', 'focDate', 'unlimitedDate')
        date: Date value in ISO format (e.g., '2014-04-29T00:00:00-0400')

    Example:
        >>> date_obj = Date(
        ...     type="onsaleDate",
        ...     date="2014-04-29T00:00:00-0400"
        ... )
        >>> date_obj.type
        'onsaleDate'
        >>> date_obj.date
        '2014-04-29T00:00:00-0400'
    """

    type: str = Field(
        ..., description="Type of date (e.g., 'onsaleDate', 'focDate', 'unlimitedDate')"
    )
    date: str = Field(
        ..., description="Date value in ISO format (e.g., '2014-04-29T00:00:00-0400')"
    )


class Price(BaseModel):
    """Price data model for Marvel API resources.

    Represents pricing information for Marvel API resources, typically
    used for comics and other purchasable items. Prices can have different
    types and are usually in USD.

    Attributes:
        type: Type of price (e.g., 'printPrice', 'digitalPrice')
        price: Price value as a float (typically in USD)

    Example:
        >>> price_obj = Price(
        ...     type="printPrice",
        ...     price=3.99
        ... )
        >>> price_obj.type
        'printPrice'
        >>> price_obj.price
        3.99
    """

    type: str = Field(..., description="Type of price (e.g., 'printPrice', 'digitalPrice')")
    price: float = Field(..., description="Price value as a float (typically in USD)")


class CreatorSummary(BaseModel):
    """Creator summary data model for Marvel API resources.

    Represents a summary of creator information (writers, artists, etc.)
    that appears in Marvel API responses. This is a lightweight version
    of the full creator data used in lists and references.

    Attributes:
        resource_uri: URI of the creator resource for fetching full details
        name: Name of the creator
        role: Role of the creator (e.g., 'writer', 'artist', 'penciller')

    Example:
        >>> creator = CreatorSummary(
        ...     resourceURI="http://gateway.marvel.com/v1/public/creators/30",
        ...     name="Stan Lee",
        ...     role="writer"
        ... )
        >>> creator.name
        'Stan Lee'
        >>> creator.role
        'writer'
    """

    resource_uri: str = Field(..., alias="resourceURI", description="URI of the creator resource")
    name: str = Field(..., description="Name of the creator")
    role: str = Field(
        ..., description="Role of the creator (e.g., 'writer', 'artist', 'penciller')"
    )


class CharacterSummary(BaseModel):
    """Character summary data model for Marvel API resources.

    Represents a summary of character information that appears in Marvel API
    responses. This is a lightweight version of the full character data
    used in lists and references.

    Attributes:
        resource_uri: URI of the character resource for fetching full details
        name: Name of the character

    Example:
        >>> character = CharacterSummary(
        ...     resourceURI="http://gateway.marvel.com/v1/public/characters/1009368",
        ...     name="Iron Man"
        ... )
        >>> character.name
        'Iron Man'
    """

    resource_uri: str = Field(..., alias="resourceURI", description="URI of the character resource")
    name: str = Field(..., description="Name of the character")


class StorySummary(BaseModel):
    """Story summary data model for Marvel API resources.

    Represents a summary of story information that appears in Marvel API
    responses. This is a lightweight version of the full story data
    used in lists and references.

    Attributes:
        resource_uri: URI of the story resource for fetching full details
        name: Name of the story
        type: Type of the story (e.g., 'cover', 'interiorStory', 'promo')

    Example:
        >>> story = StorySummary(
        ...     resourceURI="http://gateway.marvel.com/v1/public/stories/19947",
        ...     name="Cover #19947",
        ...     type="cover"
        ... )
        >>> story.name
        'Cover #19947'
        >>> story.type
        'cover'
    """

    resource_uri: str = Field(..., alias="resourceURI", description="URI of the story resource")
    name: str = Field(..., description="Name of the story")
    type: str = Field(
        ..., description="Type of the story (e.g., 'cover', 'interiorStory', 'promo')"
    )


class EventSummary(BaseModel):
    """Event summary data model for Marvel API resources.

    Represents a summary of event information that appears in Marvel API
    responses. This is a lightweight version of the full event data
    used in lists and references.

    Attributes:
        resource_uri: URI of the event resource for fetching full details
        name: Name of the event

    Example:
        >>> event = EventSummary(
        ...     resourceURI="http://gateway.marvel.com/v1/public/events/269",
        ...     name="Secret Invasion"
        ... )
        >>> event.name
        'Secret Invasion'
    """

    resource_uri: str = Field(..., alias="resourceURI", description="URI of the event resource")
    name: str = Field(..., description="Name of the event")


class SeriesSummary(BaseModel):
    """Series summary data model for Marvel API resources.

    Represents a summary of series information that appears in Marvel API
    responses. This is a lightweight version of the full series data
    used in lists and references.

    Attributes:
        resource_uri: URI of the series resource for fetching full details
        name: Name of the series

    Example:
        >>> series = SeriesSummary(
        ...     resourceURI="http://gateway.marvel.com/v1/public/series/1945",
        ...     name="Avengers (1998 - 2004)"
        ... )
        >>> series.name
        'Avengers (1998 - 2004)'
    """

    resource_uri: str = Field(..., alias="resourceURI", description="URI of the series resource")
    name: str = Field(..., description="Name of the series")


class ComicSummary(BaseModel):
    """Comic summary data model for Marvel API resources.

    Represents a summary of comic information that appears in Marvel API
    responses. This is a lightweight version of the full comic data
    used in lists and references.

    Attributes:
        resource_uri: URI of the comic resource for fetching full details
        name: Name of the comic

    Example:
        >>> comic = ComicSummary(
        ...     resourceURI="http://gateway.marvel.com/v1/public/comics/21366",
        ...     name="Avengers (1963) #1"
        ... )
        >>> comic.name
        'Avengers (1963) #1'
    """

    resource_uri: str = Field(..., alias="resourceURI", description="URI of the comic resource")
    name: str = Field(..., description="Name of the comic")
