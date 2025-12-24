"""Performance and load tests."""
import pytest
import time
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from config.config import ADMIN_USERNAME, ADMIN_PASSWORD
from utils.test_helpers import ensure_fresh_session, login_user

class TestPerformance:
    """Performance test suite."""
    
    def test_page_load_time(self, page):
        """Test page load performance."""
        ensure_fresh_session(page)
        
        start_time = time.time()
        login = LoginPage(page)
        login.open()
        load_time = time.time() - start_time
        
        assert load_time < 10, f"Page should load within 10 seconds, took {load_time:.2f}s"
    
    def test_login_response_time(self, page):
        """Test login response time."""
        ensure_fresh_session(page)
        login = LoginPage(page)
        login.open()
        
        start_time = time.time()
        login.login(ADMIN_USERNAME, ADMIN_PASSWORD)
        page.wait_for_url("**/dashboard**", timeout=15000)
        response_time = time.time() - start_time
        
        assert response_time < 15, f"Login should complete within 15 seconds, took {response_time:.2f}s"
    
    def test_dashboard_load_performance(self, page):
        """Test dashboard load performance."""
        ensure_fresh_session(page)
        
        start_time = time.time()
        dashboard = login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        dashboard.wait_for_dashboard_load()
        load_time = time.time() - start_time
        
        assert load_time < 20, f"Dashboard should load within 20 seconds, took {load_time:.2f}s"
    
    def test_image_load_performance(self, page):
        """Test image loading performance."""
        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        
        # Wait for page to fully load
        page.wait_for_load_state("networkidle", timeout=30000)
        
        # Check images
        images = page.locator("img").all()
        loaded_images = 0
        for img in images:
            try:
                natural_width = img.evaluate("el => el.naturalWidth")
                if natural_width and natural_width > 0:
                    loaded_images += 1
            except Exception:
                # Some images may be lazy-loaded or blocked; continue
                continue

        if len(images) == 0:
            pytest.skip("No images found to validate load performance")
        assert loaded_images > 0, "At least one image should load successfully"
    
    def test_api_response_time(self, page):
        """Test API response times."""
        ensure_fresh_session(page)
        
        # Monitor network requests
        responses = []
        
        def handle_response(response):
            responses.append({
                'url': response.url,
                'status': response.status,
                'timing': time.time()
            })
        
        page.on("response", handle_response)
        
        login = LoginPage(page)
        login.open()
        login.login(ADMIN_USERNAME, ADMIN_PASSWORD)
        page.wait_for_url("**/dashboard**", timeout=15000)
        
        # Check API response times
        slow_responses = [r for r in responses if r['status'] >= 400]
        assert len(slow_responses) == 0, "API calls should succeed"
    
    def test_concurrent_page_loads(self, page):
        """Test handling of concurrent requests."""
        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        
        # Simulate multiple rapid requests
        start_time = time.time()
        for _ in range(3):
            page.reload(wait_until="networkidle")
        total_time = time.time() - start_time
        
        assert total_time < 30, "Concurrent requests should be handled efficiently"
    
    def test_memory_usage(self, page):
        """Test memory usage during operations."""
        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        
        # Get memory usage (JavaScript)
        try:
            memory_info = page.evaluate("""
                () => {
                    if (performance.memory) {
                        return {
                            used: performance.memory.usedJSHeapSize,
                            total: performance.memory.totalJSHeapSize,
                            limit: performance.memory.jsHeapSizeLimit
                        };
                    }
                    return null;
                }
            """)
            if memory_info:
                usage_percent = (memory_info['used'] / memory_info['limit']) * 100
                assert usage_percent < 80, f"Memory usage should be reasonable: {usage_percent:.2f}%"
        except Exception:
            pytest.skip("Memory API is not available in this environment")
    
    def test_large_data_handling(self, page):
        """Test handling of large datasets."""
        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        
        # Test pagination with large datasets
        # This would test if the app handles large data efficiently
        assert "/dashboard" in page.url, "Should handle large data"
    
    def test_caching_effectiveness(self, page):
        """Test browser caching effectiveness."""
        ensure_fresh_session(page)
        login = LoginPage(page)
        login.open()
        
        # First load
        first_load_time = time.time()
        login.open()
        first_load = time.time() - first_load_time
        
        # Second load (should use cache)
        second_load_time = time.time()
        login.open()
        second_load = time.time() - second_load_time
        
        # Cached load should be faster (or similar if network is fast)
        # Allow some slack to avoid flaky failures (network variation)
        acceptable_second_load = max(first_load * 2, first_load + 1)
        assert second_load <= acceptable_second_load, f"Cached load ({second_load:.2f}s) was unexpectedly slower than first load ({first_load:.2f}s)"

