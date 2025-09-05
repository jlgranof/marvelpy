# Marvelpy

A fully-typed Python client for the Marvel Comics API.

## Features

- 🚀 **Async-first design** - Built with modern async/await patterns
- 🔒 **Fully typed** - Complete type hints for better IDE support
- 📚 **Comprehensive** - Full coverage of the Marvel Comics API
- 🛡️ **Enterprise-ready** - Production-grade error handling and retry logic
- 📖 **Well documented** - Extensive documentation and examples

## Quick Example

```python
import asyncio
from marvelpy import MarvelClient

async def main():
    async with MarvelClient("your_public_key", "your_private_key") as client:
        # Get characters
        characters = await client.get_characters(params={"limit": 5})
        print(f"Found {characters['data']['count']} characters")

        # Search for specific characters
        iron_man = await client.get_characters(params={"name": "iron man"})
        print(f"Iron Man: {iron_man['data']['results'][0]['name']}")

asyncio.run(main())
```

## Installation

```bash
pip install marvelpy
```

## What's Next?

- Check out the [Installation Guide](installation.md) for detailed setup instructions
- Follow the [Quick Start Guide](quickstart.md) to get up and running
- Browse the [API Reference](api/hello.md) for detailed documentation

## Development Status

**Current Version: v0.2.1**

This package now includes a fully functional MarvelClient with character access, authentication, and comprehensive error handling.

### What's Available

- **MarvelClient** - Full-featured async client for Marvel API
- **Authentication** - Automatic Marvel API authentication
- **Character Access** - Search and retrieve character information
- **Error Handling** - Robust retry logic and error management
- **Type Safety** - Complete type hints throughout
- **Test Suite** - Comprehensive tests with 85% coverage
- **Documentation** - Full API documentation with examples

### Coming Soon

Future versions will include:

- **Comics** - Access comic book data and metadata
- **Events** - Marvel universe events and storylines
- **Series** - Comic series information
- **Stories** - Individual story details
- **Creators** - Creator and artist information
- **Advanced Search** - More sophisticated filtering options
- **Caching** - Built-in response caching
- **Rate Limiting** - Automatic rate limit management

## Contributing

We welcome contributions! Please see our [Contributing Guide](contributing.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
