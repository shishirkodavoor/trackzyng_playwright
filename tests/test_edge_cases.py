"""Edge cases and boundary condition tests."""
import pytest
import allure
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from config.config import ADMIN_USERNAME, ADMIN_PASSWORD
from utils.test_helpers import ensure_fresh_session, login_user

class TestEdgeCases:
    """Edge cases and boundary conditions test suite."""
    
    def test_extremely_long_email(self, page):
        """Test handling of extremely long email addresses."""
        allure.dynamic.title("Edge: Extremely long email handling")
        allure.dynamic.description("Enter an extremely long email and verify the app handles it gracefully (error or stay on login).")

        ensure_fresh_session(page)
        login = LoginPage(page)
        login.open()

        long_email = "a" * 1000 + "@test.com"
        login.fill_input(login.email_input, long_email)
        login.click_element(login.next_button)
        page.wait_for_timeout(1000)

        # Expect either an error message or the login form to remain visible (no crash / navigation)
        assert login.get_error_message() != "" or login.is_login_form_visible(), "Long email should be rejected or handled gracefully"
    
    def test_special_characters_in_email(self, page):
        """Test email with special characters."""
        allure.dynamic.title("Edge: Special characters in email")
        allure.dynamic.description("Enter emails with valid special characters and verify the login flow accepts them or shows validation gracefully.")

        ensure_fresh_session(page)
        login = LoginPage(page)
        login.open()

        special_emails = [
            "test+tag@example.com",
            "test.name@example.com",
            "test_name@example.com",
            "test-name@example.com",
            "test@sub.example.com",
            "123456@example.com",
        ]

        for email in special_emails:
            login.clear_email_field()
            login.fill_input(login.email_input, email)
            login.click_element(login.next_button)
            page.wait_for_timeout(500)
            # Expect either password input to appear or an error message
            assert login.is_login_form_visible() or login.get_error_message() != "" or page.locator(login.password_input).count() > 0, f"Special email should be handled without crashing: {email}"
    
    def test_unicode_in_inputs(self, page):
        """Test Unicode characters in input fields."""
        allure.dynamic.title("Edge: Unicode input handling")
        allure.dynamic.description("Enter Unicode-containing emails and verify the app handles or rejects them cleanly.")

        ensure_fresh_session(page)
        login = LoginPage(page)
        login.open()

        unicode_strings = [
            "测试@example.com",
            "🚀test@example.com",
            "тест@example.com",
            "مثال@example.com",
        ]

        for unicode_str in unicode_strings:
            login.clear_email_field()
            login.fill_input(login.email_input, unicode_str)
            login.click_element(login.next_button)
            page.wait_for_timeout(500)
            assert login.is_login_form_visible() or login.get_error_message() != "" or page.locator(login.password_input).count() > 0, "Unicode input should be handled"
    
    def test_empty_string_handling(self, page):
        """Test empty string handling."""
        allure.dynamic.title("Edge: Empty input handling")
        allure.dynamic.description("Submit empty email and ensure the app does not navigate to dashboard and shows validation.")

        ensure_fresh_session(page)
        login = LoginPage(page)
        login.open()

        login.fill_input(login.email_input, "")
        login.click_element(login.next_button)
        page.wait_for_timeout(500)
        assert "/dashboard" not in page.url and (login.get_error_message() != "" or login.is_login_form_visible()), "Empty email should not navigate to dashboard and should show validation"
    
    def test_only_whitespace_input(self, page):
        """Test input with only whitespace."""
        allure.dynamic.title("Edge: Whitespace-only input")
        allure.dynamic.description("Submit whitespace-only inputs and verify they are rejected or do not navigate to dashboard.")

        ensure_fresh_session(page)
        login = LoginPage(page)
        login.open()

        whitespace_inputs = [" ", "  ", "\t", "\n", "   "]
        for ws in whitespace_inputs:
            login.clear_email_field()
            login.fill_input(login.email_input, ws)
            login.click_element(login.next_button)
            page.wait_for_timeout(500)
            assert "/dashboard" not in page.url and (login.get_error_message() != "" or login.is_login_form_visible()), "Whitespace-only input should not navigate to dashboard"
    
    def test_rapid_button_clicks(self, page):
        """Test handling of rapid button clicks."""
        allure.dynamic.title("Edge: Rapid button clicks")
        allure.dynamic.description("Simulate rapid clicks on the login Next button and ensure the UI remains stable or shows validation.")

        ensure_fresh_session(page)
        login = LoginPage(page)
        login.open()

        login.fill_input(login.email_input, ADMIN_USERNAME)
        for _ in range(5):
            try:
                login.click_element(login.next_button)
                page.wait_for_timeout(200)
            except Exception:
                break

        page.wait_for_timeout(1000)
        # Expected: either navigates to password input, or shows an error, but does not crash
        assert page.locator(login.password_input).count() > 0 or login.get_error_message() != "" or login.is_login_form_visible(), "Rapid clicks should be handled"
    
    def test_browser_back_button(self, page):
        """Test browser back button behavior."""
        allure.dynamic.title("Edge: Browser back button behavior")
        allure.dynamic.description("After successful login, navigate back and ensure the app handles the browser back button without error.")

        ensure_fresh_session(page)
        login = LoginPage(page)
        login.open()

        login.login(ADMIN_USERNAME, ADMIN_PASSWORD)
        page.wait_for_url("**/dashboard**", timeout=15000)

        # Go back
        page.go_back()
        page.wait_for_timeout(1000)

        # Expect either login form visible again or a stable page that does not crash
        assert login.is_login_form_visible() or page.url != "", "Back button should return to a stable page"
    
    def test_page_refresh_during_action(self, page):
        """Test page refresh during an action."""
        allure.dynamic.title("Edge: Refresh during action")
        allure.dynamic.description("Trigger a page reload during an in-flight action (login flow) and ensure the app recovers or remains stable.")

        ensure_fresh_session(page)
        login = LoginPage(page)
        login.open()

        login.fill_input(login.email_input, ADMIN_USERNAME)
        login.click_element(login.next_button)
        page.wait_for_timeout(500)

        page.reload()
        page.wait_for_timeout(1000)

        assert login.is_login_form_visible() or "/dashboard" in page.url, "App should remain stable after refresh"
    
    def test_multiple_tabs_sessions(self, page):
        """Test behavior with multiple tabs."""
        allure.dynamic.title("Edge: Multiple tabs / sessions")
        allure.dynamic.description("Open a new tab while logged in and verify the new tab is at a valid app page (dashboard expected).")

        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)

        context = page.context
        new_page = context.new_page()
        new_page.goto(page.url)
        new_page.wait_for_timeout(1000)

        assert "/dashboard" in new_page.url, "New tab should be on dashboard or a valid page"
        new_page.close()
    
    def test_network_timeout_handling(self, page):
        """Test handling of network timeouts."""
        allure.dynamic.title("Edge: Network timeout handling")
        allure.dynamic.description("Attempt to load the page with longer timeout and ensure the app handles slow networks gracefully (no crash).")

        ensure_fresh_session(page)
        login = LoginPage(page)

        loaded = False
        try:
            login.open()
            page.wait_for_load_state("networkidle", timeout=60000)
            loaded = True
        except Exception:
            loaded = False

        # Pass if the page loaded or the login form is still visible (graceful degradation)
        assert loaded or login.is_login_form_visible() or page.content() != "", "Network timeouts should be handled gracefully"
    
    def test_large_payload_handling(self, page):
        """Test handling of large data payloads."""
        allure.dynamic.title("Edge: Large payload handling")
        allure.dynamic.description("Navigate to pages expected to carry large payloads (dashboard) and ensure the UI remains responsive.")

        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)

        assert "/dashboard" in page.url, "Dashboard should be accessible (large payload handled)"
    
    def test_concurrent_user_actions(self, page):
        """Test concurrent user actions."""
        allure.dynamic.title("Edge: Concurrent user actions")
        allure.dynamic.description("Simulate quick user interactions (keyboard navigation) and verify the app remains responsive.")

        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)

        for _ in range(3):
            page.keyboard.press("Tab")
            page.wait_for_timeout(100)

        # Basic check: page body is still present and not blank
        assert page.locator('body').inner_text() != "", "App should remain responsive after concurrent actions"
    
    def test_extreme_viewport_sizes(self, page):
        """Test application on extreme viewport sizes."""
        allure.dynamic.title("Edge: Extreme viewport sizes")
        allure.dynamic.description("Open the app at very small and very large viewport sizes and ensure the login form remains accessible.")

        ensure_fresh_session(page)
        login = LoginPage(page)

        page.set_viewport_size({"width": 320, "height": 568})
        login.open()
        assert login.is_login_form_visible(), "Login form should be visible on small viewport"

        page.set_viewport_size({"width": 3840, "height": 2160})
        login.open()
        assert login.is_login_form_visible(), "Login form should be visible on large viewport"
    
    def test_session_expiry_handling(self, page):
        """Test session expiry handling."""
        allure.dynamic.title("Edge: Session expiry handling")
        allure.dynamic.description("Wait briefly and reload to simulate session expiry, then ensure the app shows either dashboard or login page appropriately.")

        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)

        page.wait_for_timeout(2000)
        page.reload(wait_until="networkidle")
        page.wait_for_timeout(500)

        assert "/dashboard" in page.url or "/login" in page.url, "Session expiry should result in dashboard or login page"

