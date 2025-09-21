# Selenium module imports: pip install selenium
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.common.keys import Keys
from app.services.webdriver import Webdriver
# Python internal imports.
from ...utils.colors import GREEN, RESET, RED
from pdb import set_trace

class Login:
    def __init__(self, web: Webdriver, url: str, username: str, password: str) -> None:
        self.login_url = url
        self.web: Webdriver = web
        self.username = username
        self.password = password
        self.success = False
        self.fails = 0
    
    def login(self, signed: bool = False) -> bool:
        try: 
            print('Login X or Twitter.', end = '')
            if not signed:
                self.web.window_handles(0)
                self.web.driver.get(self.login_url)
                signed = True
            
            self.web.window_handles(0)
            WDW(self.web.driver, 50).until(lambda _: self.sign_login(self.username, self.password))
            print(f'{GREEN}Logged to X.{RESET}')
            self.fails = 0  # Reset the counter.
            return True
            
        except:
            self.fails += 1
            if self.fails < (4 if signed else 2):  # Retry to login.
                print(f'{RED}Login to X failed. Retrying.{RESET}')
                self.web.driver.get(self.login_url) 
                return self.login(signed)
            
            self.web.quit()
            return False
        
    def sign_login(self, username: str, password: str) -> bool:
        try:  # Try until it works for 30 seconds.
            self.web.send_keys("//input[@type='text']", username + Keys.ENTER)
            from time import sleep
            sleep(10)
            self.web.send_keys("//input[@type='password']", password + Keys.ENTER)
            print("logged")
            return True
        
        except Exception:
            return False
    