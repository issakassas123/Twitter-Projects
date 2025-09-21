from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager as CDM
from webdriver_manager.core.driver_cache import DriverCacheManager as DCM
from selenium.webdriver.common.action_chains import ActionChains as AC
from webdriver_manager.firefox import GeckoDriverManager as GDM
from selenium.webdriver.chrome.service import Service as SC
from selenium.webdriver.firefox.service import Service as SG
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.common.exceptions import TimeoutException
from time import sleep
from os import name as osname, devnull
from os.path import abspath, exists
from platform import system
from json import dumps
from ..utils.colors import GREEN, RED, YELLOW, RESET
import json

class BrowserHistory:
    def __init__(self):
        self.history = []

    def add_entry(self, url, title):
        self.history.append({"url": url, "title": title})

    def save_history(self, filename):
        with open(filename, "w") as f:
            json.dump(self.history, f)

class Webdriver:
    """Webdriver class and methods to prevent exceptions."""
    def __init__(self, browser: int, browser_path: str) -> None:
        self.browser_path = browser_path  # Get the browser path.
        self.driver: webdriver.Chrome = self.firefox() if browser == 1 else self.chrome()
        self.window = browser  # Window handle value.
        self.new_switch_handle = False
        self.browser_history = BrowserHistory()

    def save_history(self, filename):
        self.browser_history.save_history(filename)
            
    def firefox(self) -> webdriver:
        """Start a Firefox webdriver and return its state."""
        options = webdriver.FirefoxOptions()  # Configure options for Firefox.
        options.add_argument('--headless')  # Headless mode.
        options.add_argument('--mute-audio')  # Audio is muted.
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--disable-dev-shm-usage')
        options.set_preference('intl.accept_languages', 'en,en-US')
        options.set_preference('permissions.default.image', 2)
        options.set_preference('permissions.default.stylesheet', 2)
        # DeprecationWarning using
        driver = webdriver.Firefox(service = SG(self.browser_path), # executable_path.
        options = options, service_log_path = devnull)  # Disable Firefox logs.
        driver.maximize_window()  # Maximize window to reach all elements.
        return driver

    def chrome(self) -> webdriver.Chrome:
        """Start a Chrome webdriver and return its state."""
        options = webdriver.ChromeOptions()  # Configure options for Chrome.
        # UNQUOTE THIS TO ENABLE THE HEADLESS MODE.
        #options.add_argument("--headless")
        options.add_experimental_option("detach", True)
        options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
        options.add_argument('--log-level=3')  # No logs is printed.
        options.add_argument('--mute-audio')  # Audio is muted.
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--lang=en-US')  # Set webdriver language
        # driver = webdriver.Chrome(options = options, log_level = 0, 
        # driver_executable_path = self.browser_path, version_main = Webdriver.chrome_version(True)
        driver = webdriver.Chrome(options = options)
        
        self.send(driver, 'Network.setBlockedURLs', {'urls': ['www.google-analytics.com', 
        'static.cloudflareinsights.com', 'bat.bing.com', 'fonts.gstatic.com', 'cdnjs.cloudflare.com']})
        self.send(driver, 'Network.enable')  # Confirm the blocked URLs.
        driver.maximize_window()  # Maximize window to reach all elements.
        
        return driver
    
    @staticmethod
    def chrome_version(default_version: bool = False) -> float | int:
        """Return the Google Chrome version."""
        from webdriver_manager.core.os_manager import ChromeType, OperationSystemManager as OSM
        version = OSM().get_browser_version_from_os(ChromeType.GOOGLE)
        
        return int(version.split('.')[0]) if version else (None if default_version else 110)
    
    def send(self, driver: webdriver.Chrome, cmd: str, params: dict = {}) -> None:
        """Run a specific command with parameters in the webdriver."""
        # Execute the command.
        driver.command_executor._request('POST', f'{driver.command_executor._url }/session/{driver.session_id}/chromium/send_command_and_get_result',
        dumps({'cmd': cmd, 'params': params}))
        
    def quit(self) -> None:
        """Stop the webdriver."""
        try:  # Try to close the webdriver.
            self.driver.quit()
            
        except Exception:  # The webdriver is closed
            pass  # or no webdriver is started.

    def page_error(self) -> bool:
        """Check if the page is correctly displayed."""
        #self.window_handles(1)  # Switch to OpenSea.
        for text in ['This page is lost', 'something went wrong']:
            try:  # Check if the text is visible.
                self.visible(f'//*[contains(@class, "error") and contains(text(), "{text}")]', 1)
                print(f'{YELLOW}404 page error.{RESET}')
                return True  # Element is visible.
            
            except Exception:  # Not visible.
                continue  # Ignore the exception.
            
        return False  # No 404 page error.

    def clickable(self, element: str) -> None:
        """Click on an element if it's clickable using Selenium."""
        try:
            WDW(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, element))).click()
            
        except TimeoutException:
            print(f"Element '{element}' was not clickable within the timeout period.")

    def find_elements(self, element: str):
        try:
            return self.driver.find_elements(By.XPATH, element)
            
        except Exception as ex: print(ex)
            
    def find_element(self, element: str):
        try:
            return self.driver.find_element(By.XPATH, element)
                
        except Exception as ex: print(ex)

    def find_css(self, element):
        return self.driver.find_elements(By.CSS_SELECTOR, element)
    
    def visible(self, element: str, timer: int = 5) -> object:
        """Check if an element is visible using Selenium."""
        return WDW(self.driver, timer).until(EC.visibility_of_element_located((By.XPATH, element)))

    def send_keys(self, element: str, keys: str) -> None:
        """Send keys to an element if it's visible using Selenium."""
        try: 
            self.visible(element).send_keys(keys)
            
        except Exception:  # Some elements are not visible but are present.
            WDW(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element))).send_keys(keys)

    def clear_text(self, element) -> None:
        """Clear text from an input."""
        self.clickable(element)  # Click on the element then select its text.
        control = Keys.COMMAND if system() == 'Darwin' else Keys.CONTROL
        
        if self.window == 1:  # GeckoDriver (Mozilla Firefox).
            self.send_keys(element, (control, 'a'))
            
        else:  # ChromeDriver (Google Chrome).
            AC(self.driver).key_down(control).send_keys('a').key_up(control).perform()

    def is_empty(self, element: str, data: str, value: str = '') -> bool:
        """Check if data is empty and input its value."""
        if data != value:  # Check if the data is not an empty string
            self.send_keys(element, data)  # or a default value, and send it.
            return False
        
        return True
    
    def window_handles(self, window_number: int) -> None:
        """Check for window handles and wait until a specific tab is opened."""
        if self.new_switch_handle and window_number in (0, 1):
            window_number = {0: 1, 1: 0}[window_number]
            
        from datetime import datetime, timedelta
        now = datetime.now()  # Get the current datetime.
        while datetime.now() - now <= timedelta(seconds=5):
            try:  # Try to switch to the correct window.
                WDW(self.driver, 20).until(lambda _: len(self.driver.window_handles) > window_number)
                # Switch to the asked tab.
                self.driver.switch_to.window(self.driver.window_handles[window_number])
                
                return  # The switch is done.
            
            except Exception:  # A tab has been closed/opened.
                pass  # Retry until the datetime is finished.
            
        raise Exception('Cannot switch to the selected tab.')
    
    def scroll(self):
        # self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        import time
        while True:
            # Scroll down to the bottom
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
            #self.driver.find_element_by_tag_name('body').send_keys(Keys.END)
            # Wait for some time to load content
            time.sleep(2)  # You can adjust the sleep time as needed
            # Check if the page has reached the bottom
            if self.driver.execute_script("return window.innerHeight + window.scrollY") >= self.driver.execute_script("return document.body.scrollHeight"):
                break
            
    def scroll_to_bottom(self):
        from time import sleep
        # Scroll down to the bottom of the page
        total_height = self.driver.execute_script("return document.body.scrollHeight")
        scroll_speed = 50  # Adjust the scroll speed (smaller values for slower scrolling)
        
        for i in range(0, total_height, scroll_speed):
            self.driver.execute_script(f"window.scrollTo(0, {i});")
            sleep(0.1)  # Adjust the sleep time between scrolls if needed
            
    def nscrolls(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
def download_browser(browser: int) -> str:
    """Try to download the webdriver using the Driver Manager."""
    try:
        # Set the name of the webdriver according to browser choice.
        webdriver = 'GeckoDriver' if browser == 1 else 'ChromeDriver'
        print(f'Downloading the {webdriver}.', end=' ')
        
        # Download the webdriver using the Driver Manager module.
        browser_path = GDM(cache_manager=DCM(root_dir='assets')).install() \
        if browser == 1 else CDM(cache_manager=DCM(root_dir='assets')).install()        
            
        print(f'{GREEN}{webdriver} downloaded:{RESET} \n{browser_path}')
        return browser_path  # Return the path of the webdriver.
    
    except Exception:
        print(f'{RED}Browser download failed.{RESET}')
        # Set the browser path as "assets/" + browser + extension.
        browser_path = abspath('assets/' + ('geckodriver' if browser == 1 \
        else 'chromedriver') + ('.exe' if osname == 'nt' else '')).replace('\\', '/')
        
        # Check if an executable is already in this path, else exit.
        if not exists(browser_path):
            exit('Download the webdriver and place it in the assets/ folder.')
            
        print(f'Webdriver path set as {browser_path}')
        return browser_path