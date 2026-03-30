"""
Configuration loader module for YAML-based settings management.
Supports environment-specific configurations with variable substitution.
"""

import yaml
import os
import re
import logging
from typing import Dict, Any, Optional, Union
from pathlib import Path

logger = logging.getLogger(__name__)

class ConfigError(Exception):
    """Custom exception for configuration-related errors."""
    pass

class ConfigLoader:
    """Load and manage YAML configuration with environment variable support."""
    
    _config = None
    _current_env = None
    
    @classmethod
    def load_config(cls, config_file: Optional[str] = None) -> Dict[str, Any]:
        """
        Load configuration from YAML file with caching.
        
        Args:
            config_file: Path to config file. Defaults to config/config.yaml
            
        Returns:
            Dict containing the full configuration
            
        Raises:
            ConfigError: If config file not found or YAML parsing fails
        """
        if cls._config is not None:
            return cls._config
        
        if config_file is None:
            # Default config file path
            current_dir = Path(__file__).parent
            config_file = current_dir / "config.yaml"
        else:
            config_file = Path(config_file)
        
        if not config_file.exists():
            raise ConfigError(f"Configuration file not found: {config_file}")
        
        try:
            with open(config_file, 'r', encoding='utf-8') as file:
                cls._config = yaml.safe_load(file)
            
            # Validate config structure
            cls._validate_config()
            logger.info(f"Configuration loaded successfully from {config_file}")
            return cls._config
            
        except yaml.YAMLError as e:
            raise ConfigError(f"Error parsing YAML configuration: {str(e)}")
        except Exception as e:
            raise ConfigError(f"Unexpected error loading configuration: {str(e)}")
    
    @classmethod
    def get_environment_config(cls, environment: str = None) -> Dict[str, Any]:
        """
        Get environment-specific configuration with variable substitution.
        
        Args:
            environment: Environment name (dev, staging, prod). Defaults to TEST_ENV
            
        Returns:
            Dict containing environment-specific configuration
            
        Raises:
            ConfigError: If environment not found in config
        """
        config = cls.load_config()
        
        if environment is None:
            environment = os.getenv("TEST_ENV", "dev")
        
        cls._current_env = environment
        
        environments = config.get('environments', {})
        if environment not in environments:
            available = list(environments.keys())
            raise ConfigError(f"Environment '{environment}' not found. Available: {available}")
        
        env_config = environments[environment].copy()
        
        # Replace environment variables recursively
        env_config = cls._replace_env_vars(env_config)
        
        logger.info(f"Loaded configuration for environment: {environment}")
        return env_config
    
    @classmethod
    def get_global_config(cls, section: str) -> Dict[str, Any]:
        """
        Get global configuration section (logging, reporting, etc.).
        
        Args:
            section: Configuration section name
            
        Returns:
            Dict containing section configuration
            
        Raises:
            ConfigError: If section not found
        """
        config = cls.load_config()
        
        if section not in config:
            available = [k for k in config.keys() if k != 'environments']
            raise ConfigError(f"Configuration section '{section}' not found. Available: {available}")
        
        section_config = config[section].copy()
        return cls._replace_env_vars(section_config)
    
    @classmethod
    def get_value(cls, path: str, default: Any = None, environment: str = None) -> Any:
        """
        Get configuration value using dot notation.
        
        Args:
            path: Dot notation path (e.g., 'database.host', 'logging.level')
            default: Default value if path not found
            environment: Environment to search in (optional)
            
        Returns:
            Configuration value or default
            
        Examples:
            get_value('base_url')                    # From current environment
            get_value('logging.level')               # From global config  
            get_value('database.port', 5432)        # With default
            get_value('base_url', env='staging')     # Specific environment
        """
        if environment:
            config = cls.get_environment_config(environment)
        else:
            # Try environment config first, then global
            try:
                config = cls.get_environment_config(cls._current_env or 'dev')
            except ConfigError:
                config = cls.load_config()
        
        keys = path.split('.')
        value = config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value if value is not None else default
    
    @classmethod
    def get_current_environment(cls) -> str:
        """Get the currently loaded environment name."""
        return cls._current_env or os.getenv("TEST_ENV", "dev")
    
    @classmethod
    def reload_config(cls) -> None:
        """Force reload configuration from file."""
        cls._config = None
        cls._current_env = None
        logger.info("Configuration cache cleared - will reload on next access")
    
    @classmethod
    def _replace_env_vars(cls, config_dict: Union[Dict, Any]) -> Any:
        """
        Recursively replace ${VAR_NAME} patterns with environment variables.
        
        Args:
            config_dict: Configuration dictionary or value
            
        Returns:
            Configuration with environment variables substituted
        """
        if isinstance(config_dict, dict):
            return {key: cls._replace_env_vars(value) for key, value in config_dict.items()}
        elif isinstance(config_dict, list):
            return [cls._replace_env_vars(item) for item in config_dict]
        elif isinstance(config_dict, str):
            return cls._substitute_env_vars(config_dict)
        else:
            return config_dict
    
    @classmethod
    def _substitute_env_vars(cls, text: str) -> str:
        """
        Replace ${VAR_NAME} patterns in a string with environment variables.
        
        Args:
            text: String potentially containing ${VAR} patterns
            
        Returns:
            String with variables substituted
        """
        pattern = re.compile(r'\$\{([^}]+)\}')
        
        def replace_var(match):
            var_name = match.group(1)
            var_value = os.getenv(var_name)
            
            if var_value is None:
                logger.warning(f"Environment variable '{var_name}' not set, keeping placeholder")
                return match.group(0)  # Return original ${VAR} if not found
            
            return var_value
        
        return pattern.sub(replace_var, text)
    
    @classmethod
    def _validate_config(cls) -> None:
        """
        Validate configuration structure and required fields.
        
        Raises:
            ConfigError: If configuration is invalid
        """
        if not cls._config:
            raise ConfigError("Configuration is empty")
        
        # Check for required top-level sections
        required_sections = ['environments']
        for section in required_sections:
            if section not in cls._config:
                raise ConfigError(f"Required configuration section '{section}' missing")
        
        # Validate environments section
        environments = cls._config['environments']
        if not environments:
            raise ConfigError("No environments configured")
        
        # Check each environment has required fields
        required_env_fields = ['base_url', 'browser']
        for env_name, env_config in environments.items():
            if not isinstance(env_config, dict):
                raise ConfigError(f"Environment '{env_name}' configuration must be a dictionary")
            
            for field in required_env_fields:
                if field not in env_config:
                    logger.warning(f"Environment '{env_name}' missing recommended field '{field}'")
        
        logger.info("Configuration validation passed")

# Convenience functions for common operations
def get_env_config(environment: str = None) -> Dict[str, Any]:
    """Shortcut to get environment configuration."""
    return ConfigLoader.get_environment_config(environment)

def get_config_value(path: str, default: Any = None, environment: str = None) -> Any:
    """Shortcut to get configuration value by path."""
    return ConfigLoader.get_value(path, default, environment)

def get_current_env() -> str:
    """Shortcut to get current environment name."""
    return ConfigLoader.get_current_environment()