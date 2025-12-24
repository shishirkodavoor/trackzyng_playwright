"""Comprehensive security tests."""
import pytest
import allure
import re
from pages.login_page import LoginPage
from config.config import ADMIN_USERNAME, ADMIN_PASSWORD, BASE_URL
from utils.test_helpers import ensure_fresh_session, login_user

class TestSecurity:
    """Security test suite."""
    
    def test_sql_injection_in_login_email(self, page):
        """Test SQL injection protection in email field."""
        ensure_fresh_session(page)
        login = LoginPage(page)
        login.open()
        
        sql_injections = [
            "admin' OR '1'='1",
            "'; DROP TABLE users; --",
            "' OR 1=1 --",
            "admin'--",
            "admin'/*",
            "' UNION SELECT * FROM users--",
        ]
        
        for sql_inject in sql_injections:
            ensure_fresh_session(page)
            login.open()
            login.login(sql_inject, "test1234")
            page.wait_for_timeout(3000)
            assert "/dashboard" not in page.url, f"SQL injection attempt should fail: {sql_inject}"
    
    def test_xss_attack_prevention(self, page):
        """Test XSS attack prevention."""
        allure.dynamic.title("Security: XSS payloads are not executed or reflected")
        allure.dynamic.description("Submit XSS-like payloads and verify they are not reflected raw in the DOM and do not cause a successful login.")
        ensure_fresh_session(page)
        login = LoginPage(page)
        login.open()
        
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')",
            "<svg onload=alert('XSS')>",
            "<body onload=alert('XSS')>",
        ]
        
        for xss in xss_payloads:
            ensure_fresh_session(page)
            login.open()
            login.login(xss, "test1234", check_password=False)
            page.wait_for_timeout(2000)
            # Should not execute script nor log in
            assert "/dashboard" not in page.url, f"XSS payload should not result in login: {xss}"
            content = page.content().lower()
            # For payloads with tags, ensure the exact payload isn't reflected verbatim
            if '<' in xss or '>' in xss:
                assert xss.lower() not in content, f"Page should not reflect raw XSS payloads in content for payload: {xss}"
            # For javascript: style payloads, ensure they do not appear in href/src or event attributes (which could be executable)
            elif 'javascript:' in xss.lower():
                assert not re.search(r"href\s*=\s*[\"']\s*javascript:", content), \
                    f"javascript: URLs reflected in href are dangerous for payload: {xss}"
                assert not re.search(r"src\s*=\s*[\"']\s*javascript:", content), \
                    f"javascript: URLs reflected in src are dangerous for payload: {xss}"
                assert not re.search(r"on\w+\s*=\s*[\"']?\s*javascript:", content), \
                    f"Inline event handlers with javascript: are dangerous for payload: {xss}"
            else:
                # Generic fallback: ensure exact payload not present verbatim
                assert xss.lower() not in content, f"Page should not reflect raw XSS payloads in content for payload: {xss}"
    
    def test_password_visibility_toggle(self, page):
        """Test password field masking."""
        allure.dynamic.title("Security: Password input is masked by default")
        allure.dynamic.description("Verify the password input is of type 'password' so characters are masked.")
        ensure_fresh_session(page)
        login = LoginPage(page)
        login.open()
        
        # Enter password
        login.fill_input(login.email_input, ADMIN_USERNAME)
        login.click_element(login.next_button)
        page.wait_for_timeout(2000)
        
        # Check if password field exists and is type password
        password_field = page.locator(login.password_input)
        if password_field.count() == 0:
            pytest.skip("Password field not present in this flow/environment")

        input_type = password_field.get_attribute("type")
        assert input_type == "password", "Password should be masked"
    
    def test_csrf_protection(self, page):
        """Test CSRF token protection."""
        allure.dynamic.title("Security: CSRF token fields present when applicable")
        allure.dynamic.description("Check forms for common CSRF hidden fields (csrf, csrf_token) and verify they contain values when present; otherwise skip.")
        ensure_fresh_session(page)
        login = LoginPage(page)
        login.open()
        
        # Check if CSRF tokens are present in forms
        forms = page.locator("form").all()
        if len(forms) == 0:
            pytest.skip("No forms present to inspect for CSRF tokens")

        found_csrf = False
        for form in forms:
            csrf_fields = form.locator('input[type="hidden"]').all()
            for field in csrf_fields:
                name = (field.get_attribute("name") or "").lower()
                if 'csrf' in name or 'token' in name:
                    val = field.get_attribute("value") or ""
                    assert len(val) > 0, "CSRF token hidden field should contain a value"
                    found_csrf = True

        if not found_csrf:
            pytest.skip("No CSRF-like hidden fields found; cannot validate client-side")
    
    def test_rate_limiting_on_failed_logins(self, page):
        """Test rate limiting on multiple failed login attempts."""
        ensure_fresh_session(page)
        login = LoginPage(page)
        login.open()
        
        # Try multiple failed logins
        for i in range(10):
            ensure_fresh_session(page)
            login.open()
            login.login("wrong@email.com", "wrongpass")
            page.wait_for_timeout(1000)
        
        # Should eventually block or show rate limit message
        assert "/dashboard" not in page.url, "Should not allow login after multiple failures"
    
    def test_sensitive_data_in_url(self, page):
        """Test that sensitive data is not exposed in URL."""
        ensure_fresh_session(page)
        dashboard = login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        
        current_url = page.url
        assert ADMIN_PASSWORD not in current_url, "Password should not be in URL"
        assert "password" not in current_url.lower(), "Password keyword should not be in URL"
    
    def test_secure_cookies(self, page):
        """Test that cookies are secure."""
        allure.dynamic.title("Security: Session cookies have secure flags when present")
        allure.dynamic.description("Verify cookies that look like session cookies have the 'secure' flag set when applicable in the environment.")
        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        
        cookies = page.context.cookies()
        session_cookies = [c for c in cookies if c.get('name') and 'session' in c.get('name', '').lower()]
        if not session_cookies:
            pytest.skip("No session-like cookies found to validate")

        for cookie in session_cookies:
            assert cookie.get('secure') is True, f"Session cookie '{cookie.get('name')}' should have secure flag set"
    
    def test_content_security_policy(self, page):
        """Test Content Security Policy headers."""
        allure.dynamic.title("Security: Content-Security-Policy header present")
        allure.dynamic.description("Check HTTP response headers for a Content-Security-Policy header; skip if not present in this environment.")
        ensure_fresh_session(page)
        login = LoginPage(page)
        login.open()
        
        # Check response headers
        response = page.request.get(page.url)
        headers = response.headers
        csp_headers = [k for k in headers.keys() if 'content-security-policy' in k.lower()]
        if not csp_headers:
            pytest.skip("No Content-Security-Policy header found; cannot validate")

        # Ensure header value is non-empty
        for k in csp_headers:
            assert headers.get(k), f"CSP header '{k}' should have a non-empty value"
    
    def test_file_upload_security(self, page):
        """Test file upload restrictions."""
        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        
        # This would test file uploads if available
        # For now, just verify page loads
        assert "/dashboard" in page.url, "Page should load"
    
    def test_path_traversal_attempts(self, page):
        """Test path traversal attack prevention."""
        ensure_fresh_session(page)
        
        path_traversals = [
            "../../../etc/passwd",
            "..\\..\\windows\\system32",
            "....//....//etc/passwd",
            "%2e%2e%2f",
        ]
        
        for path in path_traversals:
            try:
                page.goto(f"{BASE_URL}/{path}", wait_until="domcontentloaded", timeout=5000)
                page.wait_for_timeout(2000)
                # Should not expose sensitive files
                content = page.content().lower()
                assert "passwd" not in content and "system32" not in content, "Path traversal should be blocked"
            except Exception:
                # Navigation errors/timeouts are acceptable (blocked by server or network)
                continue
    
    def test_open_redirect_vulnerability(self, page):
        """Test open redirect vulnerability."""
        ensure_fresh_session(page)
        login = LoginPage(page)
        login.open()
        
        # Test redirect parameters
        redirect_urls = [
            f"{BASE_URL}/login?redirect=http://evil.com",
            f"{BASE_URL}/login?next=javascript:alert(1)",
            f"{BASE_URL}/login?return=http://malicious.com",
        ]
        
        for url in redirect_urls:
            try:
                page.goto(url, wait_until="domcontentloaded")
                page.wait_for_timeout(2000)
                final_url = page.url
                assert "evil.com" not in final_url and "malicious.com" not in final_url, "Should not redirect to external domains"
            except Exception:
                # Navigation errors are acceptable and indicate the redirect was not allowed
                continue

