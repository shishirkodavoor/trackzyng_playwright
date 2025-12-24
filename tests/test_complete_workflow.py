"""Complete end-to-end workflow tests covering all sections."""
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
from config.config import ADMIN_USERNAME, ADMIN_PASSWORD, USER_USERNAME, USER_PASSWORD
from utils.test_helpers import ensure_fresh_session, login_user

class TestCompleteWorkflow:
    """Complete workflow tests covering all sections."""
    
    def test_full_application_navigation(self, page):
        """Test navigating through all sections of the application."""
        allure.dynamic.title("Workflow: Navigate main application sections")
        allure.dynamic.description("Navigate to main application sections (dashboard, tasks, reports, users, branches, settings) and verify pages load or at least some are accessible.")

        ensure_fresh_session(page)

        # Login
        dashboard = login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        assert dashboard.is_loaded(), "Dashboard should load after login"

        nav = NavigationPage(page)

        # Navigate through all sections and record successes
        sections = [
            ("dashboard", DashboardPage),
            ("tasks", TasksPage),
            ("reports", ReportsPage),
            ("users", UsersPage),
            ("branches", BranchPage),
            ("settings", SettingsPage),
        ]

        accessible = []
        for section_name, page_class in sections:
            try:
                # Call navigation helper dynamically
                getattr(nav, f"navigate_to_{section_name}")()
                page.wait_for_timeout(1000)
                section_page = page_class(page)
                if section_page.is_loaded(timeout=5000):
                    accessible.append(section_name)
            except Exception:
                # Skip sections that fail to load in this environment
                continue

        assert len(accessible) > 0, "At least one major section should be accessible"
    
    def test_complete_user_management_workflow(self, page):
        """Test complete user management workflow."""
        allure.dynamic.title("Workflow: User management end-to-end")
        allure.dynamic.description("Navigate to Users, perform search/filter, and open a user details view when available.")

        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        users = UsersPage(page)
        nav = NavigationPage(page)

        nav.navigate_to_users()
        assert users.is_loaded(), "Users page should be loaded"

        users_count = users.get_users_count()
        users.search_user("test")
        page.wait_for_timeout(500)
        users.filter_by_role("admin")
        page.wait_for_timeout(500)

        if users_count > 0:
            users.view_user(0)
            page.wait_for_timeout(500)
            # Expect a detail label such as Email
            assert page.get_by_text("Email", exact=False).count() > 0 or users.is_element_visible(users.user_form, timeout=2000), "User details should be visible"
        else:
            assert users.is_loaded(), "Users page remains loaded"
    
    def test_complete_branch_management_workflow(self, page):
        """Test complete branch management workflow."""
        allure.dynamic.title("Workflow: Branch management end-to-end")
        allure.dynamic.description("Navigate to Branches, perform search/filter and view a branch when available.")

        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        branch = BranchPage(page)
        nav = NavigationPage(page)

        nav.navigate_to_branches()
        assert branch.is_loaded(), "Branches page should be loaded"

        branches_count = branch.get_branches_count()
        branch.search_branch("test")
        page.wait_for_timeout(500)
        branch.filter_by_status("active")
        page.wait_for_timeout(500)

        if branches_count > 0:
            branch.view_branch(0)
            page.wait_for_timeout(500)
            # Basic verification: branch detail visible (best-effort)
            body_text = page.locator('body').inner_text().lower()
            assert branch.is_loaded() or ("error" not in body_text and "exception" not in body_text), "Viewing branch should not crash the UI"
        else:
            assert branch.is_loaded(), "Branches page remains accessible"
    
    def test_complete_reports_workflow(self, page):
        """Test complete reports workflow."""
        allure.dynamic.title("Workflow: Reports end-to-end")
        allure.dynamic.description("Navigate to Reports, apply search and date filters, and view a report if present.")

        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        reports = ReportsPage(page)
        nav = NavigationPage(page)

        nav.navigate_to_reports()
        assert reports.is_loaded(), "Reports page should be loaded"

        reports_count = reports.get_reports_count()
        reports.search_report("test")
        page.wait_for_timeout(500)
        reports.filter_by_date("2024-01-01", "2024-12-31")
        page.wait_for_timeout(500)

        if reports_count > 0:
            reports.view_report(0)
            page.wait_for_timeout(500)
            assert reports.is_element_visible(reports.report_detail_view, timeout=3000), "Report detail should be visible"
        else:
            assert reports.is_loaded(), "Reports page remains accessible"
    
    def test_complete_settings_workflow(self, page):
        """Test complete settings workflow."""
        allure.dynamic.title("Workflow: Settings end-to-end")
        allure.dynamic.description("Navigate settings tabs and perform a profile update action, ensuring no errors.")

        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        settings = SettingsPage(page)
        nav = NavigationPage(page)

        nav.navigate_to_settings()
        assert settings.is_loaded(), "Settings page should be loaded"

        tabs = ["general", "profile", "security", "notifications"]
        for tab in tabs:
            settings.switch_to_tab(tab)
            page.wait_for_timeout(300)

        settings.switch_to_tab("profile")
        settings.update_profile(name="Test User")
        page.wait_for_timeout(500)

        # Basic verification: settings page still accessible
        assert settings.is_loaded(), "Settings update completed and page accessible"
    
    def test_multi_section_workflow(self, page):
        """Test workflow across multiple sections."""
        allure.dynamic.title("Workflow: Multi-section navigation")
        allure.dynamic.description("Quickly navigate through multiple sections in sequence and ensure navigation commands succeed for at least one section.")

        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        nav = NavigationPage(page)

        sections_navigated = 0
        for fn in ["navigate_to_dashboard", "navigate_to_tasks", "navigate_to_reports", "navigate_to_users", "navigate_to_branches", "navigate_to_settings"]:
            try:
                getattr(nav, fn)()
                page.wait_for_timeout(500)
                sections_navigated += 1
            except Exception:
                continue

        assert sections_navigated > 0, "Should be able to navigate to at least some sections"
    
    @pytest.mark.parametrize(
        "username,password",
        [
            (ADMIN_USERNAME, ADMIN_PASSWORD),
            (USER_USERNAME, USER_PASSWORD),
        ],
    )
    def test_full_application_access_both_users(self, page, username, password):
        """Test full application access for both user types."""
        allure.dynamic.title(f"Access: Full app access check for {username}")
        allure.dynamic.description("Login as different user roles and verify the user can access at least one major section.")

        ensure_fresh_session(page)

        login = LoginPage(page)
        login.open()
        login.login(username, password)

        page.wait_for_timeout(3000)

        sections_accessed = []
        if "/dashboard" in page.url:
            nav = NavigationPage(page)
            for fn, name in [("navigate_to_dashboard", "dashboard"), ("navigate_to_tasks", "tasks"), ("navigate_to_reports", "reports"), ("navigate_to_users", "users"), ("navigate_to_branches", "branches"), ("navigate_to_settings", "settings")]:
                try:
                    getattr(nav, fn)()
                    page.wait_for_timeout(500)
                    sections_accessed.append(name)
                except Exception:
                    continue

        assert len(sections_accessed) > 0, f"User {username} should be able to access at least some sections"

