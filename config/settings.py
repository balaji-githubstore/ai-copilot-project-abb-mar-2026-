"""
Centralized settings and logging configuration for the Selenium pytest framework.
Handles initial setup and provides configuration access patterns.
"""

import logging
import logging.handlers
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from config.config_loader import ConfigLoader, ConfigError

class LogConfig:
    """Centralized logging configuration using YAML settings."""
    
    _logger_configured = False
    
    @classmethod
    def setup_logging(cls, environment: str = None, log_level: Optional[str] = None) -> logging.Logger:
        """
        Configure logging based on YAML configuration.
        
        Args:
            environment: Environment name for config lookup
            log_level: Override log level (DEBUG, INFO, WARNING, ERROR)
            
        Returns:
            Configured root logger
        """
        if cls._logger_configured:
            return logging.getLogger()
        
        try:
            # Load logging configuration from YAML
            log_config = ConfigLoader.get_global_config('logging')
            
            # Override log level if provided
            if log_level:
                log_config['level'] = log_level.upper()
            
            # Create logs directory
            log_dir = Path(log_config.get('log_dir', 'logs'))
            log_dir.mkdir(exist_ok=True)
            
            # Configure root logger
            root_logger = logging.getLogger()
            root_logger.setLevel(getattr(logging, log_config['level']))
            
            # Clear any existing handlers
            if root_logger.hasHandlers():
                root_logger.handlers.clear()
            
            # Create formatter
            formatter = logging.Formatter(
                log_config['format'],
                datefmt=log_config['date_format']
            )
            
            # Setup file handler if enabled
            if log_config.get('log_to_file', True):
                cls._setup_file_handler(root_logger, formatter, log_config, log_dir)
            
            # Setup console handler if enabled  
            if log_config.get('log_to_console', True):
                cls._setup_console_handler(root_logger, formatter, log_config)
            
            cls._logger_configured = True
            root_logger.info("Logging configuration initialized successfully")
            root_logger.info(f"Environment: {ConfigLoader.get_current_environment()}")
            
            return root_logger
            
        except ConfigError as e:
            # Fallback to basic logging if config fails
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to load logging config, using defaults: {e}")
            return logging.getLogger()
    
    @classmethod
    def _setup_file_handler(cls, logger: logging.Logger, formatter: logging.Formatter, 
                           config: dict, log_dir: Path) -> None:
        """Setup rotating file handler for logging."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"test_execution_{timestamp}.log"
        
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=config.get('max_bytes', 10485760),  # 10 MB default
            backupCount=config.get('backup_count', 5)
        )
        
        file_level = config.get('file_level', config['level'])
        file_handler.setLevel(getattr(logging, file_level))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    @classmethod 
    def _setup_console_handler(cls, logger: logging.Logger, formatter: logging.Formatter,
                              config: dict) -> None:
        """Setup console handler for logging."""
        console_handler = logging.StreamHandler(sys.stdout)
        
        console_level = config.get('console_level', config['level'])
        console_handler.setLevel(getattr(logging, console_level))
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """Get a named logger with proper configuration."""
        if not cls._logger_configured:
            cls.setup_logging()
        return logging.getLogger(name)

class Settings:
    """Central settings management for the test framework."""
    
    _initialized = False
    
    @classmethod
    def initialize(cls, environment: str = None) -> None:
        """
        Initialize framework settings.
        
        Args:
            environment: Target environment (dev, staging, prod)
        """
        if cls._initialized:
            return
        
        # Setup logging first
        LogConfig.setup_logging(environment)
        logger = logging.getLogger(__name__)
        
        try:
            # Load environment configuration
            env_config = ConfigLoader.get_environment_config(environment)
            logger.info(f"Framework initialized for environment: {ConfigLoader.get_current_environment()}")
            
            # Set up directories
            cls._setup_directories()
            
            cls._initialized = True
            
        except ConfigError as e:
            logger.error(f"Failed to initialize settings: {e}")
            raise
    
    @classmethod
    def _setup_directories(cls) -> None:
        """Create necessary directories for reports, logs, etc."""
        try:
            report_config = ConfigLoader.get_global_config('reporting')
            
            # Create report directories
            report_dir = Path(report_config.get('report_dir', 'reports'))
            screenshot_dir = Path(report_config.get('screenshot_dir', 'reports/screenshots'))
            
            report_dir.mkdir(exist_ok=True)
            screenshot_dir.mkdir(parents=True, exist_ok=True)
            
            logger = logging.getLogger(__name__)
            logger.info("Framework directories created successfully")
            
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.warning(f"Failed to create directories: {e}")
    
    @classmethod
    def get_base_url(cls) -> str:
        """Get base URL for current environment."""
        return ConfigLoader.get_value('base_url')
    
    @classmethod
    def get_browser(cls) -> str:
        """Get browser configuration for current environment."""
        return ConfigLoader.get_value('browser', 'chrome')
    
    @classmethod
    def is_headless(cls) -> bool:
        """Check if headless mode is enabled."""
        return ConfigLoader.get_value('headless', False)
    
    @classmethod
    def get_wait_timeout(cls, wait_type: str = 'explicit') -> int:
        """
        Get wait timeout values.
        
        Args:
            wait_type: Type of wait ('implicit', 'explicit', 'page_load')
            
        Returns:
            Timeout value in seconds
        """
        timeout_key = f"{wait_type}_wait"
        if wait_type == 'page_load':
            timeout_key = 'page_load_timeout'
        
        return ConfigLoader.get_value(timeout_key, 10)
    
    @classmethod
    def get_test_data(cls, data_key: str) -> dict:
        """
        Get test data configuration.
        
        Args:
            data_key: Test data key (e.g., 'users', 'test_urls')
            
        Returns:
            Dict containing test data
        """
        return ConfigLoader.get_global_config('test_data').get(data_key, {})
    
    @classmethod
    def is_initialized(cls) -> bool:
        """Check if settings have been initialized."""
        return cls._initialized
    
    @classmethod
    def reset(cls) -> None:
        """Reset settings (useful for testing)."""
        cls._initialized = False
        LogConfig._logger_configured = False
        ConfigLoader.reload_config()

# Convenience functions for common configuration access
def get_env_setting(key: str, default=None):
    """Get environment-specific setting."""
    return ConfigLoader.get_value(key, default)

def get_global_setting(section: str, key: str = None, default=None):
    """Get global configuration setting."""
    config = ConfigLoader.get_global_config(section)
    if key:
        return config.get(key, default)
    return config

def setup_framework(environment: str = None):
    """Quick setup function for the entire framework."""
    Settings.initialize(environment)
    return LogConfig.get_logger(__name__)