"""Series data models for Marvel API.

This module contains data models for Marvel series, including the main
Series model and related list structures. Series are collections of
comics that share a common title and are typically published over time,
representing ongoing storylines or character arcs.
"""

from typing import List, Optional

from pydantic import Field

from .base import BaseListResponse, BaseModel, BaseResponse, DataContainer
from .common import (
    URL,
    CharacterSummary,
    ComicSummary,
    CreatorSummary,
    EventSummary,
    Image,
    SeriesSummary,
    StorySummary,
)


class CharacterList(BaseModel):
    """Character list for series.

    Represents a collection of characters that appear in a specific series,
    including pagination metadata and a list of character summaries.

    Attributes:
        available: Number of characters available for this series
        returned: Number of characters returned in this response
        collection_uri: URI of the characters collection for this series
        items: List of character summaries that appear in this series

    Example:
        >>> character_list = CharacterList(
        ...     available=25,
        ...     returned=10,
        ...     collectionURI="http://gateway.marvel.com/v1/public/series/1991/characters",
        ...     items=[CharacterSummary(resourceURI="...", name="Iron Man")]
        ... )
        >>> character_list.available
        25
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
    """Comic list for series.

    Represents a collection of comics that are part of a specific series,
    including pagination metadata and a list of comic summaries.

    Attributes:
        available: Number of comics available for this series
        returned: Number of comics returned in this response
        collection_uri: URI of the comics collection for this series
        items: List of comic summaries that are part of this series

    Example:
        >>> comic_list = ComicList(
        ...     available=200,
        ...     returned=50,
        ...     collectionURI="http://gateway.marvel.com/v1/public/series/1991/comics",
        ...     items=[ComicSummary(resourceURI="...", name="Avengers (1998) #1")]
        ... )
        >>> comic_list.available
        200
        >>> len(comic_list.items)
        1
    """

    available: int = Field(..., description="Number of comics available")
    returned: int = Field(..., description="Number of comics returned")
    collection_uri: str = Field(
        ..., alias="collectionURI", description="URI of the comics collection"
    )
    items: List[ComicSummary] = Field(default_factory=list, description="List of comic summaries")


class CreatorList(BaseModel):
    """Creator list for series.

    Represents a collection of creators who worked on comics in a specific
    series, including pagination metadata and a list of creator summaries.

    Attributes:
        available: Number of creators available for this series
        returned: Number of creators returned in this response
        collection_uri: URI of the creators collection for this series
        items: List of creator summaries who worked on this series

    Example:
        >>> creator_list = CreatorList(
        ...     available=15,
        ...     returned=8,
        ...     collectionURI="http://gateway.marvel.com/v1/public/series/1991/creators",
        ...     items=[CreatorSummary(resourceURI="...", name="Kurt Busiek", role="writer")]
        ... )
        >>> creator_list.available
        15
        >>> len(creator_list.items)
        1
    """

    available: int = Field(..., description="Number of creators available")
    returned: int = Field(..., description="Number of creators returned")
    collection_uri: str = Field(
        ..., alias="collectionURI", description="URI of the creators collection"
    )
    items: List[CreatorSummary] = Field(
        default_factory=list, description="List of creator summaries"
    )


class EventList(BaseModel):
    """Event list for series.

    Represents a collection of events that are related to a specific series,
    including pagination metadata and a list of event summaries.

    Attributes:
        available: Number of events available for this series
        returned: Number of events returned in this response
        collection_uri: URI of the events collection for this series
        items: List of event summaries related to this series

    Example:
        >>> event_list = EventList(
        ...     available=5,
        ...     returned=3,
        ...     collectionURI="http://gateway.marvel.com/v1/public/series/1991/events",
        ...     items=[EventSummary(resourceURI="...", name="Secret Invasion")]
        ... )
        >>> event_list.available
        5
        >>> len(event_list.items)
        1
    """

    available: int = Field(..., description="Number of events available")
    returned: int = Field(..., description="Number of events returned")
    collection_uri: str = Field(
        ..., alias="collectionURI", description="URI of the events collection"
    )
    items: List[EventSummary] = Field(default_factory=list, description="List of event summaries")


class StoryList(BaseModel):
    """Story list for series.

    Represents a collection of stories that are part of a specific series,
    including pagination metadata and a list of story summaries.

    Attributes:
        available: Number of stories available for this series
        returned: Number of stories returned in this response
        collection_uri: URI of the stories collection for this series
        items: List of story summaries that are part of this series

    Example:
        >>> story_list = StoryList(
        ...     available=300,
        ...     returned=75,
        ...     collectionURI="http://gateway.marvel.com/v1/public/series/1991/stories",
        ...     items=[StorySummary(resourceURI="...", name="Cover #1", type="cover")]
        ... )
        >>> story_list.available
        300
        >>> len(story_list.items)
        1
    """

    available: int = Field(..., description="Number of stories available")
    returned: int = Field(..., description="Number of stories returned")
    collection_uri: str = Field(
        ..., alias="collectionURI", description="URI of the stories collection"
    )
    items: List[StorySummary] = Field(default_factory=list, description="List of story summaries")


class Series(BaseModel):
    """Series data model for Marvel API.

    Represents a Marvel series with all associated information including
    basic details, description, publication dates, and related resources.
    Series are collections of comics that share a common title and are
    typically published over time.

    Attributes:
        id: Unique identifier for the series
        title: Title of the series
        description: Description of the series (may be empty)
        resource_uri: URI of the series resource
        urls: List of URLs associated with the series
        start_year: Year the series started
        end_year: Year the series ended (may be None for ongoing series)
        rating: Rating of the series (may be empty)
        modified: Date the series was last modified (ISO format)
        thumbnail: Series thumbnail image (may be None)
        comics: Comics that are part of this series
        stories: Stories that are part of this series
        events: Events related to this series
        characters: Characters that appear in this series
        creators: Creators who worked on this series
        next: Next series in chronological order (may be None)
        previous: Previous series in chronological order (may be None)

    Example:
        >>> series = Series(
        ...     id=1991,
        ...     title="Avengers (1998 - 2004)",
        ...     description="The Avengers reunite to face new threats...",
        ...     resourceURI="http://gateway.marvel.com/v1/public/series/1991",
        ...     urls=[URL(type="detail", url="http://marvel.com/comics/series/1991/avengers_1998_-_2004")],
        ...     start_year=1998,
        ...     end_year=2004,
        ...     rating="",
        ...     modified="2013-11-20T17:40:18-0500",
        ...     thumbnail=Image(path="http://i.annihil.us/u/prod/marvel/i/mg/9/c0/527bb7b37ff55", extension="jpg"),
        ...     comics=ComicList(available=200, returned=50, collectionURI="...", items=[]),
        ...     stories=StoryList(available=300, returned=75, collectionURI="...", items=[]),
        ...     events=EventList(available=5, returned=3, collectionURI="...", items=[]),
        ...     characters=CharacterList(available=25, returned=10, collectionURI="...", items=[]),
        ...     creators=CreatorList(available=15, returned=8, collectionURI="...", items=[]),
        ...     next=None,
        ...     previous=None
        ... )
        >>> series.title
        'Avengers (1998 - 2004)'
        >>> series.id
        1991
    """

    id: int = Field(..., description="Unique identifier for the series")
    title: str = Field(..., description="Title of the series")
    description: str = Field(..., description="Description of the series")
    resource_uri: str = Field(..., alias="resourceURI", description="URI of the series resource")
    urls: List[URL] = Field(
        default_factory=list, description="List of URLs associated with the series"
    )
    start_year: int = Field(..., description="Year the series started")
    end_year: Optional[int] = Field(None, description="Year the series ended")
    rating: str = Field(..., description="Rating of the series")
    modified: str = Field(..., description="Date the series was last modified")
    thumbnail: Optional[Image] = Field(None, description="Series thumbnail image")
    comics: ComicList = Field(..., description="Comics that are part of this series")
    stories: StoryList = Field(..., description="Stories that are part of this series")
    events: EventList = Field(..., description="Events related to this series")
    characters: CharacterList = Field(..., description="Characters that appear in this series")
    creators: CreatorList = Field(..., description="Creators who worked on this series")
    next: Optional["SeriesSummary"] = Field(None, description="Next series in chronological order")
    previous: Optional["SeriesSummary"] = Field(
        None, description="Previous series in chronological order"
    )


class SeriesListResponse(BaseListResponse[Series]):
    """Series list response.

    Represents a Marvel API response containing a list of series
    with pagination metadata. This is the standard response format
    for series list endpoints.

    Attributes:
        code: HTTP status code
        status: Status message
        copyright: Copyright notice
        attribution_text: Text attribution
        attribution_html: HTML attribution
        etag: ETag for caching
        data: DataContainer with series list and pagination info

    Example:
        >>> response = SeriesListResponse(
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
        ...         results=[Series(id=1991, title="Avengers (1998 - 2004)", ...)]
        ...     )
        ... )
        >>> response.data.results[0].title
        'Avengers (1998 - 2004)'
    """

    data: DataContainer[Series] = Field(..., description="Series data container")


class SeriesResponse(BaseResponse[Series]):
    """Single series response.

    Represents a Marvel API response containing a single series
    with full details. This is the standard response format for
    individual series endpoints.

    Attributes:
        code: HTTP status code
        status: Status message
        copyright: Copyright notice
        attribution_text: Text attribution
        attribution_html: HTML attribution
        etag: ETag for caching
        data: Series data

    Example:
        >>> response = SeriesResponse(
        ...     code=200,
        ...     status="Ok",
        ...     copyright="© 2024 MARVEL",
        ...     attributionText="Data provided by Marvel. © 2024 MARVEL",
        ...     attributionHTML="<a href='http://marvel.com'>Data provided by Marvel. © 2024 MARVEL</a>",
        ...     etag="etag123",
        ...     data=Series(id=1991, title="Avengers (1998 - 2004)", ...)
        ... )
        >>> response.data.title
        'Avengers (1998 - 2004)'
    """

    data: Series = Field(..., description="Series data")
