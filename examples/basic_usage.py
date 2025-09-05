"""Basic usage example for MarvelClient v1.0.0 with type-safe models."""

import asyncio
import os

from marvelpy import MarvelClient
from marvelpy.models import Character, CharacterListResponse

# Try to load from .env file if it exists
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, use system env vars


async def main() -> None:
    """Demonstrate basic MarvelClient usage with new type-safe models."""
    # Get API keys from environment variables (from .env file or system env)
    public_key = os.getenv("MARVEL_PUBLIC_KEY")
    private_key = os.getenv("MARVEL_PRIVATE_KEY")

    if not public_key or not private_key:
        print("Please set MARVEL_PUBLIC_KEY and MARVEL_PRIVATE_KEY environment variables")
        print("You can get these from https://developer.marvel.com/")
        return

    # Create client instance
    async with MarvelClient(public_key, private_key) as client:
        try:
            # Test health check
            print("🔍 Testing API connection...")
            health = await client.health_check()
            print(f"✅ API Status: {health['status']}")

            # Get some characters and convert to type-safe models
            print("\n🦸 Fetching characters with type-safe models...")
            characters_data = await client.get_characters(params={"limit": 5})
            response: CharacterListResponse = CharacterListResponse(**characters_data)
            print(f"Found {response.data.count} characters")

            # Show first character details with type hints
            if response.data.results:
                first_char: Character = response.data.results[0]
                print(f"First character: {first_char.name}")
                print(f"Character ID: {first_char.id}")
                print(
                    f"Description: {first_char.description[:100]}..."
                    if first_char.description
                    else "No description"
                )
                print(f"Comics available: {first_char.comics.available}")
                print(f"Series available: {first_char.series.available}")

            # Search for specific characters with type safety
            print("\n🔍 Searching for Iron Man with type-safe models...")
            search_data = await client.get_characters(params={"name": "iron man"})
            search_response: CharacterListResponse = CharacterListResponse(**search_data)
            print(f"Found {search_response.data.count} characters matching 'iron man'")

            if search_response.data.results:
                for char in search_response.data.results[:3]:
                    print(f"  - {char.name} (ID: {char.id})")
                    print(f"    Comics: {char.comics.available}, Series: {char.series.available}")

            print("\n🎉 Key Benefits of v1.0.0:")
            print("✅ Full type safety with Pydantic v2 models")
            print("✅ IntelliSense support in your IDE")
            print("✅ Runtime validation of API responses")
            print("✅ All Marvel API entities supported")

        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
