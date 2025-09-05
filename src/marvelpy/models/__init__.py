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
from .creator import (
    CharacterList as CreatorCharacterList,
)
from .creator import (
    ComicList as CreatorComicList,
)
from .creator import (
    Creator,
    CreatorListResponse,
    CreatorResponse,
)
from .creator import (
    EventList as CreatorEventList,
)
from .creator import (
    SeriesList as CreatorSeriesList,
)
from .creator import (
    StoryList as CreatorStoryList,
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
from .series import (
    CharacterList as SeriesCharacterList,
)
from .series import (
    ComicList as SeriesComicList,
)
from .series import (
    CreatorList as SeriesCreatorList,
)
from .series import (
    EventList as SeriesEventList,
)
from .series import (
    Series,
    SeriesListResponse,
    SeriesResponse,
)
from .series import (
    StoryList as SeriesStoryList,
)
from .story import (
    CharacterList as StoryCharacterList,
)
from .story import (
    ComicList as StoryComicList,
)
from .story import (
    CreatorList as StoryCreatorList,
)
from .story import (
    EventList as StoryEventList,
)
from .story import (
    SeriesList as StorySeriesList,
)
from .story import (
    Story,
    StoryListResponse,
    StoryResponse,
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
    # Series models
    "Series",
    "SeriesResponse",
    "SeriesListResponse",
    "SeriesCharacterList",
    "SeriesComicList",
    "SeriesCreatorList",
    "SeriesEventList",
    "SeriesStoryList",
    # Story models
    "Story",
    "StoryResponse",
    "StoryListResponse",
    "StoryCharacterList",
    "StoryComicList",
    "StoryCreatorList",
    "StoryEventList",
    "StorySeriesList",
    # Creator models
    "Creator",
    "CreatorResponse",
    "CreatorListResponse",
    "CreatorCharacterList",
    "CreatorComicList",
    "CreatorEventList",
    "CreatorSeriesList",
    "CreatorStoryList",
]
