import pytest
from utils.api_client import ApiClient

@pytest.fixture(scope="module")
def api_client():
    return ApiClient()


def test_create_token_positive(api_client):
    """
    Проверка успешного создания токена при корректных данных
    """
    payload = {
        "username": "admin",
        "password": "password123"
    }

    response = api_client.post("/auth", data=payload)

    # Проверяем код ответа
    assert response.status_code == 200, f"Unexpected status: {response.status_code}, body: {response.text}"

    # Проверяем, что вернулся токен
    response_json = response.json()
    assert "token" in response_json, "Token not found in response"
    assert len(response_json["token"]) > 0


def test_create_token_negative(api_client):
    """
    Проверка ошибки при неверных данных
    """
    payload = {
        "username": "admin",
        "password": "wrongpassword"
    }

    response = api_client.post("/auth", data=payload)

    assert response.status_code == 200, "API не возвращает 200 при ошибке, нужно проверить поведение"
    assert response.json()["reason"] == "Bad credentials", "Сообщение об ошибке некорректно"

def test_get_booking_positive(api_client):
    """
    Проверка успешного получения списка всех бронирований
    """

    response = api_client.get("/booking")

    # Проверяем код ответа
    assert response.status_code == 200, f"Unexpected status: {response.status_code}, body: {response.text}"

    # Проверяем, что вернулся список бронирований
    response_json = response.json()
    assert isinstance(response_json, list), "Response is not a list"
    assert len(response_json) > 0, "Booking list is empty"

    for booking in response_json:
        assert "bookingid" in booking, f"Missing 'bookingid' in {booking}"