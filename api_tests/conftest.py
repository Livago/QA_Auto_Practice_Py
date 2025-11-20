from datetime import date, timedelta

import pytest
from utils.api_client import ApiClient


@pytest.fixture(scope="session")
def api_client():
    """Shared API client for all API tests."""
    return ApiClient()


@pytest.fixture(scope="session")
def valid_auth_payload():
    """Credentials provided by the Restful Booker documentation."""
    return {"username": "admin", "password": "password123"}


@pytest.fixture
def invalid_auth_payload(valid_auth_payload):
    """Helper payload with incorrect password for negative tests."""
    payload = valid_auth_payload.copy()
    payload["password"] = "wrong-password"
    return payload


@pytest.fixture(scope="session")
def auth_token(api_client, valid_auth_payload):
    """Generate an auth token once per session for destructive operations."""
    response = api_client.post("/auth", json=valid_auth_payload)
    response.raise_for_status()
    return response.json()["token"]


@pytest.fixture
def authorized_headers(auth_token):
    """Base headers carrying the auth cookie."""
    return {"Cookie": f"token={auth_token}"}


@pytest.fixture
def booking_payload():
    """Base booking payload used in multiple scenarios (cloned per test)."""
    today = date.today()
    return {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": today.isoformat(),
            "checkout": (today + timedelta(days=3)).isoformat(),
        },
        "additionalneeds": "Breakfast",
    }


@pytest.fixture
def created_booking(api_client, booking_payload, auth_token):
    """Create a booking before a test and ensure cleanup afterward."""
    response = api_client.post("/booking", json=booking_payload)
    response.raise_for_status()
    booking_id = response.json()["bookingid"]
    yield {"id": booking_id, "payload": booking_payload}
    # Use the auth token to delete the booking and keep the environment clean.
    api_client.delete(
        f"/booking/{booking_id}",
        headers={"Cookie": f"token={auth_token}"},
    )
