"""Story data models for Marvel API.

This module contains data models for Marvel stories, including the main
Story model and related list structures. Stories are individual narrative
units within comics, representing specific plotlines, covers, or other
content types that make up the comic book experience.
"""

from typing import List, Optional

from pydantic import Field

from .base import BaseListResponse, BaseModel, BaseResponse, DataContainer
from .common import (
    CharacterSummary,
    ComicSummary,
    CreatorSummary,
    EventSummary,
    Image,
    SeriesSummary,
)


class CharacterList(BaseModel):
    """Character list for story.

    Represents a collection of characters that appear in a specific story,
    including pagination metadata and a list of character summaries.

    Attributes:
        available: Number of characters available for this story
        returned: Number of characters returned in this response
        collection_uri: URI of the characters collection for this story
        items: List of character summaries that appear in this story

    Example:
        >>> character_list = CharacterList(
        ...     available=10,
        ...     returned=5,
        ...     collectionURI="http://gateway.marvel.com/v1/public/stories/12345/characters",
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


class ComicList(BaseModel):
    """Comic list for story.

    Represents a collection of comics that contain a specific story,
    including pagination metadata and a list of comic summaries.

    Attributes:
        available: Number of comics available for this story
        returned: Number of comics returned in this response
        collection_uri: URI of the comics collection for this story
        items: List of comic summaries that contain this story

    Example:
        >>> comic_list = ComicList(
        ...     available=5,
        ...     returned=3,
        ...     collectionURI="http://gateway.marvel.com/v1/public/stories/12345/comics",
        ...     items=[ComicSummary(resourceURI="...", name="Avengers (1963) #1")]
        ... )
        >>> comic_list.available
        5
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
    """Creator list for story.

    Represents a collection of creators who worked on a specific story,
    including pagination metadata and a list of creator summaries.

    Attributes:
        available: Number of creators available for this story
        returned: Number of creators returned in this response
        collection_uri: URI of the creators collection for this story
        items: List of creator summaries who worked on this story

    Example:
        >>> creator_list = CreatorList(
        ...     available=8,
        ...     returned=4,
        ...     collectionURI="http://gateway.marvel.com/v1/public/stories/12345/creators",
        ...     items=[CreatorSummary(resourceURI="...", name="Stan Lee", role="writer")]
        ... )
        >>> creator_list.available
        8
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
    """Event list for story.

    Represents a collection of events that are related to a specific story,
    including pagination metadata and a list of event summaries.

    Attributes:
        available: Number of events available for this story
        returned: Number of events returned in this response
        collection_uri: URI of the events collection for this story
        items: List of event summaries related to this story

    Example:
        >>> event_list = EventList(
        ...     available=3,
        ...     returned=2,
        ...     collectionURI="http://gateway.marvel.com/v1/public/stories/12345/events",
        ...     items=[EventSummary(resourceURI="...", name="Secret Invasion")]
        ... )
        >>> event_list.available
        3
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
    """Series list for story.

    Represents a collection of series that contain a specific story,
    including pagination metadata and a list of series summaries.

    Attributes:
        available: Number of series available for this story
        returned: Number of series returned in this response
        collection_uri: URI of the series collection for this story
        items: List of series summaries that contain this story

    Example:
        >>> series_list = SeriesList(
        ...     available=2,
        ...     returned=1,
        ...     collectionURI="http://gateway.marvel.com/v1/public/stories/12345/series",
        ...     items=[SeriesSummary(resourceURI="...", name="Avengers (1998 - 2004)")]
        ... )
        >>> series_list.available
        2
        >>> len(series_list.items)
        1
    """

    available: int = Field(..., description="Number of series available")
    returned: int = Field(..., description="Number of series returned")
    collection_uri: str = Field(
        ..., alias="collectionURI", description="URI of the series collection"
    )
    items: List[SeriesSummary] = Field(default_factory=list, description="List of series summaries")


class Story(BaseModel):
    """Story data model for Marvel API.

    Represents a Marvel story with all associated information including
    basic details, description, type, and related resources. Stories are
    individual narrative units within comics, representing specific plotlines,
    covers, or other content types.

    Attributes:
        id: Unique identifier for the story
        title: Title of the story
        description: Description of the story (may be empty)
        resource_uri: URI of the story resource
        type: Type of the story (e.g., "cover", "interiorStory", "promo")
        modified: Date the story was last modified (ISO format)
        thumbnail: Story thumbnail image (may be None)
        comics: Comics that contain this story
        series: Series that contain this story
        events: Events related to this story
        characters: Characters that appear in this story
        creators: Creators who worked on this story
        original_issue: Original issue where this story first appeared (may be None)

    Example:
        >>> story = Story(
        ...     id=12345,
        ...     title="Cover #1",
        ...     description="Cover story for Avengers #1",
        ...     resourceURI="http://gateway.marvel.com/v1/public/stories/12345",
        ...     type="cover",
        ...     modified="2013-11-20T17:40:18-0500",
        ...     thumbnail=Image(path="http://i.annihil.us/u/prod/marvel/i/mg/9/c0/527bb7b37ff55", extension="jpg"),
        ...     comics=ComicList(available=5, returned=3, collectionURI="...", items=[]),
        ...     series=SeriesList(available=2, returned=1, collectionURI="...", items=[]),
        ...     events=EventList(available=3, returned=2, collectionURI="...", items=[]),
        ...     characters=CharacterList(available=10, returned=5, collectionURI="...", items=[]),
        ...     creators=CreatorList(available=8, returned=4, collectionURI="...", items=[]),
        ...     original_issue=None
        ... )
        >>> story.title
        'Cover #1'
        >>> story.id
        12345
    """

    id: int = Field(..., description="Unique identifier for the story")
    title: str = Field(..., description="Title of the story")
    description: str = Field(..., description="Description of the story")
    resource_uri: str = Field(..., alias="resourceURI", description="URI of the story resource")
    type: str = Field(..., description="Type of the story")
    modified: str = Field(..., description="Date the story was last modified")
    thumbnail: Optional[Image] = Field(None, description="Story thumbnail image")
    comics: ComicList = Field(..., description="Comics that contain this story")
    series: SeriesList = Field(..., description="Series that contain this story")
    events: EventList = Field(..., description="Events related to this story")
    characters: CharacterList = Field(..., description="Characters that appear in this story")
    creators: CreatorList = Field(..., description="Creators who worked on this story")
    original_issue: Optional[ComicSummary] = Field(
        None, description="Original issue where this story first appeared"
    )


class StoryListResponse(BaseListResponse[Story]):
    """Story list response.

    Represents a Marvel API response containing a list of stories
    with pagination metadata. This is the standard response format
    for story list endpoints.

    Attributes:
        code: HTTP status code
        status: Status message
        copyright: Copyright notice
        attribution_text: Text attribution
        attribution_html: HTML attribution
        etag: ETag for caching
        data: DataContainer with story list and pagination info

    Example:
        >>> response = StoryListResponse(
        ...     code=200,
        ...     status="Ok",
        ...     copyright="© 2024 MARVEL",
        ...     attributionText="Data provided by Marvel. © 2024 MARVEL",
        ...     attributionHTML="<a href='http://marvel.com'>Data provided by Marvel. © 2024 MARVEL</a>",
        ...     etag="etag123",
        ...     data=DataContainer(
        ...         offset=0,
        ...         limit=20,
        ...         total=500,
        ...         count=20,
        ...         results=[Story(id=12345, title="Cover #1", ...)]
        ...     )
        ... )
        >>> response.data.results[0].title
        'Cover #1'
    """

    data: DataContainer[Story] = Field(..., description="Story data container")


class StoryResponse(BaseResponse[Story]):
    """Single story response.

    Represents a Marvel API response containing a single story
    with full details. This is the standard response format for
    individual story endpoints.

    Attributes:
        code: HTTP status code
        status: Status message
        copyright: Copyright notice
        attribution_text: Text attribution
        attribution_html: HTML attribution
        etag: ETag for caching
        data: Story data

    Example:
        >>> response = StoryResponse(
        ...     code=200,
        ...     status="Ok",
        ...     copyright="© 2024 MARVEL",
        ...     attributionText="Data provided by Marvel. © 2024 MARVEL",
        ...     attributionHTML="<a href='http://marvel.com'>Data provided by Marvel. © 2024 MARVEL</a>",
        ...     etag="etag123",
        ...     data=Story(id=12345, title="Cover #1", ...)
        ... )
        >>> response.data.title
        'Cover #1'
    """

    data: Story = Field(..., description="Story data")
