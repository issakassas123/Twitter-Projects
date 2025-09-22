import re
from langdetect import detect as lang

def get_pattern_match(pattern, text):
    matches = re.findall(pattern, text)
    if matches:
        return matches
    
class Tweet:
    def __init__(self, username, date, post: str, views, likes = 0):
        self.username = username
        self.likes = likes
        self.date = date
        self.tweet = post
        self.views = views
        self.hashtags = "#"
        self.language_code = ""

    def unicode_arabic(self, txt: str):
        text = txt.encode('utf-8').decode('unicode-escape')
        return text

    def createData(self):
        # Extracting hashtags using regular expressions
        hashtagsList = get_pattern_match(r'#\w+', self.tweet)

        if hashtagsList:
            self.hashtags = " ".join(hashtagsList)
            for hashtag in hashtagsList:
                self.tweet = self.tweet.replace(hashtag, "")

            self.language_code = lang(self.tweet)
        
        else:
            self.hashtags = ""
            self.language_code = lang(self.tweet)

        data = {
            "username": self.username,
            "text": self.tweet,
            "likes": self.likes,
            "views": self.views,
            "date": self.date,
            "hashtags": self.hashtags,
            "language": self.language_code
        }

        return data