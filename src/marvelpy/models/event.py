"""Event data models for Marvel API.

This module contains data models for Marvel events, including the main
Event model and related list structures. Events are major storylines
in the Marvel universe that span across multiple comics, series, and
characters, representing significant narrative arcs.
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
    """Character list for event.

    Represents a collection of characters involved in a specific event,
    including pagination metadata and a list of character summaries.

    Attributes:
        available: Number of characters available for this event
        returned: Number of characters returned in this response
        collection_uri: URI of the characters collection for this event
        items: List of character summaries involved in this event

    Example:
        >>> character_list = CharacterList(
        ...     available=50,
        ...     returned=20,
        ...     collectionURI="http://gateway.marvel.com/v1/public/events/269/characters",
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
    """Comic list for event.

    Represents a collection of comics that are part of a specific event,
    including pagination metadata and a list of comic summaries.

    Attributes:
        available: Number of comics available for this event
        returned: Number of comics returned in this response
        collection_uri: URI of the comics collection for this event
        items: List of comic summaries that are part of this event

    Example:
        >>> comic_list = ComicList(
        ...     available=100,
        ...     returned=25,
        ...     collectionURI="http://gateway.marvel.com/v1/public/events/269/comics",
        ...     items=[ComicSummary(resourceURI="...", name="Avengers (1963) #1")]
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


class CreatorList(BaseModel):
    """Creator list for event.

    Represents a collection of creators who worked on comics related to
    a specific event, including pagination metadata and a list of creator summaries.

    Attributes:
        available: Number of creators available for this event
        returned: Number of creators returned in this response
        collection_uri: URI of the creators collection for this event
        items: List of creator summaries who worked on this event

    Example:
        >>> creator_list = CreatorList(
        ...     available=25,
        ...     returned=10,
        ...     collectionURI="http://gateway.marvel.com/v1/public/events/269/creators",
        ...     items=[CreatorSummary(resourceURI="...", name="Stan Lee", role="writer")]
        ... )
        >>> creator_list.available
        25
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


class SeriesList(BaseModel):
    """Series list for event.

    Represents a collection of series that are part of a specific event,
    including pagination metadata and a list of series summaries.

    Attributes:
        available: Number of series available for this event
        returned: Number of series returned in this response
        collection_uri: URI of the series collection for this event
        items: List of series summaries that are part of this event

    Example:
        >>> series_list = SeriesList(
        ...     available=15,
        ...     returned=5,
        ...     collectionURI="http://gateway.marvel.com/v1/public/events/269/series",
        ...     items=[SeriesSummary(resourceURI="...", name="Avengers (1998 - 2004)")]
        ... )
        >>> series_list.available
        15
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
    """Story list for event.

    Represents a collection of stories that are part of a specific event,
    including pagination metadata and a list of story summaries.

    Attributes:
        available: Number of stories available for this event
        returned: Number of stories returned in this response
        collection_uri: URI of the stories collection for this event
        items: List of story summaries that are part of this event

    Example:
        >>> story_list = StoryList(
        ...     available=200,
        ...     returned=50,
        ...     collectionURI="http://gateway.marvel.com/v1/public/events/269/stories",
        ...     items=[StorySummary(resourceURI="...", name="Cover #1", type="cover")]
        ... )
        >>> story_list.available
        200
        >>> len(story_list.items)
        1
    """

    available: int = Field(..., description="Number of stories available")
    returned: int = Field(..., description="Number of stories returned")
    collection_uri: str = Field(
        ..., alias="collectionURI", description="URI of the stories collection"
    )
    items: List[StorySummary] = Field(default_factory=list, description="List of story summaries")


class Event(BaseModel):
    """Event data model for Marvel API.

    Represents a Marvel event with all associated information including
    basic details, description, dates, and related resources. Events are
    major storylines in the Marvel universe that span across multiple
    comics, series, and characters.

    Attributes:
        id: Unique identifier for the event
        title: Title of the event
        description: Description of the event (may be empty)
        resource_uri: URI of the event resource
        urls: List of URLs associated with the event
        modified: Date the event was last modified (ISO format)
        start: Start date of the event (ISO format, may be empty)
        end: End date of the event (ISO format, may be empty)
        thumbnail: Event thumbnail image (may be None)
        comics: Comics that are part of this event
        stories: Stories that are part of this event
        series: Series that are part of this event
        characters: Characters involved in this event
        creators: Creators who worked on this event
        next: Next event in chronological order (may be None)
        previous: Previous event in chronological order (may be None)

    Example:
        >>> event = Event(
        ...     id=269,
        ...     title="Secret Invasion",
        ...     description="The shape-shifting alien race known as the Skrulls...",
        ...     resourceURI="http://gateway.marvel.com/v1/public/events/269",
        ...     urls=[URL(type="detail", url="http://marvel.com/comics/events/269/secret_invasion")],
        ...     modified="2013-11-20T17:40:18-0500",
        ...     start="2008-04-01 00:00:00",
        ...     end="2008-12-01 00:00:00",
        ...     thumbnail=Image(path="http://i.annihil.us/u/prod/marvel/i/mg/9/c0/527bb7b37ff55", extension="jpg"),
        ...     comics=ComicList(available=100, returned=25, collectionURI="...", items=[]),
        ...     stories=StoryList(available=200, returned=50, collectionURI="...", items=[]),
        ...     series=SeriesList(available=15, returned=5, collectionURI="...", items=[]),
        ...     characters=CharacterList(available=50, returned=20, collectionURI="...", items=[]),
        ...     creators=CreatorList(available=25, returned=10, collectionURI="...", items=[]),
        ...     next=None,
        ...     previous=None
        ... )
        >>> event.title
        'Secret Invasion'
        >>> event.id
        269
    """

    id: int = Field(..., description="Unique identifier for the event")
    title: str = Field(..., description="Title of the event")
    description: str = Field(..., description="Description of the event")
    resource_uri: str = Field(..., alias="resourceURI", description="URI of the event resource")
    urls: List[URL] = Field(
        default_factory=list, description="List of URLs associated with the event"
    )
    modified: str = Field(..., description="Date the event was last modified")
    start: Optional[str] = Field(None, description="Start date of the event")
    end: Optional[str] = Field(None, description="End date of the event")
    thumbnail: Optional[Image] = Field(None, description="Event thumbnail image")
    comics: ComicList = Field(..., description="Comics that are part of this event")
    stories: StoryList = Field(..., description="Stories that are part of this event")
    series: SeriesList = Field(..., description="Series that are part of this event")
    characters: CharacterList = Field(..., description="Characters involved in this event")
    creators: CreatorList = Field(..., description="Creators who worked on this event")
    next: Optional["EventSummary"] = Field(None, description="Next event in chronological order")
    previous: Optional["EventSummary"] = Field(
        None, description="Previous event in chronological order"
    )


class EventListResponse(BaseListResponse[Event]):
    """Event list response.

    Represents a Marvel API response containing a list of events
    with pagination metadata. This is the standard response format
    for event list endpoints.

    Attributes:
        code: HTTP status code
        status: Status message
        copyright: Copyright notice
        attribution_text: Text attribution
        attribution_html: HTML attribution
        etag: ETag for caching
        data: DataContainer with event list and pagination info

    Example:
        >>> response = EventListResponse(
        ...     code=200,
        ...     status="Ok",
        ...     copyright="© 2024 MARVEL",
        ...     attributionText="Data provided by Marvel. © 2024 MARVEL",
        ...     attributionHTML="<a href='http://marvel.com'>Data provided by Marvel. © 2024 MARVEL</a>",
        ...     etag="etag123",
        ...     data=DataContainer(
        ...         offset=0,
        ...         limit=20,
        ...         total=50,
        ...         count=20,
        ...         results=[Event(id=269, title="Secret Invasion", ...)]
        ...     )
        ... )
        >>> response.data.results[0].title
        'Secret Invasion'
    """

    data: DataContainer[Event] = Field(..., description="Event data container")


class EventResponse(BaseResponse[Event]):
    """Single event response.

    Represents a Marvel API response containing a single event
    with full details. This is the standard response format for
    individual event endpoints.

    Attributes:
        code: HTTP status code
        status: Status message
        copyright: Copyright notice
        attribution_text: Text attribution
        attribution_html: HTML attribution
        etag: ETag for caching
        data: Event data

    Example:
        >>> response = EventResponse(
        ...     code=200,
        ...     status="Ok",
        ...     copyright="© 2024 MARVEL",
        ...     attributionText="Data provided by Marvel. © 2024 MARVEL",
        ...     attributionHTML="<a href='http://marvel.com'>Data provided by Marvel. © 2024 MARVEL</a>",
        ...     etag="etag123",
        ...     data=Event(id=269, title="Secret Invasion", ...)
        ... )
        >>> response.data.title
        'Secret Invasion'
    """

    data: Event = Field(..., description="Event data")
