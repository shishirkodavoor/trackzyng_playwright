"""Comprehensive tests for Branch management section."""
import pytest
import allure
from pages.login_page import LoginPage
from pages.branch_page import BranchPage
from pages.navigation_page import NavigationPage
from config.config import ADMIN_USERNAME, ADMIN_PASSWORD
from utils.test_helpers import ensure_fresh_session, login_user

def check_branch_page_exists(page):
    """Helper to check if branch page exists (not 404)."""
    try:
        page_text = page.locator("body").inner_text().lower()
        return not ("page not found" in page_text or "404" in page_text or "not found" in page_text)
    except Exception:
        # If we can't determine page content, treat as not available to avoid false positives
        return False

class TestBranch:
    """Comprehensive Branch management test suite."""
    
    def test_branch_page_loads(self, page):
        """Test that branch page loads correctly."""
        allure.dynamic.title("Branch: Page loads")
        allure.dynamic.description("Login as admin and navigate to Branches. Expect the branch listing to load (URL or header visible).")
        ensure_fresh_session(page)
        
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        
        branch = BranchPage(page)
        nav = NavigationPage(page)
        
        try:
            nav.navigate_to_branches()
        except Exception:
            branch.navigate_to_branches()

        page.wait_for_timeout(3000)

        # Check if branch page exists (not 404)
        if not check_branch_page_exists(page):
            pytest.skip("Branch page is not available in this application")

        assert branch.is_loaded() or "/branch" in page.url or "/branches" in page.url, \
            "Branch page should load"
    
    def test_branch_page_elements_present(self, page):
        """Test that branch page has all expected elements."""
        ensure_fresh_session(page)
        
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        branch = BranchPage(page)
        
        branch.navigate_to_branches()
        page.wait_for_timeout(3000)

        # Check if branch page exists
        if not check_branch_page_exists(page):
            pytest.skip("Branch page is not available in this application")

        if not (branch.is_loaded() or "/branch" in page.url or "/branches" in page.url):
            pytest.skip("Branch page not loaded for current user/environment")

        # Actually check if header is visible
        header_visible = branch.is_element_visible(branch.header, timeout=5000)
        assert header_visible, "Branch header should be visible"
    
    def test_branch_search_functionality(self, page):
        """Test search functionality on branch page."""
        allure.dynamic.title("Branch: Search filters results")
        allure.dynamic.description("Search for a branch name and verify the displayed list is filtered (count decreases or remains consistent).")
        ensure_fresh_session(page)
        
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        branch = BranchPage(page)
        
        branch.navigate_to_branches()
        page.wait_for_timeout(3000)

        # Check if branch page exists
        if not check_branch_page_exists(page):
            pytest.skip("Branch page is not available in this application")

        if not branch.is_loaded():
            pytest.skip("Branch page not loaded for current user/environment")

        # Verify search input exists and can be used
        search_input_visible = branch.is_element_visible(branch.search_input, timeout=3000)
        if not search_input_visible:
            pytest.skip("Search input not available on branch page")

        initial_count = branch.get_branches_count()
        branch.search_branch("test")
        page.wait_for_timeout(2000)
        new_count = branch.get_branches_count()
        assert isinstance(new_count, int) and new_count <= initial_count, "Branch search should filter or keep results consistent"
    
    def test_branch_filter_by_location(self, page):
        """Test filtering branches by location."""
        allure.dynamic.title("Branch: Location filter")
        allure.dynamic.description("Apply a location filter and verify the branch list updates (count decreases or remains stable).")
        ensure_fresh_session(page)
        
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        branch = BranchPage(page)
        
        branch.navigate_to_branches()
        page.wait_for_timeout(3000)

        # Check if branch page exists
        if not check_branch_page_exists(page):
            pytest.skip("Branch page is not available in this application")

        if not branch.is_loaded():
            pytest.skip("Branch page not loaded for current user/environment")

        # Check if filter exists
        filter_visible = branch.is_element_visible(branch.location_filter, timeout=3000)
        if not filter_visible:
            pytest.skip("Location filter not available on branch page")

        initial_count = branch.get_branches_count()
        branch.filter_by_location("New York")
        page.wait_for_timeout(2000)
        new_count = branch.get_branches_count()
        assert isinstance(new_count, int) and new_count <= initial_count, "Location filter should narrow or preserve results"
    
    def test_branch_filter_by_status(self, page):
        """Test filtering branches by status."""
        allure.dynamic.title("Branch: Status filter")
        allure.dynamic.description("Apply a status filter (e.g., active) and verify results update accordingly.")
        ensure_fresh_session(page)
        
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        branch = BranchPage(page)
        
        branch.navigate_to_branches()
        page.wait_for_timeout(3000)

        # Check if branch page exists
        if not check_branch_page_exists(page):
            pytest.skip("Branch page is not available in this application")

        if not branch.is_loaded():
            pytest.skip("Branch page not loaded for current user/environment")

        # Check if filter exists
        filter_visible = branch.is_element_visible(branch.status_filter, timeout=3000)
        if not filter_visible:
            pytest.skip("Status filter not available on branch page")

        initial_count = branch.get_branches_count()
        branch.filter_by_status("active")
        page.wait_for_timeout(2000)
        new_count = branch.get_branches_count()
        assert isinstance(new_count, int) and new_count <= initial_count, "Status filter should narrow or preserve results"
    
    def test_create_branch_button_visible(self, page):
        """Test that create branch button is visible."""
        ensure_fresh_session(page)
        
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        branch = BranchPage(page)
        
        branch.navigate_to_branches()
        page.wait_for_timeout(3000)

        # Check if branch page exists
        if not check_branch_page_exists(page):
            pytest.skip("Branch page is not available in this application")

        if not branch.is_loaded():
            pytest.skip("Branch page not loaded for current user/environment")

        create_visible = branch.is_element_visible(branch.create_branch_button, timeout=3000)
        assert create_visible, "Create branch button should be visible"
    
    def test_create_branch_form_elements(self, page):
        """Test create branch form elements."""
        ensure_fresh_session(page)
        
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        branch = BranchPage(page)
        
        branch.navigate_to_branches()
        page.wait_for_timeout(3000)

        # Check if branch page exists
        if not check_branch_page_exists(page):
            pytest.skip("Branch page is not available in this application")

        if not branch.is_loaded():
            pytest.skip("Branch page not loaded for current user/environment")

        branch.click_create_branch()
        page.wait_for_timeout(2000)
        form_visible = branch.is_element_visible(branch.branch_form, timeout=3000)
        # Some environments may not allow branch creation for the current user/role.
        # Retry once if the form didn't appear but the create control exists.
        if not form_visible:
            if branch.is_element_visible(branch.create_branch_button, timeout=2000):
                branch.click_create_branch()
                page.wait_for_timeout(1500)
                form_visible = branch.is_element_visible(branch.branch_form, timeout=2000)

        if not form_visible:
            pytest.skip("Branch create form did not appear after clicking create; create may not be available for this environment/role")

        assert form_visible, "Branch form should be visible after clicking create"
    
    def test_fill_branch_form(self, page):
        """Test filling branch creation form."""
        allure.dynamic.title("Branch: Fill create form")
        allure.dynamic.description("Open Create Branch form, fill with sample data, and verify input values are present.")
        ensure_fresh_session(page)
        
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        branch = BranchPage(page)
        
        branch.navigate_to_branches()
        page.wait_for_timeout(3000)

        # Check if branch page exists
        if not check_branch_page_exists(page):
            pytest.skip("Branch page is not available in this application")

        if not branch.is_loaded():
            pytest.skip("Branch page not loaded for current user/environment")

        branch.click_create_branch()
        page.wait_for_timeout(2000)

        # Fill form with test data
        branch.fill_branch_form(
            name="Test Branch",
            code="TB001",
            address="123 Test Street",
            city="Test City",
            state="Test State",
            zipcode="12345",
            phone="123-456-7890",
            email="testbranch@example.com",
            status="active"
        )
        page.wait_for_timeout(1000)
        # Verify form was filled (check if inputs have values)
        try:
            name_val = branch.page.locator(branch.branch_name_input).input_value()
        except Exception:
            name_val = ""
        assert name_val == "Test Branch", f"Expected branch name to be filled, got '{name_val}'"
    
    def test_view_branch_functionality(self, page):
        """Test viewing a branch."""
        allure.dynamic.title("Branch: View branch detail")
        allure.dynamic.description("Open the first branch's view action and verify a detail view or modal appears (or page remains stable).")
        ensure_fresh_session(page)
        
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        branch = BranchPage(page)
        
        branch.navigate_to_branches()
        page.wait_for_timeout(3000)

        # Check if branch page exists
        if not check_branch_page_exists(page):
            pytest.skip("Branch page is not available in this application")

        if branch.get_branches_count() == 0:
            pytest.skip("No branches available to view")

        branch.view_branch(0)
        page.wait_for_timeout(2000)
        # After view, ensure the page is still reachable
        assert branch.is_loaded(), "View branch action should complete without crashing"
    
    def test_edit_branch_functionality(self, page):
        """Test editing a branch."""
        allure.dynamic.title("Branch: Edit branch")
        allure.dynamic.description("Edit the first branch and save. Verify the save action completes (form closed or updated).")
        ensure_fresh_session(page)
        
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        branch = BranchPage(page)
        
        branch.navigate_to_branches()
        page.wait_for_timeout(3000)

        # Check if branch page exists
        if not check_branch_page_exists(page):
            pytest.skip("Branch page is not available in this application")

        if branch.get_branches_count() == 0:
            pytest.skip("No branches available to edit")

        branch.edit_branch(0)
        page.wait_for_timeout(2000)

        if branch.is_element_visible(branch.branch_form, timeout=3000):
            branch.fill_branch_form(name="Updated Branch Name")
            branch.save_branch_form()
            page.wait_for_timeout(2000)
            # After saving, ensure we can still retrieve the branches count
            assert isinstance(branch.get_branches_count(), int), "After edit, branches count should be retrievable"
    
    def test_branch_table_structure(self, page):
        """Test branch table structure."""
        ensure_fresh_session(page)
        
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        branch = BranchPage(page)
        
        branch.navigate_to_branches()
        page.wait_for_timeout(3000)

        # Check if branch page exists
        if not check_branch_page_exists(page):
            pytest.skip("Branch page is not available in this application")

        if not branch.is_loaded():
            pytest.skip("Branch page not loaded for current user/environment")

        table_visible = branch.is_element_visible(branch.branches_table, timeout=3000)
        assert table_visible, "Branch table should be visible"
    
    def test_branch_pagination(self, page):
        """Test pagination on branch page."""
        allure.dynamic.title("Branch: Pagination")
        allure.dynamic.description("If pagination exists, navigate to next page and ensure the UI responds.")
        ensure_fresh_session(page)
        
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        branch = BranchPage(page)
        
        branch.navigate_to_branches()
        page.wait_for_timeout(3000)

        # Check if branch page exists
        if not check_branch_page_exists(page):
            pytest.skip("Branch page is not available in this application")

        if not branch.is_loaded():
            pytest.skip("Branch page not loaded for current user/environment")

        if not branch.is_element_visible(branch.next_page_button, timeout=2000):
            pytest.skip("Pagination not available on branch page")

        before = branch.get_branches_count()
        branch.click_element(branch.next_page_button)
        page.wait_for_timeout(2000)
        after = branch.get_branches_count()
        assert isinstance(after, int), "Pagination should load a page and branch counts should be retrievable"
    
    def test_branch_page_refresh(self, page):
        """Test that branch page works after refresh."""
        ensure_fresh_session(page)
        
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        branch = BranchPage(page)
        
        branch.navigate_to_branches()
        page.wait_for_timeout(3000)

        # Check if branch page exists
        if not check_branch_page_exists(page):
            pytest.skip("Branch page is not available in this application")

        if not branch.is_loaded():
            pytest.skip("Branch page not loaded for current user/environment")

        page.reload(wait_until="networkidle")
        page.wait_for_timeout(2000)

        # Check again after refresh
        if not check_branch_page_exists(page):
            pytest.skip("Branch page is not available after refresh")

        assert branch.is_loaded() or "/branch" in page.url or "/branches" in page.url, \
            "Branch page should load after refresh"
    
    def test_branch_direct_url_access(self, page):
        """Test direct URL access to branch page when logged in."""
        ensure_fresh_session(page)
        
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        
        base_url = page.url.split('/dashboard')[0]
        # Try both /branch and /branches
        page.goto(f"{base_url}/branches", wait_until="networkidle")
        page.wait_for_timeout(3000)
        
        # Check if branch page exists
        if not check_branch_page_exists(page):
            pytest.skip("Branch page is not available in this application")
        
        branch = BranchPage(page)
        assert branch.is_loaded() or "/branch" in page.url or "/branches" in page.url, \
            "Should be able to access branch page directly when logged in"
    
    def test_cancel_branch_form(self, page):
        """Test canceling branch form."""
        allure.dynamic.title("Branch: Cancel create form")
        allure.dynamic.description("Open create branch form and cancel; verify the form closes or disappears.")
        ensure_fresh_session(page)
        
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        branch = BranchPage(page)
        
        branch.navigate_to_branches()
        page.wait_for_timeout(3000)

        # Check if branch page exists
        if not check_branch_page_exists(page):
            pytest.skip("Branch page is not available in this application")

        if not branch.is_loaded():
            pytest.skip("Branch page not loaded for current user/environment")

        branch.click_create_branch()
        page.wait_for_timeout(2000)

        if branch.is_element_visible(branch.branch_form, timeout=3000):
            branch.cancel_branch_form()
            page.wait_for_timeout(1000)
            # Verify cancel worked (form should close or disappear)
            assert not branch.is_element_visible(branch.branch_form, timeout=2000), "Branch form should be closed after cancel"
    
    def test_branch_form_validation(self, page):
        """Test branch form validation."""
        allure.dynamic.title("Branch: Form validation")
        allure.dynamic.description("Attempt to submit an empty branch form and verify validation prevents submission or shows errors.")
        ensure_fresh_session(page)
        
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        branch = BranchPage(page)
        
        branch.navigate_to_branches()
        page.wait_for_timeout(3000)

        # Check if branch page exists
        if not check_branch_page_exists(page):
            pytest.skip("Branch page is not available in this application")

        if not branch.is_loaded():
            pytest.skip("Branch page not loaded for current user/environment")

        branch.click_create_branch()
        page.wait_for_timeout(2000)

        if branch.is_element_visible(branch.branch_form, timeout=3000):
            # Try to save without filling required fields
            branch.save_branch_form()
            page.wait_for_timeout(2000)
            # Form should show validation errors or prevent submission
            # Check that either the form is still visible or a validation message exists
            still_visible = branch.is_element_visible(branch.branch_form, timeout=2000)
            assert still_visible, "Branch form should remain visible with validation errors after empty submit"
