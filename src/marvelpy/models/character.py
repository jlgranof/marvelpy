"""Character data models for Marvel API.

This module contains data models for Marvel characters, including the main
Character model and related list structures. Characters are one of the
primary entities in the Marvel API, representing superheroes, villains,
and other characters from the Marvel universe.
"""

from typing import List, Optional

from pydantic import Field

from .base import BaseListResponse, BaseModel, BaseResponse, DataContainer
from .common import (
    URL,
    ComicSummary,
    EventSummary,
    Image,
    SeriesSummary,
    StorySummary,
)


class ComicList(BaseModel):
    """Comic list for character.

    Represents a collection of comics featuring a specific character,
    including pagination metadata and a list of comic summaries.

    Attributes:
        available: Number of comics available for this character
        returned: Number of comics returned in this response
        collection_uri: URI of the comics collection for this character
        items: List of comic summaries featuring this character

    Example:
        >>> comic_list = ComicList(
        ...     available=100,
        ...     returned=20,
        ...     collectionURI="http://gateway.marvel.com/v1/public/characters/1009368/comics",
        ...     items=[ComicSummary(resourceURI="...", name="Avengers #1")]
        ... )
        >>> comic_list.available
        100
        >>> len(comic_list.items)
        1
    """

    available: int = Field(..., description="Number of comics available")
    returned: int = Field(..., description="Number of comics returned")
    collection_uri: str = Field(
        ..., alias="collectionURI", description="URI of the comics collection"
    )
    items: List[ComicSummary] = Field(default_factory=list, description="List of comic summaries")


class StoryList(BaseModel):
    """Story list for character.

    Represents a collection of stories featuring a specific character,
    including pagination metadata and a list of story summaries.

    Attributes:
        available: Number of stories available for this character
        returned: Number of stories returned in this response
        collection_uri: URI of the stories collection for this character
        items: List of story summaries featuring this character

    Example:
        >>> story_list = StoryList(
        ...     available=50,
        ...     returned=10,
        ...     collectionURI="http://gateway.marvel.com/v1/public/characters/1009368/stories",
        ...     items=[StorySummary(resourceURI="...", name="Cover #1", type="cover")]
        ... )
        >>> story_list.available
        50
        >>> len(story_list.items)
        1
    """

    available: int = Field(..., description="Number of stories available")
    returned: int = Field(..., description="Number of stories returned")
    collection_uri: str = Field(
        ..., alias="collectionURI", description="URI of the stories collection"
    )
    items: List[StorySummary] = Field(default_factory=list, description="List of story summaries")


class EventList(BaseModel):
    """Event list for character.

    Represents a collection of events featuring a specific character,
    including pagination metadata and a list of event summaries.

    Attributes:
        available: Number of events available for this character
        returned: Number of events returned in this response
        collection_uri: URI of the events collection for this character
        items: List of event summaries featuring this character

    Example:
        >>> event_list = EventList(
        ...     available=25,
        ...     returned=5,
        ...     collectionURI="http://gateway.marvel.com/v1/public/characters/1009368/events",
        ...     items=[EventSummary(resourceURI="...", name="Secret Invasion")]
        ... )
        >>> event_list.available
        25
        >>> len(event_list.items)
        1
    """

    available: int = Field(..., description="Number of events available")
    returned: int = Field(..., description="Number of events returned")
    collection_uri: str = Field(
        ..., alias="collectionURI", description="URI of the events collection"
    )
    items: List[EventSummary] = Field(default_factory=list, description="List of event summaries")


class SeriesList(BaseModel):
    """Series list for character.

    Represents a collection of series featuring a specific character,
    including pagination metadata and a list of series summaries.

    Attributes:
        available: Number of series available for this character
        returned: Number of series returned in this response
        collection_uri: URI of the series collection for this character
        items: List of series summaries featuring this character

    Example:
        >>> series_list = SeriesList(
        ...     available=75,
        ...     returned=15,
        ...     collectionURI="http://gateway.marvel.com/v1/public/characters/1009368/series",
        ...     items=[SeriesSummary(resourceURI="...", name="Avengers (1998 - 2004)")]
        ... )
        >>> series_list.available
        75
        >>> len(series_list.items)
        1
    """

    available: int = Field(..., description="Number of series available")
    returned: int = Field(..., description="Number of series returned")
    collection_uri: str = Field(
        ..., alias="collectionURI", description="URI of the series collection"
    )
    items: List[SeriesSummary] = Field(default_factory=list, description="List of series summaries")


class Character(BaseModel):
    """Character data model for Marvel API.

    Represents a Marvel character with all associated information including
    basic details, description, images, and related resources. Characters
    are central entities in the Marvel universe and appear across comics,
    events, series, and stories.

    Attributes:
        id: Unique identifier for the character
        name: Name of the character
        description: Description of the character (may be empty)
        modified: Date the character was last modified (ISO format)
        resource_uri: URI of the character resource
        urls: List of URLs associated with the character
        thumbnail: Character thumbnail image (may be None)
        comics: Comics featuring this character
        stories: Stories featuring this character
        events: Events featuring this character
        series: Series featuring this character

    Example:
        >>> character = Character(
        ...     id=1009368,
        ...     name="Iron Man",
        ...     description="Wounded, captured and forced to build a weapon by his enemies...",
        ...     modified="2014-04-29T14:18:17-0400",
        ...     resourceURI="http://gateway.marvel.com/v1/public/characters/1009368",
        ...     urls=[URL(type="detail", url="http://marvel.com/characters/9/iron_man")],
        ...     thumbnail=Image(path="http://i.annihil.us/u/prod/marvel/i/mg/9/c0/527bb7b37ff55", extension="jpg"),
        ...     comics=ComicList(available=100, returned=20, collectionURI="...", items=[]),
        ...     stories=StoryList(available=50, returned=10, collectionURI="...", items=[]),
        ...     events=EventList(available=25, returned=5, collectionURI="...", items=[]),
        ...     series=SeriesList(available=75, returned=15, collectionURI="...", items=[])
        ... )
        >>> character.name
        'Iron Man'
        >>> character.id
        1009368
    """

    id: int = Field(..., description="Unique identifier for the character")
    name: str = Field(..., description="Name of the character")
    description: str = Field(..., description="Description of the character")
    modified: str = Field(..., description="Date the character was last modified")
    resource_uri: str = Field(..., alias="resourceURI", description="URI of the character resource")
    urls: List[URL] = Field(
        default_factory=list, description="List of URLs associated with the character"
    )
    thumbnail: Optional[Image] = Field(None, description="Character thumbnail image")
    comics: ComicList = Field(..., description="Comics featuring this character")
    stories: StoryList = Field(..., description="Stories featuring this character")
    events: EventList = Field(..., description="Events featuring this character")
    series: SeriesList = Field(..., description="Series featuring this character")


class CharacterListResponse(BaseListResponse[Character]):
    """Character list response.

    Represents a Marvel API response containing a list of characters
    with pagination metadata. This is the standard response format
    for character list endpoints.

    Attributes:
        code: HTTP status code
        status: Status message
        copyright: Copyright notice
        attribution_text: Text attribution
        attribution_html: HTML attribution
        etag: ETag for caching
        data: DataContainer with character list and pagination info

    Example:
        >>> response = CharacterListResponse(
        ...     code=200,
        ...     status="Ok",
        ...     copyright="© 2024 MARVEL",
        ...     attributionText="Data provided by Marvel. © 2024 MARVEL",
        ...     attributionHTML="<a href='http://marvel.com'>Data provided by Marvel. © 2024 MARVEL</a>",
        ...     etag="etag123",
        ...     data=DataContainer(
        ...         offset=0,
        ...         limit=20,
        ...         total=100,
        ...         count=20,
        ...         results=[Character(id=1009368, name="Iron Man", ...)]
        ...     )
        ... )
        >>> response.data.results[0].name
        'Iron Man'
    """

    data: DataContainer[Character] = Field(..., description="Character data container")


class CharacterResponse(BaseResponse[Character]):
    """Single character response.

    Represents a Marvel API response containing a single character
    with full details. This is the standard response format for
    individual character endpoints.

    Attributes:
        code: HTTP status code
        status: Status message
        copyright: Copyright notice
        attribution_text: Text attribution
        attribution_html: HTML attribution
        etag: ETag for caching
        data: Character data

    Example:
        >>> response = CharacterResponse(
        ...     code=200,
        ...     status="Ok",
        ...     copyright="© 2024 MARVEL",
        ...     attributionText="Data provided by Marvel. © 2024 MARVEL",
        ...     attributionHTML="<a href='http://marvel.com'>Data provided by Marvel. © 2024 MARVEL</a>",
        ...     etag="etag123",
        ...     data=Character(id=1009368, name="Iron Man", ...)
        ... )
        >>> response.data.name
        'Iron Man'
    """

    data: Character = Field(..., description="Character data")
