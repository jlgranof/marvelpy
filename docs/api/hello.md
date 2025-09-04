# Hello Module

The hello module provides a simple demonstration function for the Marvelpy package.

## Functions

::: marvelpy.hello.hello_world
    options:
      show_source: true
      show_root_heading: true
      show_root_toc_entry: true
      show_signature_annotations: true
      separate_signature: true
      show_bases: false
      show_submodules: false
      group_by_category: false
      members_order: source

## Examples

### Basic Usage

```python
from marvelpy.hello import hello_world

# Get the hello message
message = hello_world()
print(message)
# Output: "Hello from Marvelpy!"
```

### Type Checking

```python
from marvelpy.hello import hello_world

# The function returns a string
result = hello_world()
assert isinstance(result, str)
assert len(result) > 0
```

### Integration Example

```python
import marvelpy

# Using the function from the main package
def greet_user():
    return marvelpy.hello_world()

# Use in your application
greeting = greet_user()
print(f"Welcome! {greeting}")
```

## Notes

This is a demonstration function included in the initial release of Marvelpy. It serves as a placeholder while the full Marvel Comics API client is being developed.
