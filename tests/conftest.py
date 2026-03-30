"""
Pytest configuration and fixtures for the Selenium test framework.
Provides WebDriver management, logging setup, and test infrastructure.
"""

import pytest
import logging
import os
from datetime import datetime
from utils.driver_factory import DriverFactory
from config.settings import Settings, setup_framework
from pages.login_page import LoginPage

# Initialize framework on import
setup_framework()
logger = logging.getLogger(__name__)


# ============= Session Scope Fixtures =============

@pytest.fixture(scope="session")
def test_environment():
    """Setup test environment for the entire session."""
    env = os.getenv("TEST_ENV", "dev")
    logger.info(f"Starting test session for environment: {env}")
    
    # Initialize framework settings
    Settings.initialize(env)
    
    yield env
    
    logger.info("Test session completed")


# ============= Function Scope Fixtures =============

@pytest.fixture(scope="function")
def driver(test_environment):
    """
    Create and configure WebDriver instance for each test.
    
    Args:
        test_environment: Environment configuration from session fixture
        
    Yields:
        WebDriver: Configured WebDriver instance
    """
    logger.info("Creating WebDriver instance for test")
    
    # Get browser configuration
    browser = Settings.get_browser()
    headless = Settings.is_headless()
    
    # Create driver instance
    driver_instance = DriverFactory.create_driver(browser=browser, headless=headless)
    
    # Configure driver timeouts
    implicit_wait = Settings.get_wait_timeout('implicit')
    page_load_timeout = Settings.get_wait_timeout('page_load')
    
    driver_instance.implicitly_wait(implicit_wait)
    driver_instance.set_page_load_timeout(page_load_timeout)
    
    # Maximize window if not headless
    if not headless:
        driver_instance.maximize_window()
    
    logger.info(f"WebDriver created successfully - Browser: {browser}, Headless: {headless}")
    
    yield driver_instance
    
    # Teardown - quit driver
    try:
        DriverFactory.quit_driver(driver_instance)
        logger.info("WebDriver quit successfully")
    except Exception as e:
        logger.error(f"Error during WebDriver cleanup: {str(e)}")


# ============= Page Object Fixtures =============

@pytest.fixture
def login_page(driver):
    """
    Create LoginPage instance.
    
    Args:
        driver: WebDriver instance
        
    Returns:
        LoginPage: Configured login page object
    """
    return LoginPage(driver)


# ============= Utility Fixtures =============

@pytest.fixture
def test_data():
    """Provide test data for login scenarios."""
    return {
        "valid_email": "test@example.com",
        "valid_password": "Test@123456",
        "invalid_emails": [
            "invalid-email",
            "@gmail.com", 
            "user@",
            "user@domain",
            "user..double@gmail.com",
            "user name@gmail.com",
        ],
        "invalid_passwords": [
            "wrong",
            "12345",
            "",
            " ",
            "password123!@#$%^&*()",
        ],
        "sql_injection_patterns": [
            "admin'--",
            "admin' OR '1'='1",
            "'; DROP TABLE users; --",
            "admin' UNION SELECT * FROM users --",
        ],
    }


# ============= Screenshot and Reporting Fixtures =============

@pytest.fixture(autouse=True)
def screenshot_on_failure(request, driver):
    """
    Automatically capture screenshot on test failure.
    
    Args:
        request: Pytest request object
        driver: WebDriver instance
    """
    yield
    
    # Check if test failed
    if request.node.rep_call.failed if hasattr(request.node, 'rep_call') else False:
        try:
            # Create screenshots directory
            screenshot_dir = "reports/screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            
            # Generate screenshot filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = request.node.name.replace("::", "_").replace("[", "_").replace("]", "_")
            screenshot_path = os.path.join(screenshot_dir, f"{test_name}_{timestamp}.png")
            
            # Capture screenshot
            driver.save_screenshot(screenshot_path)
            logger.error(f"Test failed - Screenshot saved: {screenshot_path}")
            
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {str(e)}")


@pytest.fixture(autouse=True)
def log_test_execution(request):
    """
    Log test execution start and completion.
    
    Args:
        request: Pytest request object
    """
    test_name = request.node.name
    logger.info(f"Starting test: {test_name}")
    
    start_time = datetime.now()
    
    yield
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    if hasattr(request.node, 'rep_call'):
        if request.node.rep_call.passed:
            logger.info(f"Test PASSED: {test_name} (Duration: {duration:.2f}s)")
        elif request.node.rep_call.failed:
            logger.error(f"Test FAILED: {test_name} (Duration: {duration:.2f}s)")
        elif request.node.rep_call.skipped:
            logger.warning(f"Test SKIPPED: {test_name}")
    else:
        logger.info(f"Test completed: {test_name} (Duration: {duration:.2f}s)")


# ============= Browser-specific Fixtures =============

@pytest.fixture(params=["chrome", "firefox"])
def multi_browser_driver(request, test_environment):
    """
    Parametrized fixture for cross-browser testing.
    
    Args:
        request: Pytest request object
        test_environment: Environment configuration
        
    Yields:
        WebDriver: Browser-specific WebDriver instance
    """
    browser = request.param
    logger.info(f"Creating {browser} driver for cross-browser test")
    
    driver_instance = DriverFactory.create_driver(browser=browser, headless=True)
    
    yield driver_instance
    
    DriverFactory.quit_driver(driver_instance)
    logger.info(f"{browser} driver quit successfully")


# ============= Pytest Hooks =============

def pytest_configure(config):
    """Configure pytest with custom settings."""
    # Add custom markers
    config.addinivalue_line("markers", "login: Login functionality tests")
    config.addinivalue_line("markers", "critical: Critical path tests")
    config.addinivalue_line("markers", "cross_browser: Cross-browser compatibility tests")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to add test result information to the request object.
    This enables access to test results in fixtures.
    """
    outcome = yield
    rep = outcome.get_result()
    
    setattr(item, f"rep_{rep.when}", rep)


def pytest_collection_modifyitems(config, items):
    """
    Modify test collection to add markers based on test names.
    
    Args:
        config: Pytest configuration
        items: List of collected test items
    """
    for item in items:
        # Add login marker to login tests
        if "login" in item.name.lower():
            item.add_marker(pytest.mark.login)
        
        # Add critical marker to critical tests
        if "critical" in item.name.lower() or "invalid_login" in item.name:
            item.add_marker(pytest.mark.critical)


def pytest_html_report_title(report):
    """Customize HTML report title."""
    report.title = "Facebook Login Test Execution Report"


def pytest_html_results_table_header(cells):
    """Customize HTML report table headers."""
    cells.insert(2, '<th class="sortable time" data-column-type="time">Duration</th>')


def pytest_html_results_table_row(report, cells):
    """Customize HTML report table rows."""  
    cells.insert(2, f'<td class="col-time">{report.duration:.2f}s</td>')