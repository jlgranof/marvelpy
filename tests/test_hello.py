"""Tests for the hello module."""

import logging

from marvelpy.hello import hello_world

# Configure logging for tests
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_hello_world():
    """Test the hello_world function."""
    logger.info("Testing hello_world function")
    
    result = hello_world()
    assert result == "Hello from Marvelpy!"
    assert isinstance(result, str)
    
    logger.info("✅ hello_world test completed successfully")


def test_hello_world_returns_string():
    """Test that hello_world returns a string type."""
    logger.info("Testing hello_world returns string type")
    
    result = hello_world()
    assert isinstance(result, str)
    assert len(result) > 0
    
    logger.info("✅ hello_world string type test completed successfully")


def test_hello_world_contains_marvelpy():
    """Test that hello_world contains the package name."""
    logger.info("Testing hello_world contains Marvelpy")
    
    result = hello_world()
    assert "Marvelpy" in result
    
    logger.info("✅ hello_world Marvelpy content test completed successfully")
