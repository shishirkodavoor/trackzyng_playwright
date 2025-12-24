import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from config.config import (
    ADMIN_USERNAME,
    ADMIN_PASSWORD,
    USER_USERNAME,
    USER_PASSWORD,
)
from utils.test_helpers import ensure_fresh_session

# LOGIN PAGE

def test_login_page_loads(page):
    """
    Login page should load successfully
    """
    ensure_fresh_session(page)

    login = LoginPage(page)
    login.open()

    assert page.url.startswith("http")
    assert page.title() != ""

# ADMIN LOGIN (AUTHORIZED)

def test_admin_login_success(page):
    """
    Admin credentials should be able to access dashboard
    """
    ensure_fresh_session(page)

    login = LoginPage(page)
    login.open()
    login.login(ADMIN_USERNAME, ADMIN_PASSWORD)

    # URL is the source of truth
    page.wait_for_url("**/dashboard**", timeout=15000)

    assert "/dashboard" in page.url


def test_dashboard_visible_after_admin_login(page):
    """
    Dashboard should be reachable after admin login
 """
    ensure_fresh_session(page)

    login = LoginPage(page)
    dashboard = DashboardPage(page)

    login.open()
    login.login(ADMIN_USERNAME, ADMIN_PASSWORD)

    page.wait_for_url("**/dashboard**", timeout=15000)

    # Soft UI assertion (not critical)
    header = page.locator(dashboard.header)
    header.wait_for(state="visible", timeout=15000)
    assert header.is_visible()

# EMAIL NORMALIZATION 

@pytest.mark.parametrize(
    "username,password",
    [
        (" kranjith@codezyng.com  ", ADMIN_PASSWORD),
        ("KRANJITH@CODEZYNG.COM", ADMIN_PASSWORD),
    ],
)
def test_login_with_trimmed_and_uppercase_email(page, username, password):
    """
    Backend trims spaces and normalizes email case
    """
    ensure_fresh_session(page)

    login = LoginPage(page)
    login.open()
    login.login(username, password)

    page.wait_for_url("**/dashboard**", timeout=15000)
    assert "/dashboard" in page.url

# USER LOGIN (NOT AUTHORIZED)

def test_user_login_not_authorized(page):
   
    ensure_fresh_session(page)

    login = LoginPage(page)
    login.open()
    login.login(USER_USERNAME, USER_PASSWORD)

    # Give auth + routing time
    page.wait_for_timeout(3000)

    # User should never reach dashboard
    assert "/dashboard" not in page.url

# DIRECT DASHBOARD ACCESS PROTECTION

def test_dashboard_url_blocked_without_login(page):
    ensure_fresh_session(page)

    page.goto(
        "https://staging.portal.trackzyng.codezyng.com/dashboard",
        wait_until="domcontentloaded"
    )

    # Wait until redirect finishes
    page.wait_for_function(
        "() => !window.location.pathname.includes('dashboard')",
        timeout=10000
    )

    assert "/dashboard" not in page.url



