"""
Tests for configuration
"""
import pytest
from src.config import Settings


def test_settings_defaults():
    """Test default settings"""
    settings = Settings()
    assert settings.algorithm == "HS256"
    assert settings.access_token_expire_minutes == 30
    assert settings.api_host == "0.0.0.0"
    assert settings.api_port == 8000


def test_settings_custom():
    """Test custom settings"""
    settings = Settings(
        api_port=9000,
        debug=True
    )
    assert settings.api_port == 9000
    assert settings.debug == True