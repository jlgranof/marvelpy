"""Example: Advanced usage patterns."""

import asyncio
import os

from marvelpy import MarvelClient

# Load environment variables
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


async def advanced_usage() -> None:
    """Demonstrate advanced usage patterns."""
    public_key = os.getenv("MARVEL_PUBLIC_KEY")
    private_key = os.getenv("MARVEL_PRIVATE_KEY")

    if not public_key or not private_key:
        print("❌ Please set MARVEL_PUBLIC_KEY and MARVEL_PRIVATE_KEY environment variables")
        return

    # Example 1: Custom client configuration
    print("🔧 Example 1: Custom client configuration")
    print("=" * 50)

    custom_client = MarvelClient(
        public_key=public_key,
        private_key=private_key,
        timeout=60.0,  # 60 second timeout
        max_retries=5,  # 5 retry attempts
    )

    try:
        characters = await custom_client.get_characters(params={"limit": 3})
        print(f"✅ Found {characters['data']['count']} characters with custom config")
    finally:
        await custom_client.close()

    # Example 2: Multiple concurrent requests
    print("\n🚀 Example 2: Multiple concurrent requests")
    print("=" * 50)

    async with MarvelClient(public_key, private_key) as client:
        # Create multiple tasks
        tasks = [
            client.get_characters(params={"name": "iron man"}),
            client.get_characters(params={"name": "hulk"}),
            client.get_characters(params={"name": "thor"}),
            client.get_characters(params={"name": "captain america"}),
            client.health_check(),
        ]

        # Execute all requests concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)

        print("✅ Concurrent requests completed:")
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"   {i + 1}. Error: {result}")
            else:
                # result is a dict, use type narrowing
                if "data" in result and "results" in result["data"]:  # type: ignore[operator,index]
                    if result["data"]["results"]:  # type: ignore[index]
                        char = result["data"]["results"][0]  # type: ignore[index]
                        print(f"   {i + 1}. {char['name']} (ID: {char['id']})")
                    else:
                        print(f"   {i + 1}. No results found")
                else:
                    print(f"   {i + 1}. Health check: {result.get('status', 'Unknown')}")  # type: ignore[union-attr]

    # Example 3: Character details analysis
    print("\n📊 Example 3: Character details analysis")
    print("=" * 50)

    async with MarvelClient(public_key, private_key) as client:
        # Get Iron Man details
        iron_man_results = await client.get_characters(params={"name": "iron man"})

        if iron_man_results["data"]["results"]:
            iron_man = iron_man_results["data"]["results"][0]

            print(f"📋 Character Analysis: {iron_man['name']}")
            print(f"   ID: {iron_man['id']}")
            print(f"   Description: {iron_man.get('description', 'No description')[:100]}...")
            print(f"   Comics: {iron_man['comics']['available']}")
            print(f"   Series: {iron_man['series']['available']}")
            print(f"   Stories: {iron_man['stories']['available']}")
            print(f"   Events: {iron_man['events']['available']}")

            # Show some comics
            if iron_man["comics"]["items"]:
                print("   Recent Comics:")
                for comic in iron_man["comics"]["items"][:3]:
                    print(f"     - {comic['name']}")

    # Example 4: Pagination example
    print("\n📄 Example 4: Pagination")
    print("=" * 50)

    async with MarvelClient(public_key, private_key) as client:
        page_size = 5
        total_pages = 3

        for page in range(total_pages):
            offset = page * page_size
            characters = await client.get_characters(params={"limit": page_size, "offset": offset})

            print(f"📄 Page {page + 1} (offset {offset}):")
            for char in characters["data"]["results"]:
                print(f"   - {char['name']} (ID: {char['id']})")

    print("\n🎉 Advanced usage examples complete!")


if __name__ == "__main__":
    asyncio.run(advanced_usage())
