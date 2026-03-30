"""
Test runner script for executing Facebook login tests.
Provides convenient commands for running different test scenarios.
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config.settings import setup_framework

# Setup logging
logger = setup_framework()


def run_command(cmd, description):
    """
    Execute a shell command and handle the result.
    
    Args:
        cmd: Command to execute
        description: Description of what the command does
    """
    print(f"\n🚀 {description}")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 60)
    
    try:
        result = subprocess.run(cmd, capture_output=False, text=True, check=False)
        
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
        else:
            print(f"❌ {description} failed with exit code {result.returncode}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error running {description}: {str(e)}")
        return False


def run_invalid_login_tests():
    """Run all invalid login tests."""
    cmd = [
        "python", "-m", "pytest",
        "tests/test_login/test_login.py::TestLogin::test_invalid_login_wrong_email_format",
        "tests/test_login/test_login.py::TestLogin::test_invalid_login_nonexistent_email", 
        "tests/test_login/test_login.py::TestLogin::test_invalid_login_wrong_password",
        "tests/test_login/test_login.py::TestLogin::test_invalid_login_empty_fields",
        "-v",
        "--html=reports/invalid_login_report.html",
        "--self-contained-html",
        "--tb=short"
    ]
    
    return run_command(cmd, "Running invalid login tests")


def run_all_login_tests():
    """Run all login-related tests."""
    cmd = [
        "python", "-m", "pytest",
        "tests/test_login/",
        "-v",
        "--html=reports/login_tests_report.html", 
        "--self-contained-html",
        "--tb=short",
        "-m", "login"
    ]
    
    return run_command(cmd, "Running all login tests")


def run_critical_login_tests():
    """Run only critical login tests."""
    cmd = [
        "python", "-m", "pytest",
        "tests/test_login/",
        "-v", 
        "--html=reports/critical_login_report.html",
        "--self-contained-html",
        "--tb=short",
        "-m", "critical and login"
    ]
    
    return run_command(cmd, "Running critical login tests")


def run_single_test(test_name):
    """
    Run a specific test by name.
    
    Args:
        test_name: Name of the test method (without test_ prefix)
    """
    full_test_name = f"tests/test_login/test_login.py::TestLogin::test_{test_name}"
    
    cmd = [
        "python", "-m", "pytest", 
        full_test_name,
        "-v",
        "--html=reports/single_test_report.html",
        "--self-contained-html",
        "--tb=long",
        "-s"  # Show print statements
    ]
    
    return run_command(cmd, f"Running single test: {test_name}")


def run_cross_browser_tests():
    """Run tests across multiple browsers."""
    cmd = [
        "python", "-m", "pytest",
        "tests/test_login/test_login.py::TestLogin::test_invalid_login_wrong_email_format",
        "--html=reports/cross_browser_report.html",
        "--self-contained-html",
        "-v"
    ]
    
    return run_command(cmd, "Running cross-browser tests")


def setup_test_environment():
    """Setup test environment and verify configuration."""
    print("🔧 Setting up test environment...")
    
    try:
        # Test configuration loading
        from config.config_loader import ConfigLoader
        config = ConfigLoader.get_environment_config('dev')
        print(f"✅ Configuration loaded for: {ConfigLoader.get_current_environment()}")
        print(f"   Base URL: {config['base_url']}")
        print(f"   Browser: {config['browser']}")
        print(f"   Headless: {config['headless']}")
        
        # Create necessary directories
        os.makedirs("reports", exist_ok=True)
        os.makedirs("reports/screenshots", exist_ok=True)
        os.makedirs("logs", exist_ok=True)
        print("✅ Test directories created")
        
        # Test WebDriver creation
        from utils.driver_factory import DriverFactory
        print("🧪 Testing WebDriver creation...")
        
        try:
            driver = DriverFactory.create_driver(headless=True)
            driver.get("https://www.facebook.com/login")
            print("✅ WebDriver test successful")
            DriverFactory.quit_driver(driver)
        except Exception as e:
            print(f"❌ WebDriver test failed: {str(e)}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Environment setup failed: {str(e)}")
        return False


def main():
    """Main test runner interface."""
    print("=" * 60)
    print("🎯 Facebook Invalid Login Test Runner")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print_usage()
        return
    
    command = sys.argv[1].lower()
    
    # Setup environment first
    if not setup_test_environment():
        print("❌ Environment setup failed. Exiting.")
        sys.exit(1)
    
    success = False
    
    if command == "invalid":
        success = run_invalid_login_tests()
    elif command == "all":
        success = run_all_login_tests()
    elif command == "critical":
        success = run_critical_login_tests()
    elif command == "single" and len(sys.argv) > 2:
        test_name = sys.argv[2]
        success = run_single_test(test_name)
    elif command == "cross-browser":
        success = run_cross_browser_tests()
    elif command == "setup":
        success = True  # Already ran setup
        print("🎉 Environment setup completed successfully!")
    else:
        print_usage()
        return
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 Test execution completed successfully!")
        print("📊 Check the reports/ directory for HTML test reports")
        print("📸 Check reports/screenshots/ for failure screenshots")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    print("=" * 60)


def print_usage():
    """Print usage instructions."""
    print("""
Usage: python run_tests.py <command> [options]

Commands:
  invalid        Run all invalid login test scenarios
  all           Run all login tests 
  critical      Run only critical login tests
  single <name> Run a specific test (e.g., 'single invalid_login_wrong_email_format')
  cross-browser Run tests across multiple browsers
  setup         Setup and verify test environment

Examples:
  python run_tests.py invalid
  python run_tests.py single invalid_login_empty_fields
  python run_tests.py critical
  python run_tests.py setup

Environment Variables:
  TEST_ENV=dev      Set test environment (dev, staging, prod)
  BROWSER=chrome    Override browser (chrome, firefox, edge)  
  HEADLESS=true     Run in headless mode
  
Reports:
  HTML reports will be generated in the reports/ directory
  Screenshots on failure will be saved in reports/screenshots/
    """)


if __name__ == "__main__":
    main()