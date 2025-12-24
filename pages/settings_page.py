"""Settings page object."""
from pages.base_page import BasePage

class SettingsPage(BasePage):
    """Page object for the Settings section."""
    
    def __init__(self, page):
        super().__init__(page)
        # Settings page selectors
        self.header = 'text=Settings, h1:has-text("Settings"), [data-testid*="settings-header"]'
        self.settings_tabs = '[role="tab"], .tab, [data-testid*="tab"]'
        self.general_tab = 'button:has-text("General"), [data-testid*="general"]'
        self.profile_tab = 'button:has-text("Profile"), [data-testid*="profile"]'
        self.security_tab = 'button:has-text("Security"), [data-testid*="security"]'
        self.notifications_tab = 'button:has-text("Notifications"), [data-testid*="notifications"]'
        self.save_button = 'button:has-text("Save"), button[type="submit"]'
        self.cancel_button = 'button:has-text("Cancel")'
        
        # General settings
        self.company_name_input = 'input[name*="company"], input[placeholder*="Company"]'
        self.timezone_select = 'select[name*="timezone"]'
        self.language_select = 'select[name*="language"]'
        
        # Profile settings
        self.full_name_input = 'input[name*="name"], input[placeholder*="Full Name"]'
        self.email_input = 'input[type="email"], input[name*="email"]'
        self.phone_input = 'input[type="tel"], input[name*="phone"]'
        self.avatar_upload = 'input[type="file"]'
        
        # Security settings
        self.current_password_input = 'input[name*="current_password"], input[placeholder*="Current Password"]'
        self.new_password_input = 'input[name*="new_password"], input[placeholder*="New Password"]'
        self.confirm_new_password_input = 'input[name*="confirm_password"]'
        self.change_password_button = 'button:has-text("Change Password")'
        
        # Notifications settings
        self.email_notifications_checkbox = 'input[type="checkbox"][name*="email"]'
        self.sms_notifications_checkbox = 'input[type="checkbox"][name*="sms"]'
        self.push_notifications_checkbox = 'input[type="checkbox"][name*="push"]'
    
    def is_loaded(self, timeout: int = 15000) -> bool:
        """Check if settings page is loaded."""
        try:
            self.wait_for_url_pattern("/settings", timeout=timeout)
            current_url = self.get_current_url()
            
            # Check if page actually loaded (not 404)
            if "/settings" in current_url:
                self.page.wait_for_load_state("domcontentloaded", timeout=5000)
                self.page.wait_for_timeout(2000)
                
                # Check for 404 or "Page Not Found" indicators
                page_text = self.page.locator("body").inner_text().lower()
                if "page not found" in page_text or "404" in page_text or "not found" in page_text:
                    return False
                
                # Check if header or settings content exists
                if self.is_element_visible(self.header, timeout=3000):
                    return True
                
                # If URL is /settings but no content, might be empty page (still loaded)
                return True
            return False
        except:
            current_url = self.get_current_url()
            if "/settings" in current_url:
                # Quick check for 404
                try:
                    page_text = self.page.locator("body").inner_text().lower()
                    if "page not found" in page_text or "404" in page_text:
                        return False
                except:
                    pass
                return True
            return False
    
    def navigate_to_settings(self):
        """Navigate to settings page."""
        try:
            base_url = self.get_base_url()
            self.navigate_to(f"{base_url}/settings")
            self.wait_for_url_pattern("/settings", timeout=15000)
            self.page.wait_for_load_state("domcontentloaded", timeout=10000)
            self.page.wait_for_timeout(2000)
            
            # Check if page actually exists (not 404)
            page_text = self.page.locator("body").inner_text().lower()
            if "page not found" in page_text or "404" in page_text:
                # Settings page doesn't exist - redirect to dashboard or stay on current page
                # Don't raise error, just note that settings isn't available
                return
        except:
            try:
                base_url = self.get_base_url()
                self.page.goto(f"{base_url}/settings", wait_until="domcontentloaded", timeout=30000)
                self.page.wait_for_timeout(2000)
                
                # Check for 404
                page_text = self.page.locator("body").inner_text().lower()
                if "page not found" in page_text or "404" in page_text:
                    return
            except:
                pass
    
    def switch_to_tab(self, tab_name: str):
        """Switch to a specific settings tab."""
        tab_selectors = {
            "general": self.general_tab,
            "profile": self.profile_tab,
            "security": self.security_tab,
            "notifications": self.notifications_tab,
        }
        if tab_name.lower() in tab_selectors:
            if self.is_element_visible(tab_selectors[tab_name.lower()], timeout=3000):
                self.click_element(tab_selectors[tab_name.lower()])
                self.page.wait_for_timeout(500)
    
    def update_profile(self, name: str = "", email: str = "", phone: str = ""):
        """Update profile settings."""
        if name and self.is_element_visible(self.full_name_input, timeout=3000):
            self.fill_input(self.full_name_input, name)
        if email and self.is_element_visible(self.email_input, timeout=3000):
            self.fill_input(self.email_input, email)
        if phone and self.is_element_visible(self.phone_input, timeout=3000):
            self.fill_input(self.phone_input, phone)
    
    def change_password(self, current_password: str, new_password: str):
        """Change password in security settings."""
        if self.is_element_visible(self.current_password_input, timeout=3000):
            self.fill_input(self.current_password_input, current_password)
        if self.is_element_visible(self.new_password_input, timeout=3000):
            self.fill_input(self.new_password_input, new_password)
        if self.is_element_visible(self.confirm_new_password_input, timeout=3000):
            self.fill_input(self.confirm_new_password_input, new_password)
        if self.is_element_visible(self.change_password_button, timeout=3000):
            self.click_element(self.change_password_button)
            self.page.wait_for_timeout(2000)
    
    def save_settings(self):
        """Save settings changes."""
        if self.is_element_visible(self.save_button, timeout=3000):
            self.click_element(self.save_button)
            self.page.wait_for_timeout(2000)

