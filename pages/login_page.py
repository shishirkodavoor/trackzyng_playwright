"""Login page object."""
from config.config import BASE_URL
from pages.base_page import BasePage

class LoginPage(BasePage):
    """Page object for the login page."""
    
    def __init__(self, page):
        super().__init__(page)
        # Step 1: Email input + Next button
        self.email_input = 'input[id="«r0»"]'
        self.next_button = 'button:has-text("Next")'

        # Step 2: Password input + Sign in button
        self.password_input = 'input[id="«r3»"]'
        self.signin_button = 'button:has-text("Sign in")'
        
        # Additional selectors for comprehensive testing
        self.error_message = '[role="alert"], .error, [class*="error"], [class*="alert"]'
        self.login_form = 'form, [role="form"]'
        self.remember_me = 'input[type="checkbox"][name*="remember"], input[type="checkbox"][id*="remember"]'
        self.forgot_password_link = 'a:has-text("Forgot"), a:has-text("forgot")'
    
    def open(self):
        """Open the login page."""
        self.navigate_to(BASE_URL)
        self.page.locator(self.email_input).wait_for(state="visible", timeout=15000)
    
    def login(self, username, password, check_password=True):
        """Perform login with username and password."""
        # Step 1: enter email and click Next
        self.fill_input(self.email_input, username)
        self.click_element(self.next_button)

        # Step 2: fill password if needed
        if check_password:
            try:
                self.page.locator(self.password_input).wait_for(state="visible", timeout=5000)
                self.fill_input(self.password_input, password)
                self.click_element(self.signin_button)
            except:
                # password field did not appear (invalid username)
                pass
    
    def is_login_form_visible(self) -> bool:
        """Check if login form is visible."""
        return self.is_element_visible(self.email_input, timeout=5000)
    
    def get_error_message(self) -> str:
        """Get error message if present."""
        if self.is_element_visible(self.error_message, timeout=3000):
            return self.get_text(self.error_message)
        return ""
    
    def clear_email_field(self):
        """Clear the email input field."""
        self.page.locator(self.email_input).clear()
    
    def clear_password_field(self):
        """Clear the password input field."""
        try:
            self.page.locator(self.password_input).clear()
        except:
            pass
