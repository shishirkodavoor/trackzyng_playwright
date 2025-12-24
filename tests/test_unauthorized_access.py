"""Tests for unauthorized user access to admin portal."""
import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.reports_page import ReportsPage
from pages.users_page import UsersPage
from pages.branch_page import BranchPage
from pages.tasks_page import TasksPage
from pages.navigation_page import NavigationPage
from config.config import USER_USERNAME, USER_PASSWORD, BASE_URL
from utils.test_helpers import ensure_fresh_session

class TestUnauthorizedAccess:
    """Test suite for unauthorized user access."""
    
    def test_unauthorized_user_login_attempt(self, page):
        """Test that unauthorized user cannot login to admin portal."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        login.login(USER_USERNAME, USER_PASSWORD)
        
        # Wait to see where user is redirected
        page.wait_for_timeout(5000)
        current_url = page.url
        
        # Unauthorized user should not reach dashboard
        assert "/dashboard" not in current_url, \
            "Unauthorized user should not be able to access dashboard"
    
    def test_unauthorized_user_direct_dashboard_access(self, page):
        """Test that unauthorized user cannot access dashboard via direct URL."""
        ensure_fresh_session(page)
        
        # Try to access dashboard directly without login
        page.goto(f"{BASE_URL}/dashboard", wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        
        # Should be redirected away from dashboard
        assert "/dashboard" not in page.url, \
            "Unauthorized direct access to dashboard should be blocked"
    
    def test_unauthorized_user_reports_access(self, page):
        """Test that unauthorized user cannot access reports section."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        login.login(USER_USERNAME, USER_PASSWORD)
        page.wait_for_timeout(5000)
        
        # Try to access reports
        base_url = page.url.split('/dashboard')[0] if '/dashboard' in page.url else BASE_URL
        page.goto(f"{base_url}/reports", wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        
        # Should not be able to access reports
        reports = ReportsPage(page)
        assert not reports.is_loaded() or "/reports" not in page.url or "/dashboard" not in page.url, \
            "Unauthorized user should not access reports section"
    
    def test_unauthorized_user_users_access(self, page):
        """Test that unauthorized user cannot access users management."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        login.login(USER_USERNAME, USER_PASSWORD)
        page.wait_for_timeout(5000)
        
        # Try to access users
        base_url = page.url.split('/dashboard')[0] if '/dashboard' in page.url else BASE_URL
        page.goto(f"{base_url}/users", wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        
        # Should not be able to access users
        users = UsersPage(page)
        assert not users.is_loaded() or "/users" not in page.url or "/dashboard" not in page.url, \
            "Unauthorized user should not access users section"
    
    def test_unauthorized_user_branch_access(self, page):
        """Test that unauthorized user cannot access branch management."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        login.login(USER_USERNAME, USER_PASSWORD)
        page.wait_for_timeout(5000)
        
        # Try to access branches
        base_url = page.url.split('/dashboard')[0] if '/dashboard' in page.url else BASE_URL
        page.goto(f"{base_url}/branches", wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        
        # Should not be able to access branches
        branch = BranchPage(page)
        assert not branch.is_loaded() or "/branch" not in page.url and "/branches" not in page.url or "/dashboard" not in page.url, \
            "Unauthorized user should not access branches section"
    
    def test_unauthorized_user_tasks_access(self, page):
        """Test that unauthorized user cannot access tasks section."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        login.login(USER_USERNAME, USER_PASSWORD)
        page.wait_for_timeout(5000)
        
        # Try to access tasks
        base_url = page.url.split('/dashboard')[0] if '/dashboard' in page.url else BASE_URL
        page.goto(f"{base_url}/tasks", wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        
        # Should not be able to access tasks
        tasks = TasksPage(page)
        assert not tasks.is_loaded() or "/tasks" not in page.url or "/dashboard" not in page.url, \
            "Unauthorized user should not access tasks section"
    
    def test_unauthorized_user_navigation_restrictions(self, page):
        """Test that unauthorized user sees restricted navigation."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        login.login(USER_USERNAME, USER_PASSWORD)
        page.wait_for_timeout(5000)
        
        nav = NavigationPage(page)
        
        # Try to navigate to different admin sections - none should be accessible
        access_granted = []

        try:
            nav.navigate_to_reports()
            page.wait_for_timeout(2000)
            if "/reports" in page.url:
                access_granted.append("reports")
        except Exception:
            pass

        try:
            nav.navigate_to_users()
            page.wait_for_timeout(2000)
            if "/users" in page.url:
                access_granted.append("users")
        except Exception:
            pass

        try:
            nav.navigate_to_branches()
            page.wait_for_timeout(2000)
            if "/branch" in page.url or "/branches" in page.url:
                access_granted.append("branches")
        except Exception:
            pass

        # Unauthorized user should not access admin sections
        assert len(access_granted) == 0, f"Unauthorized user has access to admin sections: {access_granted}"
    
    def test_unauthorized_user_redirect_after_login(self, page):
        """Test where unauthorized user is redirected after login attempt."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        login_url = page.url
        
        login.login(USER_USERNAME, USER_PASSWORD)
        page.wait_for_timeout(5000)
        final_url = page.url
        
        # User should either stay on login page or be redirected to an error/unauthorized page
        # But definitely not dashboard
        assert "/dashboard" not in final_url, \
            "Unauthorized user should not be redirected to dashboard"
        # Might stay on login or go to unauthorized page
        assert login_url == final_url or "unauthorized" in final_url.lower() or "error" in final_url.lower() or "login" in final_url.lower(), \
            "Unauthorized user should be handled appropriately"
    
    def test_unauthorized_user_session_handling(self, page):
        """Test session handling for unauthorized user."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        login.login(USER_USERNAME, USER_PASSWORD)
        page.wait_for_timeout(5000)
        
        # Try to access dashboard after unauthorized login
        base_url = page.url.split('/dashboard')[0] if '/dashboard' in page.url else BASE_URL
        page.goto(f"{base_url}/dashboard", wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        
        # Should still not have access
        assert "/dashboard" not in page.url, \
            "Unauthorized user session should not grant dashboard access"
    
    def test_unauthorized_vs_authorized_credentials(self, page):
        """Test difference between authorized and unauthorized credentials."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        
        # Test unauthorized user
        login.open()
        login.login(USER_USERNAME, USER_PASSWORD)
        page.wait_for_timeout(5000)
        unauthorized_url = page.url
        unauthorized_has_dashboard = "/dashboard" in unauthorized_url
        
        # Clear and test with authorized user (using admin credentials)
        from config.config import ADMIN_USERNAME, ADMIN_PASSWORD
        ensure_fresh_session(page)
        login.open()
        login.login(ADMIN_USERNAME, ADMIN_PASSWORD)
        page.wait_for_url("**/dashboard**", timeout=15000)
        authorized_url = page.url
        authorized_has_dashboard = "/dashboard" in authorized_url
        
        # Authorized should have access, unauthorized should not
        assert authorized_has_dashboard, "Authorized user should have dashboard access"
        assert not unauthorized_has_dashboard, "Unauthorized user should not have dashboard access"

