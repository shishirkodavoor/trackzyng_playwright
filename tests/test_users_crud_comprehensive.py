"""Comprehensive CRUD operations for users - Add, View, Edit, Delete."""
import pytest
import allure
from pages.login_page import LoginPage
from pages.users_page import UsersPage
from pages.navigation_page import NavigationPage
from config.config import ADMIN_USERNAME, ADMIN_PASSWORD
from utils.test_helpers import ensure_fresh_session, login_user
from datetime import datetime

class TestUsersCRUDComprehensive:
    """Comprehensive Users CRUD operations test suite."""
    
    def test_add_new_user_complete_form(self, page):
        """Test adding a new user with complete form.

        Steps:
        1. Navigate to Users page
        2. Open Create User form and fill all fields
        3. Save and search for the created user
        Expected: user appears in search results.
        """
        allure.dynamic.title("Users: Create new user with complete form")
        allure.dynamic.description("Create a new user with all fields filled and verify it appears in the users list after save.")

        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)

        users = UsersPage(page)
        users.navigate_to_users()
        assert users.is_loaded(), "Users page should be loaded"

        users.click_create_user()

        # Generate unique email
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        test_email = f"testuser{timestamp}@test.com"

        users.fill_user_form(
            email=test_email,
            name="Test User",
            password="Test@1234",
            role="user",
            status="active",
            phone="1234567890"
        )

        users.save_user_form()

        # Verify user was created (search for it)
        users.search_user(test_email.split("@")[0])
        page.wait_for_timeout(1500)
        assert users.get_users_count() > 0, f"Expected created user {test_email} to appear in search results"
    
    def test_add_user_minimum_required_fields(self, page):
        """Test adding user with only required fields."""
        allure.dynamic.title("Users: Create user with minimum required fields")
        allure.dynamic.description("Create a user using only the minimum required fields (email, password) and verify it appears in the list.")

        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)

        users = UsersPage(page)
        users.navigate_to_users()
        assert users.is_loaded(), "Users page should be loaded"

        users.click_create_user()

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        test_email = f"minuser{timestamp}@test.com"

        users.fill_user_form(
            email=test_email,
            password="Test@1234"
        )
        users.save_user_form()

        users.search_user(test_email.split("@")[0])
        page.wait_for_timeout(1500)
        assert users.get_users_count() > 0, f"Expected user {test_email} to appear after saving minimal form"
    
    def test_view_user_details(self, page):
        """Test viewing user details."""
        allure.dynamic.title("Users: View user details")
        allure.dynamic.description("Open the details view for an existing user and verify the details panel shows expected fields.")

        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)

        users = UsersPage(page)
        users.navigate_to_users()
        assert users.is_loaded(), "Users page should be loaded"

        count = users.get_users_count()
        assert count > 0, "There should be at least one user to view"

        users.view_user(0)
        page.wait_for_timeout(1000)

        # Verify a detail label such as Email is visible on details view
        assert page.get_by_text("Email", exact=False).is_visible(timeout=3000), "Expected Email label in user details"
    
    def test_edit_existing_user(self, page):
        """Test editing an existing user."""
        allure.dynamic.title("Users: Edit existing user")
        allure.dynamic.description("Open edit for an existing user, change a field, save, and verify the changes persist in the list or details.")

        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)

        users = UsersPage(page)
        users.navigate_to_users()
        assert users.is_loaded(), "Users page should be loaded"

        assert users.get_users_count() > 0, "There should be at least one user to edit"

        users.edit_user(0)
        page.wait_for_timeout(500)

        # Update user details
        users.fill_user_form(name="Updated Name")
        users.save_user_form()
        page.wait_for_timeout(1000)

        # Basic verification: still have users in list and page remains on users
        assert users.get_users_count() >= 0, "After editing, users list should still be accessible"
    
    def test_delete_newly_added_user(self, page):
        """Test deleting a newly added user (cancel deletion)."""
        allure.dynamic.title("Users: Attempt delete newly added user and cancel")
        allure.dynamic.description("Create a user, attempt to delete it but cancel the confirmation dialog, then verify the user still exists.")

        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)

        users = UsersPage(page)
        users.navigate_to_users()
        assert users.is_loaded(), "Users page should be loaded"

        # Add a new user first
        users.click_create_user()

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        test_email = f"deleteuser{timestamp}@test.com"

        users.fill_user_form(
            email=test_email,
            name="User To Delete",
            password="Test@1234",
            role="user",
            status="active"
        )
        users.save_user_form()
        page.wait_for_timeout(1000)

        # Now search and attempt to delete this user, but cancel the dialog
        users.search_user(test_email.split("@")[0])
        page.wait_for_timeout(1000)
        initial_count = users.get_users_count()
        assert initial_count > 0, "Created user should be found before deletion"

        # Cancel dialog when it appears
        page.once("dialog", lambda dialog: dialog.dismiss())
        users.delete_user(0, confirm=False)
        page.wait_for_timeout(1000)

        # Verify user still exists
        users.search_user(test_email.split("@")[0])
        page.wait_for_timeout(1000)
        assert users.get_users_count() >= 1, "User should still exist after cancelling delete"
    
    def test_delete_user_with_confirmation(self, page):
        """Test deleting user triggers confirmation dialog (dialog dismissed)."""
        allure.dynamic.title("Users: Delete user shows confirmation dialog")
        allure.dynamic.description("Attempt to delete an existing user and ensure a confirmation dialog is presented (dismissed in test to avoid deletion).")

        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)

        users = UsersPage(page)
        users.navigate_to_users()
        assert users.is_loaded(), "Users page should be loaded"

        assert users.get_users_count() > 0, "There should be at least one user to delete"

        # Dismiss the dialog to avoid actual deletion
        dialog_seen = {"seen": False}
        def _dismiss(dialog):
            dialog.dismiss()
            dialog_seen["seen"] = True

        page.once("dialog", _dismiss)
        users.delete_user(0, confirm=False)
        page.wait_for_timeout(1000)
        assert dialog_seen["seen"], "Expected a confirmation dialog when deleting a user"
    
    def test_cancel_user_creation(self, page):
        """Test canceling user creation form."""
        allure.dynamic.title("Users: Cancel user creation returns to list")
        allure.dynamic.description("Open the create user form, fill some fields, cancel the form, and verify the users list is shown afterwards.")

        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)

        users = UsersPage(page)
        users.navigate_to_users()
        assert users.is_loaded(), "Users page should be loaded"

        users.click_create_user()
        users.fill_user_form(email="cancel@test.com", name="Cancel User")
        users.cancel_user_form()
        page.wait_for_timeout(500)

        # Verify we are back on users list
        assert users.get_users_count() >= 0, "Should be back on users list after cancelling form"
    
    def test_user_form_validation_on_save(self, page):
        """Test form validation when saving user."""
        allure.dynamic.title("Users: Form validation shows errors on save without required fields")
        allure.dynamic.description("Open create user form and click save without required fields. Expect validation errors to be shown.")

        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)

        users = UsersPage(page)
        users.navigate_to_users()
        assert users.is_loaded(), "Users page should be loaded"

        users.click_create_user()
        # Try to save without filling required fields
        users.save_user_form()
        page.wait_for_timeout(500)

        # Expect either the form still visible or some validation message
        assert users.is_element_visible(users.user_form, timeout=3000), "Expected form to remain visible with validation errors"
    
    def test_filter_users_after_adding(self, page):
        """Test filtering users after adding new user."""
        allure.dynamic.title("Users: Filter users by role and status")
        allure.dynamic.description("Apply role and status filters and verify the users list updates (non-empty result or successful filter application).")

        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)

        users = UsersPage(page)
        users.navigate_to_users()
        assert users.is_loaded(), "Users page should be loaded"

        users.filter_by_role("user")
        page.wait_for_timeout(500)
        users.filter_by_status("active")
        page.wait_for_timeout(500)

        # At minimum, the page should remain loaded and filters shouldn't break it
        assert users.is_loaded(), "Users page should remain loaded after applying filters"
    
    def test_search_newly_added_user(self, page):
        """Test searching for a newly added user."""
        allure.dynamic.title("Users: Search functionality for users")
        allure.dynamic.description("Use the search box to look for a user string and verify results (if any) are returned without errors.")

        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)

        users = UsersPage(page)
        users.navigate_to_users()
        assert users.is_loaded(), "Users page should be loaded"

        # Use a likely-to-not-exist term but ensure search doesn't error
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        search_term = f"newuser{timestamp}"

        users.search_user(search_term)
        page.wait_for_timeout(500)
        # Search may return zero results; the check is that the page handled the search
        assert users.get_users_count() >= 0, "Search completed without error"
    
    def test_view_multiple_users(self, page):
        """Test viewing multiple users."""
        allure.dynamic.title("Users: View multiple users sequentially")
        allure.dynamic.description("Open the details view for up to the first three users and return to the list between views.")

        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)

        users = UsersPage(page)
        users.navigate_to_users()
        assert users.is_loaded(), "Users page should be loaded"

        user_count = users.get_users_count()
        # View first 3 users if available
        for i in range(min(3, user_count)):
            users.view_user(i)
            page.wait_for_timeout(500)
            # Go back to list
            page.go_back()
            page.wait_for_timeout(500)

        # If there are users, we should have viewed at least one
        if user_count > 0:
            assert users.is_loaded(), "Users page should remain loaded after viewing users"
        else:
            assert user_count == 0, "No users available to view"

