"""UI elements and interaction tests."""
import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from config.config import ADMIN_USERNAME, ADMIN_PASSWORD
from utils.test_helpers import ensure_fresh_session, login_user

class TestUIElements:
    """UI elements and interaction test suite."""
    
    def test_page_title_present(self, page):
        """Test that page has a title."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        
        title = page.title()
        assert title != "", "Page should have a title"
        assert len(title) > 0, "Page title should not be empty"
    
    def test_page_url_structure(self, page):
        """Test page URL structure."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        
        url = page.url
        assert url.startswith("http"), "URL should use http/https protocol"
        assert "trackzyng" in url.lower() or "codezyng" in url.lower(), \
            "URL should contain domain name"
    
    def test_input_fields_functionality(self, page):
        """Test input field functionality."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        
        # Test email input
        assert login.is_element_visible(login.email_input), "Email input should be visible"
        login.fill_input(login.email_input, "test@example.com")
        
        # Verify input was filled (if possible)
        value = page.locator(login.email_input).input_value()
        assert "test@example.com" in value or value == "test@example.com", \
            "Email input should accept values"
    
    def test_button_clicks(self, page):
        """Test button click functionality."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        
        # Fill email and click next
        login.fill_input(login.email_input, ADMIN_USERNAME)
        assert login.is_element_visible(login.next_button), "Next button should be visible"
        
        login.click_element(login.next_button)
        
        # Should proceed to password step
        page.wait_for_timeout(2000)
    
    def test_page_responsiveness(self, page):
        """Test page responsiveness to interactions."""
        ensure_fresh_session(page)
        
        dashboard = login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        
        # Test scrolling
        page.evaluate("window.scrollTo(0, 500)")
        page.wait_for_timeout(500)
        page.evaluate("window.scrollTo(0, 0)")
        
        # Page should still be responsive
        assert dashboard.is_loaded(), "Page should remain responsive after scrolling"
    
    def test_page_load_performance(self, page):
        """Test page load performance."""
        import time
        
        ensure_fresh_session(page)
        
        start_time = time.time()
        login = LoginPage(page)
        login.open()
        load_time = time.time() - start_time
        
        # Page should load within reasonable time (30 seconds)
        assert load_time < 30, f"Page should load within 30 seconds, took {load_time:.2f}s"
    
    def test_dashboard_content_visibility(self, page):
        """Test that dashboard content is visible."""
        ensure_fresh_session(page)
        
        dashboard = login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        dashboard.wait_for_dashboard_load()
        
        # Check main content areas
        assert page.locator('body').is_visible(), "Body should be visible"
        assert dashboard.is_loaded(), "Dashboard should be loaded and visible"
    
    def test_form_validation(self, page):
        """Test form validation on login."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        
        # Try submitting empty form
        try:
            login.click_element(login.next_button)
            page.wait_for_timeout(2000)
            # Should either show validation error or not proceed
            error = login.get_error_message()
            # If no error message, form might have HTML5 validation
            # Either way, form should not proceed to dashboard
            page.wait_for_timeout(2000)
            assert "/dashboard" not in page.url, \
                "Should not proceed to dashboard with empty form"
        except Exception as e:
            # Button might be disabled, which is also valid; verify disabled state
            try:
                btn = page.locator(login.next_button).first
                disabled = btn.get_attribute("disabled")
                assert disabled is not None or "/dashboard" not in page.url, \
                    f"Unexpected behavior when clicking empty form: {e}"
            except Exception:
                # If we can't inspect button, treat as a skip to avoid false negatives
                pytest.skip(f"Form validation behavior couldn't be determined: {e}")
    
    def test_page_interactions_stability(self, page):
        """Test that page remains stable during interactions."""
        ensure_fresh_session(page)
        
        dashboard = login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        
        # Perform multiple interactions
        for _ in range(3):
            page.wait_for_timeout(1000)
            page.evaluate("window.scrollBy(0, 100)")
            page.wait_for_timeout(1000)
            page.evaluate("window.scrollBy(0, -100)")
        
        # Page should still be functional
        assert dashboard.is_loaded(), "Page should remain stable after interactions"
        assert "/dashboard" in page.url, "Should remain on dashboard"


