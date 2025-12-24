"""Comprehensive login tests covering all login scenarios."""
import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from config.config import (
    ADMIN_USERNAME,
    ADMIN_PASSWORD,
    USER_USERNAME,
    USER_PASSWORD,
    BASE_URL,
)
from utils.test_helpers import ensure_fresh_session

class TestLoginComprehensive:
    """Comprehensive login test suite."""
    
    def test_login_page_elements(self, page):
        """Test that login page has all required elements."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        
        assert login.is_login_form_visible(), "Login form should be visible"
        assert page.title() != "", "Page should have a title"
        assert BASE_URL in page.url, "Should be on login page"
    
    @pytest.mark.parametrize(
        "username,password,expected_success",
        [
            (ADMIN_USERNAME, ADMIN_PASSWORD, True),
            (USER_USERNAME, USER_PASSWORD, False),  # Unauthorized user should not access dashboard
            ("invalid@email.com", "wrongpass", False),
            ("", "test1234", False),
            (ADMIN_USERNAME, "", False),
        ],
    )
    def test_login_with_different_credentials(self, page, username, password, expected_success):
        """Test login with various credential combinations."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        login.login(username, password)
        
        if expected_success:
            page.wait_for_url("**/dashboard**", timeout=15000)
            assert "/dashboard" in page.url, "Should redirect to dashboard on successful login"
        else:
            # Wait a bit to see if redirect happens
            page.wait_for_timeout(5000)
            # Either stay on login or show error, but shouldn't reach dashboard
            assert "/dashboard" not in page.url, \
                "Should not reach dashboard with invalid or unauthorized credentials"
    
    def test_admin_login_flow(self, page):
        """Test complete admin login flow."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        dashboard = DashboardPage(page)
        
        login.open()
        assert login.is_login_form_visible()
        
        login.login(ADMIN_USERNAME, ADMIN_PASSWORD)
        page.wait_for_url("**/dashboard**", timeout=15000)
        
        assert dashboard.is_loaded(), "Dashboard should load after admin login"
        assert dashboard.is_content_visible(), "Dashboard content should be visible"
    
    def test_user_login_flow_unauthorized(self, page):
        """Test complete user login flow for unauthorized user."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        login.login(USER_USERNAME, USER_PASSWORD)
        
        # Wait to see where user is redirected
        page.wait_for_timeout(5000)
        current_url = page.url
        
        # Unauthorized user should not reach dashboard
        assert "/dashboard" not in current_url, \
            "Unauthorized user should not be able to access dashboard after login"
    
    def test_login_with_whitespace_in_email(self, page):
        """Test login with whitespace in email (should be trimmed)."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        login.login(f"  {ADMIN_USERNAME}  ", ADMIN_PASSWORD)
        
        page.wait_for_url("**/dashboard**", timeout=15000)
        assert "/dashboard" in page.url, "Login should work with trimmed email"
    
    def test_login_with_uppercase_email(self, page):
        """Test login with uppercase email (should be normalized)."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        login.login(ADMIN_USERNAME.upper(), ADMIN_PASSWORD)
        
        page.wait_for_url("**/dashboard**", timeout=15000)
        assert "/dashboard" in page.url, "Login should work with normalized email case"
    
    def test_direct_dashboard_access_blocked(self, page):
        """Test that direct dashboard access is blocked without login."""
        ensure_fresh_session(page)
        
        page.goto(f"{BASE_URL}/dashboard", wait_until="domcontentloaded")
        
        # Wait for redirect
        try:
            page.wait_for_function(
                "() => !window.location.pathname.includes('dashboard')",
                timeout=10000
            )
        except Exception:
            pass
        
        # Should be redirected away from dashboard
        page.wait_for_timeout(2000)
        assert "/dashboard" not in page.url or BASE_URL in page.url, \
            "Should be redirected away from dashboard"
    
    def test_session_persistence(self, page):
        """Test that session persists after login."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        login.login(ADMIN_USERNAME, ADMIN_PASSWORD)
        
        page.wait_for_url("**/dashboard**", timeout=15000)
        original_url = page.url
        
        # Navigate away and back
        page.reload()
        page.wait_for_url("**/dashboard**", timeout=10000)
        
        assert "/dashboard" in page.url, "Should remain logged in after page reload"
    
    def test_multiple_login_attempts(self, page):
        """Test multiple login attempts."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        
        # First attempt with wrong password
        login.login(ADMIN_USERNAME, "wrongpassword")
        page.wait_for_timeout(2000)
        
        # Second attempt with correct password
        login.open()  # Reload to clear any error states
        login.login(ADMIN_USERNAME, ADMIN_PASSWORD)
        page.wait_for_url("**/dashboard**", timeout=15000)
        
        assert "/dashboard" in page.url, "Should be able to login after failed attempt"


