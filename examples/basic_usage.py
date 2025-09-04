"""Basic usage example for MarvelClient."""

import asyncio
import os

from marvelpy import MarvelClient

# Try to load from .env file if it exists
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, use system env vars


async def main() -> None:
    """Demonstrate basic MarvelClient usage."""
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
            print("Testing API connection...")
            health = await client.health_check()
            print(f"API Status: {health}")

            # Get some characters
            print("\nFetching characters...")
            characters = await client.get_characters(params={"limit": 5})
            print(f"Found {characters['data']['count']} characters")

            # Show first character details
            if characters["data"]["results"]:
                first_char = characters["data"]["results"][0]
                print(f"First character: {first_char['name']}")
                print(f"Character ID: {first_char['id']}")

            # Search for specific characters
            print("\nSearching for Iron Man...")
            search_results = await client.get_characters(params={"name": "iron man"})
            print(f"Found {search_results['data']['count']} characters matching 'iron man'")
            if search_results["data"]["results"]:
                for char in search_results["data"]["results"][:3]:
                    print(f"  - {char['name']} (ID: {char['id']})")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
