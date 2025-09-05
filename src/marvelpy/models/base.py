"""Base model classes for Marvel API responses."""

from typing import Generic, List, TypeVar

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field

T = TypeVar("T")


class BaseModel(PydanticBaseModel):  # type: ignore[misc]
    """Base model class with common configuration."""

    model_config = ConfigDict(
        extra="allow",  # Allow extra fields from API
        validate_assignment=True,
        use_enum_values=True,
    )


class BaseResponse(BaseModel, Generic[T]):
    """Base response wrapper for single items."""

    code: int = Field(..., description="HTTP status code")
    status: str = Field(..., description="Status message")
    copyright: str = Field(..., description="Copyright notice")
    attribution_text: str = Field(..., alias="attributionText", description="Attribution text")
    attribution_html: str = Field(..., alias="attributionHTML", description="Attribution HTML")
    etag: str = Field(..., description="ETag for caching")
    data: T = Field(..., description="Response data")


class BaseListResponse(BaseModel, Generic[T]):
    """Base response wrapper for list items."""

    code: int = Field(..., description="HTTP status code")
    status: str = Field(..., description="Status message")
    copyright: str = Field(..., description="Copyright notice")
    attribution_text: str = Field(..., alias="attributionText", description="Attribution text")
    attribution_html: str = Field(..., alias="attributionHTML", description="Attribution HTML")
    etag: str = Field(..., description="ETag for caching")
    data: "DataContainer[T]" = Field(..., description="Response data container")


class DataContainer(BaseModel, Generic[T]):
    """Container for list response data."""

    offset: int = Field(..., description="Number of skipped results")
    limit: int = Field(..., description="Maximum number of results returned")
    total: int = Field(..., description="Total number of results available")
    count: int = Field(..., description="Number of results returned in this response")
    results: List[T] = Field(..., description="List of results")
