<!-- Copilot instructions for AI coding agents working on this Playwright test suite -->

Purpose
- Help an AI agent be immediately productive: explain repo structure, test/report flows, and concrete places to change Allure test titles/descriptions and fix flakiness.

Quick architecture (big picture)
- Tests: `tests/` — Pytest + Playwright sync fixtures drive browser-based E2E tests.
- Page objects: `pages/` — encapsulate selectors and interactions (e.g., `DashboardPage`, `ReportsPage`, `BranchPage`). Prefer calling these helpers from tests.
- Fixtures & CI hooks: `conftest.py` — provides `page` fixture and screenshot-on-failure hook.
- Reporting: `pytest.ini` (adds `--alluredir=reports/allure-results`), `utils/report_generator.py` + `generate_report.py` (post-process Allure JSON into additional outputs).

Key developer workflows (commands)
- Run tests, collect Allure results (configured in `pytest.ini`):
  ```bash
  pytest --alluredir=reports/allure-results
  ```
- Generate Allure HTML (requires Allure CLI / `brew install allure`):
  ```bash
  allure generate reports/allure-results -o reports/allure-report --clean
  allure open reports/allure-report
  ```
- Create the Excel/summary report: `python generate_report.py` (calls `utils/report_generator.py`).

Project-specific conventions & patterns
- Naming: Current Allure entries are derived from test function names and docstrings. There are no ubiquitous `allure.title()` or `@allure.description` annotations in tests — add them where clearer names are needed.
- Page-objects: Tests use `login_user(page, ...)` and then call `DashboardPage` helpers like `wait_for_dashboard_load()` and `is_loaded()`. Prefer asserting on page-object methods instead of raw page checks.
- Wait strategy: Tests frequently use `page.wait_for_url("**/dashboard**", timeout=15000)` and page-object `wait_for_*` helpers. Keep explicit waits rather than blind sleeps.
- Screenshots: `conftest.py` saves screenshots on failure to `screenshots/`. Use these paths in Allure attachments when adding richer descriptions.

Common flakiness patterns (where to look)
- Fixture teardown errors in Allure containers: `conftest.py` fixture uses `with sync_playwright() as p:` then yields `page` and calls `context.close()` / `browser.close()` on teardown — failures during teardown can appear as broken tests in Allure. If you see "BrowserContext.close: Connection closed while reading from the driver" in `reports/allure-results/*.json`, consider
  - ensuring tests close pages/contexts only once, or
  - moving teardown into `try/finally` to avoid double-close.
- Broad/weak assertions like `assert True` or OR-chains can hide real failures or create false positives/negatives. Replace them with explicit checks (e.g., verify exported file exists, verify specific UI text).
- Missing or inconsistent waits before assertions (e.g., relying on DOM immediately after click). Use page-object `wait_for_*` helpers and `page.wait_for_url` with timeouts.

Where to update Allure titles & descriptions (concrete files)
- `tests/test_branch.py`: tests that create branches — add `allure.dynamic.title()` like
  `allure.dynamic.title("Branch: Create with valid name -> success")` and a short `allure.dynamic.description()` enumerating steps & expected result.
- `tests/test_reports.py`: exporting/downloading tests — instead of `assert True`, assert the exported file or download confirmation element. Add a descriptive title like
  `allure.dynamic.title("Reports: Export CSV downloads file")` and description with the expected filename/location.
- `tests/test_dashboard_elements.py` & `tests/test_performance.py`: dashboard load checks — use `DashboardPage.wait_for_dashboard_load()` then
  `allure.dynamic.title("Dashboard: Loads and shows metric cards within 20s")` with a description including performance threshold.

Concrete example (how an AI should change a test)
1. Import allure at top: `import allure`
2. Replace docstring-only title with dynamic metadata:

```python
import allure

def test_reports_export_functionality(page):
    allure.dynamic.title("Reports: Export CSV downloads file")
    allure.dynamic.description(
        "Steps:\n1. Login as admin\n2. Navigate to Reports\n3. Click Export\nExpected: download starts and a success toast appears; exported file named report_*.csv"
    )
    # then use page-object methods and explicit assertions
    reports = ReportsPage(page)
    reports.click_export()
    assert reports.download_completed("report_"), "Expected exported file present"
```

Report-generator notes
- `utils/report_generator.py` parses `reports/allure-results/*.json` — update this file only if you want to change column mappings or extract `description`/`fullName` fields. The script already expects `reports/allure-results/` (see `generate_report.py`).

Testing & verification guidance for the agent
- Run a focused subset when changing names/flaky fixes (fast feedback):
  ```bash
  pytest tests/test_reports.py::test_reports_export_functionality -q --maxfail=1
  ```
- Re-run full suite and regenerate Allure HTML only when stable:
  ```bash
  pytest --alluredir=reports/allure-results
  allure generate reports/allure-results -o reports/allure-report --clean
  ```

Takeaways for automated edits
- Prefer adding `allure.dynamic.title()`+`allure.dynamic.description()` to tests where a reviewer needs clarity: branch creation, reports export, dashboard load.
- Replace weak assertions with explicit page-object checks (e.g., `ReportsPage.download_completed()` or `DashboardPage.is_loaded()`), and add short human-readable descriptions.
- Avoid changing the underlying report-generator unless adding new fields — a simpler route is adding richer Allure metadata in tests.

If any areas are unclear or you want me to: (pick one)
- I can open and patch the specific tests (`tests/test_branch.py`, `tests/test_reports.py`, `tests/test_dashboard_elements.py`) to add `allure.dynamic.*` metadata and more explicit assertions.
- I can modify `conftest.py` to harden teardown to avoid BrowserContext close errors.

End of instructions.
