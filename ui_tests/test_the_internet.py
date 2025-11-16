import pytest
from playwright.sync_api import Page

from ui_tests.conftest import base_url

BASE_URL = "https://the-internet.herokuapp.com"
VALID_USERNAME = "tomsmith"
VALID_PASSWORD = "SuperSecretPassword!"

pytestmark = pytest.mark.ui


def test_successful_login_displays_success_banner(page: Page):
    """Happy path login flow on the classic Herokuapp form."""
    page.goto(f"{base_url}/login")
    page.get_by_label("Username").fill(VALID_USERNAME)
    page.get_by_label("Password").fill(VALID_PASSWORD)
    page.get_by_role("button", name="Login").click()

    assert page.url.endswith("/secure"), "Expected redirect to /secure area"
    flash_text = page.locator("#flash").inner_text()
    assert "You logged into a secure area!" in flash_text


def test_failed_login_rejects_user(page: Page):
    """Negative login to demonstrate form validation feedback."""
    page.goto(f"{BASE_URL}/login")
    page.get_by_label("Username").fill(VALID_USERNAME)
    page.get_by_label("Password").fill("WrongPassword")
    page.get_by_role("button", name="Login").click()

    assert page.url.endswith("/login")
    flash_text = page.locator("#flash").inner_text()
    assert "Your password is invalid!" in flash_text


def test_checkboxes_can_be_toggled(page: Page):
    """Checks basic state changes on an accessible checkbox list."""
    page.goto(f"{BASE_URL}/checkboxes")

    checkboxes = page.locator("#checkboxes input")
    first_box = checkboxes.nth(0)
    second_box = checkboxes.nth(1)

    first_box.check()
    assert first_box.is_checked()

    second_box.uncheck()
    assert not second_box.is_checked()
