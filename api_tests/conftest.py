import pytest
from utils.api_client import ApiClient


@pytest.fixture(scope="session")
def api_client():
    """Shared API client for all API tests."""
    return ApiClient()
