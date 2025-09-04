# MarvelClient

The main client class for interacting with the Marvel Comics API.

## Import

```python
from marvelpy import MarvelClient
```

## Constructor

```python
MarvelClient(
    public_key: str,
    private_key: str,
    base_url: Optional[str] = None,
    timeout: float = 30.0,
    max_retries: int = 3
)
```

### Parameters

- **public_key** (str): Marvel API public key
- **private_key** (str): Marvel API private key
- **base_url** (Optional[str]): Base URL for the Marvel API (defaults to official API)
- **timeout** (float): Request timeout in seconds (default: 30)
- **max_retries** (int): Maximum number of retry attempts (default: 3)

## Methods

### get

Make a GET request to the Marvel API.

```python
async def get(
    endpoint: str,
    params: Optional[Dict[str, Any]] = None,
    **kwargs: Any
) -> Dict[str, Any]
```

**Parameters:**
- **endpoint** (str): API endpoint path
- **params** (Optional[Dict[str, Any]]): Query parameters
- **kwargs**: Additional arguments for httpx request

**Returns:**
- Dict[str, Any]: JSON response data

**Example:**
```python
# Get a specific character
character = await client.get("characters/1009368")

# Get characters with parameters
characters = await client.get("characters", params={"limit": 10, "offset": 0})
```

### get_characters

Get characters from the Marvel API.

```python
async def get_characters(
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

**Parameters:**
- **params** (Optional[Dict[str, Any]]): Query parameters for filtering characters

**Returns:**
- Dict[str, Any]: Characters data from the API

**Example:**
```python
# Get all characters
characters = await client.get_characters()

# Get characters with limit
characters = await client.get_characters(params={"limit": 5})

# Search for specific characters
iron_man = await client.get_characters(params={"name": "iron man"})
```

### health_check

Check if the Marvel API is accessible.

```python
async def health_check() -> Dict[str, Any]
```

**Returns:**
- Dict[str, Any]: API status information

**Example:**
```python
status = await client.health_check()
print(f"API Status: {status['status']}")
```

## Context Manager

The MarvelClient supports async context manager for automatic resource cleanup:

```python
async with MarvelClient("public_key", "private_key") as client:
    # Use the client
    characters = await client.get_characters()
    # Client is automatically closed when exiting the context
```

## Error Handling

The client includes automatic retry logic for server errors (5xx) with exponential backoff:

```python
try:
    characters = await client.get_characters()
except httpx.HTTPError as e:
    print(f"HTTP error: {e}")
except httpx.RequestError as e:
    print(f"Request error: {e}")
```

## Authentication

Authentication is handled automatically. The client will add the required authentication parameters (apikey, ts, hash) to every request.

## Examples

### Basic Usage

```python
import asyncio
from marvelpy import MarvelClient

async def main():
    async with MarvelClient("your_public_key", "your_private_key") as client:
        # Health check
        status = await client.health_check()
        print(f"API Status: {status['status']}")
        
        # Get characters
        characters = await client.get_characters(params={"limit": 5})
        print(f"Found {characters['data']['count']} characters")
        
        # Search for Iron Man
        iron_man = await client.get_characters(params={"name": "iron man"})
        if iron_man['data']['results']:
            print(f"Found: {iron_man['data']['results'][0]['name']}")

asyncio.run(main())
```

### Custom Configuration

```python
async def main():
    # Custom timeout and retry settings
    client = MarvelClient(
        public_key="your_public_key",
        private_key="your_private_key",
        timeout=60.0,  # 60 second timeout
        max_retries=5  # 5 retry attempts
    )
    
    try:
        characters = await client.get_characters()
        print(f"Found {characters['data']['count']} characters")
    finally:
        await client.close()  # Don't forget to close!

asyncio.run(main())
```
