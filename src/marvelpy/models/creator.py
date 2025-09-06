"""Creator data models for Marvel API.

This module contains data models for Marvel creators, including the main
Creator model and related list structures. Creators are the people who
work on Marvel comics, including writers, artists, editors, and other
contributors to the creative process.
"""

from typing import List, Optional

from pydantic import Field

from .base import BaseListResponse, BaseModel, BaseResponse, DataContainer
from .common import (
    URL,
    CharacterSummary,
    ComicSummary,
    EventSummary,
    Image,
    SeriesSummary,
    StorySummary,
)


class CharacterList(BaseModel):
    """Character list for creator.

    Represents a collection of characters that a specific creator has worked on,
    including pagination metadata and a list of character summaries.

    Attributes:
        available: Number of characters available for this creator
        returned: Number of characters returned in this response
        collection_uri: URI of the characters collection for this creator
        items: List of character summaries that this creator has worked on

    Example:
        >>> character_list = CharacterList(
        ...     available=50,
        ...     returned=20,
        ...     collectionURI="http://gateway.marvel.com/v1/public/creators/30/characters",
        ...     items=[CharacterSummary(resourceURI="...", name="Iron Man")]
        ... )
        >>> character_list.available
        50
        >>> len(character_list.items)
        1
    """

    available: int = Field(..., description="Number of characters available")
    returned: int = Field(..., description="Number of characters returned")
    collection_uri: str = Field(
        ..., alias="collectionURI", description="URI of the characters collection"
    )
    items: List[CharacterSummary] = Field(
        default_factory=list, description="List of character summaries"
    )


class ComicList(BaseModel):
    """Comic list for creator.

    Represents a collection of comics that a specific creator has worked on,
    including pagination metadata and a list of comic summaries.

    Attributes:
        available: Number of comics available for this creator
        returned: Number of comics returned in this response
        collection_uri: URI of the comics collection for this creator
        items: List of comic summaries that this creator has worked on

    Example:
        >>> comic_list = ComicList(
        ...     available=500,
        ...     returned=100,
        ...     collectionURI="http://gateway.marvel.com/v1/public/creators/30/comics",
        ...     items=[ComicSummary(resourceURI="...", name="Amazing Spider-Man #1")]
        ... )
        >>> comic_list.available
        500
        >>> len(comic_list.items)
        1
    """

    available: int = Field(..., description="Number of comics available")
    returned: int = Field(..., description="Number of comics returned")
    collection_uri: str = Field(
        ..., alias="collectionURI", description="URI of the comics collection"
    )
    items: List[ComicSummary] = Field(default_factory=list, description="List of comic summaries")


class EventList(BaseModel):
    """Event list for creator.

    Represents a collection of events that a specific creator has worked on,
    including pagination metadata and a list of event summaries.

    Attributes:
        available: Number of events available for this creator
        returned: Number of events returned in this response
        collection_uri: URI of the events collection for this creator
        items: List of event summaries that this creator has worked on

    Example:
        >>> event_list = EventList(
        ...     available=10,
        ...     returned=5,
        ...     collectionURI="http://gateway.marvel.com/v1/public/creators/30/events",
        ...     items=[EventSummary(resourceURI="...", name="Secret Invasion")]
        ... )
        >>> event_list.available
        10
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
    """Series list for creator.

    Represents a collection of series that a specific creator has worked on,
    including pagination metadata and a list of series summaries.

    Attributes:
        available: Number of series available for this creator
        returned: Number of series returned in this response
        collection_uri: URI of the series collection for this creator
        items: List of series summaries that this creator has worked on

    Example:
        >>> series_list = SeriesList(
        ...     available=25,
        ...     returned=10,
        ...     collectionURI="http://gateway.marvel.com/v1/public/creators/30/series",
        ...     items=[SeriesSummary(resourceURI="...", name="Amazing Spider-Man (1963 - 1998)")]
        ... )
        >>> series_list.available
        25
        >>> len(series_list.items)
        1
    """

    available: int = Field(..., description="Number of series available")
    returned: int = Field(..., description="Number of series returned")
    collection_uri: str = Field(
        ..., alias="collectionURI", description="URI of the series collection"
    )
    items: List[SeriesSummary] = Field(default_factory=list, description="List of series summaries")


class StoryList(BaseModel):
    """Story list for creator.

    Represents a collection of stories that a specific creator has worked on,
    including pagination metadata and a list of story summaries.

    Attributes:
        available: Number of stories available for this creator
        returned: Number of stories returned in this response
        collection_uri: URI of the stories collection for this creator
        items: List of story summaries that this creator has worked on

    Example:
        >>> story_list = StoryList(
        ...     available=1000,
        ...     returned=200,
        ...     collectionURI="http://gateway.marvel.com/v1/public/creators/30/stories",
        ...     items=[StorySummary(resourceURI="...", name="Cover #1", type="cover")]
        ... )
        >>> story_list.available
        1000
        >>> len(story_list.items)
        1
    """

    available: int = Field(..., description="Number of stories available")
    returned: int = Field(..., description="Number of stories returned")
    collection_uri: str = Field(
        ..., alias="collectionURI", description="URI of the stories collection"
    )
    items: List[StorySummary] = Field(default_factory=list, description="List of story summaries")


class Creator(BaseModel):
    """Creator data model for Marvel API.

    Represents a Marvel creator with all associated information including
    basic details, description, and related resources. Creators are the
    people who work on Marvel comics, including writers, artists, editors,
    and other contributors to the creative process.

    Attributes:
        id: Unique identifier for the creator
        first_name: First name of the creator
        middle_name: Middle name of the creator (may be empty)
        last_name: Last name of the creator
        suffix: Suffix of the creator (may be empty)
        full_name: Full name of the creator
        modified: Date the creator was last modified (ISO format)
        resource_uri: URI of the creator resource
        urls: List of URLs associated with the creator
        thumbnail: Creator thumbnail image (may be None)
        comics: Comics that this creator has worked on
        series: Series that this creator has worked on
        stories: Stories that this creator has worked on
        events: Events that this creator has worked on
        characters: Characters that this creator has worked on

    Example:
        >>> creator = Creator(
        ...     id=30,
        ...     firstName="Stan",
        ...     middleName="",
        ...     lastName="Lee",
        ...     suffix="",
        ...     fullName="Stan Lee",
        ...     modified="2013-11-20T17:40:18-0500",
        ...     resourceURI="http://gateway.marvel.com/v1/public/creators/30",
        ...     urls=[],
        ...     thumbnail=Image(path="http://i.annihil.us/u/prod/marvel/i/mg/9/c0/527bb7b37ff55", extension="jpg"),
        ...     comics=ComicList(available=500, returned=100, collectionURI="...", items=[]),
        ...     series=SeriesList(available=25, returned=10, collectionURI="...", items=[]),
        ...     stories=StoryList(available=1000, returned=200, collectionURI="...", items=[]),
        ...     events=EventList(available=10, returned=5, collectionURI="...", items=[]),
        ...     characters=CharacterList(available=50, returned=20, collectionURI="...", items=[])
        ... )
        >>> creator.full_name
        'Stan Lee'
        >>> creator.id
        30
    """

    id: int = Field(..., description="Unique identifier for the creator")
    first_name: str = Field(..., alias="firstName", description="First name of the creator")
    middle_name: str = Field(..., alias="middleName", description="Middle name of the creator")
    last_name: str = Field(..., alias="lastName", description="Last name of the creator")
    suffix: str = Field(..., description="Suffix of the creator")
    full_name: str = Field(..., alias="fullName", description="Full name of the creator")
    modified: str = Field(..., description="Date the creator was last modified")
    resource_uri: str = Field(..., alias="resourceURI", description="URI of the creator resource")
    urls: List["URL"] = Field(
        default_factory=list, description="List of URLs associated with the creator"
    )
    thumbnail: Optional[Image] = Field(None, description="Creator thumbnail image")
    comics: ComicList = Field(..., description="Comics that this creator has worked on")
    series: SeriesList = Field(..., description="Series that this creator has worked on")
    stories: StoryList = Field(..., description="Stories that this creator has worked on")
    events: EventList = Field(..., description="Events that this creator has worked on")
    characters: Optional[CharacterList] = Field(None, description="Characters that this creator has worked on")


class CreatorListResponse(BaseListResponse[Creator]):
    """Creator list response.

    Represents a Marvel API response containing a list of creators
    with pagination metadata. This is the standard response format
    for creator list endpoints.

    Attributes:
        code: HTTP status code
        status: Status message
        copyright: Copyright notice
        attribution_text: Text attribution
        attribution_html: HTML attribution
        etag: ETag for caching
        data: DataContainer with creator list and pagination info

    Example:
        >>> response = CreatorListResponse(
        ...     code=200,
        ...     status="Ok",
        ...     copyright="© 2024 MARVEL",
        ...     attributionText="Data provided by Marvel. © 2024 MARVEL",
        ...     attributionHTML="<a href='http://marvel.com'>Data provided by Marvel. © 2024 MARVEL</a>",
        ...     etag="etag123",
        ...     data=DataContainer(
        ...         offset=0,
        ...         limit=20,
        ...         total=200,
        ...         count=20,
        ...         results=[Creator(id=30, fullName="Stan Lee", ...)]
        ...     )
        ... )
        >>> response.data.results[0].full_name
        'Stan Lee'
    """

    data: DataContainer[Creator] = Field(..., description="Creator data container")


class CreatorResponse(BaseResponse[Creator]):
    """Single creator response.

    Represents a Marvel API response containing a single creator
    with full details. This is the standard response format for
    individual creator endpoints.

    Attributes:
        code: HTTP status code
        status: Status message
        copyright: Copyright notice
        attribution_text: Text attribution
        attribution_html: HTML attribution
        etag: ETag for caching
        data: Creator data

    Example:
        >>> response = CreatorResponse(
        ...     code=200,
        ...     status="Ok",
        ...     copyright="© 2024 MARVEL",
        ...     attributionText="Data provided by Marvel. © 2024 MARVEL",
        ...     attributionHTML="<a href='http://marvel.com'>Data provided by Marvel. © 2024 MARVEL</a>",
        ...     etag="etag123",
        ...     data=Creator(id=30, fullName="Stan Lee", ...)
        ... )
        >>> response.data.full_name
        'Stan Lee'
    """

    data: Creator = Field(..., description="Creator data")
