"""
Simple configuration usage examples and validation script.
Run this script to test the configuration system.
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.config_loader import ConfigLoader, ConfigError, get_env_config, get_config_value
from config.settings import Settings, setup_framework

def test_basic_config_loading():
    """Test basic configuration loading."""
    print("🔧 Testing basic configuration loading...")
    
    try:
        # Load configuration
        config = ConfigLoader.load_config()
        print(f"✅ Configuration loaded successfully")
        print(f"   Available environments: {list(config['environments'].keys())}")
        
        # Test environment-specific config
        for env in ['dev', 'staging', 'prod']:
            env_config = ConfigLoader.get_environment_config(env)
            print(f"   {env}: {env_config['base_url']}")
            
        print()
        
    except Exception as e:
        print(f"❌ Configuration loading failed: {e}")
        return False
    
    return True

def test_environment_variables():
    """Test environment variable substitution."""
    print("🔧 Testing environment variable substitution...")
    
    # Set test environment variables
    os.environ['DB_PASSWORD'] = 'test_password_123'
    os.environ['TEST_PASSWORD'] = 'user_password_456'
    
    try:
        config = get_env_config('dev')
        db_password = config['database']['password']
        
        if db_password == 'test_password_123':
            print("✅ Environment variable substitution working")
        else:
            print(f"❌ Environment variable substitution failed: got '{db_password}'")
            return False
            
        print()
        
    except Exception as e:
        print(f"❌ Environment variable test failed: {e}")
        return False
    
    return True

def test_config_value_access():
    """Test dot notation configuration access."""
    print("🔧 Testing configuration value access...")
    
    try:
        # Test environment-specific values
        base_url = get_config_value('base_url', environment='dev')
        print(f"✅ base_url (dev): {base_url}")
        
        # Test global configuration values
        log_level = get_config_value('logging.level')
        print(f"✅ log_level: {log_level}")
        
        # Test with defaults
        missing_value = get_config_value('non.existent.key', 'default_value')
        print(f"✅ default value handling: {missing_value}")
        
        print()
        
    except Exception as e:
        print(f"❌ Configuration access failed: {e}")
        return False
    
    return True

def test_settings_initialization():
    """Test Settings class initialization."""
    print("🔧 Testing Settings initialization...")
    
    try:
        # Initialize settings
        setup_framework('dev')
        
        # Test convenience methods
        base_url = Settings.get_base_url()
        browser = Settings.get_browser()
        is_headless = Settings.is_headless()
        
        print(f"✅ Settings initialized successfully")
        print(f"   Base URL: {base_url}")
        print(f"   Browser: {browser}")
        print(f"   Headless: {is_headless}")
        
        print()
        
    except Exception as e:
        print(f"❌ Settings initialization failed: {e}")
        return False
    
    return True

def test_error_handling():
    """Test configuration error handling."""
    print("🔧 Testing error handling...")
    
    try:
        # Test invalid environment
        try:
            get_env_config('invalid_env')
            print("❌ Should have raised ConfigError for invalid environment")
            return False
        except ConfigError:
            print("✅ Invalid environment error handled correctly")
        
        # Test invalid configuration section
        try:
            ConfigLoader.get_global_config('invalid_section')
            print("❌ Should have raised ConfigError for invalid section")
            return False
        except ConfigError:
            print("✅ Invalid section error handled correctly")
        
        print()
        
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False
    
    return True

def print_configuration_summary():
    """Print a summary of the current configuration."""
    print("📋 Configuration Summary")
    print("=" * 50)
    
    try:
        current_env = ConfigLoader.get_current_environment()
        config = get_env_config(current_env)
        
        print(f"Environment: {current_env}")
        print(f"Base URL: {config['base_url']}")
        print(f"Browser: {config['browser']}")
        print(f"Headless: {config['headless']}")
        print(f"Implicit Wait: {config['implicit_wait']}s")
        print(f"Explicit Wait: {config['explicit_wait']}s")
        print(f"Page Load Timeout: {config['page_load_timeout']}s")
        
        # Global configuration
        logging_config = ConfigLoader.get_global_config('logging')
        reporting_config = ConfigLoader.get_global_config('reporting')
        
        print(f"\nLogging Level: {logging_config['level']}")
        print(f"Report Directory: {reporting_config['report_dir']}")
        print(f"Screenshot on Failure: {reporting_config['screenshot_on_failure']}")
        
        print("\n" + "=" * 50)
        
    except Exception as e:
        print(f"❌ Failed to generate summary: {e}")

def main():
    """Run all configuration tests."""
    print("🚀 Configuration System Test Suite")
    print("=" * 50)
    
    tests = [
        test_basic_config_loading,
        test_environment_variables,
        test_config_value_access,
        test_settings_initialization,
        test_error_handling,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        if test():
            passed += 1
        else:
            failed += 1
    
    print(f"\n📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All configuration tests passed!")
        print_configuration_summary()
    else:
        print("⚠️  Some configuration tests failed. Check the output above.")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)