"""Demo showcasing all Marvel API models in v1.0.0.

This example demonstrates the new type-safe model system with all Marvel API entities:
Characters, Comics, Events, Series, Stories, and Creators.

Note: This example uses the current client API and converts responses to type-safe models.
Future versions will have dedicated endpoint methods for each entity type.
"""

import asyncio
import os

from marvelpy import MarvelClient
from marvelpy.models import (
    Character,
    CharacterListResponse,
    ComicListResponse,
    CreatorListResponse,
    EventListResponse,
    SeriesListResponse,
    StoryListResponse,
)

# Load environment variables
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


async def demonstrate_characters(client: MarvelClient) -> None:
    """Demonstrate Character models and functionality."""
    print("🦸 CHARACTERS")
    print("=" * 50)

    # Get characters and convert to type-safe models
    characters_data = await client.get_characters(params={"limit": 3})
    response: CharacterListResponse = CharacterListResponse(**characters_data)
    print(f"Found {response.data.count} characters (showing first 3)")

    for character in response.data.results:
        print(f"\n📖 {character.name}")
        print(f"   ID: {character.id}")
        print(
            f"   Description: {character.description[:100]}..."
            if character.description
            else "   No description"
        )
        print(f"   Comics: {character.comics.available}")
        print(f"   Series: {character.series.available}")
        print(f"   Stories: {character.stories.available}")
        print(f"   Events: {character.events.available}")

    # Search for a specific character
    print("\n🔍 Searching for Iron Man...")
    search_data = await client.get_characters(params={"name": "iron man"})
    search_response: CharacterListResponse = CharacterListResponse(**search_data)
    if search_response.data.results:
        iron_man: Character = search_response.data.results[0]
        print(f"✅ Found: {iron_man.name} (ID: {iron_man.id})")


async def demonstrate_comics(client: MarvelClient) -> None:
    """Demonstrate Comic models and functionality."""
    print("\n📚 COMICS")
    print("=" * 50)

    # Get comics and convert to type-safe models
    comics_data = await client.get("comics", params={"limit": 3})
    response: ComicListResponse = ComicListResponse(**comics_data)
    print(f"Found {response.data.count} comics (showing first 3)")

    for comic in response.data.results:
        print(f"\n📖 {comic.title}")
        print(f"   Issue #: {comic.issue_number}")
        print(f"   Format: {comic.format}")
        print(f"   Page Count: {comic.page_count}")
        print(f"   Characters: {comic.characters.available}")
        print(f"   Creators: {comic.creators.available}")
        print(f"   Stories: {comic.stories.available}")
        print(f"   Events: {comic.events.available}")

        # Show some creators if available
        if comic.creators.items:
            creator_names = [creator.name for creator in comic.creators.items[:3]]
            print(f"   Sample Creators: {', '.join(creator_names)}")


async def demonstrate_events(client: MarvelClient) -> None:
    """Demonstrate Event models and functionality."""
    print("\n🎭 EVENTS")
    print("=" * 50)

    # Get events and convert to type-safe models
    events_data = await client.get("events", params={"limit": 3})
    response: EventListResponse = EventListResponse(**events_data)
    print(f"Found {response.data.count} events (showing first 3)")

    for event in response.data.results:
        print(f"\n🎪 {event.title}")
        print(f"   ID: {event.id}")
        print(f"   Start: {event.start}")
        print(f"   End: {event.end}")
        print(f"   Comics: {event.comics.available}")
        print(f"   Characters: {event.characters.available}")
        print(f"   Creators: {event.creators.available}")
        print(f"   Series: {event.series.available}")
        print(f"   Stories: {event.stories.available}")


async def demonstrate_series(client: MarvelClient) -> None:
    """Demonstrate Series models and functionality."""
    print("\n📺 SERIES")
    print("=" * 50)

    # Get series and convert to type-safe models
    series_data = await client.get("series", params={"limit": 3})
    response: SeriesListResponse = SeriesListResponse(**series_data)
    print(f"Found {response.data.count} series (showing first 3)")

    for series in response.data.results:
        print(f"\n📺 {series.title}")
        print(f"   ID: {series.id}")
        print(f"   Years: {series.start_year}-{series.end_year or 'Present'}")
        print(f"   Rating: {series.rating or 'Not rated'}")
        print(f"   Comics: {series.comics.available}")
        print(f"   Characters: {series.characters.available}")
        print(f"   Creators: {series.creators.available}")
        print(f"   Events: {series.events.available}")
        print(f"   Stories: {series.stories.available}")


async def demonstrate_stories(client: MarvelClient) -> None:
    """Demonstrate Story models and functionality."""
    print("\n📝 STORIES")
    print("=" * 50)

    # Get stories and convert to type-safe models
    stories_data = await client.get("stories", params={"limit": 3})
    response: StoryListResponse = StoryListResponse(**stories_data)
    print(f"Found {response.data.count} stories (showing first 3)")

    for story in response.data.results:
        print(f"\n📝 {story.title}")
        print(f"   ID: {story.id}")
        print(f"   Type: {story.type}")
        print(f"   Comics: {story.comics.available}")
        print(f"   Characters: {story.characters.available}")
        print(f"   Creators: {story.creators.available}")
        print(f"   Events: {story.events.available}")
        print(f"   Series: {story.series.available}")


async def demonstrate_creators(client: MarvelClient) -> None:
    """Demonstrate Creator models and functionality."""
    print("\n👨‍🎨 CREATORS")
    print("=" * 50)

    # Get creators and convert to type-safe models
    creators_data = await client.get("creators", params={"limit": 3})
    response: CreatorListResponse = CreatorListResponse(**creators_data)
    print(f"Found {response.data.count} creators (showing first 3)")

    for creator in response.data.results:
        print(f"\n👨‍🎨 {creator.full_name}")
        print(f"   ID: {creator.id}")
        print(f"   First Name: {creator.first_name}")
        print(f"   Last Name: {creator.last_name}")
        if creator.middle_name:
            print(f"   Middle Name: {creator.middle_name}")
        if creator.suffix:
            print(f"   Suffix: {creator.suffix}")
        print(f"   Comics: {creator.comics.available}")
        print(f"   Series: {creator.series.available}")
        print(f"   Stories: {creator.stories.available}")
        print(f"   Events: {creator.events.available}")
        print(f"   Characters: {creator.characters.available if creator.characters else 0}")


async def main() -> None:
    """Main function demonstrating all Marvel API models."""
    # Get API keys from environment variables
    public_key = os.getenv("MARVEL_PUBLIC_KEY")
    private_key = os.getenv("MARVEL_PRIVATE_KEY")

    if not public_key or not private_key:
        print("❌ Please set MARVEL_PUBLIC_KEY and MARVEL_PRIVATE_KEY environment variables")
        print("You can get these from https://developer.marvel.com/")
        return

    print("🚀 Marvelpy v1.0.0 - Models Demo")
    print("=" * 60)

    # Create client instance
    async with MarvelClient(public_key, private_key) as client:
        try:
            # Test health check
            print("🔍 Testing API connection...")
            health = await client.health_check()
            print(f"✅ API Status: {health['status']}")

            # Demonstrate all entity types
            await demonstrate_characters(client)
            await demonstrate_comics(client)
            await demonstrate_events(client)
            await demonstrate_series(client)
            await demonstrate_stories(client)
            await demonstrate_creators(client)

            print("\n🎉 Demo completed successfully!")
            print("\nKey Benefits of v1.0.0:")
            print("✅ 100% Type Safety with Pydantic v2 models")
            print("✅ Full async/await support")
            print("✅ All Marvel API entities supported")
            print("✅ Comprehensive relationship modeling")
            print("✅ Enterprise-grade error handling")
            print("✅ Runtime validation of API responses")

        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
