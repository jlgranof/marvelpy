# Marvelpy Examples

This directory contains examples demonstrating how to use the Marvelpy v1.0.0 client with the new type-safe model system.

## Prerequisites

1. **Marvel API Keys**: Get your API keys from [Marvel Developer Portal](https://developer.marvel.com/)
2. **Environment Variables**: Set your API keys as environment variables:
   ```bash
   export MARVEL_PUBLIC_KEY="your_public_key_here"
   export MARVEL_PRIVATE_KEY="your_private_key_here"
   ```

## Examples

### Basic Usage (Type-Safe Models)

```bash
python examples/basic_usage.py
```

This example demonstrates:
- Creating a MarvelClient instance with v1.0.0
- Testing API connection
- Fetching characters with full type safety
- Using Pydantic v2 models for validation
- IntelliSense support and type hints

### Models Demo

```bash
python examples/models_demo.py
```

This example demonstrates:
- All Marvel API entities (Characters, Comics, Events, Series, Stories, Creators)
- Type-safe model usage for each entity type
- Converting API responses to Pydantic v2 models
- Full async/await support
- Enterprise-grade error handling

### Character Search

```bash
python examples/character_search.py
```

This example demonstrates:
- Searching for popular Marvel characters
- Character filtering and pagination
- Handling search results with type safety
- Character metadata analysis

### Error Handling

```bash
python examples/error_handling.py
```

This example demonstrates:
- Valid and invalid API requests
- Error handling patterns with type-safe models
- Timeout configuration
- Health check functionality

### Advanced Usage

```bash
python examples/advanced_usage.py
```

This example demonstrates:
- Custom client configuration
- Concurrent request handling
- Character details analysis with models
- Pagination patterns

## Running Examples

Make sure you have the package installed in development mode:

```bash
pip install -e .
```

Then run any example:

```bash
python examples/basic_usage.py
```

## API Key Setup

1. Visit [Marvel Developer Portal](https://developer.marvel.com/)
2. Sign up for a free account
3. Generate your API keys
4. Set them as environment variables:

```bash
# On macOS/Linux
export MARVEL_PUBLIC_KEY="your_public_key"
export MARVEL_PRIVATE_KEY="your_private_key"

# On Windows
set MARVEL_PUBLIC_KEY=your_public_key
set MARVEL_PRIVATE_KEY=your_private_key
```

## Rate Limits

The Marvel API has rate limits:
- 3000 requests per day
- 100 requests per hour

The client includes automatic retry logic for server errors, but be mindful of these limits in your applications.
