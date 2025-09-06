"""Comprehensive endpoint demonstration for Marvelpy v1.0.0.

This example demonstrates all endpoint classes and their capabilities
with real API calls and type-safe models. This showcases the endpoint
architecture that will be integrated into the enhanced MarvelClient.
"""

import asyncio
import os

from marvelpy.endpoints import (
    CharactersEndpoint,
    ComicsEndpoint,
    CreatorsEndpoint,
    EventsEndpoint,
    SeriesEndpoint,
    StoriesEndpoint,
)
from marvelpy.models import (
    Character,
    CharacterListResponse,
    Comic,
    ComicListResponse,
    Creator,
    CreatorListResponse,
    Event,
    EventListResponse,
    Series,
    SeriesListResponse,
    Story,
    StoryListResponse,
)

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


async def demonstrate_characters_endpoint() -> None:
    """Demonstrate CharactersEndpoint functionality."""
    print("🦸 CHARACTERS ENDPOINT DEMONSTRATION")
    print("=" * 50)
    
    # Get API keys
    public_key = os.getenv("MARVEL_PUBLIC_KEY")
    private_key = os.getenv("MARVEL_PRIVATE_KEY")
    
    if not public_key or not private_key:
        print("❌ API keys not found")
        return
    
    # Initialize endpoint
    endpoint = CharactersEndpoint(
        base_url="https://gateway.marvel.com",
        public_key=public_key,
        private_key=private_key,
    )
    
    # List characters with filtering
    print("\n📋 Listing characters with filtering...")
    characters = await endpoint.list_characters(
        name_starts_with="Spider",
        limit=5
    )
    print(f"Found {characters.data.count} characters starting with 'Spider'")
    
    for char in characters.data.results:
        print(f"  - {char.name} (ID: {char.id})")
    
    # Get specific character (use first character from the list)
    print("\n🕷️ Getting a specific character by ID...")
    if characters.data.results:
        first_char_id = characters.data.results[0].id
        character = await endpoint.get_character(first_char_id)
        print(f"Character: {character.name}")
        print(f"Description: {character.description[:100]}..." if character.description else "No description")
    else:
        print("No characters found to demonstrate get_character")
    
    # Get character's comics
    print("\n📚 Getting character's comics...")
    if characters.data.results:
        first_char_id = characters.data.results[0].id
        char_comics = await endpoint.get_comics(first_char_id, limit=3)
        print(f"Character appears in {char_comics.data.total} comics (showing first 3):")
        
        for comic in char_comics.data.results:
            print(f"  - {comic.title} (Issue #{comic.issue_number})")
        
        # Get character's events
        print("\n🎭 Getting character's events...")
        char_events = await endpoint.get_events(first_char_id, limit=3)
        print(f"Character appears in {char_events.data.total} events (showing first 3):")
        
        for event in char_events.data.results:
            print(f"  - {event.title}")
    else:
        print("No characters found to demonstrate related resources")


async def demonstrate_comics_endpoint() -> None:
    """Demonstrate ComicsEndpoint functionality."""
    print("\n\n📚 COMICS ENDPOINT DEMONSTRATION")
    print("=" * 50)
    
    # Get API keys
    public_key = os.getenv("MARVEL_PUBLIC_KEY")
    private_key = os.getenv("MARVEL_PRIVATE_KEY")
    
    if not public_key or not private_key:
        print("❌ API keys not found")
        return
    
    # Initialize endpoint
    endpoint = ComicsEndpoint(
        base_url="https://gateway.marvel.com",
        public_key=public_key,
        private_key=private_key,
    )
    
    # List comics with filtering
    print("\n📋 Listing comics with filtering...")
    comics = await endpoint.list_comics(
        title_starts_with="Amazing Spider-Man",
        limit=5
    )
    print(f"Found {comics.data.count} comics starting with 'Amazing Spider-Man'")
    
    for comic in comics.data.results:
        print(f"  - {comic.title} (Issue #{comic.issue_number})")
    
    # Get specific comic (use first comic from the list)
    print("\n📖 Getting a specific comic...")
    if comics.data.results:
        first_comic_id = comics.data.results[0].id
        comic = await endpoint.get_comic(first_comic_id)
        print(f"Comic: {comic.title}")
        print(f"Issue #: {comic.issue_number}")
        print(f"Characters: {comic.characters.available}")
        
        # Get comic's characters
        print("\n🦸 Getting comic's characters...")
        comic_characters = await endpoint.get_characters(first_comic_id, limit=3)
        print(f"Comic has {comic_characters.data.total} characters (showing first 3):")
        
        for char in comic_characters.data.results:
            print(f"  - {char.name}")
        
        # Get comic's creators
        print("\n✍️ Getting comic's creators...")
        comic_creators = await endpoint.get_creators(first_comic_id, limit=3)
        print(f"Comic has {comic_creators.data.total} creators (showing first 3):")
        
        for creator in comic_creators.data.results:
            print(f"  - {creator.full_name}")
    else:
        print("No comics found to demonstrate get_comic")


async def demonstrate_events_endpoint() -> None:
    """Demonstrate EventsEndpoint functionality."""
    print("\n\n🎭 EVENTS ENDPOINT DEMONSTRATION")
    print("=" * 50)
    
    # Get API keys
    public_key = os.getenv("MARVEL_PUBLIC_KEY")
    private_key = os.getenv("MARVEL_PRIVATE_KEY")
    
    if not public_key or not private_key:
        print("❌ API keys not found")
        return
    
    # Initialize endpoint
    endpoint = EventsEndpoint(
        base_url="https://gateway.marvel.com",
        public_key=public_key,
        private_key=private_key,
    )
    
    # List events
    print("\n📋 Listing Marvel events...")
    events = await endpoint.list_events(limit=5)
    print(f"Found {events.data.count} events (showing first 5):")
    
    for event in events.data.results:
        print(f"  - {event.title}")
        print(f"    Start: {event.start}, End: {event.end}")
    
    # Get specific event (use first event from the list)
    print("\n🎪 Getting a specific event...")
    if events.data.results:
        first_event_id = events.data.results[0].id
        event = await endpoint.get_event(first_event_id)
        print(f"Event: {event.title}")
        print(f"Description: {event.description[:100]}..." if event.description else "No description")
        
        # Get event's comics
        print("\n📚 Getting event's comics...")
        event_comics = await endpoint.get_comics(first_event_id, limit=3)
        print(f"Event has {event_comics.data.total} comics (showing first 3):")
        
        for comic in event_comics.data.results:
            print(f"  - {comic.title}")
        
        # Get event's characters
        print("\n🦸 Getting event's characters...")
        event_characters = await endpoint.get_characters(first_event_id, limit=3)
        print(f"Event has {event_characters.data.total} characters (showing first 3):")
        
        for char in event_characters.data.results:
            print(f"  - {char.name}")
    else:
        print("No events found to demonstrate get_event")


async def demonstrate_series_endpoint() -> None:
    """Demonstrate SeriesEndpoint functionality."""
    print("\n\n📖 SERIES ENDPOINT DEMONSTRATION")
    print("=" * 50)
    
    # Get API keys
    public_key = os.getenv("MARVEL_PUBLIC_KEY")
    private_key = os.getenv("MARVEL_PRIVATE_KEY")
    
    if not public_key or not private_key:
        print("❌ API keys not found")
        return
    
    # Initialize endpoint
    endpoint = SeriesEndpoint(
        base_url="https://gateway.marvel.com",
        public_key=public_key,
        private_key=private_key,
    )
    
    # List series
    print("\n📋 Listing comic series...")
    series = await endpoint.list_series(
        title_starts_with="Amazing Spider-Man",
        limit=5
    )
    print(f"Found {series.data.count} series starting with 'Amazing Spider-Man'")
    
    for s in series.data.results:
        years = f"{s.start_year}-{s.end_year or 'Present'}" if s.start_year else "Unknown years"
        print(f"  - {s.title} ({years})")
    
    # Get specific series (use first series from the list)
    print("\n📚 Getting a specific series...")
    if series.data.results:
        first_series_id = series.data.results[0].id
        series_obj = await endpoint.get_series(first_series_id)
        print(f"Series: {series_obj.title}")
        years = f"{series_obj.start_year}-{series_obj.end_year or 'Present'}" if series_obj.start_year else "Unknown years"
        print(f"Years: {years}")
        print(f"Comics: {series_obj.comics.available}")
        
        # Get series' comics
        print("\n📖 Getting series' comics...")
        series_comics = await endpoint.get_comics(first_series_id, limit=3)
        print(f"Series has {series_comics.data.total} comics (showing first 3):")
        
        for comic in series_comics.data.results:
            print(f"  - {comic.title} (Issue #{comic.issue_number})")
        
        # Get series' characters
        print("\n🦸 Getting series' characters...")
        series_characters = await endpoint.get_characters(first_series_id, limit=3)
        print(f"Series has {series_characters.data.total} characters (showing first 3):")
        
        for char in series_characters.data.results:
            print(f"  - {char.name}")
    else:
        print("No series found to demonstrate get_series")


async def demonstrate_stories_endpoint() -> None:
    """Demonstrate StoriesEndpoint functionality."""
    print("\n\n📝 STORIES ENDPOINT DEMONSTRATION")
    print("=" * 50)
    
    # Get API keys
    public_key = os.getenv("MARVEL_PUBLIC_KEY")
    private_key = os.getenv("MARVEL_PRIVATE_KEY")
    
    if not public_key or not private_key:
        print("❌ API keys not found")
        return
    
    # Initialize endpoint
    endpoint = StoriesEndpoint(
        base_url="https://gateway.marvel.com",
        public_key=public_key,
        private_key=private_key,
    )
    
    # List stories
    print("\n📋 Listing stories...")
    stories = await endpoint.list_stories(limit=5)
    print(f"Found {stories.data.count} stories (showing first 5):")
    
    for story in stories.data.results:
        print(f"  - {story.title} (Type: {story.type})")
    
    # Get specific story (using a known story ID)
    print("\n📖 Getting a specific story...")
    try:
        story = await endpoint.get_story(7)  # This should exist based on our previous tests
        print(f"Story: {story.title}")
        print(f"Type: {story.type}")
        print(f"Comics: {story.comics.available}")
        
        # Get story's characters
        print("\n🦸 Getting story's characters...")
        story_characters = await endpoint.get_characters(7, limit=3)
        print(f"Story has {story_characters.data.total} characters (showing first 3):")
        
        for char in story_characters.data.results:
            print(f"  - {char.name}")
            
    except Exception as e:
        print(f"Could not get specific story: {e}")


async def demonstrate_creators_endpoint() -> None:
    """Demonstrate CreatorsEndpoint functionality."""
    print("\n\n✍️ CREATORS ENDPOINT DEMONSTRATION")
    print("=" * 50)
    
    # Get API keys
    public_key = os.getenv("MARVEL_PUBLIC_KEY")
    private_key = os.getenv("MARVEL_PRIVATE_KEY")
    
    if not public_key or not private_key:
        print("❌ API keys not found")
        return
    
    # Initialize endpoint
    endpoint = CreatorsEndpoint(
        base_url="https://gateway.marvel.com",
        public_key=public_key,
        private_key=private_key,
    )
    
    # List creators
    print("\n📋 Listing creators...")
    creators = await endpoint.list_creators(
        first_name="Stan",
        limit=5
    )
    print(f"Found {creators.data.count} creators with first name 'Stan'")
    
    for creator in creators.data.results:
        print(f"  - {creator.full_name}")
    
    # Get specific creator
    print("\n👨‍💼 Getting Stan Lee...")
    stan_lee = await endpoint.get_creator(30)
    print(f"Creator: {stan_lee.full_name}")
    print(f"Comics: {stan_lee.comics.available}")
    print(f"Series: {stan_lee.series.available}")
    
    # Get creator's comics
    print("\n📚 Getting Stan Lee's comics...")
    stan_comics = await endpoint.get_comics(30, limit=3)
    print(f"Stan Lee worked on {stan_comics.data.total} comics (showing first 3):")
    
    for comic in stan_comics.data.results:
        print(f"  - {comic.title}")
    
    # Note: Creator-character relationships are not available in the Marvel API
    print("\n📝 Note: Creator-character relationships are not available in the Marvel API")
    print("   The API only provides creator-comic, creator-series, creator-event, and creator-story relationships")


async def main() -> None:
    """Demonstrate all endpoint classes with real API calls."""
    # Get API keys from environment variables
    public_key = os.getenv("MARVEL_PUBLIC_KEY")
    private_key = os.getenv("MARVEL_PRIVATE_KEY")

    if not public_key or not private_key:
        print("❌ Please set MARVEL_PUBLIC_KEY and MARVEL_PRIVATE_KEY environment variables")
        print("You can get these from https://developer.marvel.com/")
        return

    try:
        print("🚀 Marvelpy v1.0.0 - Endpoint Classes Demonstration")
        print("=" * 60)
        print("This demo showcases all 6 endpoint classes with real API calls")
        print("These endpoint classes will be integrated into the enhanced MarvelClient")
        print("=" * 60)
        
        # Demonstrate all endpoint classes
        await demonstrate_characters_endpoint()
        await demonstrate_comics_endpoint()
        await demonstrate_events_endpoint()
        await demonstrate_series_endpoint()
        await demonstrate_stories_endpoint()
        await demonstrate_creators_endpoint()
        
        print("\n\n🎉 ENDPOINT DEMONSTRATION COMPLETE!")
        print("=" * 60)
        print("✅ All 6 endpoint classes demonstrated successfully")
        print("✅ Type-safe models working perfectly")
        print("✅ Real API calls completed")
        print("✅ Comprehensive functionality showcased")
        print("✅ Ready for integration into enhanced MarvelClient")
        print("\nKey Benefits of Endpoint Architecture:")
        print("🔹 Clean separation of concerns")
        print("🔹 Type-safe method signatures")
        print("🔹 Comprehensive filtering options")
        print("🔹 Related resource access")
        print("🔹 Consistent error handling")
        print("🔹 Easy to extend and maintain")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
