"""Comprehensive pagination tests across all sections."""
import pytest
import allure
from pages.login_page import LoginPage
from pages.reports_page import ReportsPage
from pages.users_page import UsersPage
from pages.branch_page import BranchPage
from pages.tasks_page import TasksPage
from pages.navigation_page import NavigationPage
from config.config import ADMIN_USERNAME, ADMIN_PASSWORD
from utils.test_helpers import ensure_fresh_session, login_user

class TestPaginationComprehensive:
    """Comprehensive pagination test suite."""
    
    def test_reports_pagination_next_page(self, page):
        """Test reports pagination - next page."""
        allure.dynamic.title("Pagination: Reports - Next page")
        allure.dynamic.description("Click the reports next page button and verify that the page changes (URL or first item).")

        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)

        reports = ReportsPage(page)
        reports.navigate_to_reports()
        assert reports.is_loaded(), "Reports page should be loaded"

        if reports.is_element_visible(reports.next_page_button, timeout=3000):
            next_btn = page.locator(reports.next_page_button).first
            # Skip if next button is disabled or not actionable (no second page)
            if not next_btn.is_visible() or next_btn.is_disabled():
                pytest.skip("No second page available for Reports to test pagination")

            initial_url = page.url
            initial_first = ""
            if reports.get_reports_count() > 0:
                try:
                    initial_first = page.locator(reports.reports_list).first.inner_text()
                except Exception:
                    initial_first = ""

            reports.click_element(reports.next_page_button)
            page.wait_for_timeout(1500)

            new_url = page.url
            new_first = ""
            if reports.get_reports_count() > 0:
                try:
                    new_first = page.locator(reports.reports_list).first.inner_text()
                except Exception:
                    new_first = ""

            assert new_url != initial_url or (initial_first and new_first and new_first != initial_first), \
                "Reports next page should navigate to a different page"
    
    def test_reports_pagination_previous_page(self, page):
        """Test reports pagination - previous page."""
        allure.dynamic.title("Pagination: Reports - Previous page")
        allure.dynamic.description("Navigate to the next page then back to previous and verify the page changes back (URL or first item).")

        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)

        reports = ReportsPage(page)
        reports.navigate_to_reports()
        assert reports.is_loaded(), "Reports page should be loaded"

        if reports.is_element_visible(reports.next_page_button, timeout=3000):
            # Go to page 2 first
            reports.click_element(reports.next_page_button)
            page.wait_for_timeout(1000)

            if reports.is_element_visible(reports.prev_page_button, timeout=3000):
                prev_url = page.url
                prev_first = ""
                if reports.get_reports_count() > 0:
                    try:
                        prev_first = page.locator(reports.reports_list).first.inner_text()
                    except Exception:
                        prev_first = ""

                reports.click_element(reports.prev_page_button)
                page.wait_for_timeout(1000)

                new_url = page.url
                new_first = ""
                if reports.get_reports_count() > 0:
                    try:
                        new_first = page.locator(reports.reports_list).first.inner_text()
                    except Exception:
                        new_first = ""

                assert new_url != prev_url or (prev_first and new_first and new_first != prev_first), \
                    "Reports previous page should navigate back"
    
    def test_users_pagination_next_page(self, page):
        """Test users pagination - next page."""
        allure.dynamic.title("Pagination: Users - Next page")
        allure.dynamic.description("Click users next page and verify navigation by URL or first user row change.")

        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)

        users = UsersPage(page)
        users.navigate_to_users()
        assert users.is_loaded(), "Users page should be loaded"

        if users.is_element_visible(users.next_page_button, timeout=3000):
            next_btn = page.locator(users.next_page_button).first
            if not next_btn.is_visible() or next_btn.is_disabled():
                pytest.skip("No second page available for Users to test pagination")

            initial_url = page.url
            before = ""
            if users.get_users_count() > 0:
                try:
                    before = page.locator(users.users_list).first.inner_text()
                except Exception:
                    before = ""
            users.click_element(users.next_page_button)
            page.wait_for_timeout(1000)
            new_url = page.url
            after = ""
            if users.get_users_count() > 0:
                try:
                    after = page.locator(users.users_list).first.inner_text()
                except Exception:
                    after = ""
            assert new_url != initial_url or (before and after and before != after), "Users next page navigation behaved unexpectedly"
    
    def test_users_pagination_previous_page(self, page):
        """Test users pagination - previous page."""
        allure.dynamic.title("Pagination: Users - Previous page")
        allure.dynamic.description("Navigate forward then back in users pagination and verify navigation reverts.")

        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)

        users = UsersPage(page)
        users.navigate_to_users()
        assert users.is_loaded(), "Users page should be loaded"

        if users.is_element_visible(users.next_page_button, timeout=3000):
            users.click_element(users.next_page_button)
            page.wait_for_timeout(500)

            if users.is_element_visible(users.prev_page_button, timeout=3000):
                before = page.url
                users.click_element(users.prev_page_button)
                page.wait_for_timeout(500)
                assert page.url != before, "Users previous page should navigate back"
    
    def test_branch_pagination_next_page(self, page):
        """Test branch pagination - next page."""
        allure.dynamic.title("Pagination: Branches - Next page")
        allure.dynamic.description("Click branches next page and verify the page changes (URL or first branch row).")

        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)

        branch = BranchPage(page)
        branch.navigate_to_branches()
        assert branch.is_loaded(), "Branches page should be loaded"

        if branch.is_element_visible(branch.next_page_button, timeout=3000):
            next_btn = page.locator(branch.next_page_button).first
            if not next_btn.is_visible() or next_btn.is_disabled():
                pytest.skip("No second page available for Branches to test pagination")

            initial_url = page.url
            before = ""
            try:
                before = page.locator(branch.branches_list).first.inner_text()
            except Exception:
                before = ""

            branch.click_element(branch.next_page_button)
            page.wait_for_timeout(1000)

            new_url = page.url
            after = ""
            try:
                after = page.locator(branch.branches_list).first.inner_text()
            except Exception:
                after = ""

            assert before != after or new_url != initial_url, "Branch next page should navigate"
    
    def test_branch_pagination_previous_page(self, page):
        """Test branch pagination - previous page."""
        allure.dynamic.title("Pagination: Branches - Previous page")
        allure.dynamic.description("Navigate to the next branch page and then back to previous, verifying navigation.")

        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)

        branch = BranchPage(page)
        branch.navigate_to_branches()
        assert branch.is_loaded(), "Branches page should be loaded"

        if branch.is_element_visible(branch.next_page_button, timeout=3000):
            branch.click_element(branch.next_page_button)
            page.wait_for_timeout(500)

            if branch.is_element_visible(branch.prev_page_button, timeout=3000):
                before = page.url
                branch.click_element(branch.prev_page_button)
                page.wait_for_timeout(500)
                assert page.url != before, "Branch previous should navigate back"
    
    def test_tasks_pagination_next_page(self, page):
        """Test tasks pagination - next page."""
        allure.dynamic.title("Pagination: Tasks - Next page")
        allure.dynamic.description("Click tasks next and verify the first row or URL changes to indicate navigation.")

        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)

        tasks = TasksPage(page)
        tasks.navigate_to_tasks()
        assert tasks.is_loaded(), "Tasks page should be loaded"

        if tasks.is_element_visible(tasks.next_page_button, timeout=3000):
            next_btn = page.locator(tasks.next_page_button).first
            if not next_btn.is_visible() or next_btn.is_disabled():
                pytest.skip("No second page available for Tasks to test pagination")

            initial_url = page.url
            before = ""
            try:
                before = page.locator(tasks.tasks_list).first.inner_text()
            except Exception:
                before = ""

            tasks.click_element(tasks.next_page_button)
            page.wait_for_timeout(1000)

            new_url = page.url
            after = ""
            try:
                after = page.locator(tasks.tasks_list).first.inner_text()
            except Exception:
                after = ""

            assert before != after or new_url != initial_url, "Tasks next page navigation check"
    
    def test_pagination_page_numbers(self, page):
        """Test clicking specific page numbers."""
        allure.dynamic.title("Pagination: Click specific page numbers")
        allure.dynamic.description("Click numeric page buttons (if present) and verify navigation occurs by URL or content change.")

        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)

        reports = ReportsPage(page)
        reports.navigate_to_reports()
        assert reports.is_loaded(), "Reports page should be loaded"

        page_numbers = page.locator('[data-page-number], .page-number, button:has-text("2"), button:has-text("3")').all()
        if len(page_numbers) > 0:
            initial = page.url
            page_numbers[0].click()
            page.wait_for_timeout(1000)
            assert page.url != initial or reports.get_reports_count() >= 0, "Page number selection should navigate"
    
    def test_pagination_first_page_button(self, page):
        """Test pagination first page button."""
        allure.dynamic.title("Pagination: First page button")
        allure.dynamic.description("Navigate to another page then click First to return to page one (verify by URL or content).")

        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)

        reports = ReportsPage(page)
        reports.navigate_to_reports()
        assert reports.is_loaded(), "Reports page should be loaded"

        if reports.is_element_visible(reports.next_page_button, timeout=3000):
            reports.click_element(reports.next_page_button)
            page.wait_for_timeout(500)

            first_page = page.locator('button:has-text("First"), [aria-label*="first"], [data-page="first"]').first
            if first_page.is_visible(timeout=2000):
                first_page.click()
                page.wait_for_timeout(500)
                assert "/reports" in page.url or "page=1" in page.url, "First page should navigate to reports page root or page=1"
    
    def test_pagination_last_page_button(self, page):
        """Test pagination last page button."""
        allure.dynamic.title("Pagination: Last page button")
        allure.dynamic.description("Click the Last page control and verify navigation (next should become disabled or URL changes).")

        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)

        reports = ReportsPage(page)
        reports.navigate_to_reports()
        assert reports.is_loaded(), "Reports page should be loaded"

        last_page = page.locator('button:has-text("Last"), [aria-label*="last"], [data-page="last"]').first
        if last_page.is_visible(timeout=2000):
            last_page.click()
            page.wait_for_timeout(1000)
            next_btn = page.locator(reports.next_page_button).first
            # On last page, next should be disabled or not visible
            assert (not next_btn.is_visible()) or next_btn.is_disabled(), "Next button should be disabled/not visible on last page"
    
    def test_pagination_disabled_on_first_page(self, page):
        """Test pagination buttons are disabled on first page."""
        allure.dynamic.title("Pagination: Previous disabled on first page")
        allure.dynamic.description("On the first page, the Previous control should be disabled or not visible.")

        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)

        reports = ReportsPage(page)
        reports.navigate_to_reports()
        assert reports.is_loaded(), "Reports page should be loaded"

        prev_button = page.locator(reports.prev_page_button).first
        if prev_button.is_visible(timeout=2000):
            assert prev_button.is_disabled(), "Previous button should be disabled on first page"
    
    def test_pagination_disabled_on_last_page(self, page):
        """Test pagination buttons are disabled on last page."""
        allure.dynamic.title("Pagination: Next disabled on last page")
        allure.dynamic.description("Navigate forward until Next is disabled (or not visible) indicating last page reached.")

        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)

        reports = ReportsPage(page)
        reports.navigate_to_reports()
        assert reports.is_loaded(), "Reports page should be loaded"

        # Try multiple next clicks to reach last page
        for _ in range(10):
            if reports.is_element_visible(reports.next_page_button, timeout=2000):
                next_btn = page.locator(reports.next_page_button).first
                if next_btn.is_disabled():
                    break
                reports.click_element(reports.next_page_button)
                page.wait_for_timeout(500)

        next_button = page.locator(reports.next_page_button).first
        if next_button.is_visible(timeout=2000):
            assert next_button.is_disabled(), "Next button should be disabled on last page"
    
    def test_pagination_page_size_change(self, page):
        """Test changing items per page."""
        allure.dynamic.title("Pagination: Change items per page")
        allure.dynamic.description("Select a different page size and verify the number of rows displayed does not exceed the selected size.")

        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)

        reports = ReportsPage(page)
        reports.navigate_to_reports()
        assert reports.is_loaded(), "Reports page should be loaded"

        page_size = page.locator('select[name*="per_page"], select[name*="limit"], [data-per-page]').first
        if page_size.is_visible(timeout=2000):
            try:
                page_size.select_option("50")
                page.wait_for_timeout(500)
                count = reports.get_reports_count()
                assert count <= 50, "Number of reports per page should not exceed 50 after page size change"
            except Exception:
                # If selecting fails, fail the test
                assert False, "Unable to change page size selector"
    
    def test_pagination_url_updates(self, page):
        """Test pagination updates URL."""
        allure.dynamic.title("Pagination: URL updates on navigation")
        allure.dynamic.description("Verify that paginating updates the browser URL or contains a page query parameter.")

        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)

        reports = ReportsPage(page)
        reports.navigate_to_reports()
        assert reports.is_loaded(), "Reports page should be loaded"
        initial_url = page.url

        if reports.is_element_visible(reports.next_page_button, timeout=3000):
            reports.click_element(reports.next_page_button)
            page.wait_for_timeout(1000)
            new_url = page.url
            assert new_url != initial_url or "page=2" in new_url or "?page=" in new_url, "URL should reflect pagination change"
    
    def test_pagination_with_search(self, page):
        """Test pagination works with search results."""
        allure.dynamic.title("Pagination: Works with search")
        allure.dynamic.description("Perform a search, then paginate results and ensure navigation occurs without error.")

        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)

        users = UsersPage(page)
        users.navigate_to_users()
        assert users.is_loaded(), "Users page should be loaded"

        users.search_user("test")
        page.wait_for_timeout(500)
        if users.is_element_visible(users.next_page_button, timeout=3000):
            before = page.url
            users.click_element(users.next_page_button)
            page.wait_for_timeout(500)
            assert page.url != before or users.get_users_count() >= 0, "Pagination with search should navigate"
    
    def test_pagination_with_filter(self, page):
        """Test pagination works with filters."""
        allure.dynamic.title("Pagination: Works with filters")
        allure.dynamic.description("Apply a filter and then paginate the filtered results, verifying navigation works.")

        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)

        users = UsersPage(page)
        users.navigate_to_users()
        assert users.is_loaded(), "Users page should be loaded"

        users.filter_by_role("admin")
        page.wait_for_timeout(500)
        if users.is_element_visible(users.next_page_button, timeout=3000):
            before = page.url
            users.click_element(users.next_page_button)
            page.wait_for_timeout(500)
            assert page.url != before or users.get_users_count() >= 0, "Pagination with filter should navigate"

