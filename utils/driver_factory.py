"""
WebDriver factory for managing browser instances with configuration support.
Handles Chrome, Firefox, and Edge browsers with customizable options.
"""

import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from config.config_loader import get_config_value
from config.settings import Settings

logger = logging.getLogger(__name__)


class DriverFactory:
    """Factory class for creating and managing WebDriver instances."""
    
    @staticmethod
    def create_driver(browser=None, headless=None, **kwargs):
        """
        Create WebDriver instance based on configuration or parameters.
        
        Args:
            browser: Browser name ('chrome', 'firefox', 'edge') 
            headless: Override headless setting
            **kwargs: Additional driver options
            
        Returns:
            WebDriver: Configured WebDriver instance
            
        Raises:
            ValueError: If unsupported browser specified
        """
        # Use config values if not provided
        if browser is None:
            browser = Settings.get_browser()
        if headless is None:
            headless = Settings.is_headless()
        
        browser = browser.lower()
        logger.info(f"Creating {browser} driver (headless: {headless})")
        
        if browser == "chrome":
            return DriverFactory._create_chrome_driver(headless, **kwargs)
        elif browser == "firefox":
            return DriverFactory._create_firefox_driver(headless, **kwargs)
        elif browser == "edge":
            return DriverFactory._create_edge_driver(headless, **kwargs)
        else:
            raise ValueError(f"Unsupported browser: {browser}. Supported: chrome, firefox, edge")
    
    @staticmethod
    def _create_chrome_driver(headless=False, **kwargs):
        """
        Create Chrome WebDriver with optimized settings.
        
        Args:
            headless: Run in headless mode
            **kwargs: Additional Chrome options
            
        Returns:
            Chrome WebDriver instance
        """
        options = webdriver.ChromeOptions()
        
        # Load Chrome options from config
        chrome_options = get_config_value('webdriver.chrome_options', [])
        for option in chrome_options:
            options.add_argument(option)
        
        # Headless mode
        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
        
        # Additional performance and stability options
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Window size configuration
        window_size = get_config_value('window_size', '1920,1080')
        if window_size and ',' in window_size:
            width, height = window_size.split(',')
            options.add_argument(f"--window-size={width},{height}")
        
        # Download directory
        download_dir = get_config_value('webdriver.download_directory')
        if download_dir:
            prefs = {
                "download.default_directory": download_dir,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            }
            options.add_experimental_option("prefs", prefs)
        
        # Apply any additional options passed as kwargs
        for key, value in kwargs.items():
            if key.startswith('arg_'):
                options.add_argument(value)
            elif key.startswith('pref_'):
                options.add_experimental_option(key[5:], value)
        
        # Create driver with service
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Configure timeouts
        DriverFactory._configure_driver_timeouts(driver)
        
        # Remove automation indicators
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        logger.info("Chrome driver created successfully")
        return driver
    
    @staticmethod
    def _create_firefox_driver(headless=False, **kwargs):
        """
        Create Firefox WebDriver with optimized settings.
        
        Args:
            headless: Run in headless mode
            **kwargs: Additional Firefox options
            
        Returns:
            Firefox WebDriver instance
        """
        options = webdriver.FirefoxOptions()
        
        # Load Firefox options from config
        firefox_options = get_config_value('webdriver.firefox_options', [])
        for option in firefox_options:
            options.add_argument(option)
        
        # Headless mode
        if headless:
            options.add_argument("--headless")
        
        # Window size configuration
        window_size = get_config_value('window_size', '1920,1080')
        if window_size and ',' in window_size:
            width, height = window_size.split(',')
            options.add_argument(f"--width={width}")
            options.add_argument(f"--height={height}")
        
        # Download directory
        download_dir = get_config_value('webdriver.download_directory')
        if download_dir:
            options.set_preference("browser.download.folderList", 2)
            options.set_preference("browser.download.dir", download_dir)
            options.set_preference("browser.download.useDownloadDir", True)
            options.set_preference("browser.helperApps.neverAsk.saveToDisk", 
                                 "application/pdf,application/octet-stream")
        
        # Apply additional options from kwargs
        for key, value in kwargs.items():
            if key.startswith('arg_'):
                options.add_argument(value)
            elif key.startswith('pref_'):
                options.set_preference(key[5:], value)
        
        # Create driver with service
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        
        # Configure timeouts
        DriverFactory._configure_driver_timeouts(driver)
        
        logger.info("Firefox driver created successfully")
        return driver
    
    @staticmethod
    def _create_edge_driver(headless=False, **kwargs):
        """
        Create Edge WebDriver with optimized settings.
        
        Args:
            headless: Run in headless mode
            **kwargs: Additional Edge options
            
        Returns:
            Edge WebDriver instance
        """
        options = webdriver.EdgeOptions()
        
        # Basic options
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        
        # Headless mode
        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
        
        # Window size configuration
        window_size = get_config_value('window_size', '1920,1080')
        if window_size and ',' in window_size:
            width, height = window_size.split(',')
            options.add_argument(f"--window-size={width},{height}")
        
        # Apply additional options from kwargs
        for key, value in kwargs.items():
            if key.startswith('arg_'):
                options.add_argument(value)
        
        # Create driver with service
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
        
        # Configure timeouts
        DriverFactory._configure_driver_timeouts(driver)
        
        logger.info("Edge driver created successfully")
        return driver
    
    @staticmethod
    def _configure_driver_timeouts(driver):
        """
        Configure standard timeouts for the WebDriver instance.
        
        Args:
            driver: WebDriver instance to configure
        """
        # Set implicit wait
        implicit_wait = Settings.get_wait_timeout('implicit')
        driver.implicitly_wait(implicit_wait)
        
        # Set page load timeout
        page_load_timeout = Settings.get_wait_timeout('page_load')
        driver.set_page_load_timeout(page_load_timeout)
        
        # Set script timeout
        script_timeout = get_config_value('webdriver.performance.script_timeout', 30)
        driver.set_script_timeout(script_timeout)
        
        logger.debug(f"Driver timeouts configured - implicit: {implicit_wait}s, "
                    f"page load: {page_load_timeout}s, script: {script_timeout}s")
    
    @staticmethod
    def quit_driver(driver):
        """
        Safely quit WebDriver instance.
        
        Args:
            driver: WebDriver instance to quit
        """
        if driver:
            try:
                driver.quit()
                logger.info("Driver quit successfully")
            except Exception as e:
                logger.warning(f"Error quitting driver: {str(e)}")
    
    @staticmethod
    def get_supported_browsers():
        """
        Get list of supported browsers.
        
        Returns:
            List[str]: Supported browser names
        """
        return ['chrome', 'firefox', 'edge']
    
    @staticmethod
    def is_driver_responsive(driver, timeout=5):
        """
        Check if driver is responsive by executing a simple command.
        
        Args:
            driver: WebDriver instance to test
            timeout: Timeout for the test
            
        Returns:
            bool: True if driver is responsive
        """
        try:
            driver.set_script_timeout(timeout)
            driver.execute_script("return true;")
            return True
        except Exception as e:
            logger.warning(f"Driver responsiveness check failed: {str(e)}")
            return False
        


