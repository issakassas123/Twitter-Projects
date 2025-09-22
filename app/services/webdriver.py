from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains as AC
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from os import devnull, listdir
from os.path import join
from platform import system
from json import dumps, dump, load
from ..utils.colors import GREEN, RED, YELLOW, RESET

class BrowserHistory:
    def __init__(self):
        self.history = []

    def add_entry(self, url, title):
        self.history.append({"url": url, "title": title})

    def save_history(self, filename):
        with open(filename, "w") as f:
            dump(self.history, f)

class Webdriver:
    """Webdriver class fully updated for Selenium 4.35.0."""
    def __init__(self, browser: int) -> None:
        """browser: 1 = Firefox, 2 = Chrome"""
        self.browser = browser
        self.driver = self._start_driver()
        print(f"{GREEN}Webdriver started.{RESET}")
        self.window = browser
        self.new_switch_handle = False
        self.browser_history = BrowserHistory()

    def _start_driver(self):
        if self.browser == 1:
            return self._firefox()
        else:
            return self._chrome()

    def _firefox(self) -> webdriver.Firefox:
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')  # Headless mode.
        options.add_argument('--mute-audio')  # Audio is muted.
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--disable-dev-shm-usage')
        options.set_preference('intl.accept_languages', 'en,en-US')
        options.set_preference('permissions.default.image', 2)
        options.set_preference('permissions.default.stylesheet', 2)

        service = FirefoxService(executable_path=GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options, service_log_path=devnull)
        driver.maximize_window()
        return driver

    def _chrome(self) -> webdriver.Chrome:
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
        options.add_argument("--log-level=3")
        options.add_argument("--mute-audio")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--lang=en-US")

        service = ChromeService(executable_path = ChromeDriverManager().install())
        driver = webdriver.Chrome(service = service, options = options)

        # Optional network blocking (Chromium only)
        self.send(driver, "Network.setBlockedURLs", {
            "urls": [
                "www.google-analytics.com",
                "static.cloudflareinsights.com",
                "bat.bing.com",
                "fonts.gstatic.com",
                "cdnjs.cloudflare.com"
            ]
        })
        
        self.send(driver, "Network.enable")
        driver.maximize_window()
        return driver

    def send(self, driver: webdriver.Chrome, cmd: str, params: dict = {}) -> None:
        """Run a specific Chromium command (works with Selenium 4.35)."""
        driver.execute_cdp_cmd(cmd, params)

    def quit(self):
        try:
            self.driver.quit()
        except Exception:
            pass

    def clickable(self, element: str, timeout=15):
        try:
            WDW(self.driver, timeout).until(EC.element_to_be_clickable((By.XPATH, element))).click()
        except TimeoutException:
            print(f"Element '{element}' was not clickable within {timeout} seconds.")

    def visible(self, element: str, timer: int = 5):
        return WDW(self.driver, timer).until(EC.visibility_of_element_located((By.XPATH, element)))

    def find_element(self, element: str):
        try:
            return self.driver.find_element(By.XPATH, element)
        except Exception as ex:
            print(ex)

    def find_elements(self, element: str):
        try:
            return self.driver.find_elements(By.XPATH, element)
        except Exception as ex:
            print(ex)

    def send_keys(self, element: str, keys: str):
        try:
            self.visible(element).send_keys(keys)
        except Exception:
            WDW(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, element))).send_keys(keys)

    def clear_text(self, element):
        self.clickable(element)
        control = Keys.COMMAND if system() == "Darwin" else Keys.CONTROL
        AC(self.driver).key_down(control).send_keys("a").key_up(control).perform()

    def scroll(self):
        import time
        while True:
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
            time.sleep(2)
            if self.driver.execute_script("return window.innerHeight + window.scrollY") >= \
               self.driver.execute_script("return document.body.scrollHeight"):
                break

    def save_history(self, filename):
        self.browser_history.save_history(filename)
