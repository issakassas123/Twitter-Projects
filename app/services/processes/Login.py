from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from app.services.webdriver import Webdriver
from ...utils.colors import GREEN, RED, RESET

class Login:
    def __init__(self, web: Webdriver, url: str, username: str, password: str, phone: str) -> None:
        self.web: Webdriver = web
        self.login_url = url
        self.username = username
        self.password = password
        self.phone = phone
        self.success = False
        self.fails = 0

    def login(self) -> bool:
        """Dynamic login handling: username, password, optional phone/email."""
        max_retries = 3
        while self.fails < max_retries:
            try:
                print('Logging into X/Twitter...', end='')
                self.web.driver.get(self.login_url)
                self.web.driver.switch_to.window(self.web.driver.window_handles[0])

                try:
                    username_input = WDW(self.web.driver, 5).until(
                        EC.visibility_of_element_located((By.NAME, "text"))
                    )
                    username_input.send_keys(self.username + Keys.ENTER)
                    username_found = True
                except TimeoutException:
                    pass
                
                password_found = False
                phone_found = False

                # Dynamic loop for login inputs
                for _ in range(3):  # Try up to 5 steps
                    if not password_found:
                        try:
                            password_input = WDW(self.web.driver, 5).until(
                                EC.visibility_of_element_located((By.NAME, "password"))
                            )
                            password_input.send_keys(self.password + Keys.ENTER)
                            password_found = True
                        except TimeoutException:
                            pass

                    if not phone_found:
                        try:
                            phone_input = WDW(self.web.driver, 15).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[data-testid="ocfEnterTextTextInput"]'))
                            )
                            ActionChains(self.web.driver).move_to_element(phone_input).click().perform()
                            phone_input.send_keys(self.phone + Keys.ENTER)
                            phone_found = True
                        except TimeoutException:
                            pass

                    if password_found and phone_found:
                        break

                print(f'\n{GREEN}Logged into X/Twitter successfully!{RESET}')
                self.success = True
                return True

            except Exception as e:
                self.fails += 1
                print(f'{RED}Login attempt {self.fails} failed: {e}{RESET}')

        print(f'{RED}All login attempts failed.{RESET}')
        self.web.quit()
        return False
