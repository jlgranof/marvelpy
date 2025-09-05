"""Base model classes for Marvel API responses."""

from typing import Generic, List, TypeVar

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field

T = TypeVar("T")


class BaseModel(PydanticBaseModel):  # type: ignore[misc]
    """Base model class for all Marvel API data models.

    This class provides common configuration for all Marvel API response models,
    including field validation, extra field handling, and enum value processing.

    Configuration:
        - extra="allow": Allows additional fields from the API that aren't defined
          in the model schema, ensuring compatibility with API changes
        - validate_assignment=True: Validates field assignments after model creation
          to maintain data integrity
        - use_enum_values=True: Uses enum values instead of enum objects for
          serialization compatibility

    Example:
        >>> class Character(BaseModel):
        ...     name: str
        ...     id: int
        >>> char = Character(name="Iron Man", id=1009368, extra_field="allowed")
        >>> char.name
        'Iron Man'
    """

    model_config = ConfigDict(
        extra="allow",  # Allow extra fields from API
        validate_assignment=True,
        use_enum_values=True,
    )


class BaseResponse(BaseModel, Generic[T]):
    """Base response wrapper for single Marvel API items.

    This class represents the standard Marvel API response structure for single
    items (e.g., a single character, comic, event, etc.). It includes metadata
    about the response and the actual data payload.

    Attributes:
        code: HTTP status code returned by the API
        status: Human-readable status message from the API
        copyright: Copyright notice from Marvel
        attribution_text: Text attribution required by Marvel API terms
        attribution_html: HTML attribution required by Marvel API terms
        etag: ETag header value for caching purposes
        data: The actual data payload of type T

    Example:
        >>> response = BaseResponse(
        ...     code=200,
        ...     status="Ok",
        ...     copyright="© 2024 MARVEL",
        ...     attributionText="Data provided by Marvel. © 2024 MARVEL",
        ...     attributionHTML="<a href='http://marvel.com'>Data provided by Marvel. © 2024 MARVEL</a>",
        ...     etag="etag123",
        ...     data={"id": 1009368, "name": "Iron Man"}
        ... )
        >>> response.data["name"]
        'Iron Man'
    """

    code: int = Field(..., description="HTTP status code")
    status: str = Field(..., description="Status message")
    copyright: str = Field(..., description="Copyright notice")
    attribution_text: str = Field(..., alias="attributionText", description="Attribution text")
    attribution_html: str = Field(..., alias="attributionHTML", description="Attribution HTML")
    etag: str = Field(..., description="ETag for caching")
    data: T = Field(..., description="Response data")


class BaseListResponse(BaseModel, Generic[T]):
    """Base response wrapper for Marvel API list responses.

    This class represents the standard Marvel API response structure for list
    endpoints (e.g., characters, comics, events, etc.). It includes metadata
    about the response and a DataContainer with pagination information and results.

    Attributes:
        code: HTTP status code returned by the API
        status: Human-readable status message from the API
        copyright: Copyright notice from Marvel
        attribution_text: Text attribution required by Marvel API terms
        attribution_html: HTML attribution required by Marvel API terms
        etag: ETag header value for caching purposes
        data: DataContainer containing pagination metadata and results list

    Example:
        >>> response = BaseListResponse(
        ...     code=200,
        ...     status="Ok",
        ...     copyright="© 2024 MARVEL",
        ...     attributionText="Data provided by Marvel. © 2024 MARVEL",
        ...     attributionHTML="<a href='http://marvel.com'>Data provided by Marvel. © 2024 MARVEL</a>",
        ...     etag="etag123",
        ...     data=DataContainer(
        ...         offset=0,
        ...         limit=20,
        ...         total=100,
        ...         count=20,
        ...         results=[{"id": 1009368, "name": "Iron Man"}]
        ...     )
        ... )
        >>> response.data.results[0]["name"]
        'Iron Man'
    """

    code: int = Field(..., description="HTTP status code")
    status: str = Field(..., description="Status message")
    copyright: str = Field(..., description="Copyright notice")
    attribution_text: str = Field(..., alias="attributionText", description="Attribution text")
    attribution_html: str = Field(..., alias="attributionHTML", description="Attribution HTML")
    etag: str = Field(..., description="ETag for caching")
    data: "DataContainer[T]" = Field(..., description="Response data container")


class DataContainer(BaseModel, Generic[T]):
    """Container for Marvel API list response data with pagination metadata.

    This class encapsulates the pagination information and results list that
    comes with Marvel API list responses. It provides all the necessary
    information for implementing pagination in client applications.

    Attributes:
        offset: Number of results skipped (used for pagination)
        limit: Maximum number of results returned in this response
        total: Total number of results available across all pages
        count: Number of results actually returned in this response
        results: List of actual data items of type T

    Example:
        >>> container = DataContainer(
        ...     offset=0,
        ...     limit=20,
        ...     total=100,
        ...     count=20,
        ...     results=[{"id": 1009368, "name": "Iron Man"}]
        ... )
        >>> container.total
        100
        >>> len(container.results)
        1
        >>> container.has_more_pages()
        True  # if total > offset + count
    """

    offset: int = Field(..., description="Number of skipped results")
    limit: int = Field(..., description="Maximum number of results returned")
    total: int = Field(..., description="Total number of results available")
    count: int = Field(..., description="Number of results returned in this response")
    results: List[T] = Field(..., description="List of results")
