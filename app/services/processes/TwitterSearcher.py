from app.services.webdriver import Webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from time import sleep

class Searcher:
    def __init__(self, web : Webdriver):
        self.web: Webdriver = web
        self.all_tweets = {}
        
    def search(self, search: str) -> bool:
        try:  # Try until it works for 20 seconds.
            self.web.send_keys("//input[@data-testid='SearchBox_Search_Input']", search + Keys.ENTER)
            self.web.clickable('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/section/div/div/div[3]/div/div/div/div/div[2]/div/div[1]/div/div[1]/a')
            
        except Exception as ex:
            print(ex)
        
    def tweets(self):
        #scroll with javascript
        self.web.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
        tweets_divs = self.web.find_css("div.css-1rynq56.r-8akbws.r-krxsd3.r-dnmrzs.r-1udh08x.r-bcqeeo.r-qvutc0.r-1qd0xha.r-a023e6.r-rjixqe.r-16dba41.r-bnwqim")
        # username_divs = self.web.find_css("div.css-175oi2r.r-1iusvr4.r-16y2uox.r-1777fci.r-kzbkwu")
        posts = {}
        try:
            for div in tweets_divs:
                if len(div.text.strip()) != 0 and div.text.strip() not in posts.values():
                    posts[tweets_divs.index(div)] = div.text.strip()

            return posts
        
        except StaleElementReferenceException as ex:
            return self.tweets()
                
    def scroll(self):
        list_posts = []
        # Scroll down to the bottom of the page
        total_height = self.web.driver.execute_script("return document.body.scrollHeight")
        scroll_speed = 10
        
        j = 0
        for i in range(0, total_height, scroll_speed):
            posts = self.tweets()
            self.web.driver.execute_script(f"window.scrollTo(0, {i});")
            print(posts)
            # if len(posts.values()) != 0:
            #     posts = list(posts.values())
            #     for post in posts:
            #         list_posts.append(post)
            #         self.all_tweets[str(j)] = post
            #         j += 1
      
            sleep(0.1)  # Adjust the sleep time between scrolls if needed
            
        print(self.all_tweets)