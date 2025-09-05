"""Tests for base model classes."""

from typing import Any, Dict

import pytest
from pydantic import ValidationError

from marvelpy.models.base import BaseListResponse, BaseModel, BaseResponse, DataContainer


class TestBaseModel:
    """Test cases for BaseModel."""

    def test_base_model_creation(self):
        """Test BaseModel can be instantiated with data."""
        model = BaseModel()
        assert isinstance(model, BaseModel)

    def test_base_model_extra_fields_allowed(self):
        """Test BaseModel allows extra fields."""
        model = BaseModel(extra_field="test_value")
        assert hasattr(model, "extra_field")
        assert model.extra_field == "test_value"

    def test_base_model_validation_assignment(self):
        """Test BaseModel validates assignment."""
        model = BaseModel()
        # This should not raise an error due to extra="allow"
        model.extra_field = "test"
        assert model.extra_field == "test"


class TestDataContainer:
    """Test cases for DataContainer."""

    def test_data_container_creation(self):
        """Test DataContainer can be created with required fields."""
        container: DataContainer[str] = DataContainer(
            offset=0, limit=20, total=100, count=20, results=["item1", "item2"]
        )

        assert container.offset == 0
        assert container.limit == 20
        assert container.total == 100
        assert container.count == 20
        assert container.results == ["item1", "item2"]

    def test_data_container_missing_required_fields(self):
        """Test DataContainer raises ValidationError for missing fields."""
        with pytest.raises(ValidationError):
            DataContainer(offset=0, limit=20)  # Missing total, count, results

    def test_data_container_empty_results(self):
        """Test DataContainer with empty results list."""
        container: DataContainer[str] = DataContainer(
            offset=0, limit=20, total=0, count=0, results=[]
        )

        assert container.results == []
        assert container.count == 0
        assert container.total == 0


class TestBaseResponse:
    """Test cases for BaseResponse."""

    def test_base_response_creation(self):
        """Test BaseResponse can be created with required fields."""
        response: BaseResponse[str] = BaseResponse(
            code=200,
            status="Ok",
            copyright="© 2024 MARVEL",
            attributionText="Data provided by Marvel. © 2024 MARVEL",
            attributionHTML="<a href='http://marvel.com'>Data provided by Marvel. © 2024 MARVEL</a>",
            etag="etag123",
            data="test_data",
        )

        assert response.code == 200
        assert response.status == "Ok"
        assert response.copyright == "© 2024 MARVEL"
        assert response.attribution_text == "Data provided by Marvel. © 2024 MARVEL"
        assert (
            response.attribution_html
            == "<a href='http://marvel.com'>Data provided by Marvel. © 2024 MARVEL</a>"
        )
        assert response.etag == "etag123"
        assert response.data == "test_data"

    def test_base_response_with_dict_data(self):
        """Test BaseResponse with dictionary data."""
        data: Dict[str, Any] = {"id": 1, "name": "Test Character"}
        response: BaseResponse[Dict[str, Any]] = BaseResponse(
            code=200,
            status="Ok",
            copyright="© 2024 MARVEL",
            attributionText="Data provided by Marvel. © 2024 MARVEL",
            attributionHTML="<a href='http://marvel.com'>Data provided by Marvel. © 2024 MARVEL</a>",
            etag="etag123",
            data=data,
        )

        assert response.data == data
        assert response.data["id"] == 1
        assert response.data["name"] == "Test Character"

    def test_base_response_missing_required_fields(self):
        """Test BaseResponse raises ValidationError for missing fields."""
        with pytest.raises(ValidationError):
            BaseResponse(code=200, status="Ok")  # Missing other required fields


class TestBaseListResponse:
    """Test cases for BaseListResponse."""

    def test_base_list_response_creation(self):
        """Test BaseListResponse can be created with required fields."""
        data_container: DataContainer[str] = DataContainer(
            offset=0, limit=20, total=100, count=20, results=["item1", "item2"]
        )

        response: BaseListResponse[str] = BaseListResponse(
            code=200,
            status="Ok",
            copyright="© 2024 MARVEL",
            attributionText="Data provided by Marvel. © 2024 MARVEL",
            attributionHTML="<a href='http://marvel.com'>Data provided by Marvel. © 2024 MARVEL</a>",
            etag="etag123",
            data=data_container,
        )

        assert response.code == 200
        assert response.status == "Ok"
        assert response.copyright == "© 2024 MARVEL"
        assert response.attribution_text == "Data provided by Marvel. © 2024 MARVEL"
        assert (
            response.attribution_html
            == "<a href='http://marvel.com'>Data provided by Marvel. © 2024 MARVEL</a>"
        )
        assert response.etag == "etag123"
        assert response.data == data_container
        assert response.data.results == ["item1", "item2"]

    def test_base_list_response_missing_required_fields(self):
        """Test BaseListResponse raises ValidationError for missing fields."""
        with pytest.raises(ValidationError):
            BaseListResponse(code=200, status="Ok")  # Missing other required fields


class TestGenericTypes:
    """Test cases for generic type functionality."""

    def test_base_response_generic_type(self):
        """Test BaseResponse works with different data types."""
        # Test with string data
        str_response: BaseResponse[str] = BaseResponse(
            code=200,
            status="Ok",
            copyright="© 2024 MARVEL",
            attributionText="Data provided by Marvel. © 2024 MARVEL",
            attributionHTML="<a href='http://marvel.com'>Data provided by Marvel. © 2024 MARVEL</a>",
            etag="etag123",
            data="string_data",
        )
        assert str_response.data == "string_data"

        # Test with dict data
        dict_response: BaseResponse[Dict[str, str]] = BaseResponse(
            code=200,
            status="Ok",
            copyright="© 2024 MARVEL",
            attributionText="Data provided by Marvel. © 2024 MARVEL",
            attributionHTML="<a href='http://marvel.com'>Data provided by Marvel. © 2024 MARVEL</a>",
            etag="etag123",
            data={"key": "value"},
        )
        assert dict_response.data == {"key": "value"}

    def test_data_container_generic_type(self):
        """Test DataContainer works with different result types."""
        # Test with string results
        str_container: DataContainer[str] = DataContainer(
            offset=0, limit=20, total=100, count=2, results=["item1", "item2"]
        )
        assert str_container.results == ["item1", "item2"]

        # Test with dict results
        dict_container: DataContainer[Dict[str, int]] = DataContainer(
            offset=0, limit=20, total=100, count=2, results=[{"id": 1}, {"id": 2}]
        )
        assert dict_container.results == [{"id": 1}, {"id": 2}]
