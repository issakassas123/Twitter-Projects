import os
from time import sleep
from getpass import getpass
from app.utils.const import PATH
from app.services.webdriver import Webdriver
from app.utils.colors import RED, RESET
from app.services.processes.login import Login
from pdb import set_trace
from app.utils.const import FIRST_PAGE, ENTER, SECOND_PAGE, URL, USERNAME, PASSWORD, ALL_DONE
from app.utils.colors import YELLOW
from app.utils.func import cls
from app.services.processes.TwitterSearcher import Searcher

def login(browser: int, browser_path: str) -> Webdriver:
    """Login to a specific website."""
    while True:
        web = None  # Prevent Exception.
        try:  # Try to start a webdriver.
            web = Webdriver(browser, browser_path)
            
        except Exception as error:
            print(f'{RED}Something went wrong with your webdriver.\n{error}{RESET}')
            
        try:  # Try to login to a wallet and OpenSea.
            if Login(web, URL, USERNAME, PASSWORD).login():
                return web  # Stop the while loop.
            
        except Exception:  # Stop the browser.
            web.quit() if web is not None else None
            
def user(PATH : str):
    current_directory = os.path.dirname(os.path.realpath(__file__))
    driver_path = os.path.join(current_directory, PATH)
    return driver_path
            
if __name__ == "__main__":
    try:
        #chdir(dirname(abspath(__file__)))  # Move to the actual path.
        cls()  # Clear console.
        #print(FIRST_PAGE)  # License, author and version.
        #input(ENTER)  # Press enter to continue.
        cls()  # Clear console.
        #print(SECOND_PAGE)  # License and author.
        driver_path = user(PATH)
        # print(driver_path)
        # webdriver_instance = Webdriver(browser = 2, browser_path = driver_path)
        cls()  # Clear console.
        while True:  # It does several processes every 12 hours.
            web = login(0, driver_path)  # Start the process.
            if web != None:  # This is the end of the process.
                break  # Stop everything.
        
        search_item = "@JackySkaff"
        searcher = Searcher(web)
        searcher.search(search_item)
        searcher.scroll()
        
        print(f'{YELLOW}\nRestarting the webdriver.\n{RESET}')
        print(ALL_DONE)  # Script stops, all done.
            
    except KeyboardInterrupt:
        print(f'\n\n{YELLOW}The program has been stopped by the user.{RESET}')
        
    except Exception as error:
        print(f'{RED}Something went wrong.{RESET}\n{error}')