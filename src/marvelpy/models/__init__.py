"""Marvel API data models."""

from .base import BaseListResponse, BaseModel, BaseResponse, DataContainer
from .character import (
    Character,
    CharacterListResponse,
    CharacterResponse,
    ComicList,
    EventList,
    SeriesList,
    StoryList,
)
from .comic import (
    CharacterList,
    Comic,
    ComicListResponse,
    ComicResponse,
    CreatorList,
)
from .comic import (
    EventList as ComicEventList,
)
from .comic import (
    StoryList as ComicStoryList,
)
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
from .event import (
    CharacterList as EventCharacterList,
)
from .event import (
    ComicList as EventComicList,
)
from .event import (
    CreatorList as EventCreatorList,
)
from .event import (
    Event,
    EventListResponse,
    EventResponse,
)
from .event import (
    SeriesList as EventSeriesList,
)
from .event import (
    StoryList as EventStoryList,
)

__all__ = [
    # Base models
    "BaseModel",
    "BaseResponse",
    "BaseListResponse",
    "DataContainer",
    # Common types
    "Image",
    "URL",
    "TextObject",
    "Date",
    "Price",
    "CreatorSummary",
    "CharacterSummary",
    "StorySummary",
    "EventSummary",
    "SeriesSummary",
    "ComicSummary",
    # Character models
    "Character",
    "CharacterResponse",
    "CharacterListResponse",
    "ComicList",
    "StoryList",
    "EventList",
    "SeriesList",
    # Comic models
    "Comic",
    "ComicResponse",
    "ComicListResponse",
    "CharacterList",
    "CreatorList",
    "ComicEventList",
    "ComicStoryList",
    # Event models
    "Event",
    "EventResponse",
    "EventListResponse",
    "EventCharacterList",
    "EventComicList",
    "EventCreatorList",
    "EventSeriesList",
    "EventStoryList",
]
