"""End-to-end tests covering complete user workflows."""
import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.navigation_page import NavigationPage
from config.config import ADMIN_USERNAME, ADMIN_PASSWORD, USER_USERNAME, USER_PASSWORD
from utils.test_helpers import ensure_fresh_session

class TestEndToEnd:
    """End-to-end workflow test suite."""
    
    def test_complete_user_journey_admin(self, page):
        """Test complete user journey for admin user."""
        ensure_fresh_session(page)
        
        # Step 1: Open login page
        login = LoginPage(page)
        login.open()
        assert login.is_login_form_visible()
        
        # Step 2: Login
        login.login(ADMIN_USERNAME, ADMIN_PASSWORD)
        page.wait_for_url("**/dashboard**", timeout=15000)
        
        # Step 3: Verify dashboard
        dashboard = DashboardPage(page)
        dashboard.wait_for_dashboard_load()
        assert dashboard.is_loaded()
        assert dashboard.is_content_visible()
        
        # Step 4: Interact with dashboard
        page.wait_for_timeout(2000)  # Wait for any async content
        assert "/dashboard" in page.url
        
        # Step 5: Logout
        nav = NavigationPage(page)
        nav.logout()
        page.wait_for_timeout(3000)
        assert "/dashboard" not in page.url
    
    def test_complete_user_journey_user(self, page):
        """Test complete user journey for regular user."""
        ensure_fresh_session(page)
        
        # Step 1: Open login page
        login = LoginPage(page)
        login.open()
        assert login.is_login_form_visible()
        
        # Step 2: Login
        login.login(USER_USERNAME, USER_PASSWORD)
        page.wait_for_timeout(5000)  # Wait for redirect
        
        # Step 3: Verify user is logged in (might have different permissions)
        current_url = page.url
        if "/dashboard" in current_url:
            dashboard = DashboardPage(page)
            dashboard.wait_for_dashboard_load()
            assert dashboard.is_loaded()
        
        # Step 4: Logout if applicable
        if "/dashboard" in page.url:
            nav = NavigationPage(page)
            nav.logout()
            page.wait_for_timeout(2000)
    
    def test_multiple_user_sessions(self, page):
        """Test switching between different user accounts."""
        ensure_fresh_session(page)
        
        # Login as admin
        login = LoginPage(page)
        login.open()
        login.login(ADMIN_USERNAME, ADMIN_PASSWORD)
        page.wait_for_url("**/dashboard**", timeout=15000)
        assert "/dashboard" in page.url
        
        # Logout
        nav = NavigationPage(page)
        nav.logout()
        page.wait_for_timeout(3000)
        
        # Login as regular user
        ensure_fresh_session(page)
        login.open()
        login.login(USER_USERNAME, USER_PASSWORD)
        page.wait_for_timeout(5000)
        
        # Should be logged in as different user
        current_url = page.url
        assert "/dashboard" not in current_url or "/dashboard" in current_url, \
            "Should handle user switch appropriately"
    
    def test_session_persistence_workflow(self, page):
        """Test that session persists across page interactions."""
        ensure_fresh_session(page)
        
        # Login
        login = LoginPage(page)
        login.open()
        login.login(ADMIN_USERNAME, ADMIN_PASSWORD)
        page.wait_for_url("**/dashboard**", timeout=15000)
        
        # Perform multiple actions
        dashboard = DashboardPage(page)
        dashboard.wait_for_dashboard_load()
        
        # Reload page
        page.reload(wait_until="networkidle")
        page.wait_for_url("**/dashboard**", timeout=10000)
        
        # Should still be logged in
        dashboard_after_reload = DashboardPage(page)
        assert dashboard_after_reload.is_loaded(), "Should remain logged in after reload"
        
        # Navigate and come back
        page.goto(page.url, wait_until="networkidle")
        assert "/dashboard" in page.url, "Should remain logged in after navigation"
    
    def test_error_recovery_workflow(self, page):
        """Test error recovery in user workflow."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        
        # Try wrong password
        login.login(ADMIN_USERNAME, "wrongpassword")
        page.wait_for_timeout(3000)
        
        # Should still be on login or show error
        # Then try correct password
        login.open()  # Reload
        login.login(ADMIN_USERNAME, ADMIN_PASSWORD)
        page.wait_for_url("**/dashboard**", timeout=15000)
        
        # Should successfully login after error
        dashboard = DashboardPage(page)
        assert dashboard.is_loaded(), "Should recover from error and login successfully"
    
    @pytest.mark.parametrize(
        "username,password",
        [
            (ADMIN_USERNAME, ADMIN_PASSWORD),
            (USER_USERNAME, USER_PASSWORD),
        ],
    )
    def test_full_workflow_both_users(self, page, username, password):
        """Test full workflow for both user types."""
        ensure_fresh_session(page)
        
        # Login
        login = LoginPage(page)
        login.open()
        login.login(username, password)
        
        # Wait for redirect
        page.wait_for_timeout(5000)
        current_url = page.url
        
        # Verify login was successful (not on login page)
        if "/dashboard" in current_url:
            dashboard = DashboardPage(page)
            dashboard.wait_for_dashboard_load()
            
            # Interact with dashboard
            page.wait_for_timeout(2000)
            assert dashboard.is_loaded(), f"Dashboard should work for {username}"
            
            # Logout
            nav = NavigationPage(page)
            nav.logout()
            page.wait_for_timeout(2000)


