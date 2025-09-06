"""Characters endpoint for Marvel API.

This module provides the CharactersEndpoint class for interacting with
Marvel API character resources. It provides type-safe methods for
retrieving character data and related information.
"""

from typing import Any, Dict, List, Optional

from marvelpy.endpoints.base import BaseEndpoint
from marvelpy.models.character import (
    Character,
    CharacterListResponse,
    CharacterResponse,
)
from marvelpy.models.comic import ComicListResponse
from marvelpy.models.event import EventListResponse
from marvelpy.models.series import SeriesListResponse
from marvelpy.models.story import StoryListResponse


class CharactersEndpoint(BaseEndpoint):
    """Endpoint for Marvel API character resources.

    This class provides methods for retrieving character data from the
    Marvel API, including individual characters, character lists, and
    related resources like comics, events, series, and stories.

    Example:
        >>> endpoint = CharactersEndpoint(
        ...     base_url="https://gateway.marvel.com",
        ...     public_key="your_public_key",
        ...     private_key="your_private_key"
        ... )
        >>> character = await endpoint.get_character(1011334)  # Get Iron Man
        >>> characters = await endpoint.list_characters(limit=10)  # Get first 10 characters
    """

    async def get_character(self, character_id: int) -> Character:
        """Get a single character by ID.

        Args:
            character_id: The unique identifier for the character

        Returns:
            Character object containing character data

        Raises:
            MarvelAPIError: For any Marvel API related errors

        Example:
            >>> character = await endpoint.get_character(1011334)  # Get Iron Man
            >>> print(character.name)
            Iron Man
        """
        response = await self._make_request(
            "GET",
            f"/v1/public/characters/{character_id}",
            response_model=CharacterResponse,
        )
        return response.data  # type: ignore[attr-defined,no-any-return]

    async def list_characters(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        name: Optional[str] = None,
        name_starts_with: Optional[str] = None,
        modified_since: Optional[str] = None,
        comics: Optional[List[int]] = None,
        series: Optional[List[int]] = None,
        events: Optional[List[int]] = None,
        stories: Optional[List[int]] = None,
        order_by: Optional[str] = None,
    ) -> CharacterListResponse:
        """Get a list of characters with optional filtering.

        Args:
            limit: Maximum number of characters to return (default: 20, max: 100)
            offset: Number of characters to skip (default: 0)
            name: Return only characters matching the specified name
            name_starts_with: Return characters with names that begin with the specified string
            modified_since: Return only characters which have been modified since the specified date
            comics: Return only characters which appear in the specified comics
            series: Return only characters which appear the specified series
            events: Return only characters which appear in the specified events
            stories: Return only characters which appear the specified stories
            order_by: Order the result set by a field or set of fields

        Returns:
            CharacterListResponse containing list of characters and metadata

        Raises:
            MarvelAPIError: For any Marvel API related errors

        Example:
            >>> characters = await endpoint.list(
            ...     name="Iron Man",
            ...     limit=5
            ... )
            >>> print(f"Found {characters.data.total} characters")
        """
        filters: Dict[str, Any] = {}

        if name is not None:
            filters["name"] = name
        if name_starts_with is not None:
            filters["nameStartsWith"] = name_starts_with
        if modified_since is not None:
            filters["modifiedSince"] = modified_since
        if comics is not None:
            filters["comics"] = ",".join(map(str, comics))
        if series is not None:
            filters["series"] = ",".join(map(str, series))
        if events is not None:
            filters["events"] = ",".join(map(str, events))
        if stories is not None:
            filters["stories"] = ",".join(map(str, stories))
        if order_by is not None:
            filters["orderBy"] = order_by

        return await self.list(
            "/v1/public/characters",
            CharacterListResponse,
            limit=limit,
            offset=offset,
            **filters,
        )

    async def get_comics(
        self,
        character_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        format: Optional[str] = None,
        format_type: Optional[str] = None,
        no_variants: Optional[bool] = None,
        date_descriptor: Optional[str] = None,
        date_range: Optional[List[int]] = None,
        title: Optional[str] = None,
        title_starts_with: Optional[str] = None,
        start_year: Optional[int] = None,
        issue_number: Optional[int] = None,
        diamond_code: Optional[str] = None,
        digital_id: Optional[int] = None,
        upc: Optional[str] = None,
        isbn: Optional[str] = None,
        ean: Optional[str] = None,
        issn: Optional[str] = None,
        has_digital_issue: Optional[bool] = None,
        modified_since: Optional[str] = None,
        creators: Optional[List[int]] = None,
        series: Optional[List[int]] = None,
        events: Optional[List[int]] = None,
        stories: Optional[List[int]] = None,
        shared_appearances: Optional[List[int]] = None,
        collaborators: Optional[List[int]] = None,
        order_by: Optional[str] = None,
        contains: Optional[str] = None,
    ) -> ComicListResponse:
        """Get comics featuring a specific character.

        Args:
            character_id: The unique identifier for the character
            limit: Maximum number of comics to return (default: 20, max: 100)
            offset: Number of comics to skip (default: 0)
            format: Filter by the issue format
            format_type: Filter by the issue format type
            no_variants: Exclude variant comics from the result set
            date_descriptor: Return comics within a predefined date range
            date_range: Return comics within a date range
            title: Return only comics matching the specified title
            title_starts_with: Return comics with titles that begin with the specified string
            start_year: Return only comics which have been published since the specified year
            issue_number: Return only the specified comic issue number
            diamond_code: Filter by diamond code
            digital_id: Filter by digital comic id
            upc: Filter by UPC
            isbn: Filter by ISBN
            ean: Filter by EAN
            issn: Filter by ISSN
            has_digital_issue: Filter by digital comics availability
            modified_since: Return only comics which have been modified since the specified date
            creators: Return only comics which feature work by the specified creators
            series: Return only comics which are part of the specified series
            events: Return only comics which take place during the specified events
            stories: Return only comics which contain the specified stories
            shared_appearances: Return only comics in which the specified characters appear together
            collaborators: Return only comics in which the specified creators worked together
            order_by: Order the result set by a field or set of fields
            contains: Return only comics which contain the specified format

        Returns:
            ComicListResponse containing list of comics and metadata

        Raises:
            MarvelAPIError: For any Marvel API related errors

        Example:
            >>> comics = await endpoint.get_comics(
            ...     character_id=1011334,
            ...     limit=10,
            ...     format="comic"
            ... )
            >>> print(f"Found {comics.data.total} comics")
        """
        filters: Dict[str, Any] = {}

        if format is not None:
            filters["format"] = format
        if format_type is not None:
            filters["formatType"] = format_type
        if no_variants is not None:
            filters["noVariants"] = no_variants
        if date_descriptor is not None:
            filters["dateDescriptor"] = date_descriptor
        if date_range is not None:
            filters["dateRange"] = ",".join(map(str, date_range))
        if title is not None:
            filters["title"] = title
        if title_starts_with is not None:
            filters["titleStartsWith"] = title_starts_with
        if start_year is not None:
            filters["startYear"] = start_year
        if issue_number is not None:
            filters["issueNumber"] = issue_number
        if diamond_code is not None:
            filters["diamondCode"] = diamond_code
        if digital_id is not None:
            filters["digitalId"] = digital_id
        if upc is not None:
            filters["upc"] = upc
        if isbn is not None:
            filters["isbn"] = isbn
        if ean is not None:
            filters["ean"] = ean
        if issn is not None:
            filters["issn"] = issn
        if has_digital_issue is not None:
            filters["hasDigitalIssue"] = has_digital_issue
        if modified_since is not None:
            filters["modifiedSince"] = modified_since
        if creators is not None:
            filters["creators"] = ",".join(map(str, creators))
        if series is not None:
            filters["series"] = ",".join(map(str, series))
        if events is not None:
            filters["events"] = ",".join(map(str, events))
        if stories is not None:
            filters["stories"] = ",".join(map(str, stories))
        if shared_appearances is not None:
            filters["sharedAppearances"] = ",".join(map(str, shared_appearances))
        if collaborators is not None:
            filters["collaborators"] = ",".join(map(str, collaborators))
        if order_by is not None:
            filters["orderBy"] = order_by
        if contains is not None:
            filters["contains"] = contains

        return await self.get_related(
            "/v1/public/characters",
            character_id,
            "comics",
            ComicListResponse,
            limit=limit,
            offset=offset,
            **filters,
        )

    async def get_events(
        self,
        character_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        name: Optional[str] = None,
        name_starts_with: Optional[str] = None,
        modified_since: Optional[str] = None,
        creators: Optional[List[int]] = None,
        series: Optional[List[int]] = None,
        comics: Optional[List[int]] = None,
        stories: Optional[List[int]] = None,
        order_by: Optional[str] = None,
    ) -> EventListResponse:
        """Get events featuring a specific character.

        Args:
            character_id: The unique identifier for the character
            limit: Maximum number of events to return (default: 20, max: 100)
            offset: Number of events to skip (default: 0)
            name: Return only events matching the specified name
            name_starts_with: Return events with names that begin with the specified string
            modified_since: Return only events which have been modified since the specified date
            creators: Return only events which feature work by the specified creators
            series: Return only events which are part of the specified series
            comics: Return only events which take place in the specified comics
            stories: Return only events which contain the specified stories
            order_by: Order the result set by a field or set of fields

        Returns:
            EventListResponse containing list of events and metadata

        Raises:
            MarvelAPIError: For any Marvel API related errors

        Example:
            >>> events = await endpoint.get_events(
            ...     character_id=1011334,
            ...     limit=5
            ... )
            >>> print(f"Found {events.data.total} events")
        """
        filters: Dict[str, Any] = {}

        if name is not None:
            filters["name"] = name
        if name_starts_with is not None:
            filters["nameStartsWith"] = name_starts_with
        if modified_since is not None:
            filters["modifiedSince"] = modified_since
        if creators is not None:
            filters["creators"] = ",".join(map(str, creators))
        if series is not None:
            filters["series"] = ",".join(map(str, series))
        if comics is not None:
            filters["comics"] = ",".join(map(str, comics))
        if stories is not None:
            filters["stories"] = ",".join(map(str, stories))
        if order_by is not None:
            filters["orderBy"] = order_by

        return await self.get_related(
            "/v1/public/characters",
            character_id,
            "events",
            EventListResponse,
            limit=limit,
            offset=offset,
            **filters,
        )

    async def get_series(
        self,
        character_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        title: Optional[str] = None,
        title_starts_with: Optional[str] = None,
        start_year: Optional[int] = None,
        modified_since: Optional[str] = None,
        comics: Optional[List[int]] = None,
        stories: Optional[List[int]] = None,
        events: Optional[List[int]] = None,
        creators: Optional[List[int]] = None,
        series_type: Optional[str] = None,
        contains: Optional[str] = None,
        order_by: Optional[str] = None,
    ) -> SeriesListResponse:
        """Get series featuring a specific character.

        Args:
            character_id: The unique identifier for the character
            limit: Maximum number of series to return (default: 20, max: 100)
            offset: Number of series to skip (default: 0)
            title: Return only series matching the specified title
            title_starts_with: Return series with titles that begin with the specified string
            start_year: Return only series which have been published since the specified year
            modified_since: Return only series which have been modified since the specified date
            comics: Return only series which contain the specified comics
            stories: Return only series which contain the specified stories
            events: Return only series which are part of the specified events
            creators: Return only series which feature work by the specified creators
            series_type: Filter the series by publication frequency type
            contains: Return only series which contain the specified format
            order_by: Order the result set by a field or set of fields

        Returns:
            SeriesListResponse containing list of series and metadata

        Raises:
            MarvelAPIError: For any Marvel API related errors

        Example:
            >>> series = await endpoint.get_series(
            ...     character_id=1011334,
            ...     limit=10
            ... )
            >>> print(f"Found {series.data.total} series")
        """
        filters: Dict[str, Any] = {}

        if title is not None:
            filters["title"] = title
        if title_starts_with is not None:
            filters["titleStartsWith"] = title_starts_with
        if start_year is not None:
            filters["startYear"] = start_year
        if modified_since is not None:
            filters["modifiedSince"] = modified_since
        if comics is not None:
            filters["comics"] = ",".join(map(str, comics))
        if stories is not None:
            filters["stories"] = ",".join(map(str, stories))
        if events is not None:
            filters["events"] = ",".join(map(str, events))
        if creators is not None:
            filters["creators"] = ",".join(map(str, creators))
        if series_type is not None:
            filters["seriesType"] = series_type
        if contains is not None:
            filters["contains"] = contains
        if order_by is not None:
            filters["orderBy"] = order_by

        return await self.get_related(
            "/v1/public/characters",
            character_id,
            "series",
            SeriesListResponse,
            limit=limit,
            offset=offset,
            **filters,
        )

    async def get_stories(
        self,
        character_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        modified_since: Optional[str] = None,
        comics: Optional[List[int]] = None,
        series: Optional[List[int]] = None,
        events: Optional[List[int]] = None,
        creators: Optional[List[int]] = None,
        order_by: Optional[str] = None,
    ) -> StoryListResponse:
        """Get stories featuring a specific character.

        Args:
            character_id: The unique identifier for the character
            limit: Maximum number of stories to return (default: 20, max: 100)
            offset: Number of stories to skip (default: 0)
            modified_since: Return only stories which have been modified since the specified date
            comics: Return only stories which are part of the specified comics
            series: Return only stories which are part of the specified series
            events: Return only stories which are part of the specified events
            creators: Return only stories which feature work by the specified creators
            order_by: Order the result set by a field or set of fields

        Returns:
            StoryListResponse containing list of stories and metadata

        Raises:
            MarvelAPIError: For any Marvel API related errors

        Example:
            >>> stories = await endpoint.get_stories(
            ...     character_id=1011334,
            ...     limit=10
            ... )
            >>> print(f"Found {stories.data.total} stories")
        """
        filters: Dict[str, Any] = {}

        if modified_since is not None:
            filters["modifiedSince"] = modified_since
        if comics is not None:
            filters["comics"] = ",".join(map(str, comics))
        if series is not None:
            filters["series"] = ",".join(map(str, series))
        if events is not None:
            filters["events"] = ",".join(map(str, events))
        if creators is not None:
            filters["creators"] = ",".join(map(str, creators))
        if order_by is not None:
            filters["orderBy"] = order_by

        return await self.get_related(
            "/v1/public/characters",
            character_id,
            "stories",
            StoryListResponse,
            limit=limit,
            offset=offset,
            **filters,
        )
