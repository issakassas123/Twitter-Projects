from app.utils.const import PATH, USERS, URL, USERNAME, PASSWORD, PHONE, ALL_DONE, SECOND_PAGE
from app.services.webdriver import Webdriver
from app.utils.colors import RED, RESET, YELLOW
from app.services.processes.Login import Login
from app.utils.func import cls
from app.services.processes.TwitterSearcher import Searcher
from app.services.processes.Dataset import Dataset
from app.services.processes.Json import combine_json_files

def start_webdriver(browser: int) -> Webdriver:
    """Start a webdriver and login to the site with retries."""
    while True:
        web = None
        try:
            web = Webdriver(browser)
        except Exception as e:
            print(f"{RED}Webdriver error: {e}{RESET}")
            continue

        try:
            login_process = Login(web, URL, USERNAME, PASSWORD, PHONE)
            if login_process.login():
                return web
        except Exception:
            if web is not None:
                web.quit()

def main():
    try:
        cls()
        print(SECOND_PAGE)

        # Start webdriver and login
        web = start_webdriver(0)  # 0=Chrome, 1=Firefox

        for user in USERS:
            searcher = Searcher(web)
            searcher.search(user)
            searcher.collect_tweets()

        web.quit()

        # Combine JSONs and create dataset
        print(f'{YELLOW}\nCombining JSON files and creating dataset...\n{RESET}')
        
        json_file = combine_json_files()
        dataset = Dataset(json_file)
        dataset.createDataset()

        print(ALL_DONE)

    except KeyboardInterrupt:
        print(f'\n\n{YELLOW}Program stopped by user.{RESET}')
    except Exception as error:
        print(f'{RED}Something went wrong.{RESET}\n{error}')

# if __name__ == "__main__":
#     main()
