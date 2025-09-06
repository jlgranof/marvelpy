# Quick Start

Get up and running with Marvelpy v1.0.0 in minutes!

## Installation

```bash
pip install marvelpy
```

## Getting API Keys

Before you can use Marvelpy, you'll need to get API keys from Marvel:

1. Visit the [Marvel Developer Portal](https://developer.marvel.com/)
2. Sign up for a free account
3. Generate your API keys (public and private)

## Basic Usage

### Setting Up Your Client

```python
import asyncio
from marvelpy import MarvelClient

async def main():
    # Initialize the client with your API keys
    async with MarvelClient("your_public_key", "your_private_key") as client:
        # Your code here
        pass

asyncio.run(main())
```

### Working with Characters (Type-Safe!)

```python
from marvelpy.models import Character, CharacterListResponse

async def get_characters():
    async with MarvelClient("your_public_key", "your_private_key") as client:
        # Get a list of characters with full type safety
        characters_data = await client.get_characters(params={"limit": 5})
        response: CharacterListResponse = CharacterListResponse(**characters_data)
        print(f"Found {response.data.count} characters")

        # Access character data with full type hints
        if response.data.results:
            first_char: Character = response.data.results[0]
            print(f"First character: {first_char.name}")
            print(f"Description: {first_char.description}")
            print(f"Comics available: {first_char.comics.available}")

asyncio.run(get_characters())
```

### Working with Comics

```python
from marvelpy.models import Comic, ComicListResponse

async def get_comics():
    async with MarvelClient("your_public_key", "your_private_key") as client:
        # Get comics with type safety
        response: ComicListResponse = await client.comics.list(limit=3)

        for comic in response.data.results:
            print(f"Comic: {comic.title}")
            print(f"  Issue #: {comic.issue_number}")
            print(f"  Characters: {comic.characters.available}")
            print(f"  Creators: {comic.creators.available}")

asyncio.run(get_comics())
```

### Working with Events

```python
from marvelpy.models import Event, EventListResponse

async def get_events():
    async with MarvelClient("your_public_key", "your_private_key") as client:
        # Get Marvel events
        response: EventListResponse = await client.events.list(limit=5)

        for event in response.data.results:
            print(f"Event: {event.title}")
            print(f"  Start: {event.start}")
            print(f"  End: {event.end}")
            print(f"  Comics: {event.comics.available}")

asyncio.run(get_events())
```

### Working with Series

```python
from marvelpy.models import Series, SeriesListResponse

async def get_series():
    async with MarvelClient("your_public_key", "your_private_key") as client:
        # Get comic series
        response: SeriesListResponse = await client.series.list(limit=5)

        for series in response.data.results:
            print(f"Series: {series.title}")
            print(f"  Years: {series.start_year}-{series.end_year or 'Present'}")
            print(f"  Comics: {series.comics.available}")

asyncio.run(get_series())
```

### Working with Stories

```python
from marvelpy.models import Story, StoryListResponse

async def get_stories():
    async with MarvelClient("your_public_key", "your_private_key") as client:
        # Get stories
        response: StoryListResponse = await client.stories.list(limit=5)

        for story in response.data.results:
            print(f"Story: {story.title}")
            print(f"  Type: {story.type}")
            print(f"  Comics: {story.comics.available}")

asyncio.run(get_stories())
```

### Working with Creators

```python
from marvelpy.models import Creator, CreatorListResponse

async def get_creators():
    async with MarvelClient("your_public_key", "your_private_key") as client:
        # Get creators
        response: CreatorListResponse = await client.creators.list(limit=5)

        for creator in response.data.results:
            print(f"Creator: {creator.full_name}")
            print(f"  Comics: {creator.comics.available}")
            print(f"  Series: {creator.series.available}")

asyncio.run(get_creators())
```

### Health Check

```python
async def check_api():
    async with MarvelClient("your_public_key", "your_private_key") as client:
        # Check if the API is accessible
        status = await client.health_check()
        print(f"API Status: {status['status']}")

asyncio.run(check_api())
```

## What's Available in v1.0.0

Marvelpy v1.0.0 includes:

- **Complete Model System** - Full Pydantic v2 models for all Marvel API entities
- **Type Safety** - 100% type-safe with comprehensive type hints
- **All Marvel Entities** - Characters, Comics, Events, Series, Stories, Creators
- **Async/Await Support** - Full async support throughout
- **Comprehensive Testing** - 146+ tests with full coverage
- **Enterprise-Grade** - Production-ready with robust error handling
- **Rich Documentation** - Complete API documentation with examples

## Entity Models Available

- **Characters** - Superheroes, villains, and supporting characters
- **Comics** - Individual comic book issues with metadata
- **Events** - Major Marvel universe storylines and crossovers
- **Series** - Comic book series and ongoing titles
- **Stories** - Individual stories within comics
- **Creators** - Writers, artists, editors, and other contributors

## Coming in Future Versions

- **CLI Interface** - Command-line tools for easy access
- **Advanced Features** - Caching, rate limiting, retry logic
- **Enterprise Features** - Search engine, data export, batch processing

## Next Steps

- Check out the [API Reference](api/hello.md) for detailed documentation
- See the [Installation Guide](installation.md) for setup instructions
- Visit our [GitHub repository](https://github.com/jlgranof/marvelpy) for the latest updates
