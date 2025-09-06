"""Example: Error handling and retry logic."""

import asyncio
import os

from marvelpy import MarvelClient

# Load environment variables
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


async def demonstrate_error_handling() -> None:
    """Demonstrate error handling capabilities."""
    public_key = os.getenv("MARVEL_PUBLIC_KEY")
    private_key = os.getenv("MARVEL_PRIVATE_KEY")

    if not public_key or not private_key:
        print("❌ Please set MARVEL_PUBLIC_KEY and MARVEL_PRIVATE_KEY environment variables")
        return

    async with MarvelClient(public_key, private_key) as client:
        try:
            print("🧪 Testing error handling scenarios...")
            print("=" * 50)

            # Test 1: Valid request
            print("\n✅ Test 1: Valid request")
            try:
                characters = await client.list_characters(limit=1)
                print(f"   Success: Found {characters.data.count} character")
            except Exception as e:
                print(f"   Error: {e}")

            # Test 2: Non-existent character ID
            print("\n❌ Test 2: Non-existent character ID")
            try:
                result = await client.get_character(999999999)
                print(f"   Unexpected success: {result}")
            except Exception as e:
                print(f"   Expected error: {type(e).__name__}")

            # Test 3: Invalid endpoint
            print("\n❌ Test 3: Invalid endpoint")
            try:
                # This would be an invalid method call
                result = await client.get_character(-1)
                print(f"   Unexpected success: {result}")
            except Exception as e:
                print(f"   Expected error: {type(e).__name__}")

            # Test 4: Health check
            print("\n✅ Test 4: Health check")
            try:
                # Test a simple API call instead
                status = await client.list_characters(limit=1)
                print("   API Status: Success")
                print(f"   Found: {status.data.count} characters")
            except Exception as e:
                print(f"   Error: {e}")

            # Test 5: Custom timeout (very short)
            print("\n⏱️ Test 5: Custom timeout")
            try:
                # Create client with very short timeout
                fast_client = MarvelClient(
                    public_key,
                    private_key,
                    timeout=0.001,  # 1ms timeout
                )
                await fast_client.list_characters()
                await fast_client.close()
                print("   Unexpected success with short timeout")
            except Exception as e:
                print(f"   Expected timeout error: {type(e).__name__}")

            print("\n🎉 Error handling demonstration complete!")

        except Exception as e:
            print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    asyncio.run(demonstrate_error_handling())
