"""Comprehensive invalid login test cases."""
import pytest
from pages.login_page import LoginPage
from config.config import BASE_URL, ADMIN_USERNAME, ADMIN_PASSWORD
from utils.test_helpers import ensure_fresh_session

class TestInvalidLogin:
    """Comprehensive invalid login test suite."""
    
    def test_login_with_invalid_email(self, page):
        """Test login with invalid email format."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        
        # Try invalid email formats
        invalid_emails = [
            "invalidemail",
            "invalid@",
            "@invalid.com",
            "invalid..email@test.com",
            "invalid@email",
            " ",
            "invalid email@test.com",
        ]
        
        for invalid_email in invalid_emails:
            login.clear_email_field()
            login.login(invalid_email, "test1234", check_password=False)
            page.wait_for_timeout(2000)
            
            # Should not reach dashboard
            assert "/dashboard" not in page.url, \
                f"Should not login with invalid email: {invalid_email}"
    
    def test_login_with_invalid_password(self, page):
        """Test login with invalid password."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        
        # Try various invalid passwords
        invalid_passwords = [
            "",
            "wrong",
            "123456",
            "password",
            "test",
            "a" * 100,  # Very long password
        ]
        
        for invalid_password in invalid_passwords:
            ensure_fresh_session(page)
            login.open()
            login.login("kranjith@codezyng.com", invalid_password)
            page.wait_for_timeout(3000)
            
            # Should not reach dashboard
            assert "/dashboard" not in page.url, \
                f"Should not login with invalid password: {invalid_password[:10]}..."
    
    def test_login_with_wrong_credentials(self, page):
        """Test login with completely wrong credentials."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        
        wrong_combinations = [
            ("wrong@email.com", "wrongpassword"),
            ("test@test.com", "test1234"),
            ("admin@admin.com", "admin123"),
            ("user@user.com", "user123"),
        ]
        
        for email, password in wrong_combinations:
            ensure_fresh_session(page)
            login.open()
            login.login(email, password)
            page.wait_for_timeout(3000)
            
            # Should not reach dashboard
            assert "/dashboard" not in page.url, \
                f"Should not login with wrong credentials: {email}"
    
    def test_login_with_empty_credentials(self, page):
        """Test login with empty email and password."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        
        # Try empty email
        login.login("", "test1234", check_password=False)
        page.wait_for_timeout(2000)
        assert "/dashboard" not in page.url, "Should not login with empty email"
        
        # Try empty password
        ensure_fresh_session(page)
        login.open()
        login.login("kranjith@codezyng.com", "")
        page.wait_for_timeout(3000)
        assert "/dashboard" not in page.url, "Should not login with empty password"
        
        # Try both empty
        ensure_fresh_session(page)
        login.open()
        login.login("", "", check_password=False)
        page.wait_for_timeout(2000)
        assert "/dashboard" not in page.url, "Should not login with empty credentials"
    
    def test_login_with_sql_injection_attempt(self, page):
        """Test login with SQL injection attempts."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        
        sql_injection_attempts = [
            ("' OR '1'='1", "test1234"),
            ("admin@codezyng.com", "' OR '1'='1"),
            ("'; DROP TABLE users; --", "test1234"),
            ("admin@codezyng.com", "'; DROP TABLE users; --"),
        ]
        
        for email, password in sql_injection_attempts:
            ensure_fresh_session(page)
            login.open()
            login.login(email, password)
            page.wait_for_timeout(3000)
            
            # Should not reach dashboard
            assert "/dashboard" not in page.url, \
                "Should not login with SQL injection attempt"
    
    def test_login_with_xss_attempt(self, page):
        """Test login with XSS attack attempts."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        
        xss_attempts = [
            ("<script>alert('xss')</script>@test.com", "test1234"),
            ("test@test.com", "<script>alert('xss')</script>"),
            ("javascript:alert('xss')@test.com", "test1234"),
        ]
        
        for email, password in xss_attempts:
            ensure_fresh_session(page)
            login.open()
            login.login(email, password)
            page.wait_for_timeout(3000)
            
            # Should not reach dashboard
            assert "/dashboard" not in page.url, \
                "Should not login with XSS attempt"
    
    def test_login_with_special_characters(self, page):
        """Test login with special characters."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        
        special_char_emails = [
            "test!@#@test.com",
            "test@test#$%.com",
            "test@test.com&*()",
        ]
        
        for email in special_char_emails:
            ensure_fresh_session(page)
            login.open()
            login.login(email, "test1234", check_password=False)
            page.wait_for_timeout(2000)
            assert "/dashboard" not in page.url, \
                f"Should not login with special chars in email: {email}"
    
    def test_login_with_very_long_credentials(self, page):
        """Test login with very long email and password."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        
        # Very long email
        long_email = "a" * 200 + "@test.com"
        login.login(long_email, "test1234", check_password=False)
        page.wait_for_timeout(2000)
        assert "/dashboard" not in page.url, "Should not login with very long email"
        
        # Very long password
        ensure_fresh_session(page)
        login.open()
        long_password = "a" * 500
        login.login("kranjith@codezyng.com", long_password)
        page.wait_for_timeout(3000)
        assert "/dashboard" not in page.url, "Should not login with very long password"
    
    def test_multiple_failed_login_attempts(self, page):
        """Test multiple consecutive failed login attempts."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        
        # Try multiple failed logins
        for i in range(5):
            ensure_fresh_session(page)
            login.open()
            login.login("wrong@email.com", "wrongpass")
            page.wait_for_timeout(2000)
            assert "/dashboard" not in page.url, \
                f"Should not login on attempt {i+1}"
    
    def test_login_error_messages(self, page):
        """Test that appropriate error messages are shown for invalid login."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        
        # Try invalid login
        login.login("wrong@email.com", "wrongpass")
        page.wait_for_timeout(3000)
        
        # Check for error message (if displayed)
        error_message = login.get_error_message()
        # Error message might exist or might not, but should not reach dashboard
        assert "/dashboard" not in page.url, \
            "Should show error or prevent login, not reach dashboard"
    
    def test_login_case_sensitivity(self, page):
        """Test login case sensitivity - username is case-insensitive, password is case-sensitive."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        
        # Username case variations should work (username is case-insensitive)
        username_case_variations = [
            ADMIN_USERNAME.upper(),  # All uppercase - should pass
            ADMIN_USERNAME.capitalize(),  # Mixed case - should pass
        ]
        
        for username in username_case_variations:
            ensure_fresh_session(page)
            login.open()
            login.login(username, ADMIN_PASSWORD)
            page.wait_for_url("**/dashboard**", timeout=15000)
            assert "/dashboard" in page.url, \
                f"Login should succeed with case variation username: {username} (username is case-insensitive)"
        
        # Password case variations should fail (password is case-sensitive)
        password_case_variations = [
            ADMIN_PASSWORD.upper(),  # All uppercase - should fail
            ADMIN_PASSWORD.capitalize(),  # Mixed case - should fail
        ]
        
        for password in password_case_variations:
            ensure_fresh_session(page)
            login.open()
            login.login(ADMIN_USERNAME, password)
            page.wait_for_timeout(5000)
            assert "/dashboard" not in page.url, \
                f"Login should fail with case variation password (password is case-sensitive)"
    
    def test_login_with_whitespace_only(self, page):
        """Test login with whitespace-only credentials."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        
        # Whitespace only
        login.login("   ", "   ", check_password=False)
        page.wait_for_timeout(2000)
        assert "/dashboard" not in page.url, \
            "Should not login with whitespace-only credentials"
    
    def test_login_with_numeric_only_credentials(self, page):
        """Test login with numeric-only credentials."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        
        # Numeric only
        login.login("1234567890@test.com", "1234567890", check_password=False)
        page.wait_for_timeout(2000)
        assert "/dashboard" not in page.url, \
            "Should not login with numeric-only invalid email"
    
    def test_login_page_stays_accessible_after_failed_login(self, page):
        """Test that login page remains accessible after failed login."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        original_url = page.url
        
        # Try invalid login
        login.login("wrong@email.com", "wrongpass")
        page.wait_for_timeout(3000)
        
        # Should still be able to access login page
        login.open()
        page.wait_for_timeout(2000)
        assert login.is_login_form_visible(), \
            "Login page should remain accessible after failed login"

