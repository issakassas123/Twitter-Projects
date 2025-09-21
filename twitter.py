import pandas as pd
import requests

payloads = [
    { 'api_key': '8778c58dcbf3cfedebea2d5ee0f02109', 'query': 'Ukraine Russia', 'num': '25' }, 
    { 'api_key': '8778c58dcbf3cfedebea2d5ee0f02109', 'query': 'Ukraine War Prayer', 'num': '25' },
    { 'api_key': '8778c58dcbf3cfedebea2d5ee0f02109', 'query': 'Russia War Prayer', 'num': '25' }
]

# for payload in payloads:
#     response = requests.get('https://api.scraperapi.com/structured/twitter/search', params=payload)
#     twitter_data = []

#     data = response.json()
#     all_tweets = data["organic_results"]

#     for tweet in all_tweets:
#         twitter_data.append(tweet)
        
#     dataframe = pd.DataFrame(twitter_data)

#     dataframe.to_json(f"{payload["query"]}.json", orient = 'index')
#     print("Data saved to twitter_data.json")
#     print(dataframe)
    
# from googletrans import Translator

# unicode_str = r'https://twitter.com/ShankkarAiyar/status/1758490348215583026'
# decoded_str = bytes(unicode_str, 'utf-8').decode('unicode_escape')

# translator = Translator()
# translation = translator.translate(decoded_str, src='ru', dest='en')

# print(translation.text)  # Output: "First honey"

