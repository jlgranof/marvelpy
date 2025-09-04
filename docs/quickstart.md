# Quick Start

Get up and running with Marvelpy in minutes!

## Basic Usage

Start with the hello world example:

```python
import marvelpy

# Get a greeting message
message = marvelpy.hello_world()
print(message)
# Output: "Hello from Marvelpy!"
```

## What's Available

Currently, Marvelpy v0.1.0 includes:

### Hello World Function

```python
from marvelpy.hello import hello_world

# Basic usage
result = hello_world()
print(result)  # "Hello from Marvelpy!"

# Check the type
print(type(result))  # <class 'str'>
```

## Coming Soon

The full Marvel Comics API client will include:

- **Characters** - Search and retrieve character information
- **Comics** - Access comic book data and metadata
- **Events** - Marvel universe events and storylines
- **Series** - Comic series information
- **Stories** - Individual story details
- **Creators** - Creator and artist information

## Example Future Usage

```python
# This is planned functionality - not yet implemented
import marvelpy

# Initialize the client
client = marvelpy.MarvelClient(api_key="your_key", private_key="your_private_key")

# Search for characters
characters = await client.characters.search("spider-man")

# Get character details
spiderman = await client.characters.get(1009610)

# Search comics
comics = await client.comics.search("amazing spider-man")
```

## Next Steps

- Check out the [API Reference](api/hello.md) for detailed documentation
- See the [Installation Guide](installation.md) for setup instructions
- Visit our [GitHub repository](https://github.com/jlgranof/marvelpy) for the latest updates
