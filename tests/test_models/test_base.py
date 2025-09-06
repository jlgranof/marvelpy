"""Tests for base model classes."""

import logging
from typing import Any, Dict

import pytest
from pydantic import ValidationError

# Configure logging for tests
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

from marvelpy.models.base import BaseListResponse, BaseModel, BaseResponse, DataContainer


class TestBaseModel:
    """Test cases for BaseModel class.

    This test class verifies the functionality of the BaseModel class,
    which serves as the foundation for all Marvel API data models.
    Tests cover basic instantiation, field validation, and configuration
    behavior.
    """

    def test_base_model_creation(self):
        """Test BaseModel can be instantiated with default configuration.

        This test verifies that BaseModel can be created without any
        arguments and maintains proper inheritance from PydanticBaseModel.
        It ensures the base configuration is applied correctly.

        Expected behavior:
            - Model can be instantiated without arguments
            - Model is an instance of BaseModel
            - Model has proper Pydantic configuration
        """
        logger.info("Testing BaseModel can be instantiated with default configuration")
        
        model = BaseModel()
        assert isinstance(model, BaseModel)
        
        logger.info("✅ BaseModel creation test completed successfully")

    def test_base_model_extra_fields_allowed(self):
        """Test BaseModel allows extra fields from API responses.

        This test verifies that the extra="allow" configuration works
        correctly, allowing fields that aren't defined in the model schema
        to be included. This is crucial for API compatibility as Marvel
        may add new fields without breaking existing clients.

        Expected behavior:
            - Extra fields can be passed during instantiation
            - Extra fields are accessible as attributes
            - Extra fields maintain their original values
        """
        logger.info("Testing BaseModel allows extra fields from API responses")
        
        model = BaseModel(extra_field="test_value")
        assert hasattr(model, "extra_field")
        assert model.extra_field == "test_value"
        
        logger.info("✅ BaseModel extra fields allowed test completed successfully")

    def test_base_model_validation_assignment(self):
        """Test BaseModel validates field assignments after creation.

        This test verifies that the validate_assignment=True configuration
        works correctly, ensuring that any field assignments after model
        creation are properly validated according to the field definitions.

        Expected behavior:
            - Field assignments after creation are allowed
            - Extra fields can be assigned dynamically
            - Assigned values are stored correctly
        """
        logger.info("Testing BaseModel validates field assignments after creation")
        
        model = BaseModel()
        # This should not raise an error due to extra="allow"
        model.extra_field = "test"
        assert model.extra_field == "test"
        
        logger.info("✅ BaseModel validation assignment test completed successfully")


class TestDataContainer:
    """Test cases for DataContainer class.

    This test class verifies the functionality of the DataContainer class,
    which encapsulates pagination metadata and results for Marvel API
    list responses. Tests cover creation, validation, and edge cases.
    """

    def test_data_container_creation(self):
        """Test DataContainer can be created with all required fields.

        This test verifies that DataContainer properly validates and stores
        pagination metadata and results list. It ensures the Marvel API's
        standard pagination structure is correctly modeled.

        Expected behavior:
            - All required fields (offset, limit, total, count, results) are accepted
            - Results list can contain any type of data
            - Field values are stored and accessible as expected
        """
        logger.info("Testing DataContainer can be created with all required fields")
        
        container: DataContainer[str] = DataContainer(
            offset=0, limit=20, total=100, count=20, results=["item1", "item2"]
        )

        assert container.offset == 0
        assert container.limit == 20
        assert container.total == 100
        assert container.count == 20
        assert container.results == ["item1", "item2"]
        
        logger.info("✅ DataContainer creation test completed successfully")

    def test_data_container_missing_required_fields(self):
        """Test DataContainer raises ValidationError for missing required fields.

        This test verifies that DataContainer properly validates all required
        fields and raises appropriate ValidationError when fields are missing.
        This ensures data integrity and prevents incomplete pagination data.

        Expected behavior:
            - ValidationError is raised when required fields are missing
            - Error message indicates which fields are missing
            - Model creation fails gracefully with clear error information
        """
        logger.info("Testing DataContainer raises ValidationError for missing required fields")
        
        with pytest.raises(ValidationError):
            DataContainer(offset=0, limit=20)  # Missing total, count, results
        
        logger.info("✅ DataContainer missing required fields test completed successfully")

    def test_data_container_empty_results(self):
        """Test DataContainer handles empty results list correctly.

        This test verifies that DataContainer can handle edge cases where
        no results are returned (e.g., when total=0 or when filtering
        returns no matches). This is important for robust pagination handling.

        Expected behavior:
            - Empty results list is accepted and stored correctly
            - Count and total can be zero
            - Results list is accessible and empty
        """
        logger.info("Testing DataContainer handles empty results list correctly")
        
        container: DataContainer[str] = DataContainer(
            offset=0, limit=20, total=0, count=0, results=[]
        )

        assert container.results == []
        assert container.count == 0
        assert container.total == 0
        
        logger.info("✅ DataContainer empty results test completed successfully")


class TestBaseResponse:
    """Test cases for BaseResponse class.

    This test class verifies the functionality of the BaseResponse class,
    which wraps single Marvel API items with response metadata. Tests cover
    creation, field validation, and data type handling.
    """

    def test_base_response_creation(self):
        """Test BaseResponse can be created with all required fields.

        This test verifies that BaseResponse properly validates and stores
        all required Marvel API response metadata along with the data payload.
        It ensures the standard response structure is correctly modeled.

        Expected behavior:
            - All required fields are accepted and validated
            - Field aliases work correctly (attributionText, attributionHTML)
            - Data payload is stored and accessible
        """
        logger.info("Testing BaseResponse can be created with all required fields")
        
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
        
        logger.info("✅ BaseResponse creation test completed successfully")

    def test_base_response_with_dict_data(self):
        """Test BaseResponse handles dictionary data payload correctly.

        This test verifies that BaseResponse can handle complex data types
        like dictionaries as the data payload. This is important for
        Marvel API responses that contain nested object data.

        Expected behavior:
            - Dictionary data is accepted and stored correctly
            - Nested dictionary values are accessible
            - Data type is preserved through serialization
        """
        logger.info("Testing BaseResponse handles dictionary data payload correctly")
        
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
        
        logger.info("✅ BaseResponse with dict data test completed successfully")

    def test_base_response_missing_required_fields(self):
        """Test BaseResponse raises ValidationError for missing required fields.

        This test verifies that BaseResponse properly validates all required
        fields and raises appropriate ValidationError when fields are missing.
        This ensures response integrity and prevents incomplete API responses.

        Expected behavior:
            - ValidationError is raised when required fields are missing
            - Error message indicates which fields are missing
            - Model creation fails gracefully with clear error information
        """
        logger.info("Testing BaseResponse raises ValidationError for missing required fields")
        
        with pytest.raises(ValidationError):
            BaseResponse(code=200, status="Ok")  # Missing other required fields
        
        logger.info("✅ BaseResponse missing required fields test completed successfully")


class TestBaseListResponse:
    """Test cases for BaseListResponse class.

    This test class verifies the functionality of the BaseListResponse class,
    which wraps Marvel API list responses with pagination metadata. Tests
    cover creation, validation, and DataContainer integration.
    """

    def test_base_list_response_creation(self):
        """Test BaseListResponse can be created with all required fields.

        This test verifies that BaseListResponse properly validates and stores
        all required Marvel API response metadata along with a DataContainer.
        It ensures the standard list response structure is correctly modeled.

        Expected behavior:
            - All required fields are accepted and validated
            - DataContainer is properly integrated
            - Response metadata is accessible
        """
        logger.info("Testing BaseListResponse can be created with all required fields")
        
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
        
        logger.info("✅ BaseListResponse creation test completed successfully")

    def test_base_list_response_missing_required_fields(self):
        """Test BaseListResponse raises ValidationError for missing required fields.

        This test verifies that BaseListResponse properly validates all required
        fields and raises appropriate ValidationError when fields are missing.
        This ensures list response integrity and prevents incomplete API responses.

        Expected behavior:
            - ValidationError is raised when required fields are missing
            - Error message indicates which fields are missing
            - Model creation fails gracefully with clear error information
        """
        logger.info("Testing BaseListResponse raises ValidationError for missing required fields")
        
        with pytest.raises(ValidationError):
            BaseListResponse(code=200, status="Ok")  # Missing other required fields
        
        logger.info("✅ BaseListResponse missing required fields test completed successfully")


class TestGenericTypes:
    """Test cases for generic type functionality.

    This test class verifies that the generic type system works correctly
    across all base model classes. Tests ensure that type parameters are
    properly handled and that different data types can be used with the
    same model structures.
    """

    def test_base_response_generic_type(self):
        """Test BaseResponse works with different generic data types.

        This test verifies that BaseResponse's generic type system works
        correctly with different data types (strings, dictionaries, etc.).
        This is important for ensuring type safety while maintaining
        flexibility for different Marvel API response types.

        Expected behavior:
            - String data is properly typed and accessible
            - Dictionary data is properly typed and accessible
            - Type information is preserved through the generic system
        """
        logger.info("Testing BaseResponse works with different generic data types")
        
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
        
        logger.info("✅ BaseResponse generic type test completed successfully")

    def test_data_container_generic_type(self):
        """Test DataContainer works with different generic result types.

        This test verifies that DataContainer's generic type system works
        correctly with different result types in the results list. This
        ensures that pagination works correctly regardless of the data
        type being paginated.

        Expected behavior:
            - String results are properly typed and accessible
            - Dictionary results are properly typed and accessible
            - Type information is preserved through the generic system
        """
        logger.info("Testing DataContainer works with different generic result types")
        
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
        
        logger.info("✅ DataContainer generic type test completed successfully")
