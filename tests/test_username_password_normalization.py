"""Tests for username and password normalization - whitespace trimming and case sensitivity."""
import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from config.config import ADMIN_USERNAME, ADMIN_PASSWORD
from utils.test_helpers import ensure_fresh_session

class TestUsernamePasswordNormalization:
    """Test suite for username and password normalization."""
    
    def test_username_with_spaces_at_beginning_should_pass(self, page):
        """Test that spaces at beginning of username are trimmed and login succeeds."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        # Username with leading spaces
        login.login(f"  {ADMIN_USERNAME}", ADMIN_PASSWORD)
        
        page.wait_for_url("**/dashboard**", timeout=15000)
        assert "/dashboard" in page.url, "Login should succeed with leading spaces in username (trimmed)"
    
    def test_username_with_spaces_at_end_should_pass(self, page):
        """Test that spaces at end of username are trimmed and login succeeds."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        # Username with trailing spaces
        login.login(f"{ADMIN_USERNAME}  ", ADMIN_PASSWORD)
        
        page.wait_for_url("**/dashboard**", timeout=15000)
        assert "/dashboard" in page.url, "Login should succeed with trailing spaces in username (trimmed)"
    
    def test_username_with_spaces_at_both_ends_should_pass(self, page):
        """Test that spaces at both ends of username are trimmed and login succeeds."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        # Username with spaces on both ends
        login.login(f"  {ADMIN_USERNAME}  ", ADMIN_PASSWORD)
        
        page.wait_for_url("**/dashboard**", timeout=15000)
        assert "/dashboard" in page.url, "Login should succeed with spaces on both ends of username (trimmed)"
    
    def test_password_with_spaces_at_beginning_should_pass(self, page):
        """Test that spaces at beginning of password are trimmed and login succeeds."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        # Password with leading spaces
        login.login(ADMIN_USERNAME, f"  {ADMIN_PASSWORD}")
        
        page.wait_for_url("**/dashboard**", timeout=15000)
        assert "/dashboard" in page.url, "Login should succeed with leading spaces in password (trimmed)"
    
    def test_password_with_spaces_at_end_should_pass(self, page):
        """Test that spaces at end of password are trimmed and login succeeds."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        # Password with trailing spaces
        login.login(ADMIN_USERNAME, f"{ADMIN_PASSWORD}  ")
        
        page.wait_for_url("**/dashboard**", timeout=15000)
        assert "/dashboard" in page.url, "Login should succeed with trailing spaces in password (trimmed)"
    
    def test_password_with_spaces_at_both_ends_should_pass(self, page):
        """Test that spaces at both ends of password are trimmed and login succeeds."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        # Password with spaces on both ends
        login.login(ADMIN_USERNAME, f"  {ADMIN_PASSWORD}  ")
        
        page.wait_for_url("**/dashboard**", timeout=15000)
        assert "/dashboard" in page.url, "Login should succeed with spaces on both ends of password (trimmed)"
    
    def test_username_password_both_with_spaces_should_pass(self, page):
        """Test that both username and password with spaces are trimmed and login succeeds."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        # Both username and password with spaces
        login.login(f"  {ADMIN_USERNAME}  ", f"  {ADMIN_PASSWORD}  ")
        
        page.wait_for_url("**/dashboard**", timeout=15000)
        assert "/dashboard" in page.url, "Login should succeed with spaces in both username and password (trimmed)"
    
    def test_username_uppercase_should_pass(self, page):
        """Test that username in uppercase should pass (case-insensitive, auto-converted to lowercase)."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        # Username in all uppercase
        login.login(ADMIN_USERNAME.upper(), ADMIN_PASSWORD)
        
        page.wait_for_url("**/dashboard**", timeout=15000)
        assert "/dashboard" in page.url, "Login should succeed with uppercase username (case-insensitive)"
    
    def test_username_mixed_case_should_pass(self, page):
        """Test that username in mixed case should pass (case-insensitive)."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        # Username in mixed case
        login.login(ADMIN_USERNAME.capitalize(), ADMIN_PASSWORD)
        
        page.wait_for_url("**/dashboard**", timeout=15000)
        assert "/dashboard" in page.url, "Login should succeed with mixed case username (case-insensitive)"
    
    def test_username_case_variations_should_all_pass(self, page):
        """Test various username case variations should all pass."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        
        case_variations = [
            ADMIN_USERNAME.upper(),  # All uppercase
            ADMIN_USERNAME.capitalize(),  # First letter uppercase
            ADMIN_USERNAME.swapcase(),  # Swapped case
        ]
        
        for username_variant in case_variations:
            ensure_fresh_session(page)
            login.open()
            login.login(username_variant, ADMIN_PASSWORD)
            page.wait_for_url("**/dashboard**", timeout=15000)
            assert "/dashboard" in page.url, \
                f"Login should succeed with username case variation: {username_variant}"
    
    def test_password_case_sensitive_uppercase_should_fail(self, page):
        """Test that password in uppercase should fail (password is case-sensitive)."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        # Password in uppercase (should fail as password is case-sensitive)
        login.login(ADMIN_USERNAME, ADMIN_PASSWORD.upper())
        
        page.wait_for_timeout(5000)
        assert "/dashboard" not in page.url, \
            "Login should fail with uppercase password (password is case-sensitive)"
    
    def test_password_case_sensitive_mixed_case_should_fail(self, page):
        """Test that password with different case should fail (password is case-sensitive)."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        # Password with different case (should fail)
        login.login(ADMIN_USERNAME, ADMIN_PASSWORD.capitalize())
        
        page.wait_for_timeout(5000)
        assert "/dashboard" not in page.url, \
            "Login should fail with different case password (password is case-sensitive)"
    
    def test_username_uppercase_with_spaces_should_pass(self, page):
        """Test that username in uppercase with spaces should pass (both trimmed and case-normalized)."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        # Uppercase username with spaces
        login.login(f"  {ADMIN_USERNAME.upper()}  ", ADMIN_PASSWORD)
        
        page.wait_for_url("**/dashboard**", timeout=15000)
        assert "/dashboard" in page.url, \
            "Login should succeed with uppercase username with spaces (trimmed and case-normalized)"
    
    def test_password_with_spaces_but_wrong_case_should_fail(self, page):
        """Test that password with spaces but wrong case should fail (spaces trimmed but case matters)."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        # Password with spaces but wrong case (spaces will be trimmed, but case still matters)
        login.login(ADMIN_USERNAME, f"  {ADMIN_PASSWORD.upper()}  ")
        
        page.wait_for_timeout(5000)
        assert "/dashboard" not in page.url, \
            "Login should fail with wrong case password even with spaces (password is case-sensitive)"
    
    @pytest.mark.parametrize(
        "username_variant,password_variant,should_pass",
        [
            (f"  {ADMIN_USERNAME}  ", ADMIN_PASSWORD, True),  # Username with spaces
            (ADMIN_USERNAME.upper(), ADMIN_PASSWORD, True),  # Username uppercase
            (f"  {ADMIN_USERNAME.upper()}  ", ADMIN_PASSWORD, True),  # Username uppercase with spaces
            (ADMIN_USERNAME, f"  {ADMIN_PASSWORD}  ", True),  # Password with spaces
            (ADMIN_USERNAME, ADMIN_PASSWORD.upper(), False),  # Password uppercase (should fail)
            (ADMIN_USERNAME, f"  {ADMIN_PASSWORD.upper()}  ", False),  # Password uppercase with spaces (should fail)
            (f"  {ADMIN_USERNAME.upper()}  ", f"  {ADMIN_PASSWORD}  ", True),  # Both with spaces, username uppercase
        ],
    )
    def test_various_username_password_combinations(self, page, username_variant, password_variant, should_pass):
        """Test various combinations of username and password normalization."""
        ensure_fresh_session(page)
        
        login = LoginPage(page)
        login.open()
        login.login(username_variant, password_variant)
        
        if should_pass:
            page.wait_for_url("**/dashboard**", timeout=15000)
            assert "/dashboard" in page.url, \
                f"Login should succeed with: username='{username_variant[:20]}...', password='{password_variant[:5]}...'"
        else:
            page.wait_for_timeout(5000)
            assert "/dashboard" not in page.url, \
                f"Login should fail with: username='{username_variant[:20]}...', password='{password_variant[:5]}...'"

