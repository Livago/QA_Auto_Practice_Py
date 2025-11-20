import pytest

from utils.api_client import ApiClient

JSON_PLACEHOLDER_BASE = "https://jsonplaceholder.typicode.com"

pytestmark = [pytest.mark.regression]


@pytest.fixture(scope="module")
def jsonplaceholder_client():
    """Shared client targeting JSONPlaceholder, a stable demo REST API."""
    return ApiClient(base_url=JSON_PLACEHOLDER_BASE)


def test_get_users_list_returns_ten_items(jsonplaceholder_client):
    """JSONPlaceholder always ships 10 users, so that is a stability check."""
    response = jsonplaceholder_client.get("/users")
    assert response.status_code == 200

    body = response.json()
    assert isinstance(body, list)
    assert len(body) == 10
    assert all("id" in user and "email" in user for user in body)


def test_get_single_user_details(jsonplaceholder_client):
    """User #1 should exist and contain predictable name/email fields."""
    response = jsonplaceholder_client.get("/users/1")
    assert response.status_code == 200

    user = response.json()
    assert user["id"] == 1
    assert user["username"] == "Bret"
    assert user["email"] == "Sincere@april.biz"


def test_create_post_returns_created_payload(jsonplaceholder_client):
    """POST /posts echoes back the payload and adds a generated id."""
    payload = {"title": "Playwright notes", "body": "JSONPlaceholder is great", "userId": 99}
    response = jsonplaceholder_client.post("/posts", json=payload)
    assert response.status_code == 201

    response_body = response.json()
    for key, value in payload.items():
        assert response_body[key] == value
    assert response_body["id"], "The API should allocate an id for the created post"


def test_nonexistent_endpoint_returns_404(jsonplaceholder_client):
    """Verify we get 404 when hitting a non-existent resource."""
    response = jsonplaceholder_client.get("/invalid")
    assert response.status_code == 404
