from app.services.webdriver import Webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep
from .Tweets import Tweet
from .Json import Json

class Searcher:
    def __init__(self, web: Webdriver):
        self.web: Webdriver = web
        self.all_tweets = []

    def search(self, query: str) -> bool:
        """Search for a query in Twitter/X."""
        try:
            # Wait for the search input to appear
            search_input = WDW(self.web.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//input[@data-testid='SearchBox_Search_Input']"))
            )

            search_input.clear()
            search_input.send_keys(query + Keys.ENTER)
            sleep(2)  # Wait for results to load
            return True

        except TimeoutException:
            print(f"Search input not found for query: {query}")
            return False

    def scroll_step_by_step(self, scroll_increment=500, wait_time=1):
        """Scrolls the page step by step to load more tweets."""
        last_height = self.web.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.web.driver.execute_script(f"window.scrollBy(0, {scroll_increment});")
            sleep(wait_time)
            new_height = self.web.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def collect_tweets(self):
        """Collect visible tweets and store them in JSON."""
        self.scroll_step_by_step()
        tweets = self.web.find_elements('//article[@data-testid="tweet"]')

        for tweet in tweets:
            try:
                data = tweet.text.split("\n")
                if len(data) < 6:
                    continue  # Skip incomplete tweets

                # Extract numbers/likes/retweets
                stats = []
                for item in data[6:]:
                    if item.replace('.', '').replace('K', '').isdigit():
                        stats.append(item)

                json_tweet = Tweet(data[1], data[2], data[4], data[5])
                json_data = json_tweet.createData()
                json_handler = Json(json_data)
                json_handler.createJson()
                self.all_tweets.append(json_data)

            except Exception as e:
                print(f"Failed to parse tweet: {e}")

        # Scroll to bottom to ensure full page load
        self.web.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
