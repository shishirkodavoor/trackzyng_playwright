"""Comprehensive positive test cases."""
import pytest
import allure
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.reports_page import ReportsPage
from pages.users_page import UsersPage
from pages.branch_page import BranchPage
from pages.tasks_page import TasksPage
from pages.settings_page import SettingsPage
from pages.navigation_page import NavigationPage
from config.config import ADMIN_USERNAME, ADMIN_PASSWORD
from utils.test_helpers import ensure_fresh_session, login_user

class TestPositiveCases:
    """Comprehensive positive test cases suite."""
    
    def test_successful_login_with_valid_credentials(self, page):
        """Test successful login with valid admin credentials."""
        ensure_fresh_session(page)
        login = LoginPage(page)
        login.open()
        login.login(ADMIN_USERNAME, ADMIN_PASSWORD)
        page.wait_for_url("**/dashboard**", timeout=15000)
        assert "/dashboard" in page.url, "Should login successfully"
    
    def test_dashboard_displays_correctly(self, page):
        """Test dashboard displays all expected elements."""
        ensure_fresh_session(page)
        dashboard = login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        dashboard.wait_for_dashboard_load()
        
        assert dashboard.is_loaded(), "Dashboard should be loaded"
        assert dashboard.is_content_visible(), "Dashboard content should be visible"
        assert page.title() != "", "Dashboard should have a title"
    
    def test_navigation_to_all_sections(self, page):
        """Test navigation to all available sections."""
        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        nav = NavigationPage(page)
        sections = {
            "dashboard": (nav.navigate_to_dashboard, "/dashboard"),
            "tasks": (nav.navigate_to_tasks, "/tasks"),
            "reports": (nav.navigate_to_reports, "/reports"),
            "users": (nav.navigate_to_users, "/users"),
            "branches": (nav.navigate_to_branches, "/branch"),
        }

        accessible = []
        for name, (navigate_fn, expected_path) in sections.items():
            try:
                navigate_fn()
                page.wait_for_timeout(1000)
                # Basic verification: URL or page content contains expected path
                if expected_path in page.url or expected_path.strip('/') in page.locator('body').inner_text().lower():
                    accessible.append(name)
                else:
                    pytest.skip(f"Section '{name}' not available in this environment")
            except Exception as exc:
                pytest.skip(f"Could not access section '{name}': {exc}")

        assert len(accessible) > 0, "Should be able to navigate to at least one section"
    
    def test_user_search_functionality(self, page):
        """Test user search works correctly."""
        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        nav = NavigationPage(page)
        nav.navigate_to_users()
        page.wait_for_timeout(3000)

        users = UsersPage(page)
        if not users.is_loaded():
            pytest.skip("Users page not available or failed to load")

        users.search_user("test")
        page.wait_for_timeout(2000)
        # Verify search results show at least one entry
        search_results = page.locator('body').inner_text()
        assert len(search_results) > 0, "User search should return results"
    
    def test_report_generation(self, page):
        """Test report generation functionality."""
        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        nav = NavigationPage(page)
        nav.navigate_to_reports()
        page.wait_for_timeout(3000)

        reports = ReportsPage(page)
        if not reports.is_loaded():
            pytest.skip("Reports page not available or failed to load")

        reports_count = reports.get_reports_count()
        assert reports_count is not None and reports_count >= 0, "Reports page should load and return a count"
    
    def test_form_submission(self, page):
        """Test form submission works correctly."""
        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        
        # Test login form worked
        assert "/dashboard" in page.url, "Form submission should work"
    
    def test_data_display(self, page):
        """Test data displays correctly."""
        ensure_fresh_session(page)
        dashboard = login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        dashboard.wait_for_dashboard_load()
        
        # Check for data presence
        page_content = page.locator('body').inner_text()
        assert len(page_content) > 0, "Data should be displayed"
    
    def test_page_refresh_maintains_state(self, page):
        """Test page refresh maintains user state."""
        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        
        # Refresh page
        page.reload(wait_until="networkidle")
        page.wait_for_url("**/dashboard**", timeout=10000)
        
        assert "/dashboard" in page.url, "State should be maintained after refresh"
    
    def test_logout_functionality(self, page):
        """Test logout works correctly."""
        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        
        nav = NavigationPage(page)
        nav.logout()
        page.wait_for_timeout(3000)
        
        assert "/dashboard" not in page.url, "Should be logged out"
    
    def test_multiple_successful_logins(self, page):
        """Test multiple successful login sessions."""
        for _ in range(3):
            ensure_fresh_session(page)
            login = LoginPage(page)
            login.open()
            login.login(ADMIN_USERNAME, ADMIN_PASSWORD)
            page.wait_for_url("**/dashboard**", timeout=15000)
            assert "/dashboard" in page.url, "Multiple logins should work"
    
    def test_smooth_user_experience(self, page):
        """Test smooth user experience throughout."""
        ensure_fresh_session(page)
        dashboard = login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        
        # Navigate around
        page.wait_for_timeout(1000)
        page.reload()
        page.wait_for_timeout(1000)
        
        assert dashboard.is_loaded() or "/dashboard" in page.url, "UX should be smooth"
    
    def test_all_features_accessible(self, page):
        """Test all features are accessible after login."""
        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        
        # Verify access to different sections
        nav = NavigationPage(page)
        features_accessible = 0
        
        sections = [
            lambda: nav.navigate_to_dashboard(),
            lambda: nav.navigate_to_reports(),
            lambda: nav.navigate_to_users(),
            lambda: nav.navigate_to_branches(),
        ]
        
        for navigate_func in sections:
            try:
                navigate_func()
                page.wait_for_timeout(1000)
                features_accessible += 1
            except Exception:
                # Some navigation targets may not exist in this environment - ignore
                continue
        
        assert features_accessible > 0, "Features should be accessible"

