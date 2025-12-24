# Trackzyng Playwright Automation

Playwright + Pytest automation framework for Trackzyng staging portal.

## Overview

This is a comprehensive test automation framework covering all sections of the Trackzyng application including:
- Login/Authentication
- Dashboard
- Reports
- Users Management
- Branch Management
- Settings
- Navigation

## Test Credentials

Two set of credentials are configured:
1. Admin: `shashwatrane@codezyng.com` / `test1234`
2. Unauthorised User: `shishir@codezyng.com` / `test1234`

## Project Structure

```
trackzyng_playwright/
├── pages/              # Page Object Models
│   ├── base_page.py        # Base page class with common methods
│   ├── login_page.py       # Login page object
│   ├── dashboard_page.py   # Dashboard page object
│   ├── reports_page.py     # Reports section page object
│   ├── users_page.py       # Users management page object
│   ├── branch_page.py      # Branch management page object
│   ├── settings_page.py    # Settings page object
│   └── navigation_page.py  # Navigation menu page object
├── tests/              # Test suites
│   ├── test_login.py              # Login tests
│   ├── test_comprehensive_login.py # Comprehensive login scenarios
│   ├── test_dashboard.py          # Dashboard tests
│   ├── test_comprehensive_dashboard.py # Comprehensive dashboard tests
│   ├── test_reports.py            # Reports section tests
│   ├── test_users.py              # Users management tests
│   ├── test_branch.py             # Branch management tests
│   ├── test_settings.py           # Settings tests
│   ├── test_navigation.py         # Navigation tests
│   ├── test_end_to_end.py         # End-to-end workflow tests
│   ├── test_complete_workflow.py  # Complete workflow tests
│   └── test_ui_elements.py        # UI elements tests
├── utils/              # Helper utilities
│   └── test_helpers.py    # Test helper functions
└── config/             # Configuration
    └── config.py           # Test configuration and credentials
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
playwright install
```

2. (Optional) Install Allure command-line tool:
```bash
# macOS
brew install allure

# Or download from: https://github.com/allure-framework/allure2/releases
```

## Running Tests

### Run all tests and generate reports:
```bash
python run_tests.py
```

This will:
- Run all tests
- Capture screenshots on failures (saved in `screenshots/`)
- Generate HTML report (`reports/report.html`)
- Generate Allure results (`reports/allure-results/`)
- Generate Excel report (`reports/Test_Results_*.xlsx`)

### Run tests manually:
```bash
# Run all tests
pytest -v

# Run specific test file
pytest tests/test_reports.py -v

# Run with HTML report
pytest --html=reports/report.html --self-contained-html

# Run with Allure
pytest --alluredir=reports/allure-results
```

### Generate reports after test run:
```bash
# Generate Excel report
python generate_report.py

# Generate Allure HTML report (if allure CLI is installed)
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

## Test Coverage

### Login Tests
- Login page loading
- Successful login with both credentials
- Invalid credentials handling
- Email normalization (trim, case)
- Session persistence
- Direct dashboard access protection

### Dashboard Tests
- Dashboard loading after login
- Dashboard elements presence
- Page interactions
- Refresh functionality
- Content visibility

### Reports Tests
- Reports page loading
- Search functionality
- Filter by date
- View reports
- Export functionality
- Pagination
- Create/Edit/Delete operations

### Users Management Tests
- Users page loading
- Search users
- Filter by role and status
- Create user
- View user details
- Edit user
- Delete user
- Form validation
- Pagination

### Branch Management Tests
- Branch page loading
- Search branches
- Filter by location and status
- Create branch
- View branch details
- Edit branch
- Delete branch
- Form validation
- Pagination

### Settings Tests
- Settings page loading
- General settings
- Profile settings update
- Security settings (password change)
- Notifications settings
- Tab switching
- Save/Cancel functionality

### Navigation Tests
- Menu visibility
- Navigation between sections
- Logout functionality
- Direct URL access

### End-to-End Tests
- Complete user journeys
- Multi-section workflows
- Session persistence
- Error recovery

### Security Tests
- SQL injection prevention
- XSS attack prevention
- Password visibility
- Session hijacking prevention
- CSRF protection
- Rate limiting
- Secure cookies
- Path traversal prevention
- Open redirect vulnerability

### Data Validation Tests
- Email format validation
- Password strength validation
- Required field validation
- Max length validation
- Special character handling
- Unicode character handling
- Case sensitivity validation

### Performance Tests
- Page load time
- Login response time
- Dashboard load performance
- Image load performance
- API response time
- Memory usage
- Caching effectiveness

### Accessibility Tests
- Keyboard navigation
- ARIA labels
- Form labels
- Color contrast
- Screen reader compatibility
- Focus indication
- Alt text for images

### Edge Cases Tests
- Extremely long inputs
- Special characters
- Unicode handling
- Empty/whitespace inputs
- Rapid button clicks
- Browser back button
- Page refresh during actions
- Multiple tabs/sessions
- Network timeouts
- Extreme viewport sizes

### Positive Test Cases
- Successful login flows
- Feature accessibility
- Data display
- Form submissions
- Navigation flows

## Features

- **Page Object Model**: Clean separation of page logic and tests
- **Comprehensive Coverage**: Tests for all major sections and features
- **Multiple User Support**: Tests for both admin and regular users
- **Error Handling**: Graceful handling of missing elements
- **Flexible Selectors**: Multiple selector strategies for robustness
- **Helper Functions**: Reusable test utilities
- **Screenshot Capture**: Automatic screenshots on test failures
- **Allure Reports**: Detailed test reports with Allure
- **Excel Reports**: Test results exported to Excel format with test case IDs
- **Test Case IDs**: All tests mapped to test case IDs (TC_LOGIN_001, etc.)

## Reports

After running tests, the following reports are generated:

1. **HTML Report** (`reports/report.html`): Standard pytest HTML report
2. **Allure Results** (`reports/allure-results/`): Allure JSON results
3. **Allure HTML Report** (`reports/allure-report/`): Generated Allure HTML report
4. **Excel Report** (`reports/Test_Results_*.xlsx`): Excel file with test results in the format:
   - Test Case ID
   - Test Scenario
   - Test Steps
   - Test Data
   - Precondition
   - Expected Output
   - Actual Output
   - Status (Pass/Fail)
   - Remarks
   - Tested By
   - Tested Date
   - Duration

5. **Screenshots** (`screenshots/`): Screenshots captured on test failures

## Configuration

Edit `config/config.py` to update:
- Base URL
- Test credentials
- Timeout values
