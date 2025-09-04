"""Example: Character search and filtering."""

import asyncio
import os

from marvelpy import MarvelClient

# Load environment variables
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


async def search_characters() -> None:
    """Demonstrate character search functionality."""
    public_key = os.getenv("MARVEL_PUBLIC_KEY")
    private_key = os.getenv("MARVEL_PRIVATE_KEY")

    if not public_key or not private_key:
        print("❌ Please set MARVEL_PUBLIC_KEY and MARVEL_PRIVATE_KEY environment variables")
        return

    async with MarvelClient(public_key, private_key) as client:
        try:
            # Search for popular characters
            popular_heroes = [
                "iron man",
                "hulk",
                "thor",
                "captain america",
                "wolverine",
                "spider-man",
                "peter parker",  # Spider-Man's real name
            ]

            print("🔍 Searching for popular Marvel characters...")
            print("=" * 50)

            for hero in popular_heroes:
                print(f"\n🔍 Searching for: {hero}")
                try:
                    results = await client.get_characters(params={"name": hero})

                    if results["data"]["results"]:
                        character = results["data"]["results"][0]
                        print(f"✅ Found: {character['name']} (ID: {character['id']})")
                        print(f"   Comics: {character['comics']['available']}")
                        print(f"   Series: {character['series']['available']}")
                        print(f"   Stories: {character['stories']['available']}")
                    else:
                        print(f"❌ No results found for '{hero}'")

                except Exception as e:
                    print(f"❌ Error searching for '{hero}': {e}")

            # Get characters with pagination
            print("\n📄 Getting characters with pagination...")
            print("=" * 50)

            characters = await client.get_characters(params={"limit": 10, "offset": 0})
            print(f"✅ Found {characters['data']['count']} characters (showing first 10)")
            print(f"📊 Total available: {characters['data']['total']}")

            for i, char in enumerate(characters["data"]["results"][:5], 1):
                print(f"{i}. {char['name']} (ID: {char['id']})")

        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(search_characters())
