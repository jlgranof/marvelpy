"""Comic data models for Marvel API.

This module contains data models for Marvel comics, including the main
Comic model and related list structures. Comics are central entities
in the Marvel API, representing individual comic book issues with
detailed information about publication, creators, characters, and more.
"""

from typing import List, Optional

from pydantic import Field

from .base import BaseListResponse, BaseModel, BaseResponse, DataContainer
from .common import (
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


class CharacterList(BaseModel):
    """Character list for comic.

    Represents a collection of characters appearing in a specific comic,
    including pagination metadata and a list of character summaries.

    Attributes:
        available: Number of characters available for this comic
        returned: Number of characters returned in this response
        collection_uri: URI of the characters collection for this comic
        items: List of character summaries appearing in this comic

    Example:
        >>> character_list = CharacterList(
        ...     available=10,
        ...     returned=5,
        ...     collectionURI="http://gateway.marvel.com/v1/public/comics/21366/characters",
        ...     items=[CharacterSummary(resourceURI="...", name="Iron Man")]
        ... )
        >>> character_list.available
        10
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


class CreatorList(BaseModel):
    """Creator list for comic.

    Represents a collection of creators (writers, artists, etc.) who worked
    on a specific comic, including pagination metadata and a list of creator summaries.

    Attributes:
        available: Number of creators available for this comic
        returned: Number of creators returned in this response
        collection_uri: URI of the creators collection for this comic
        items: List of creator summaries who worked on this comic

    Example:
        >>> creator_list = CreatorList(
        ...     available=5,
        ...     returned=3,
        ...     collectionURI="http://gateway.marvel.com/v1/public/comics/21366/creators",
        ...     items=[CreatorSummary(resourceURI="...", name="Stan Lee", role="writer")]
        ... )
        >>> creator_list.available
        5
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


class StoryList(BaseModel):
    """Story list for comic.

    Represents a collection of stories contained in a specific comic,
    including pagination metadata and a list of story summaries.

    Attributes:
        available: Number of stories available for this comic
        returned: Number of stories returned in this response
        collection_uri: URI of the stories collection for this comic
        items: List of story summaries contained in this comic

    Example:
        >>> story_list = StoryList(
        ...     available=3,
        ...     returned=2,
        ...     collectionURI="http://gateway.marvel.com/v1/public/comics/21366/stories",
        ...     items=[StorySummary(resourceURI="...", name="Cover #1", type="cover")]
        ... )
        >>> story_list.available
        3
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
    """Event list for comic.

    Represents a collection of events that a specific comic is part of,
    including pagination metadata and a list of event summaries.

    Attributes:
        available: Number of events available for this comic
        returned: Number of events returned in this response
        collection_uri: URI of the events collection for this comic
        items: List of event summaries that this comic is part of

    Example:
        >>> event_list = EventList(
        ...     available=2,
        ...     returned=1,
        ...     collectionURI="http://gateway.marvel.com/v1/public/comics/21366/events",
        ...     items=[EventSummary(resourceURI="...", name="Secret Invasion")]
        ... )
        >>> event_list.available
        2
        >>> len(event_list.items)
        1
    """

    available: int = Field(..., description="Number of events available")
    returned: int = Field(..., description="Number of events returned")
    collection_uri: str = Field(
        ..., alias="collectionURI", description="URI of the events collection"
    )
    items: List[EventSummary] = Field(default_factory=list, description="List of event summaries")


class Comic(BaseModel):
    """Comic data model for Marvel API.

    Represents a Marvel comic with all associated information including
    publication details, creators, characters, stories, and related resources.
    Comics are central entities in the Marvel universe and contain detailed
    information about individual issues.

    Attributes:
        id: Unique identifier for the comic
        digital_id: Digital identifier for the comic (may be 0)
        title: Title of the comic
        issue_number: Issue number of the comic (may be 0)
        variant_description: Description of variant covers (may be empty)
        description: Description of the comic (may be empty)
        modified: Date the comic was last modified (ISO format)
        isbn: ISBN of the comic (may be empty)
        upc: UPC barcode of the comic (may be empty)
        diamond_code: Diamond distribution code (may be empty)
        ean: EAN barcode of the comic (may be empty)
        issn: ISSN of the comic (may be empty)
        format: Format of the comic (e.g., 'Comic', 'Trade Paperback')
        page_count: Number of pages in the comic (may be 0)
        text_objects: List of text objects (descriptions, summaries, etc.)
        resource_uri: URI of the comic resource
        urls: List of URLs associated with the comic
        series: Series this comic belongs to
        variants: List of variant comics
        collections: List of collections this comic is part of
        collected_issues: List of issues collected in this comic
        dates: List of important dates (on-sale, focus, etc.)
        prices: List of prices for different formats
        thumbnail: Comic thumbnail image (may be None)
        images: List of images for this comic
        creators: Creators who worked on this comic
        characters: Characters appearing in this comic
        stories: Stories contained in this comic
        events: Events this comic is part of

    Example:
        >>> comic = Comic(
        ...     id=21366,
        ...     digital_id=0,
        ...     title="Avengers (1963) #1",
        ...     issue_number=1,
        ...     variant_description="",
        ...     description="The Avengers are born!",
        ...     modified="2014-04-29T14:18:17-0400",
        ...     isbn="",
        ...     upc="",
        ...     diamond_code="",
        ...     ean="",
        ...     issn="",
        ...     format="Comic",
        ...     page_count=32,
        ...     text_objects=[],
        ...     resourceURI="http://gateway.marvel.com/v1/public/comics/21366",
        ...     urls=[],
        ...     series=SeriesSummary(resourceURI="...", name="Avengers (1963 - 1996)"),
        ...     variants=[],
        ...     collections=[],
        ...     collected_issues=[],
        ...     dates=[],
        ...     prices=[],
        ...     thumbnail=None,
        ...     images=[],
        ...     creators=CreatorList(available=0, returned=0, collectionURI="...", items=[]),
        ...     characters=CharacterList(available=0, returned=0, collectionURI="...", items=[]),
        ...     stories=StoryList(available=0, returned=0, collectionURI="...", items=[]),
        ...     events=EventList(available=0, returned=0, collectionURI="...", items=[])
        ... )
        >>> comic.title
        'Avengers (1963) #1'
        >>> comic.issue_number
        1
    """

    id: int = Field(..., description="Unique identifier for the comic")
    digital_id: int = Field(..., alias="digitalId", description="Digital identifier for the comic")
    title: str = Field(..., description="Title of the comic")
    issue_number: float = Field(..., alias="issueNumber", description="Issue number of the comic")
    variant_description: Optional[str] = Field(
        None, alias="variantDescription", description="Description of variant covers"
    )
    description: Optional[str] = Field(None, description="Description of the comic")
    modified: str = Field(..., description="Date the comic was last modified")
    isbn: str = Field(..., description="ISBN of the comic")
    upc: str = Field(..., description="UPC barcode of the comic")
    diamond_code: str = Field(..., alias="diamondCode", description="Diamond distribution code")
    ean: str = Field(..., description="EAN barcode of the comic")
    issn: str = Field(..., description="ISSN of the comic")
    format: str = Field(..., description="Format of the comic")
    page_count: int = Field(..., alias="pageCount", description="Number of pages in the comic")
    text_objects: List[TextObject] = Field(
        ..., alias="textObjects", description="List of text objects"
    )
    resource_uri: str = Field(..., alias="resourceURI", description="URI of the comic resource")
    urls: List[URL] = Field(
        default_factory=list, description="List of URLs associated with the comic"
    )
    series: SeriesSummary = Field(..., description="Series this comic belongs to")
    variants: List["ComicSummary"] = Field(
        default_factory=list, description="List of variant comics"
    )
    collections: List["ComicSummary"] = Field(
        default_factory=list, description="List of collections this comic is part of"
    )
    collected_issues: List["ComicSummary"] = Field(
        ..., alias="collectedIssues", description="List of issues collected in this comic"
    )
    dates: List[Date] = Field(default_factory=list, description="List of important dates")
    prices: List[Price] = Field(
        default_factory=list, description="List of prices for different formats"
    )
    thumbnail: Optional[Image] = Field(None, description="Comic thumbnail image")
    images: List[Image] = Field(default_factory=list, description="List of images for this comic")
    creators: CreatorList = Field(..., description="Creators who worked on this comic")
    characters: CharacterList = Field(..., description="Characters appearing in this comic")
    stories: StoryList = Field(..., description="Stories contained in this comic")
    events: EventList = Field(..., description="Events this comic is part of")


class ComicListResponse(BaseListResponse[Comic]):
    """Comic list response.

    Represents a Marvel API response containing a list of comics
    with pagination metadata. This is the standard response format
    for comic list endpoints.

    Attributes:
        code: HTTP status code
        status: Status message
        copyright: Copyright notice
        attribution_text: Text attribution
        attribution_html: HTML attribution
        etag: ETag for caching
        data: DataContainer with comic list and pagination info

    Example:
        >>> response = ComicListResponse(
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
        ...         results=[Comic(id=21366, title="Avengers (1963) #1", ...)]
        ...     )
        ... )
        >>> response.data.results[0].title
        'Avengers (1963) #1'
    """

    data: DataContainer[Comic] = Field(..., description="Comic data container")


class ComicResponse(BaseResponse[Comic]):
    """Single comic response.

    Represents a Marvel API response containing a single comic
    with full details. This is the standard response format for
    individual comic endpoints.

    Attributes:
        code: HTTP status code
        status: Status message
        copyright: Copyright notice
        attribution_text: Text attribution
        attribution_html: HTML attribution
        etag: ETag for caching
        data: Comic data

    Example:
        >>> response = ComicResponse(
        ...     code=200,
        ...     status="Ok",
        ...     copyright="© 2024 MARVEL",
        ...     attributionText="Data provided by Marvel. © 2024 MARVEL",
        ...     attributionHTML="<a href='http://marvel.com'>Data provided by Marvel. © 2024 MARVEL</a>",
        ...     etag="etag123",
        ...     data=Comic(id=21366, title="Avengers (1963) #1", ...)
        ... )
        >>> response.data.title
        'Avengers (1963) #1'
    """

    data: Comic = Field(..., description="Comic data")
