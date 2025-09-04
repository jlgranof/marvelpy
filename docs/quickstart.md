# Quick Start

Get up and running with Marvelpy in minutes!

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

### Getting Characters

```python
async def get_characters():
    async with MarvelClient("your_public_key", "your_private_key") as client:
        # Get a list of characters
        characters = await client.get_characters(params={"limit": 5})
        print(f"Found {characters['data']['count']} characters")

        # Show first character
        if characters['data']['results']:
            first_char = characters['data']['results'][0]
            print(f"First character: {first_char['name']}")

asyncio.run(get_characters())
```

### Searching for Characters

```python
async def search_characters():
    async with MarvelClient("your_public_key", "your_private_key") as client:
        # Search for Iron Man
        results = await client.get_characters(params={"name": "iron man"})

        if results['data']['results']:
            iron_man = results['data']['results'][0]
            print(f"Found: {iron_man['name']} (ID: {iron_man['id']})")

asyncio.run(search_characters())
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

## What's Available

Currently, Marvelpy v0.2.0 includes:

- **MarvelClient** - Full-featured async client for Marvel API
- **Authentication** - Automatic Marvel API authentication
- **Character Access** - Search and retrieve character information
- **Error Handling** - Robust retry logic and error management
- **Type Safety** - Complete type hints throughout
- **Test Suite** - Comprehensive tests with 85% coverage
- **Documentation** - Full API documentation with examples

## Coming Soon

Future versions will include:

- **Comics** - Access comic book data and metadata
- **Events** - Marvel universe events and storylines
- **Series** - Comic series information
- **Stories** - Individual story details
- **Creators** - Creator and artist information
- **Advanced Search** - More sophisticated filtering options
- **Caching** - Built-in response caching
- **Rate Limiting** - Automatic rate limit management

## Next Steps

- Check out the [API Reference](api/hello.md) for detailed documentation
- See the [Installation Guide](installation.md) for setup instructions
- Visit our [GitHub repository](https://github.com/jlgranof/marvelpy) for the latest updates
