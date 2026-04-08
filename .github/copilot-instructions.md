Repository summary

- Purpose: End-to-end UI tests (Facebook login scenarios) implemented with pytest and Selenium-style WebDriver factories. Tests live under tests/ and produce HTML reports in reports/.

Build, test and lint commands

- Install deps (venv recommended):
  python -m pip install -r requirements-dev.txt

- Run full test suite (default HTML report):
  python -m pytest
  or use the runner with presets: python run_tests.py all

- Run a single test (preferred — precise):
  python run_tests.py single <short_test_name>
  Example: python run_tests.py single invalid_login_empty_fields

  Or using pytest directly (module::class::test):
  python -m pytest tests/test_login/test_login.py::TestLogin::test_invalid_login_empty_fields -q

- Run specific groups via markers (pytest.ini defines markers):
  pytest -m login
  pytest -m "critical and login"

- Parallel runs: pytest -n auto (pytest-xdist required)

- Lint / static checks / hooks:
  - mypy: python -m mypy .
  - bandit security scan: python -m bandit -r .
  - pre-commit hooks: pre-commit run --all-files

High-level architecture

- tests/
  - Test cases are organized by feature (e.g., tests/test_login/). Tests follow pytest discovery conventions (pytest.ini: testpaths=tests, python_files=test_*.py, classes Test*).

- config/
  - Central test setup and environment handling (config_loader, settings). Environment selection via TEST_ENV env var. run_tests.py calls setup_framework from config.settings.

- utils/
  - DriverFactory and helpers for WebDriver lifecycle, screenshot capture, and common utilities used by tests and setup.

- pages/ and locators/
  - Page object model: page classes and locator definitions; tests interact via page objects to keep tests readable.

- reports/ and logs/
  - HTML test reports and screenshots are written to reports/ (runner and pytest addopts configured to write reports). Logs are written to logs/.

Key conventions (repository-specific)

- Test discovery and naming
  - Tests follow pytest naming: test_*.py, Test* classes, test_* functions (driven by pytest.ini).

- Test markers
  - Markers are predeclared in pytest.ini (smoke, regression, critical, slow, api, ui, login, checkout). Use these markers instead of ad-hoc naming for grouping.

- Test runner script
  - run_tests.py provides convenient, documented commands (invalid, all, critical, single, cross-browser, setup). Use this for reproducible runs and to generate HTML reports.

- Single-test naming used by runner
  - run_tests.py single expects the short test method name (without the test_ prefix). E.g., to run test_invalid_login_empty_fields, pass single invalid_login_empty_fields.

- Assertions
  - Tests must use assertpy assertions (assert_that) rather than raw Python asserts or pytest built-ins. Always include: from assertpy import assert_that

- Configuration via env vars
  - TEST_ENV (dev/staging/prod), BROWSER (chrome/firefox/edge), HEADLESS (true/false) — runner and config loader read/override these.

- HTML reports and artifacts
  - Tests and runner generate self-contained HTML reports (--self-contained-html). Screenshots on failure are saved to reports/screenshots/.

Other AI/assistant configs to consider

- Check and reuse any existing guidance in the repo (if more files appear): .github/, .playwright-mcp, CLAUDE.md, AGENTS.md, CONVENTIONS.md, etc. (This repo already has a .github folder — consider merging this file with existing guidance).

What was created

- .github/copilot-instructions.md added with build/test/lint commands, architecture overview, and repository conventions.

Next step

Would you like to configure any MCP servers (e.g., Playwright) for this project? If yes, specify which (Playwright, Selenium, etc.) and preferred browsers/credentials.
