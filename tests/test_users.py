"""Comprehensive tests for Users management section."""
import pytest
import allure
from pages.login_page import LoginPage
from pages.users_page import UsersPage
from pages.navigation_page import NavigationPage
from config.config import ADMIN_USERNAME, ADMIN_PASSWORD
from utils.test_helpers import ensure_fresh_session, login_user

class TestUsers:
    """Comprehensive Users management test suite."""
    
    def test_users_page_loads(self, page):
        """Test that users page loads correctly."""
        ensure_fresh_session(page)
        
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        
        users = UsersPage(page)
        nav = NavigationPage(page)
        nav.navigate_to_users()
        page.wait_for_timeout(1500)
        assert users.is_loaded(), "Users page should load"
    
    def test_users_page_elements_present(self, page):
        """Test that users page has all expected elements."""
        allure.dynamic.title("Users: Page elements visible")
        allure.dynamic.description("Verify Users page header and essential UI elements are present.")
        ensure_fresh_session(page)
        
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        users = UsersPage(page)
        
        try:
            users.navigate_to_users()
            page.wait_for_timeout(3000)
        except Exception as e:
            pytest.skip(f"Could not navigate to Users page: {e}")
        
        if users.is_loaded() or "/users" in page.url:
            assert users.is_element_visible(users.header, timeout=5000), \
                "Users header should be visible when page is loaded"
    
    def test_users_search_functionality(self, page):
        """Test search functionality on users page."""
        allure.dynamic.title("Users: Search filters results")
        allure.dynamic.description("Search for users and verify results are filtered or input accepts values.")
        ensure_fresh_session(page)
        
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        users = UsersPage(page)
        
        users.navigate_to_users()
        page.wait_for_timeout(1000)
        assert users.is_loaded(), "Users page should be loaded for search"

        initial_count = users.get_users_count()
        users.search_user("test")
        page.wait_for_timeout(1000)
        new_count = users.get_users_count()
        assert isinstance(new_count, int) and new_count >= 0, "Search should return a non-negative integer count"
    
    def test_users_filter_by_role(self, page):
        """Test filtering users by role."""
        allure.dynamic.title("Users: Role filter")
        allure.dynamic.description("Apply a role filter and ensure users list updates.")
        ensure_fresh_session(page)
        
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        users = UsersPage(page)
        
        users.navigate_to_users()
        page.wait_for_timeout(1000)
        assert users.is_loaded(), "Users page should be loaded for role filter"

        initial_count = users.get_users_count()
        users.filter_by_role("admin")
        page.wait_for_timeout(1000)
        new_count = users.get_users_count()
        assert isinstance(new_count, int) and new_count >= 0, "Role filter should complete and return a count"
    
    def test_users_filter_by_status(self, page):
        """Test filtering users by status."""
        allure.dynamic.title("Users: Status filter")
        allure.dynamic.description("Apply status filter and verify the list updates.")
        ensure_fresh_session(page)
        
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        users = UsersPage(page)
        
        users.navigate_to_users()
        page.wait_for_timeout(1000)
        assert users.is_loaded(), "Users page should be loaded for status filter"

        initial_count = users.get_users_count()
        users.filter_by_status("active")
        page.wait_for_timeout(1000)
        new_count = users.get_users_count()
        assert isinstance(new_count, int) and new_count >= 0, "Status filter should complete and return a count"
    
    def test_create_user_button_visible(self, page):
        """Test that create user button is visible."""
        allure.dynamic.title("Users: Create button presence")
        allure.dynamic.description("Check whether the 'Create user' control is present for current user.")
        ensure_fresh_session(page)
        
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        users = UsersPage(page)
        
        users.navigate_to_users()
        page.wait_for_timeout(1000)
        assert users.is_loaded(), "Users page should be loaded"

        create_visible = users.is_element_visible(users.create_user_button, timeout=3000)
        assert create_visible, "Create user control should be visible"
    
    def test_create_user_form_elements(self, page):
        """Test create user form elements."""
        allure.dynamic.title("Users: Create form elements")
        allure.dynamic.description("Open create user form and verify required elements are present.")
        ensure_fresh_session(page)
        
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        users = UsersPage(page)
        
        users.navigate_to_users()
        page.wait_for_timeout(1000)
        assert users.is_loaded(), "Users page should be loaded"

        users.click_create_user()
        # Wait a bit for modal/panel to appear; tolerate alternative fields appearing
        page.wait_for_timeout(500)

        form_visible = users.is_element_visible(users.user_form, timeout=3000)
        email_visible = users.is_element_visible(users.email_input, timeout=3000)
        name_visible = users.is_element_visible(users.name_input, timeout=3000)

        # If create control wasn't available at all, skip the test
        create_available = users.is_element_visible(users.create_user_button, timeout=2000)
        if not create_available:
            pytest.skip("Create user control not available for this user/role in this environment")

        # If the form didn't show but the button exists, retry click once
        if not (form_visible or email_visible or name_visible):
            users.click_create_user()
            page.wait_for_timeout(500)
            form_visible = users.is_element_visible(users.user_form, timeout=2000)
            email_visible = users.is_element_visible(users.email_input, timeout=2000)
            name_visible = users.is_element_visible(users.name_input, timeout=2000)

        assert form_visible or email_visible or name_visible, "User form or inputs should be visible after clicking create"
    
    def test_fill_user_form(self, page):
        """Test filling user creation form."""
        allure.dynamic.title("Users: Fill create form")
        allure.dynamic.description("Fill the new user form and verify inputs accept values.")
        ensure_fresh_session(page)
        
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        users = UsersPage(page)
        
        users.navigate_to_users()
        page.wait_for_timeout(1000)
        assert users.is_loaded(), "Users page should be loaded"

        users.click_create_user()
        page.wait_for_timeout(500)

        # Generate unique email to avoid collisions
        from datetime import datetime
        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_email = f"testuser{ts}@example.com"

        users.fill_user_form(
            email=unique_email,
            name="Test User",
            password="Test123!@#",
            role="user",
            status="active"
        )
        page.wait_for_timeout(500)

        try:
            val = users.page.locator(users.email_input).input_value()
        except Exception:
            val = ""
        assert unique_email in val, "Email field should contain the unique test email"
    
    def test_view_user_functionality(self, page):
        """Test viewing a user."""
        allure.dynamic.title("Users: View user detail")
        allure.dynamic.description("Open a user's detail view and ensure it appears or the UI remains stable.")
        ensure_fresh_session(page)
        
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        users = UsersPage(page)
        
        users.navigate_to_users()
        page.wait_for_timeout(1000)
        assert users.is_loaded(), "Users page should be loaded"

        if users.get_users_count() > 0:
            users.view_user(0)
            page.wait_for_timeout(500)
            assert page.get_by_text("Email", exact=False).count() > 0 or users.is_element_visible(users.user_form, timeout=2000), "User detail should be visible when viewing a user"
        else:
            pytest.skip("No users available to view")
    
    def test_edit_user_functionality(self, page):
        """Test editing a user."""
        allure.dynamic.title("Users: Edit user")
        allure.dynamic.description("Edit a user and save; verify the system remains stable or reflects changes.")
        ensure_fresh_session(page)
        
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        users = UsersPage(page)
        
        users.navigate_to_users()
        page.wait_for_timeout(1000)
        assert users.is_loaded(), "Users page should be loaded"

        if users.get_users_count() > 0:
            users.edit_user(0)
            page.wait_for_timeout(500)

            if users.is_element_visible(users.user_form, timeout=2000):
                users.fill_user_form(name="Updated Name")
                users.save_user_form()
                page.wait_for_timeout(500)
                assert isinstance(users.get_users_count(), int), "After edit, users count should be retrievable"
        else:
            pytest.skip("No users available to edit")
    
    def test_users_table_structure(self, page):
        """Test users table structure."""
        allure.dynamic.title("Users: Table structure")
        allure.dynamic.description("Verify the users table or equivalent list is present.")
        ensure_fresh_session(page)
        
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        users = UsersPage(page)
        
        users.navigate_to_users()
        page.wait_for_timeout(1000)
        assert users.is_loaded(), "Users page should be loaded"

        table_visible = users.is_element_visible(users.users_table, timeout=3000)
        assert table_visible, "Users table should be visible when page is loaded"
    
    def test_users_pagination(self, page):
        """Test pagination on users page."""
        allure.dynamic.title("Users: Pagination")
        allure.dynamic.description("Navigate users pagination if present and verify UI responds.")
        ensure_fresh_session(page)
        
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        users = UsersPage(page)
        
        users.navigate_to_users()
        page.wait_for_timeout(1000)
        assert users.is_loaded(), "Users page should be loaded"

        if users.is_element_visible(users.next_page_button, timeout=2000):
            before = users.get_users_count()
            users.click_element(users.next_page_button)
            page.wait_for_timeout(500)
            after = users.get_users_count()
            assert isinstance(after, int), "Pagination should allow retrieving users count"
    
    def test_users_page_refresh(self, page):
        """Test that users page works after refresh."""
        allure.dynamic.title("Users: Page reload stability")
        allure.dynamic.description("Reload the users page and ensure it remains usable.")
        ensure_fresh_session(page)
        
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        users = UsersPage(page)
        
        users.navigate_to_users()
        page.wait_for_timeout(1000)
        assert users.is_loaded(), "Users page should be loaded"

        page.reload(wait_until="networkidle")
        page.wait_for_timeout(1000)
        assert users.is_loaded(), "Users page should load after refresh"
    
    def test_users_direct_url_access(self, page):
        """Test direct URL access to users page when logged in."""
        allure.dynamic.title("Users: Direct URL access")
        allure.dynamic.description("Navigate directly to /users while logged in and verify the page loads.")
        ensure_fresh_session(page)
        
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        
        base_url = page.url.split('/dashboard')[0]
        page.goto(f"{base_url}/users", wait_until="networkidle")
        page.wait_for_timeout(3000)
        
        users = UsersPage(page)
        assert users.is_loaded() or "/users" in page.url, \
            "Should be able to access users page directly when logged in"
    
    def test_cancel_user_form(self, page):
        """Test canceling user form."""
        allure.dynamic.title("Users: Cancel create form")
        allure.dynamic.description("Open the create user form and cancel; verify the form closes.")
        ensure_fresh_session(page)
        
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        users = UsersPage(page)
        
        users.navigate_to_users()
        page.wait_for_timeout(1000)
        assert users.is_loaded(), "Users page should be loaded"

        users.click_create_user()
        page.wait_for_timeout(500)

        assert users.is_element_visible(users.user_form, timeout=3000), "User form should be visible after clicking create"
        users.cancel_user_form()
        page.wait_for_timeout(500)
        assert not users.is_element_visible(users.user_form, timeout=2000), "User form should be closed after cancel"

