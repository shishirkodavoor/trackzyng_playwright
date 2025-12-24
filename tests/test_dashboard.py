import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from config.config import ADMIN_USERNAME, ADMIN_PASSWORD
def test_dashboard_visible_after_login(page):
    """Dashboard should be visible after login."""
    login = LoginPage(page)
    dashboard = DashboardPage(page)

    login.open()
    login.login(ADMIN_USERNAME, ADMIN_PASSWORD)

    page.wait_for_url("**/dashboard**", timeout=15000)

    dashboard_header = page.locator(dashboard.header)
    dashboard_header.wait_for(state="visible", timeout=15000)
    assert dashboard_header.is_visible()
