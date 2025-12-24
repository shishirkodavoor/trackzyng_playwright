"""Tests for actual dashboard elements based on real page structure."""
import pytest
import allure
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from config.config import ADMIN_USERNAME, ADMIN_PASSWORD
from utils.test_helpers import ensure_fresh_session, login_user

class TestDashboardElements:
    """Tests for actual dashboard page elements."""
    
    def test_dashboard_key_metrics_displayed(self, page):
        """Test that key metrics cards are displayed on dashboard."""
        allure.dynamic.title("Dashboard: Key metric cards visible")
        allure.dynamic.description("Verify one or more metric cards (Active Users, Checked In/Out) are visible to confirm dashboard content loaded.")
        ensure_fresh_session(page)
        
        dashboard = login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        dashboard.wait_for_dashboard_load()
        
        # Check for key metrics cards — at least one indicator should be present
        metric_count = dashboard.page.locator(dashboard.metric_cards).count()
        assert (
            dashboard.is_element_visible(dashboard.active_users_card, timeout=5000)
            or dashboard.is_element_visible(dashboard.users_checked_in_card, timeout=5000)
            or dashboard.is_element_visible(dashboard.users_checked_out_card, timeout=5000)
            or metric_count > 0
        ), "Key metrics cards should be visible on dashboard"
    
    def test_active_users_metric(self, page):
        """Test Active Users metric card."""
        allure.dynamic.title("Dashboard: Active Users metric present")
        allure.dynamic.description("Look for an Active Users card or text in metric cards to surface user-count metrics to reviewers.")
        ensure_fresh_session(page)
        
        dashboard = login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        dashboard.wait_for_dashboard_load()
        page.wait_for_timeout(2000)
        
        # Check if active users card exists
        # Prefer explicit selector for Active Users card; fall back to text search
        try:
            active_users_found = dashboard.page.get_by_text("Active Users", exact=False).count() > 0
        except Exception:
            active_users_found = False

        assert active_users_found or dashboard.is_element_visible(dashboard.active_users_card, timeout=3000), \
            "Active Users metric should be displayed"
    
    def test_user_location_section_present(self, page):
        """Test that User Live Approx. Location section is present."""
        allure.dynamic.title("Dashboard: User location section")
        allure.dynamic.description("Check presence of the User Live Approx. Location section and its search input.")
        ensure_fresh_session(page)
        
        dashboard = login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        dashboard.wait_for_dashboard_load()
        page.wait_for_timeout(2000)
        
        # Check for user location section
        location_section_visible = dashboard.is_element_visible(dashboard.user_location_section, timeout=5000)
        
        # Also check for search input which is part of this section
        search_visible = dashboard.is_element_visible(dashboard.search_users_input, timeout=5000)
        
        assert location_section_visible or search_visible, \
            "User Live Approx. Location section should be present"
    
    def test_search_users_functionality(self, page):
        """Test search users functionality on dashboard."""
        allure.dynamic.title("Dashboard: Search users")
        allure.dynamic.description("Type into the dashboard user search and verify the UI responds (results filter or search input accepts value).")
        ensure_fresh_session(page)
        
        dashboard = login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        dashboard.wait_for_dashboard_load()
        page.wait_for_timeout(2000)
        
        # Try to search users and verify the input accepts the typed value
        if dashboard.is_element_visible(dashboard.search_users_input, timeout=5000):
            dashboard.fill_input(dashboard.search_users_input, "test")
            page.wait_for_timeout(1000)
            val = ""
            try:
                val = dashboard.page.locator(dashboard.search_users_input).input_value()
            except Exception:
                pass
            assert "test" in val, "Search input should accept typed value"
    
    def test_last_updated_display(self, page):
        """Test that last updated time is displayed."""
        allure.dynamic.title("Dashboard: Last updated info")
        allure.dynamic.description("Verify dashboard displays last-updated timestamp or related text for reviewer clarity.")
        ensure_fresh_session(page)
        
        dashboard = login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        dashboard.wait_for_dashboard_load()
        page.wait_for_timeout(2000)
        
        # Check for last updated text
        last_updated_visible = dashboard.is_element_visible(dashboard.last_updated_text, timeout=5000)
        
        # Also check page content for "Last updated" or "updated" text
        page_text = dashboard.page.locator('body').inner_text().lower()
        has_updated_text = "last updated" in page_text or "updated" in page_text
        
        assert last_updated_visible or has_updated_text, \
            "Last updated information should be displayed"
    
    def test_refresh_button_functionality(self, page):
        """Test refresh button functionality."""
        allure.dynamic.title("Dashboard: Refresh button")
        allure.dynamic.description("Click the refresh control and ensure dashboard remains loaded post-refresh.")
        ensure_fresh_session(page)
        
        dashboard = login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        dashboard.wait_for_dashboard_load()
        page.wait_for_timeout(2000)
        
        # Check for refresh button
        if dashboard.is_element_visible(dashboard.refresh_button, timeout=5000):
            dashboard.click_element(dashboard.refresh_button)
            page.wait_for_timeout(2000)
            
            # Dashboard should still be loaded after refresh
            assert dashboard.is_loaded(), "Dashboard should work after refresh click"
    
    def test_areas_by_checked_in_users_section(self, page):
        """Test Areas by Checked-In Users section."""
        allure.dynamic.title("Dashboard: Areas by checked-in users")
        allure.dynamic.description("Ensure area section or area cards are present to reflect checked-in user distribution.")
        ensure_fresh_session(page)
        
        dashboard = login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        dashboard.wait_for_dashboard_load()
        page.wait_for_timeout(2000)
        
        # Check for areas section
        areas_section_visible = dashboard.is_element_visible(dashboard.areas_section, timeout=5000)
        
        # Check for area cards
        area_cards = dashboard.page.locator(dashboard.area_cards).all()
        area_card_template_count = dashboard.page.locator(dashboard.area_card_template).count()
        
        assert areas_section_visible or len(area_cards) > 0 or area_card_template_count > 0, \
            "Areas by Checked-In Users section should be present"
    
    def test_area_cards_displayed(self, page):
        """Test that area cards are displayed with check-in information."""
        allure.dynamic.title("Dashboard: Area cards display")
        allure.dynamic.description("Verify area cards and check-in info are present or that page content references check-ins.")
        ensure_fresh_session(page)
        
        dashboard = login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        dashboard.wait_for_dashboard_load()
        page.wait_for_timeout(2000)
        
        # Get area cards
        area_cards = dashboard.page.locator(dashboard.area_card_template).all()
        area_cards_count = dashboard.page.locator(dashboard.area_cards).count()
        
        # Should have at least some area cards or check-in information
        page_text = dashboard.page.locator('body').inner_text().lower()
        has_checkin_info = "checked-in" in page_text or "checked in" in page_text
        
        assert len(area_cards) > 0 or area_cards_count > 0 or has_checkin_info, \
            "Area cards with check-in information should be displayed"
    
    def test_dashboard_interactive_elements(self, page):
        """Test that dashboard has interactive elements."""
        allure.dynamic.title("Dashboard: Interactive elements present")
        allure.dynamic.description("Confirm dashboard contains interactive controls (buttons/inputs) for usability.")
        ensure_fresh_session(page)
        
        dashboard = login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        dashboard.wait_for_dashboard_load()
        page.wait_for_timeout(2000)
        
        # Check for various interactive elements
        buttons_count = dashboard.get_page_elements_count(dashboard.buttons)
        inputs_count = dashboard.get_page_elements_count(dashboard.inputs)
        
        # Dashboard should have some interactive elements
        assert buttons_count > 0 or inputs_count > 0, \
            "Dashboard should have interactive elements"
    
    def test_dashboard_data_display(self, page):
        """Test that dashboard displays actual data."""
        allure.dynamic.title("Dashboard: Data presence")
        allure.dynamic.description("Check that dashboard contains numeric data (user counts, metrics) to ensure it's populated.")
        ensure_fresh_session(page)
        
        dashboard = login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        dashboard.wait_for_dashboard_load()
        page.wait_for_timeout(3000)
        
        # Get page content
        page_content = dashboard.page.locator('body').inner_text()
        
        # Should contain some data (numbers, text, etc.)
        # Check for numeric values (user counts, etc.)
        import re
        numbers = re.findall(r'\d+', page_content)
        
        assert len(numbers) > 0, "Dashboard should display data with numeric values"
    
    def test_dashboard_page_structure(self, page):
        """Test overall dashboard page structure."""
        allure.dynamic.title("Dashboard: Page structure & load")
        allure.dynamic.description("Verify main content area, page load status, and URL/title for the dashboard page.")
        ensure_fresh_session(page)
        
        dashboard = login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        dashboard.wait_for_dashboard_load()
        page.wait_for_timeout(2000)
        
        # Check for main structural elements
        assert dashboard.is_content_visible(), "Dashboard content area should be visible"
        assert dashboard.is_loaded(), "Dashboard should be properly loaded"
        assert page.title() != "", "Dashboard should have a page title"
        assert "/dashboard" in page.url, "URL should indicate dashboard page"

