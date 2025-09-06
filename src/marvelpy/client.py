"""Enhanced Marvel API client with comprehensive endpoint integration."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .endpoints.characters import CharactersEndpoint
from .endpoints.comics import ComicsEndpoint
from .endpoints.creators import CreatorsEndpoint
from .endpoints.events import EventsEndpoint
from .endpoints.series import SeriesEndpoint
from .endpoints.stories import StoriesEndpoint

if TYPE_CHECKING:
    from .models.character import Character, CharacterListResponse
    from .models.comic import Comic, ComicListResponse
    from .models.creator import Creator, CreatorListResponse
    from .models.event import Event, EventListResponse
    from .models.series import Series, SeriesListResponse
    from .models.story import Story, StoryListResponse


class MarvelClient:
    """Enhanced Marvel API client with comprehensive endpoint integration.

    This client provides a unified interface to all Marvel API endpoints with
    type-safe methods, comprehensive filtering, and easy access to related resources.

    Args:
        public_key: Marvel API public key
        private_key: Marvel API private key
        base_url: Base URL for the Marvel API (defaults to official API)
        timeout: Request timeout in seconds (default: 30)
        max_retries: Maximum number of retry attempts (default: 3)

    Example:
        >>> import asyncio
        >>> from marvelpy import MarvelClient
        >>>
        >>> async def main():
        ...     async with MarvelClient("public_key", "private_key") as client:
        ...         # Get a character
        ...         character = await client.get_character(1009368)
        ...         print(f"Character: {character.name}")
        ...
        ...         # Get character's comics
        ...         comics = await client.get_character_comics(1009368, limit=5)
        ...         print(f"Character appears in {comics.data.total} comics")
        ...
        ...         # Search for characters
        ...         results = await client.search_characters("iron man", limit=10)
        ...         for char in results.data.results:
        ...             print(f"- {char.name}")
        >>>
        >>> asyncio.run(main())
    """

    BASE_URL = "https://gateway.marvel.com"

    def __init__(
        self,
        public_key: str,
        private_key: str,
        base_url: str | None = None,
        timeout: float = 30.0,
        max_retries: int = 3,
    ) -> None:
        """Initialize the Marvel API client.

        Args:
            public_key: Marvel API public key
            private_key: Marvel API private key
            base_url: Base URL for the Marvel API (defaults to official API)
            timeout: Request timeout in seconds (default: 30)
            max_retries: Maximum number of retry attempts (default: 3)
        """
        self.public_key = public_key
        self.private_key = private_key
        self.base_url = base_url or self.BASE_URL
        self.timeout = timeout
        self.max_retries = max_retries

        # Initialize endpoint classes
        self.characters = CharactersEndpoint(
            base_url=self.base_url,
            public_key=self.public_key,
            private_key=self.private_key,
            timeout=self.timeout,
            max_retries=self.max_retries,
        )
        self.comics = ComicsEndpoint(
            base_url=self.base_url,
            public_key=self.public_key,
            private_key=self.private_key,
            timeout=self.timeout,
            max_retries=self.max_retries,
        )
        self.events = EventsEndpoint(
            base_url=self.base_url,
            public_key=self.public_key,
            private_key=self.private_key,
            timeout=self.timeout,
            max_retries=self.max_retries,
        )
        self.series = SeriesEndpoint(
            base_url=self.base_url,
            public_key=self.public_key,
            private_key=self.private_key,
            timeout=self.timeout,
            max_retries=self.max_retries,
        )
        self.stories = StoriesEndpoint(
            base_url=self.base_url,
            public_key=self.public_key,
            private_key=self.private_key,
            timeout=self.timeout,
            max_retries=self.max_retries,
        )
        self.creators = CreatorsEndpoint(
            base_url=self.base_url,
            public_key=self.public_key,
            private_key=self.private_key,
            timeout=self.timeout,
            max_retries=self.max_retries,
        )

    async def __aenter__(self) -> MarvelClient:
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        await self.close()

    async def close(self) -> None:
        """Close the client.

        Note: The endpoint classes use httpx.AsyncClient in context managers
        for each request, so there are no persistent clients to close.
        This method is provided for compatibility with async context managers.
        """
        pass

    # ============================================================================
    # CHARACTER METHODS
    # ============================================================================

    async def get_character(self, character_id: int) -> Character:
        """Get a single character by ID.

        Args:
            character_id: The unique identifier for the character

        Returns:
            Character object containing character data

        Example:
            >>> character = await client.get_character(1009368)
            >>> print(f"Character: {character.name}")
        """
        return await self.characters.get_character(character_id)

    async def list_characters(
        self,
        limit: int | None = None,
        offset: int | None = None,
        name: str | None = None,
        name_starts_with: str | None = None,
        modified_since: str | None = None,
        comics: list[int] | None = None,
        series: list[int] | None = None,
        events: list[int] | None = None,
        stories: list[int] | None = None,
        order_by: str | None = None,
    ) -> CharacterListResponse:
        """List characters with optional filtering.

        Args:
            limit: Limit the number of results returned
            offset: Skip the specified number of results
            name: Return only characters matching the specified name
            name_starts_with: Return characters with names that begin with the specified string
            modified_since: Return only characters which have been modified since the specified date
            comics: Return only characters which appear in the specified comics
            series: Return only characters which appear the specified series
            events: Return only characters which appear in the specified events
            stories: Return only characters which appear the specified stories
            order_by: Order the result set by a field or set of fields

        Returns:
            CharacterListResponse containing the list of characters

        Example:
            >>> characters = await client.list_characters(name_starts_with="Spider", limit=10)
            >>> print(f"Found {characters.data.total} characters")
        """
        return await self.characters.list_characters(
            limit=limit,
            offset=offset,
            name=name,
            name_starts_with=name_starts_with,
            modified_since=modified_since,
            comics=comics,
            series=series,
            events=events,
            stories=stories,
            order_by=order_by,
        )

    async def search_characters(
        self,
        query: str,
        limit: int | None = None,
        offset: int | None = None,
    ) -> CharacterListResponse:
        """Search for characters by name.

        Args:
            query: Search query (character name)
            limit: Limit the number of results returned
            offset: Skip the specified number of results

        Returns:
            CharacterListResponse containing matching characters

        Example:
            >>> results = await client.search_characters("iron man", limit=5)
            >>> for char in results.data.results:
            ...     print(f"- {char.name}")
        """
        return await self.characters.list_characters(
            name_starts_with=query,
            limit=limit,
            offset=offset,
        )

    # Character related resources
    async def get_character_comics(
        self,
        character_id: int,
        limit: int | None = None,
        offset: int | None = None,
        format: str | None = None,
        format_type: str | None = None,
        no_variants: bool | None = None,
        date_descriptor: str | None = None,
        date_range: list[int] | None = None,
        diamond_code: str | None = None,
        digital_id: int | None = None,
        upc: str | None = None,
        isbn: str | None = None,
        ean: str | None = None,
        issn: str | None = None,
        has_digital_issue: bool | None = None,
        modified_since: str | None = None,
        creators: list[int] | None = None,
        series: list[int] | None = None,
        events: list[int] | None = None,
        stories: list[int] | None = None,
        shared_appearances: list[int] | None = None,
        collaborators: list[int] | None = None,
        order_by: str | None = None,
    ) -> ComicListResponse:
        """Get comics featuring a specific character.

        Args:
            character_id: The character ID
            limit: Limit the number of results returned
            offset: Skip the specified number of results
            format: Filter by the issue format
            format_type: Filter by the issue format type
            no_variants: Exclude variant comics
            date_descriptor: Return comics within a specified date range
            date_range: Return comics within a specified date range
            diamond_code: Filter by diamond code
            digital_id: Filter by digital comic ID
            upc: Filter by UPC
            isbn: Filter by ISBN
            ean: Filter by EAN
            issn: Filter by ISSN
            has_digital_issue: Filter by digital availability
            modified_since: Return only comics modified since the specified date
            creators: Return only comics which feature work by the specified creators
            series: Return only comics which are part of the specified series
            events: Return only comics which take place during the specified events
            stories: Return only comics which contain the specified stories
            shared_appearances: Return only comics in which the specified characters appear together
            collaborators: Return only comics in which the specified creators worked together
            order_by: Order the result set by a field or set of fields

        Returns:
            ComicListResponse containing the character's comics

        Example:
            >>> comics = await client.get_character_comics(1009368, limit=5)
            >>> print(f"Character appears in {comics.data.total} comics")
        """
        return await self.characters.get_comics(
            character_id=character_id,
            limit=limit,
            offset=offset,
            format=format,
            format_type=format_type,
            no_variants=no_variants,
            date_descriptor=date_descriptor,
            date_range=date_range,
            diamond_code=diamond_code,
            digital_id=digital_id,
            upc=upc,
            isbn=isbn,
            ean=ean,
            issn=issn,
            has_digital_issue=has_digital_issue,
            modified_since=modified_since,
            creators=creators,
            series=series,
            events=events,
            stories=stories,
            shared_appearances=shared_appearances,
            collaborators=collaborators,
            order_by=order_by,
        )

    async def get_character_events(
        self,
        character_id: int,
        limit: int | None = None,
        offset: int | None = None,
        name: str | None = None,
        name_starts_with: str | None = None,
        modified_since: str | None = None,
        creators: list[int] | None = None,
        series: list[int] | None = None,
        comics: list[int] | None = None,
        stories: list[int] | None = None,
        order_by: str | None = None,
    ) -> EventListResponse:
        """Get events featuring a specific character.

        Args:
            character_id: The character ID
            limit: Limit the number of results returned
            offset: Skip the specified number of results
            name: Return only events matching the specified name
            name_starts_with: Return events with names that begin with the specified string
            modified_since: Return only events which have been modified since the specified date
            creators: Return only events which feature work by the specified creators
            series: Return only events which are part of the specified series
            comics: Return only events which take place in the specified comics
            stories: Return only events which contain the specified stories
            order_by: Order the result set by a field or set of fields

        Returns:
            EventListResponse containing the character's events

        Example:
            >>> events = await client.get_character_events(1009368, limit=3)
            >>> print(f"Character appears in {events.data.total} events")
        """
        return await self.characters.get_events(
            character_id=character_id,
            limit=limit,
            offset=offset,
            name=name,
            name_starts_with=name_starts_with,
            modified_since=modified_since,
            creators=creators,
            series=series,
            comics=comics,
            stories=stories,
            order_by=order_by,
        )

    async def get_character_series(
        self,
        character_id: int,
        limit: int | None = None,
        offset: int | None = None,
        title: str | None = None,
        title_starts_with: str | None = None,
        start_year: int | None = None,
        modified_since: str | None = None,
        comics: list[int] | None = None,
        stories: list[int] | None = None,
        events: list[int] | None = None,
        creators: list[int] | None = None,
        series_type: str | None = None,
        contains: str | None = None,
        order_by: str | None = None,
    ) -> SeriesListResponse:
        """Get series featuring a specific character.

        Args:
            character_id: The character ID
            limit: Limit the number of results returned
            offset: Skip the specified number of results
            title: Return only series matching the specified title
            title_starts_with: Return series with titles that begin with the specified string
            start_year: Return only series which started in the specified year
            modified_since: Return only series which have been modified since the specified date
            comics: Return only series which contain the specified comics
            stories: Return only series which contain the specified stories
            events: Return only series which are part of the specified events
            creators: Return only series which feature work by the specified creators
            series_type: Filter the series by publication frequency type
            contains: Return only series containing one or more comics with the specified format
            order_by: Order the result set by a field or set of fields

        Returns:
            SeriesListResponse containing the character's series

        Example:
            >>> series = await client.get_character_series(1009368, limit=5)
            >>> print(f"Character appears in {series.data.total} series")
        """
        return await self.characters.get_series(
            character_id=character_id,
            limit=limit,
            offset=offset,
            title=title,
            title_starts_with=title_starts_with,
            start_year=start_year,
            modified_since=modified_since,
            comics=comics,
            stories=stories,
            events=events,
            creators=creators,
            series_type=series_type,
            contains=contains,
            order_by=order_by,
        )

    async def get_character_stories(
        self,
        character_id: int,
        limit: int | None = None,
        offset: int | None = None,
        modified_since: str | None = None,
        comics: list[int] | None = None,
        series: list[int] | None = None,
        events: list[int] | None = None,
        creators: list[int] | None = None,
        order_by: str | None = None,
    ) -> StoryListResponse:
        """Get stories featuring a specific character.

        Args:
            character_id: The character ID
            limit: Limit the number of results returned
            offset: Skip the specified number of results
            modified_since: Return only stories which have been modified since the specified date
            comics: Return only stories contained in the specified comics
            series: Return only stories contained the specified series
            events: Return only stories which take place during the specified events
            creators: Return only stories which feature work by the specified creators
            order_by: Order the result set by a field or set of fields

        Returns:
            StoryListResponse containing the character's stories

        Example:
            >>> stories = await client.get_character_stories(1009368, limit=5)
            >>> print(f"Character appears in {stories.data.total} stories")
        """
        return await self.characters.get_stories(
            character_id=character_id,
            limit=limit,
            offset=offset,
            modified_since=modified_since,
            comics=comics,
            series=series,
            events=events,
            creators=creators,
            order_by=order_by,
        )

    async def get_character_creators(
        self,
        character_id: int,
        limit: int | None = None,
        offset: int | None = None,
        modified_since: str | None = None,
        comics: list[int] | None = None,
        series: list[int] | None = None,
        events: list[int] | None = None,
        stories: list[int] | None = None,
        order_by: str | None = None,
    ) -> CreatorListResponse:
        """Get creators who have worked on a specific character.

        Args:
            character_id: The character ID
            limit: Limit the number of results returned
            offset: Skip the specified number of results
            modified_since: Return only creators which have been modified since the specified date
            comics: Return only creators who have worked on comics in the specified list
            series: Return only creators who have worked on series in the specified list
            events: Return only creators who have worked on comics in the specified events
            stories: Return only creators who have worked on comics in the specified stories
            order_by: Order the result set by a field or set of fields

        Returns:
            CreatorListResponse containing the character's creators

        Example:
            >>> creators = await client.get_character_creators(1009368, limit=5)
            >>> print(f"Character has {creators.data.total} creators")
        """
        return await self.characters.get_creators(
            character_id=character_id,
            limit=limit,
            offset=offset,
            modified_since=modified_since,
            comics=comics,
            series=series,
            events=events,
            stories=stories,
            order_by=order_by,
        )

    # ============================================================================
    # COMIC METHODS
    # ============================================================================

    async def get_comic(self, comic_id: int) -> Comic:
        """Get a single comic by ID.

        Args:
            comic_id: The unique identifier for the comic

        Returns:
            Comic object containing comic data

        Example:
            >>> comic = await client.get_comic(21366)
            >>> print(f"Comic: {comic.title}")
        """
        return await self.comics.get_comic(comic_id)

    async def list_comics(
        self,
        limit: int | None = None,
        offset: int | None = None,
        format: str | None = None,
        format_type: str | None = None,
        no_variants: bool | None = None,
        date_descriptor: str | None = None,
        date_range: list[int] | None = None,
        diamond_code: str | None = None,
        digital_id: int | None = None,
        upc: str | None = None,
        isbn: str | None = None,
        ean: str | None = None,
        issn: str | None = None,
        has_digital_issue: bool | None = None,
        modified_since: str | None = None,
        creators: list[int] | None = None,
        characters: list[int] | None = None,
        series: list[int] | None = None,
        events: list[int] | None = None,
        stories: list[int] | None = None,
        shared_appearances: list[int] | None = None,
        collaborators: list[int] | None = None,
        order_by: str | None = None,
    ) -> ComicListResponse:
        """List comics with optional filtering.

        Args:
            limit: Limit the number of results returned
            offset: Skip the specified number of results
            format: Filter by the issue format
            format_type: Filter by the issue format type
            no_variants: Exclude variant comics
            date_descriptor: Return comics within a specified date range
            date_range: Return comics within a specified date range
            diamond_code: Filter by diamond code
            digital_id: Filter by digital comic ID
            upc: Filter by UPC
            isbn: Filter by ISBN
            ean: Filter by EAN
            issn: Filter by ISSN
            has_digital_issue: Filter by digital availability
            modified_since: Return only comics modified since the specified date
            creators: Return only comics which feature work by the specified creators
            characters: Return only comics which feature the specified characters
            series: Return only comics which are part of the specified series
            events: Return only comics which take place during the specified events
            stories: Return only comics which contain the specified stories
            shared_appearances: Return only comics in which the specified characters appear together
            collaborators: Return only comics in which the specified creators worked together
            order_by: Order the result set by a field or set of fields

        Returns:
            ComicListResponse containing the list of comics

        Example:
            >>> comics = await client.list_comics(format="comic", limit=10)
            >>> print(f"Found {comics.data.total} comics")
        """
        return await self.comics.list_comics(
            limit=limit,
            offset=offset,
            format=format,
            format_type=format_type,
            no_variants=no_variants,
            date_descriptor=date_descriptor,
            date_range=date_range,
            diamond_code=diamond_code,
            digital_id=digital_id,
            upc=upc,
            isbn=isbn,
            ean=ean,
            issn=issn,
            has_digital_issue=has_digital_issue,
            modified_since=modified_since,
            creators=creators,
            characters=characters,
            series=series,
            events=events,
            stories=stories,
            shared_appearances=shared_appearances,
            collaborators=collaborators,
            order_by=order_by,
        )

    async def search_comics(
        self,
        title: str,
        limit: int | None = None,
        offset: int | None = None,
    ) -> ComicListResponse:
        """Search for comics by title.

        Args:
            title: Search query (comic title)
            limit: Limit the number of results returned
            offset: Skip the specified number of results

        Returns:
            ComicListResponse containing matching comics

        Example:
            >>> results = await client.search_comics("amazing spider-man", limit=5)
            >>> for comic in results.data.results:
            ...     print(f"- {comic.title}")
        """
        return await self.comics.list_comics(
            title_starts_with=title,
            limit=limit,
            offset=offset,
        )

    # Comic related resources
    async def get_comic_characters(
        self,
        comic_id: int,
        limit: int | None = None,
        offset: int | None = None,
        name: str | None = None,
        name_starts_with: str | None = None,
        modified_since: str | None = None,
        series: list[int] | None = None,
        events: list[int] | None = None,
        stories: list[int] | None = None,
        order_by: str | None = None,
    ) -> CharacterListResponse:
        """Get characters appearing in a specific comic.

        Args:
            comic_id: The comic ID
            limit: Limit the number of results returned
            offset: Skip the specified number of results
            name: Return only characters matching the specified name
            name_starts_with: Return characters with names that begin with the specified string
            modified_since: Return only characters which have been modified since the specified date
            series: Return only characters which appear the specified series
            events: Return only characters which appear in the specified events
            stories: Return only characters which appear the specified stories
            order_by: Order the result set by a field or set of fields

        Returns:
            CharacterListResponse containing the comic's characters

        Example:
            >>> characters = await client.get_comic_characters(21366, limit=5)
            >>> print(f"Comic features {characters.data.total} characters")
        """
        return await self.comics.get_characters(
            comic_id=comic_id,
            limit=limit,
            offset=offset,
            name=name,
            name_starts_with=name_starts_with,
            modified_since=modified_since,
            series=series,
            events=events,
            stories=stories,
            order_by=order_by,
        )

    async def get_comic_creators(
        self,
        comic_id: int,
        limit: int | None = None,
        offset: int | None = None,
        first_name: str | None = None,
        middle_name: str | None = None,
        last_name: str | None = None,
        suffix: str | None = None,
        name_starts_with: str | None = None,
        first_name_starts_with: str | None = None,
        middle_name_starts_with: str | None = None,
        last_name_starts_with: str | None = None,
        modified_since: str | None = None,
        comics: list[int] | None = None,
        series: list[int] | None = None,
        events: list[int] | None = None,
        stories: list[int] | None = None,
        order_by: str | None = None,
    ) -> CreatorListResponse:
        """Get creators who worked on a specific comic.

        Args:
            comic_id: The comic ID
            limit: Limit the number of results returned
            offset: Skip the specified number of results
            first_name: Filter by creator first name
            middle_name: Filter by creator middle name
            last_name: Filter by creator last name
            suffix: Filter by creator suffix
            name_starts_with: Filter by creator names that begin with the specified string
            first_name_starts_with: Filter by creator first names that begin with the specified string
            middle_name_starts_with: Filter by creator middle names that begin with the specified string
            last_name_starts_with: Filter by creator last names that begin with the specified string
            modified_since: Return only creators which have been modified since the specified date
            comics: Return only creators who have worked on comics in the specified list
            series: Return only creators who have worked on series in the specified list
            events: Return only creators who have worked on comics in the specified events
            stories: Return only creators who have worked on comics in the specified stories
            order_by: Order the result set by a field or set of fields

        Returns:
            CreatorListResponse containing the comic's creators

        Example:
            >>> creators = await client.get_comic_creators(21366, limit=5)
            >>> print(f"Comic has {creators.data.total} creators")
        """
        return await self.comics.get_creators(
            comic_id=comic_id,
            limit=limit,
            offset=offset,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            suffix=suffix,
            name_starts_with=name_starts_with,
            first_name_starts_with=first_name_starts_with,
            middle_name_starts_with=middle_name_starts_with,
            last_name_starts_with=last_name_starts_with,
            modified_since=modified_since,
            comics=comics,
            series=series,
            events=events,
            stories=stories,
            order_by=order_by,
        )

    async def get_comic_events(
        self,
        comic_id: int,
        limit: int | None = None,
        offset: int | None = None,
        name: str | None = None,
        name_starts_with: str | None = None,
        modified_since: str | None = None,
        creators: list[int] | None = None,
        characters: list[int] | None = None,
        series: list[int] | None = None,
        stories: list[int] | None = None,
        order_by: str | None = None,
    ) -> EventListResponse:
        """Get events featuring a specific comic.

        Args:
            comic_id: The comic ID
            limit: Limit the number of results returned
            offset: Skip the specified number of results
            name: Return only events matching the specified name
            name_starts_with: Return events with names that begin with the specified string
            modified_since: Return only events which have been modified since the specified date
            creators: Return only events which feature work by the specified creators
            characters: Return only events which feature the specified characters
            series: Return only events which are part of the specified series
            stories: Return only events which contain the specified stories
            order_by: Order the result set by a field or set of fields

        Returns:
            EventListResponse containing the comic's events

        Example:
            >>> events = await client.get_comic_events(21366, limit=3)
            >>> print(f"Comic appears in {events.data.total} events")
        """
        return await self.comics.get_events(
            comic_id=comic_id,
            limit=limit,
            offset=offset,
            name=name,
            name_starts_with=name_starts_with,
            modified_since=modified_since,
            creators=creators,
            characters=characters,
            series=series,
            stories=stories,
            order_by=order_by,
        )

    async def get_comic_stories(
        self,
        comic_id: int,
        limit: int | None = None,
        offset: int | None = None,
        modified_since: str | None = None,
        series: list[int] | None = None,
        events: list[int] | None = None,
        creators: list[int] | None = None,
        characters: list[int] | None = None,
        order_by: str | None = None,
    ) -> StoryListResponse:
        """Get stories contained in a specific comic.

        Args:
            comic_id: The comic ID
            limit: Limit the number of results returned
            offset: Skip the specified number of results
            modified_since: Return only stories which have been modified since the specified date
            series: Return only stories contained the specified series
            events: Return only stories which take place during the specified events
            creators: Return only stories which feature work by the specified creators
            characters: Return only stories which feature the specified characters
            order_by: Order the result set by a field or set of fields

        Returns:
            StoryListResponse containing the comic's stories

        Example:
            >>> stories = await client.get_comic_stories(21366, limit=5)
            >>> print(f"Comic contains {stories.data.total} stories")
        """
        return await self.comics.get_stories(
            comic_id=comic_id,
            limit=limit,
            offset=offset,
            modified_since=modified_since,
            series=series,
            events=events,
            creators=creators,
            characters=characters,
            order_by=order_by,
        )

    # ============================================================================
    # EVENT METHODS
    # ============================================================================

    async def get_event(self, event_id: int) -> Event:
        """Get a single event by ID.

        Args:
            event_id: The unique identifier for the event

        Returns:
            Event object containing event data

        Example:
            >>> event = await client.get_event(269)
            >>> print(f"Event: {event.title}")
        """
        return await self.events.get_event(event_id)

    async def list_events(
        self,
        limit: int | None = None,
        offset: int | None = None,
        name: str | None = None,
        name_starts_with: str | None = None,
        modified_since: str | None = None,
        creators: list[int] | None = None,
        characters: list[int] | None = None,
        series: list[int] | None = None,
        comics: list[int] | None = None,
        stories: list[int] | None = None,
        order_by: str | None = None,
    ) -> EventListResponse:
        """List events with optional filtering.

        Args:
            limit: Limit the number of results returned
            offset: Skip the specified number of results
            name: Return only events matching the specified name
            name_starts_with: Return events with names that begin with the specified string
            modified_since: Return only events which have been modified since the specified date
            creators: Return only events which feature work by the specified creators
            characters: Return only events which feature the specified characters
            series: Return only events which are part of the specified series
            comics: Return only events which take place in the specified comics
            stories: Return only events which contain the specified stories
            order_by: Order the result set by a field or set of fields

        Returns:
            EventListResponse containing the list of events

        Example:
            >>> events = await client.list_events(limit=10)
            >>> print(f"Found {events.data.total} events")
        """
        return await self.events.list_events(
            limit=limit,
            offset=offset,
            name=name,
            name_starts_with=name_starts_with,
            modified_since=modified_since,
            creators=creators,
            characters=characters,
            series=series,
            comics=comics,
            stories=stories,
            order_by=order_by,
        )

    async def search_events(
        self,
        query: str,
        limit: int | None = None,
        offset: int | None = None,
    ) -> EventListResponse:
        """Search for events by name.

        Args:
            query: Search query (event name)
            limit: Limit the number of results returned
            offset: Skip the specified number of results

        Returns:
            EventListResponse containing matching events

        Example:
            >>> results = await client.search_events("secret invasion", limit=5)
            >>> for event in results.data.results:
            ...     print(f"- {event.title}")
        """
        return await self.events.list_events(
            name_starts_with=query,
            limit=limit,
            offset=offset,
        )

    # Event related resources
    async def get_event_characters(
        self,
        event_id: int,
        limit: int | None = None,
        offset: int | None = None,
        name: str | None = None,
        name_starts_with: str | None = None,
        modified_since: str | None = None,
        comics: list[int] | None = None,
        series: list[int] | None = None,
        stories: list[int] | None = None,
        order_by: str | None = None,
    ) -> CharacterListResponse:
        """Get characters appearing in a specific event.

        Args:
            event_id: The event ID
            limit: Limit the number of results returned
            offset: Skip the specified number of results
            name: Return only characters matching the specified name
            name_starts_with: Return characters with names that begin with the specified string
            modified_since: Return only characters which have been modified since the specified date
            comics: Return only characters which appear in the specified comics
            series: Return only characters which appear the specified series
            stories: Return only characters which appear the specified stories
            order_by: Order the result set by a field or set of fields

        Returns:
            CharacterListResponse containing the event's characters

        Example:
            >>> characters = await client.get_event_characters(269, limit=5)
            >>> print(f"Event features {characters.data.total} characters")
        """
        return await self.events.get_characters(
            event_id=event_id,
            limit=limit,
            offset=offset,
            name=name,
            name_starts_with=name_starts_with,
            modified_since=modified_since,
            comics=comics,
            series=series,
            stories=stories,
            order_by=order_by,
        )

    async def get_event_comics(
        self,
        event_id: int,
        limit: int | None = None,
        offset: int | None = None,
        format: str | None = None,
        format_type: str | None = None,
        no_variants: bool | None = None,
        date_descriptor: str | None = None,
        date_range: list[int] | None = None,
        diamond_code: str | None = None,
        digital_id: int | None = None,
        upc: str | None = None,
        isbn: str | None = None,
        ean: str | None = None,
        issn: str | None = None,
        has_digital_issue: bool | None = None,
        modified_since: str | None = None,
        creators: list[int] | None = None,
        characters: list[int] | None = None,
        series: list[int] | None = None,
        stories: list[int] | None = None,
        shared_appearances: list[int] | None = None,
        collaborators: list[int] | None = None,
        order_by: str | None = None,
    ) -> ComicListResponse:
        """Get comics featuring a specific event.

        Args:
            event_id: The event ID
            limit: Limit the number of results returned
            offset: Skip the specified number of results
            format: Filter by the issue format
            format_type: Filter by the issue format type
            no_variants: Exclude variant comics
            date_descriptor: Return comics within a specified date range
            date_range: Return comics within a specified date range
            diamond_code: Filter by diamond code
            digital_id: Filter by digital comic ID
            upc: Filter by UPC
            isbn: Filter by ISBN
            ean: Filter by EAN
            issn: Filter by ISSN
            has_digital_issue: Filter by digital availability
            modified_since: Return only comics modified since the specified date
            creators: Return only comics which feature work by the specified creators
            characters: Return only comics which feature the specified characters
            series: Return only comics which are part of the specified series
            stories: Return only comics which contain the specified stories
            shared_appearances: Return only comics in which the specified characters appear together
            collaborators: Return only comics in which the specified creators worked together
            order_by: Order the result set by a field or set of fields

        Returns:
            ComicListResponse containing the event's comics

        Example:
            >>> comics = await client.get_event_comics(269, limit=5)
            >>> print(f"Event has {comics.data.total} comics")
        """
        return await self.events.get_comics(
            event_id=event_id,
            limit=limit,
            offset=offset,
            format=format,
            format_type=format_type,
            no_variants=no_variants,
            date_descriptor=date_descriptor,
            date_range=date_range,
            diamond_code=diamond_code,
            digital_id=digital_id,
            upc=upc,
            isbn=isbn,
            ean=ean,
            issn=issn,
            has_digital_issue=has_digital_issue,
            modified_since=modified_since,
            creators=creators,
            characters=characters,
            series=series,
            stories=stories,
            shared_appearances=shared_appearances,
            collaborators=collaborators,
            order_by=order_by,
        )

    async def get_event_creators(
        self,
        event_id: int,
        limit: int | None = None,
        offset: int | None = None,
        first_name: str | None = None,
        middle_name: str | None = None,
        last_name: str | None = None,
        suffix: str | None = None,
        name_starts_with: str | None = None,
        first_name_starts_with: str | None = None,
        middle_name_starts_with: str | None = None,
        last_name_starts_with: str | None = None,
        modified_since: str | None = None,
        comics: list[int] | None = None,
        series: list[int] | None = None,
        stories: list[int] | None = None,
        order_by: str | None = None,
    ) -> CreatorListResponse:
        """Get creators who worked on a specific event.

        Args:
            event_id: The event ID
            limit: Limit the number of results returned
            offset: Skip the specified number of results
            first_name: Filter by creator first name
            middle_name: Filter by creator middle name
            last_name: Filter by creator last name
            suffix: Filter by creator suffix
            name_starts_with: Filter by creator names that begin with the specified string
            first_name_starts_with: Filter by creator first names that begin with the specified string
            middle_name_starts_with: Filter by creator middle names that begin with the specified string
            last_name_starts_with: Filter by creator last names that begin with the specified string
            modified_since: Return only creators which have been modified since the specified date
            comics: Return only creators who have worked on comics in the specified list
            series: Return only creators who have worked on series in the specified list
            stories: Return only creators who have worked on comics in the specified stories
            order_by: Order the result set by a field or set of fields

        Returns:
            CreatorListResponse containing the event's creators

        Example:
            >>> creators = await client.get_event_creators(269, limit=5)
            >>> print(f"Event has {creators.data.total} creators")
        """
        return await self.events.get_creators(
            event_id=event_id,
            limit=limit,
            offset=offset,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            suffix=suffix,
            name_starts_with=name_starts_with,
            first_name_starts_with=first_name_starts_with,
            middle_name_starts_with=middle_name_starts_with,
            last_name_starts_with=last_name_starts_with,
            modified_since=modified_since,
            comics=comics,
            series=series,
            stories=stories,
            order_by=order_by,
        )

    async def get_event_series(
        self,
        event_id: int,
        limit: int | None = None,
        offset: int | None = None,
        title: str | None = None,
        title_starts_with: str | None = None,
        start_year: int | None = None,
        modified_since: str | None = None,
        comics: list[int] | None = None,
        stories: list[int] | None = None,
        creators: list[int] | None = None,
        characters: list[int] | None = None,
        series_type: str | None = None,
        contains: str | None = None,
        order_by: str | None = None,
    ) -> SeriesListResponse:
        """Get series featuring a specific event.

        Args:
            event_id: The event ID
            limit: Limit the number of results returned
            offset: Skip the specified number of results
            title: Return only series matching the specified title
            title_starts_with: Return series with titles that begin with the specified string
            start_year: Return only series which started in the specified year
            modified_since: Return only series which have been modified since the specified date
            comics: Return only series which contain the specified comics
            stories: Return only series which contain the specified stories
            creators: Return only series which feature work by the specified creators
            characters: Return only series which feature the specified characters
            series_type: Filter the series by publication frequency type
            contains: Return only series containing one or more comics with the specified format
            order_by: Order the result set by a field or set of fields

        Returns:
            SeriesListResponse containing the event's series

        Example:
            >>> series = await client.get_event_series(269, limit=5)
            >>> print(f"Event has {series.data.total} series")
        """
        return await self.events.get_series(
            event_id=event_id,
            limit=limit,
            offset=offset,
            title=title,
            title_starts_with=title_starts_with,
            start_year=start_year,
            modified_since=modified_since,
            comics=comics,
            stories=stories,
            creators=creators,
            characters=characters,
            series_type=series_type,
            contains=contains,
            order_by=order_by,
        )

    async def get_event_stories(
        self,
        event_id: int,
        limit: int | None = None,
        offset: int | None = None,
        modified_since: str | None = None,
        comics: list[int] | None = None,
        series: list[int] | None = None,
        creators: list[int] | None = None,
        characters: list[int] | None = None,
        order_by: str | None = None,
    ) -> StoryListResponse:
        """Get stories featuring a specific event.

        Args:
            event_id: The event ID
            limit: Limit the number of results returned
            offset: Skip the specified number of results
            modified_since: Return only stories which have been modified since the specified date
            comics: Return only stories contained in the specified comics
            series: Return only stories contained the specified series
            creators: Return only stories which feature work by the specified creators
            characters: Return only stories which feature the specified characters
            order_by: Order the result set by a field or set of fields

        Returns:
            StoryListResponse containing the event's stories

        Example:
            >>> stories = await client.get_event_stories(269, limit=5)
            >>> print(f"Event has {stories.data.total} stories")
        """
        return await self.events.get_stories(
            event_id=event_id,
            limit=limit,
            offset=offset,
            modified_since=modified_since,
            comics=comics,
            series=series,
            creators=creators,
            characters=characters,
            order_by=order_by,
        )

    # ============================================================================
    # SERIES METHODS
    # ============================================================================

    async def get_series(self, series_id: int) -> Series:
        """Get a single series by ID.

        Args:
            series_id: The unique identifier for the series

        Returns:
            Series object containing series data

        Example:
            >>> series = await client.get_series(1991)
            >>> print(f"Series: {series.title}")
        """
        return await self.series.get_series(series_id)

    async def list_series(
        self,
        limit: int | None = None,
        offset: int | None = None,
        title: str | None = None,
        title_starts_with: str | None = None,
        start_year: int | None = None,
        modified_since: str | None = None,
        comics: list[int] | None = None,
        stories: list[int] | None = None,
        events: list[int] | None = None,
        creators: list[int] | None = None,
        characters: list[int] | None = None,
        series_type: str | None = None,
        contains: str | None = None,
        order_by: str | None = None,
    ) -> SeriesListResponse:
        """List series with optional filtering.

        Args:
            limit: Limit the number of results returned
            offset: Skip the specified number of results
            title: Return only series matching the specified title
            title_starts_with: Return series with titles that begin with the specified string
            start_year: Return only series which started in the specified year
            modified_since: Return only series which have been modified since the specified date
            comics: Return only series which contain the specified comics
            stories: Return only series which contain the specified stories
            events: Return only series which are part of the specified events
            creators: Return only series which feature work by the specified creators
            characters: Return only series which feature the specified characters
            series_type: Filter the series by publication frequency type
            contains: Return only series containing one or more comics with the specified format
            order_by: Order the result set by a field or set of fields

        Returns:
            SeriesListResponse containing the list of series

        Example:
            >>> series = await client.list_series(title_starts_with="Amazing Spider-Man", limit=10)
            >>> print(f"Found {series.data.total} series")
        """
        return await self.series.list_series(
            limit=limit,
            offset=offset,
            title=title,
            title_starts_with=title_starts_with,
            start_year=start_year,
            modified_since=modified_since,
            comics=comics,
            stories=stories,
            events=events,
            creators=creators,
            characters=characters,
            series_type=series_type,
            contains=contains,
            order_by=order_by,
        )

    async def search_series(
        self,
        query: str,
        limit: int | None = None,
        offset: int | None = None,
    ) -> SeriesListResponse:
        """Search for series by title.

        Args:
            query: Search query (series title)
            limit: Limit the number of results returned
            offset: Skip the specified number of results

        Returns:
            SeriesListResponse containing matching series

        Example:
            >>> results = await client.search_series("amazing spider-man", limit=5)
            >>> for series in results.data.results:
            ...     print(f"- {series.title}")
        """
        return await self.series.list_series(
            title_starts_with=query,
            limit=limit,
            offset=offset,
        )

    # Series related resources
    async def get_series_characters(
        self,
        series_id: int,
        limit: int | None = None,
        offset: int | None = None,
        name: str | None = None,
        name_starts_with: str | None = None,
        modified_since: str | None = None,
        comics: list[int] | None = None,
        events: list[int] | None = None,
        stories: list[int] | None = None,
        order_by: str | None = None,
    ) -> CharacterListResponse:
        """Get characters appearing in a specific series.

        Args:
            series_id: The series ID
            limit: Limit the number of results returned
            offset: Skip the specified number of results
            name: Return only characters matching the specified name
            name_starts_with: Return characters with names that begin with the specified string
            modified_since: Return only characters which have been modified since the specified date
            comics: Return only characters which appear in the specified comics
            events: Return only characters which appear in the specified events
            stories: Return only characters which appear the specified stories
            order_by: Order the result set by a field or set of fields

        Returns:
            CharacterListResponse containing the series' characters

        Example:
            >>> characters = await client.get_series_characters(1991, limit=5)
            >>> print(f"Series features {characters.data.total} characters")
        """
        return await self.series.get_characters(
            series_id=series_id,
            limit=limit,
            offset=offset,
            name=name,
            name_starts_with=name_starts_with,
            modified_since=modified_since,
            comics=comics,
            events=events,
            stories=stories,
            order_by=order_by,
        )

    async def get_series_comics(
        self,
        series_id: int,
        limit: int | None = None,
        offset: int | None = None,
        format: str | None = None,
        format_type: str | None = None,
        no_variants: bool | None = None,
        date_descriptor: str | None = None,
        date_range: list[int] | None = None,
        diamond_code: str | None = None,
        digital_id: int | None = None,
        upc: str | None = None,
        isbn: str | None = None,
        ean: str | None = None,
        issn: str | None = None,
        has_digital_issue: bool | None = None,
        modified_since: str | None = None,
        creators: list[int] | None = None,
        characters: list[int] | None = None,
        events: list[int] | None = None,
        stories: list[int] | None = None,
        shared_appearances: list[int] | None = None,
        collaborators: list[int] | None = None,
        order_by: str | None = None,
    ) -> ComicListResponse:
        """Get comics in a specific series.

        Args:
            series_id: The series ID
            limit: Limit the number of results returned
            offset: Skip the specified number of results
            format: Filter by the issue format
            format_type: Filter by the issue format type
            no_variants: Exclude variant comics
            date_descriptor: Return comics within a specified date range
            date_range: Return comics within a specified date range
            diamond_code: Filter by diamond code
            digital_id: Filter by digital comic ID
            upc: Filter by UPC
            isbn: Filter by ISBN
            ean: Filter by EAN
            issn: Filter by ISSN
            has_digital_issue: Filter by digital availability
            modified_since: Return only comics modified since the specified date
            creators: Return only comics which feature work by the specified creators
            characters: Return only comics which feature the specified characters
            events: Return only comics which take place during the specified events
            stories: Return only comics which contain the specified stories
            shared_appearances: Return only comics in which the specified characters appear together
            collaborators: Return only comics in which the specified creators worked together
            order_by: Order the result set by a field or set of fields

        Returns:
            ComicListResponse containing the series' comics

        Example:
            >>> comics = await client.get_series_comics(1991, limit=5)
            >>> print(f"Series has {comics.data.total} comics")
        """
        return await self.series.get_comics(
            series_id=series_id,
            limit=limit,
            offset=offset,
            format=format,
            format_type=format_type,
            no_variants=no_variants,
            date_descriptor=date_descriptor,
            date_range=date_range,
            diamond_code=diamond_code,
            digital_id=digital_id,
            upc=upc,
            isbn=isbn,
            ean=ean,
            issn=issn,
            has_digital_issue=has_digital_issue,
            modified_since=modified_since,
            creators=creators,
            characters=characters,
            events=events,
            stories=stories,
            shared_appearances=shared_appearances,
            collaborators=collaborators,
            order_by=order_by,
        )

    async def get_series_creators(
        self,
        series_id: int,
        limit: int | None = None,
        offset: int | None = None,
        first_name: str | None = None,
        middle_name: str | None = None,
        last_name: str | None = None,
        suffix: str | None = None,
        name_starts_with: str | None = None,
        first_name_starts_with: str | None = None,
        middle_name_starts_with: str | None = None,
        last_name_starts_with: str | None = None,
        modified_since: str | None = None,
        comics: list[int] | None = None,
        events: list[int] | None = None,
        stories: list[int] | None = None,
        order_by: str | None = None,
    ) -> CreatorListResponse:
        """Get creators who worked on a specific series.

        Args:
            series_id: The series ID
            limit: Limit the number of results returned
            offset: Skip the specified number of results
            first_name: Filter by creator first name
            middle_name: Filter by creator middle name
            last_name: Filter by creator last name
            suffix: Filter by creator suffix
            name_starts_with: Filter by creator names that begin with the specified string
            first_name_starts_with: Filter by creator first names that begin with the specified string
            middle_name_starts_with: Filter by creator middle names that begin with the specified string
            last_name_starts_with: Filter by creator last names that begin with the specified string
            modified_since: Return only creators which have been modified since the specified date
            comics: Return only creators who have worked on comics in the specified list
            events: Return only creators who have worked on comics in the specified events
            stories: Return only creators who have worked on comics in the specified stories
            order_by: Order the result set by a field or set of fields

        Returns:
            CreatorListResponse containing the series' creators

        Example:
            >>> creators = await client.get_series_creators(1991, limit=5)
            >>> print(f"Series has {creators.data.total} creators")
        """
        return await self.series.get_creators(
            series_id=series_id,
            limit=limit,
            offset=offset,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            suffix=suffix,
            name_starts_with=name_starts_with,
            first_name_starts_with=first_name_starts_with,
            middle_name_starts_with=middle_name_starts_with,
            last_name_starts_with=last_name_starts_with,
            modified_since=modified_since,
            comics=comics,
            events=events,
            stories=stories,
            order_by=order_by,
        )

    async def get_series_events(
        self,
        series_id: int,
        limit: int | None = None,
        offset: int | None = None,
        name: str | None = None,
        name_starts_with: str | None = None,
        modified_since: str | None = None,
        creators: list[int] | None = None,
        characters: list[int] | None = None,
        comics: list[int] | None = None,
        stories: list[int] | None = None,
        order_by: str | None = None,
    ) -> EventListResponse:
        """Get events featuring a specific series.

        Args:
            series_id: The series ID
            limit: Limit the number of results returned
            offset: Skip the specified number of results
            name: Return only events matching the specified name
            name_starts_with: Return events with names that begin with the specified string
            modified_since: Return only events which have been modified since the specified date
            creators: Return only events which feature work by the specified creators
            characters: Return only events which feature the specified characters
            comics: Return only events which take place in the specified comics
            stories: Return only events which contain the specified stories
            order_by: Order the result set by a field or set of fields

        Returns:
            EventListResponse containing the series' events

        Example:
            >>> events = await client.get_series_events(1991, limit=3)
            >>> print(f"Series appears in {events.data.total} events")
        """
        return await self.series.get_events(
            series_id=series_id,
            limit=limit,
            offset=offset,
            name=name,
            name_starts_with=name_starts_with,
            modified_since=modified_since,
            creators=creators,
            characters=characters,
            comics=comics,
            stories=stories,
            order_by=order_by,
        )

    async def get_series_stories(
        self,
        series_id: int,
        limit: int | None = None,
        offset: int | None = None,
        modified_since: str | None = None,
        comics: list[int] | None = None,
        events: list[int] | None = None,
        creators: list[int] | None = None,
        characters: list[int] | None = None,
        order_by: str | None = None,
    ) -> StoryListResponse:
        """Get stories in a specific series.

        Args:
            series_id: The series ID
            limit: Limit the number of results returned
            offset: Skip the specified number of results
            modified_since: Return only stories which have been modified since the specified date
            comics: Return only stories contained in the specified comics
            events: Return only stories which take place during the specified events
            creators: Return only stories which feature work by the specified creators
            characters: Return only stories which feature the specified characters
            order_by: Order the result set by a field or set of fields

        Returns:
            StoryListResponse containing the series' stories

        Example:
            >>> stories = await client.get_series_stories(1991, limit=5)
            >>> print(f"Series contains {stories.data.total} stories")
        """
        return await self.series.get_stories(
            series_id=series_id,
            limit=limit,
            offset=offset,
            modified_since=modified_since,
            comics=comics,
            events=events,
            creators=creators,
            characters=characters,
            order_by=order_by,
        )

    # ============================================================================
    # STORY METHODS
    # ============================================================================

    async def get_story(self, story_id: int) -> Story:
        """Get a single story by ID.

        Args:
            story_id: The unique identifier for the story

        Returns:
            Story object containing story data

        Example:
            >>> story = await client.get_story(12345)
            >>> print(f"Story: {story.title}")
        """
        return await self.stories.get_story(story_id)

    async def list_stories(
        self,
        limit: int | None = None,
        offset: int | None = None,
        modified_since: str | None = None,
        comics: list[int] | None = None,
        series: list[int] | None = None,
        events: list[int] | None = None,
        creators: list[int] | None = None,
        characters: list[int] | None = None,
        order_by: str | None = None,
    ) -> StoryListResponse:
        """List stories with optional filtering.

        Args:
            limit: Limit the number of results returned
            offset: Skip the specified number of results
            modified_since: Return only stories which have been modified since the specified date
            comics: Return only stories contained in the specified comics
            series: Return only stories contained the specified series
            events: Return only stories which take place during the specified events
            creators: Return only stories which feature work by the specified creators
            characters: Return only stories which feature the specified characters
            order_by: Order the result set by a field or set of fields

        Returns:
            StoryListResponse containing the list of stories

        Example:
            >>> stories = await client.list_stories(limit=10)
            >>> print(f"Found {stories.data.total} stories")
        """
        return await self.stories.list_stories(
            limit=limit,
            offset=offset,
            modified_since=modified_since,
            comics=comics,
            series=series,
            events=events,
            creators=creators,
            characters=characters,
            order_by=order_by,
        )

    # Story related resources
    async def get_story_characters(
        self,
        story_id: int,
        limit: int | None = None,
        offset: int | None = None,
        name: str | None = None,
        name_starts_with: str | None = None,
        modified_since: str | None = None,
        comics: list[int] | None = None,
        series: list[int] | None = None,
        events: list[int] | None = None,
        order_by: str | None = None,
    ) -> CharacterListResponse:
        """Get characters appearing in a specific story.

        Args:
            story_id: The story ID
            limit: Limit the number of results returned
            offset: Skip the specified number of results
            name: Return only characters matching the specified name
            name_starts_with: Return characters with names that begin with the specified string
            modified_since: Return only characters which have been modified since the specified date
            comics: Return only characters which appear in the specified comics
            series: Return only characters which appear the specified series
            events: Return only characters which appear in the specified events
            order_by: Order the result set by a field or set of fields

        Returns:
            CharacterListResponse containing the story's characters

        Example:
            >>> characters = await client.get_story_characters(12345, limit=5)
            >>> print(f"Story features {characters.data.total} characters")
        """
        return await self.stories.get_characters(
            story_id=story_id,
            limit=limit,
            offset=offset,
            name=name,
            name_starts_with=name_starts_with,
            modified_since=modified_since,
            comics=comics,
            series=series,
            events=events,
            order_by=order_by,
        )

    async def get_story_comics(
        self,
        story_id: int,
        limit: int | None = None,
        offset: int | None = None,
        format: str | None = None,
        format_type: str | None = None,
        no_variants: bool | None = None,
        date_descriptor: str | None = None,
        date_range: list[int] | None = None,
        diamond_code: str | None = None,
        digital_id: int | None = None,
        upc: str | None = None,
        isbn: str | None = None,
        ean: str | None = None,
        issn: str | None = None,
        has_digital_issue: bool | None = None,
        modified_since: str | None = None,
        creators: list[int] | None = None,
        characters: list[int] | None = None,
        series: list[int] | None = None,
        events: list[int] | None = None,
        shared_appearances: list[int] | None = None,
        collaborators: list[int] | None = None,
        order_by: str | None = None,
    ) -> ComicListResponse:
        """Get comics containing a specific story.

        Args:
            story_id: The story ID
            limit: Limit the number of results returned
            offset: Skip the specified number of results
            format: Filter by the issue format
            format_type: Filter by the issue format type
            no_variants: Exclude variant comics
            date_descriptor: Return comics within a specified date range
            date_range: Return comics within a specified date range
            diamond_code: Filter by diamond code
            digital_id: Filter by digital comic ID
            upc: Filter by UPC
            isbn: Filter by ISBN
            ean: Filter by EAN
            issn: Filter by ISSN
            has_digital_issue: Filter by digital availability
            modified_since: Return only comics modified since the specified date
            creators: Return only comics which feature work by the specified creators
            characters: Return only comics which feature the specified characters
            series: Return only comics which are part of the specified series
            events: Return only comics which take place during the specified events
            shared_appearances: Return only comics in which the specified characters appear together
            collaborators: Return only comics in which the specified creators worked together
            order_by: Order the result set by a field or set of fields

        Returns:
            ComicListResponse containing the story's comics

        Example:
            >>> comics = await client.get_story_comics(12345, limit=5)
            >>> print(f"Story appears in {comics.data.total} comics")
        """
        return await self.stories.get_comics(
            story_id=story_id,
            limit=limit,
            offset=offset,
            format=format,
            format_type=format_type,
            no_variants=no_variants,
            date_descriptor=date_descriptor,
            date_range=date_range,
            diamond_code=diamond_code,
            digital_id=digital_id,
            upc=upc,
            isbn=isbn,
            ean=ean,
            issn=issn,
            has_digital_issue=has_digital_issue,
            modified_since=modified_since,
            creators=creators,
            characters=characters,
            series=series,
            events=events,
            shared_appearances=shared_appearances,
            collaborators=collaborators,
            order_by=order_by,
        )

    async def get_story_creators(
        self,
        story_id: int,
        limit: int | None = None,
        offset: int | None = None,
        first_name: str | None = None,
        middle_name: str | None = None,
        last_name: str | None = None,
        suffix: str | None = None,
        name_starts_with: str | None = None,
        first_name_starts_with: str | None = None,
        middle_name_starts_with: str | None = None,
        last_name_starts_with: str | None = None,
        modified_since: str | None = None,
        comics: list[int] | None = None,
        series: list[int] | None = None,
        events: list[int] | None = None,
        order_by: str | None = None,
    ) -> CreatorListResponse:
        """Get creators who worked on a specific story.

        Args:
            story_id: The story ID
            limit: Limit the number of results returned
            offset: Skip the specified number of results
            first_name: Filter by creator first name
            middle_name: Filter by creator middle name
            last_name: Filter by creator last name
            suffix: Filter by creator suffix
            name_starts_with: Filter by creator names that begin with the specified string
            first_name_starts_with: Filter by creator first names that begin with the specified string
            middle_name_starts_with: Filter by creator middle names that begin with the specified string
            last_name_starts_with: Filter by creator last names that begin with the specified string
            modified_since: Return only creators which have been modified since the specified date
            comics: Return only creators who have worked on comics in the specified list
            series: Return only creators who have worked on series in the specified list
            events: Return only creators who have worked on comics in the specified events
            order_by: Order the result set by a field or set of fields

        Returns:
            CreatorListResponse containing the story's creators

        Example:
            >>> creators = await client.get_story_creators(12345, limit=5)
            >>> print(f"Story has {creators.data.total} creators")
        """
        return await self.stories.get_creators(
            story_id=story_id,
            limit=limit,
            offset=offset,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            suffix=suffix,
            name_starts_with=name_starts_with,
            first_name_starts_with=first_name_starts_with,
            middle_name_starts_with=middle_name_starts_with,
            last_name_starts_with=last_name_starts_with,
            modified_since=modified_since,
            comics=comics,
            series=series,
            events=events,
            order_by=order_by,
        )

    async def get_story_events(
        self,
        story_id: int,
        limit: int | None = None,
        offset: int | None = None,
        name: str | None = None,
        name_starts_with: str | None = None,
        modified_since: str | None = None,
        creators: list[int] | None = None,
        characters: list[int] | None = None,
        series: list[int] | None = None,
        comics: list[int] | None = None,
        order_by: str | None = None,
    ) -> EventListResponse:
        """Get events featuring a specific story.

        Args:
            story_id: The story ID
            limit: Limit the number of results returned
            offset: Skip the specified number of results
            name: Return only events matching the specified name
            name_starts_with: Return events with names that begin with the specified string
            modified_since: Return only events which have been modified since the specified date
            creators: Return only events which feature work by the specified creators
            characters: Return only events which feature the specified characters
            series: Return only events which are part of the specified series
            comics: Return only events which take place in the specified comics
            order_by: Order the result set by a field or set of fields

        Returns:
            EventListResponse containing the story's events

        Example:
            >>> events = await client.get_story_events(12345, limit=3)
            >>> print(f"Story appears in {events.data.total} events")
        """
        return await self.stories.get_events(
            story_id=story_id,
            limit=limit,
            offset=offset,
            name=name,
            name_starts_with=name_starts_with,
            modified_since=modified_since,
            creators=creators,
            characters=characters,
            series=series,
            comics=comics,
            order_by=order_by,
        )

    async def get_story_series(
        self,
        story_id: int,
        limit: int | None = None,
        offset: int | None = None,
        title: str | None = None,
        title_starts_with: str | None = None,
        start_year: int | None = None,
        modified_since: str | None = None,
        comics: list[int] | None = None,
        events: list[int] | None = None,
        creators: list[int] | None = None,
        characters: list[int] | None = None,
        series_type: str | None = None,
        contains: str | None = None,
        order_by: str | None = None,
    ) -> SeriesListResponse:
        """Get series containing a specific story.

        Args:
            story_id: The story ID
            limit: Limit the number of results returned
            offset: Skip the specified number of results
            title: Return only series matching the specified title
            title_starts_with: Return series with titles that begin with the specified string
            start_year: Return only series which started in the specified year
            modified_since: Return only series which have been modified since the specified date
            comics: Return only series which contain the specified comics
            events: Return only series which are part of the specified events
            creators: Return only series which feature work by the specified creators
            characters: Return only series which feature the specified characters
            series_type: Filter the series by publication frequency type
            contains: Return only series containing one or more comics with the specified format
            order_by: Order the result set by a field or set of fields

        Returns:
            SeriesListResponse containing the story's series

        Example:
            >>> series = await client.get_story_series(12345, limit=3)
            >>> print(f"Story appears in {series.data.total} series")
        """
        return await self.stories.get_series(
            story_id=story_id,
            limit=limit,
            offset=offset,
            title=title,
            title_starts_with=title_starts_with,
            start_year=start_year,
            modified_since=modified_since,
            comics=comics,
            events=events,
            creators=creators,
            characters=characters,
            series_type=series_type,
            contains=contains,
            order_by=order_by,
        )

    # ============================================================================
    # CREATOR METHODS
    # ============================================================================

    async def get_creator(self, creator_id: int) -> Creator:
        """Get a single creator by ID.

        Args:
            creator_id: The unique identifier for the creator

        Returns:
            Creator object containing creator data

        Example:
            >>> creator = await client.get_creator(30)
            >>> print(f"Creator: {creator.full_name}")
        """
        return await self.creators.get_creator(creator_id)

    async def list_creators(
        self,
        limit: int | None = None,
        offset: int | None = None,
        first_name: str | None = None,
        middle_name: str | None = None,
        last_name: str | None = None,
        suffix: str | None = None,
        name_starts_with: str | None = None,
        first_name_starts_with: str | None = None,
        middle_name_starts_with: str | None = None,
        last_name_starts_with: str | None = None,
        modified_since: str | None = None,
        comics: list[int] | None = None,
        series: list[int] | None = None,
        events: list[int] | None = None,
        stories: list[int] | None = None,
        order_by: str | None = None,
    ) -> CreatorListResponse:
        """List creators with optional filtering.

        Args:
            limit: Limit the number of results returned
            offset: Skip the specified number of results
            first_name: Filter by creator first name
            middle_name: Filter by creator middle name
            last_name: Filter by creator last name
            suffix: Filter by creator suffix
            name_starts_with: Filter by creator names that begin with the specified string
            first_name_starts_with: Filter by creator first names that begin with the specified string
            middle_name_starts_with: Filter by creator middle names that begin with the specified string
            last_name_starts_with: Filter by creator last names that begin with the specified string
            modified_since: Return only creators which have been modified since the specified date
            comics: Return only creators who have worked on comics in the specified list
            series: Return only creators who have worked on series in the specified list
            events: Return only creators who have worked on comics in the specified events
            stories: Return only creators who have worked on comics in the specified stories
            order_by: Order the result set by a field or set of fields

        Returns:
            CreatorListResponse containing the list of creators

        Example:
            >>> creators = await client.list_creators(first_name="Stan", limit=10)
            >>> print(f"Found {creators.data.total} creators")
        """
        return await self.creators.list_creators(
            limit=limit,
            offset=offset,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            suffix=suffix,
            name_starts_with=name_starts_with,
            first_name_starts_with=first_name_starts_with,
            middle_name_starts_with=middle_name_starts_with,
            last_name_starts_with=last_name_starts_with,
            modified_since=modified_since,
            comics=comics,
            series=series,
            events=events,
            stories=stories,
            order_by=order_by,
        )

    async def search_creators(
        self,
        query: str,
        limit: int | None = None,
        offset: int | None = None,
    ) -> CreatorListResponse:
        """Search for creators by name.

        Args:
            query: Search query (creator name)
            limit: Limit the number of results returned
            offset: Skip the specified number of results

        Returns:
            CreatorListResponse containing matching creators

        Example:
            >>> results = await client.search_creators("stan lee", limit=5)
            >>> for creator in results.data.results:
            ...     print(f"- {creator.full_name}")
        """
        return await self.creators.list_creators(
            name_starts_with=query,
            limit=limit,
            offset=offset,
        )

    # Creator related resources
    async def get_creator_comics(
        self,
        creator_id: int,
        limit: int | None = None,
        offset: int | None = None,
        format: str | None = None,
        format_type: str | None = None,
        no_variants: bool | None = None,
        date_descriptor: str | None = None,
        date_range: list[int] | None = None,
        diamond_code: str | None = None,
        digital_id: int | None = None,
        upc: str | None = None,
        isbn: str | None = None,
        ean: str | None = None,
        issn: str | None = None,
        has_digital_issue: bool | None = None,
        modified_since: str | None = None,
        characters: list[int] | None = None,
        series: list[int] | None = None,
        events: list[int] | None = None,
        stories: list[int] | None = None,
        shared_appearances: list[int] | None = None,
        collaborators: list[int] | None = None,
        order_by: str | None = None,
    ) -> ComicListResponse:
        """Get comics created by a specific creator.

        Args:
            creator_id: The creator ID
            limit: Limit the number of results returned
            offset: Skip the specified number of results
            format: Filter by the issue format
            format_type: Filter by the issue format type
            no_variants: Exclude variant comics
            date_descriptor: Return comics within a specified date range
            date_range: Return comics within a specified date range
            diamond_code: Filter by diamond code
            digital_id: Filter by digital comic ID
            upc: Filter by UPC
            isbn: Filter by ISBN
            ean: Filter by EAN
            issn: Filter by ISSN
            has_digital_issue: Filter by digital availability
            modified_since: Return only comics modified since the specified date
            characters: Return only comics which feature the specified characters
            series: Return only comics which are part of the specified series
            events: Return only comics which take place during the specified events
            stories: Return only comics which contain the specified stories
            shared_appearances: Return only comics in which the specified characters appear together
            collaborators: Return only comics in which the specified creators worked together
            order_by: Order the result set by a field or set of fields

        Returns:
            ComicListResponse containing the creator's comics

        Example:
            >>> comics = await client.get_creator_comics(30, limit=5)
            >>> print(f"Creator worked on {comics.data.total} comics")
        """
        return await self.creators.get_comics(
            creator_id=creator_id,
            limit=limit,
            offset=offset,
            format=format,
            format_type=format_type,
            no_variants=no_variants,
            date_descriptor=date_descriptor,
            date_range=date_range,
            diamond_code=diamond_code,
            digital_id=digital_id,
            upc=upc,
            isbn=isbn,
            ean=ean,
            issn=issn,
            has_digital_issue=has_digital_issue,
            modified_since=modified_since,
            characters=characters,
            series=series,
            events=events,
            stories=stories,
            shared_appearances=shared_appearances,
            collaborators=collaborators,
            order_by=order_by,
        )

    async def get_creator_events(
        self,
        creator_id: int,
        limit: int | None = None,
        offset: int | None = None,
        name: str | None = None,
        name_starts_with: str | None = None,
        modified_since: str | None = None,
        characters: list[int] | None = None,
        series: list[int] | None = None,
        comics: list[int] | None = None,
        stories: list[int] | None = None,
        order_by: str | None = None,
    ) -> EventListResponse:
        """Get events featuring work by a specific creator.

        Args:
            creator_id: The creator ID
            limit: Limit the number of results returned
            offset: Skip the specified number of results
            name: Return only events matching the specified name
            name_starts_with: Return events with names that begin with the specified string
            modified_since: Return only events which have been modified since the specified date
            characters: Return only events which feature the specified characters
            series: Return only events which are part of the specified series
            comics: Return only events which take place in the specified comics
            stories: Return only events which contain the specified stories
            order_by: Order the result set by a field or set of fields

        Returns:
            EventListResponse containing the creator's events

        Example:
            >>> events = await client.get_creator_events(30, limit=3)
            >>> print(f"Creator worked on {events.data.total} events")
        """
        return await self.creators.get_events(
            creator_id=creator_id,
            limit=limit,
            offset=offset,
            name=name,
            name_starts_with=name_starts_with,
            modified_since=modified_since,
            characters=characters,
            series=series,
            comics=comics,
            stories=stories,
            order_by=order_by,
        )

    async def get_creator_series(
        self,
        creator_id: int,
        limit: int | None = None,
        offset: int | None = None,
        title: str | None = None,
        title_starts_with: str | None = None,
        start_year: int | None = None,
        modified_since: str | None = None,
        comics: list[int] | None = None,
        stories: list[int] | None = None,
        events: list[int] | None = None,
        characters: list[int] | None = None,
        series_type: str | None = None,
        contains: str | None = None,
        order_by: str | None = None,
    ) -> SeriesListResponse:
        """Get series featuring work by a specific creator.

        Args:
            creator_id: The creator ID
            limit: Limit the number of results returned
            offset: Skip the specified number of results
            title: Return only series matching the specified title
            title_starts_with: Return series with titles that begin with the specified string
            start_year: Return only series which started in the specified year
            modified_since: Return only series which have been modified since the specified date
            comics: Return only series which contain the specified comics
            stories: Return only series which contain the specified stories
            events: Return only series which are part of the specified events
            characters: Return only series which feature the specified characters
            series_type: Filter the series by publication frequency type
            contains: Return only series containing one or more comics with the specified format
            order_by: Order the result set by a field or set of fields

        Returns:
            SeriesListResponse containing the creator's series

        Example:
            >>> series = await client.get_creator_series(30, limit=5)
            >>> print(f"Creator worked on {series.data.total} series")
        """
        return await self.creators.get_series(
            creator_id=creator_id,
            limit=limit,
            offset=offset,
            title=title,
            title_starts_with=title_starts_with,
            start_year=start_year,
            modified_since=modified_since,
            comics=comics,
            stories=stories,
            events=events,
            characters=characters,
            series_type=series_type,
            contains=contains,
            order_by=order_by,
        )

    async def get_creator_stories(
        self,
        creator_id: int,
        limit: int | None = None,
        offset: int | None = None,
        modified_since: str | None = None,
        comics: list[int] | None = None,
        series: list[int] | None = None,
        events: list[int] | None = None,
        characters: list[int] | None = None,
        order_by: str | None = None,
    ) -> StoryListResponse:
        """Get stories featuring work by a specific creator.

        Args:
            creator_id: The creator ID
            limit: Limit the number of results returned
            offset: Skip the specified number of results
            modified_since: Return only stories which have been modified since the specified date
            comics: Return only stories contained in the specified comics
            series: Return only stories contained the specified series
            events: Return only stories which take place during the specified events
            characters: Return only stories which feature the specified characters
            order_by: Order the result set by a field or set of fields

        Returns:
            StoryListResponse containing the creator's stories

        Example:
            >>> stories = await client.get_creator_stories(30, limit=5)
            >>> print(f"Creator worked on {stories.data.total} stories")
        """
        return await self.creators.get_stories(
            creator_id=creator_id,
            limit=limit,
            offset=offset,
            modified_since=modified_since,
            comics=comics,
            series=series,
            events=events,
            characters=characters,
            order_by=order_by,
        )
