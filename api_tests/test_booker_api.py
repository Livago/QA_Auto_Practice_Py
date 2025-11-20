import pytest

pytestmark = [pytest.mark.smoke]


def test_create_token_positive(api_client, valid_auth_payload):
    """Valid credentials should yield a token so we can perform admin actions."""
    response = api_client.post("/auth", json=valid_auth_payload)
    assert response.status_code == 200

    body = response.json()
    assert body.get("token"), "Expected API to return a non-empty token"


def test_create_token_negative(api_client, invalid_auth_payload):
    """Broken credentials must return an error without exposing sensitive data."""
    response = api_client.post("/auth", json=invalid_auth_payload)
    assert response.status_code == 200, "Service returns 200 with an explanatory reason"
    assert response.json()["reason"] == "Bad credentials"


def test_get_booking_positive(api_client):
    """The booking list should be a non-empty collection of identifiers."""
    response = api_client.get("/booking")
    assert response.status_code == 200

    bookings = response.json()
    assert isinstance(bookings, list) and bookings, "Booking collection is empty"
    assert all("bookingid" in item for item in bookings[:5])


def test_create_booking_returns_payload_clone(api_client, booking_payload):
    """Verify that booking creation echoes the payload back to the caller."""
    response = api_client.post("/booking", json=booking_payload)
    assert response.status_code == 200

    body = response.json()
    created_booking = body["booking"]

    # Ensure every field in the payload was stored correctly.
    for key, value in booking_payload.items():
        assert created_booking[key] == value


def test_update_booking_replaces_entire_record(api_client, created_booking, authorized_headers):
    """PUT should replace the booking with a brand-new payload."""
    booking_id = created_booking["id"]
    updated_payload = {
        "firstname": "Jane",
        "lastname": "Smith",
        "totalprice": 200,
        "depositpaid": False,
        "bookingdates": created_booking["payload"]["bookingdates"],
        "additionalneeds": "Airport pickup",
    }
    headers = {**authorized_headers, "Content-Type": "application/json"}

    response = api_client.put(f"/booking/{booking_id}", json=updated_payload, headers=headers)
    assert response.status_code == 200

    updated_body = response.json()
    assert updated_body["firstname"] == "Jane"
    assert updated_body["lastname"] == "Smith"
    assert updated_body["additionalneeds"] == "Airport pickup"


def test_partial_update_booking_changes_subset(api_client, created_booking, authorized_headers):
    """PATCH is useful for tweaking only a few attributes without rebuilding payloads."""
    booking_id = created_booking["id"]
    patch_payload = {"firstname": "Alex", "additionalneeds": "Dinner"}
    headers = {**authorized_headers, "Content-Type": "application/json"}

    response = api_client.patch(f"/booking/{booking_id}", json=patch_payload, headers=headers)
    assert response.status_code == 200

    patched = response.json()
    assert patched["firstname"] == "Alex"
    assert patched["additionalneeds"] == "Dinner"


def test_delete_booking_removes_record(api_client, booking_payload, authorized_headers):
    """Delete should make the booking unreachable afterwards."""
    create_response = api_client.post("/booking", json=booking_payload)
    create_response.raise_for_status()
    booking_id = create_response.json()["bookingid"]

    delete_response = api_client.delete(f"/booking/{booking_id}", headers=authorized_headers)
    assert delete_response.status_code == 201  # API returns 201 on successful delete

    # After deletion the API responds with 404 for GET.
    verify_response = api_client.get(f"/booking/{booking_id}")
    assert verify_response.status_code == 404
