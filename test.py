import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
#import fasttext
from sklearn.model_selection import train_test_split
import spacy
from textblob import TextBlob
from langdetect import detect

def detect_language(text):
    try:
        language_code = detect(text)
        return language_code
    
    except:
        return None
    
# nlp = spacy.load("fr_core_news_sm")
# text = "Bonjour"
# doc = nlp(text)
# language = doc.lang_
# print(language)  # Output: 'de'

# Preprocessing and data preparation
from langdetect import detect as detect_language
import pandas as pd

dictionary = {
    "0": 'Ukr_Freedom000\n@Ukr_Patriot777\n·\n19h\nFPV and M2 Bradley interaction.\n\nThe Russians tried to storm our positions, but were defeated before they reached them #UkraineWar\n4\n8\n72\n4.6K', 
    "1": 'Hunter UA ✠\n@UaCoins\n·\n2h\nTwo Russians became "good", five more were injured. The armored tractor MT-LB of the occupiers was hit\n\nSpectacular video of the combat work of the 128th separate mountain assault brigade of the Zakarpattia#UkraineWar #UkraineRussiaWar #UkraineWarNews #RussiaIsATerroristState\n3\n13\n652', 
    "2": "Richard\n@ricwe123\n·\n2h\nJoe Biden's remarks on the conflict in Ukraine from two years ago.....\n#Ukraine️ #Russia #Putin #UkraineRussianWar\n#UkraineRussiaWar\n#UkraineWar #Ukrainekrieg\n#Crimea #JoeBiden #Biden\n2\n6\n15\n1.3K", 
    "3": 'War Armor\n@StettingerN\n·\n4h\nDestroyed Russian vehicles. Source https://t.me/WarZoneInc/72388…\n2x destroyed Russian MT-LB \nDestroyed Russian BMP-2\nDestroyed Russian T-72 (maybe already on the ORYX list) possibly old. \n@Rebel44CZ\n #UkraineWar #Ukraina #Russia\n0:36\n2\n10\n147\n8.6K', 
    "4": "Hunter UA ✠\n@UaCoins\n·\n1h\n It doesn't even understand why he fights, why he kills, and why he dies. Occupiers, go home and drink vodka while you are still alive...#UkraineWar #UkraineRussiaWar #UkraineWarNews #RussiaIsATerroristState\n1\n5\n16\n599"
}

def get_pattern_match(pattern, text):
    matches = re.findall(pattern, text)
    if matches:
        return matches

data = []
for post in dictionary.values():
    poster = post.split('\n')
    tweet = ''
    username = poster[0]
    for i in range(4, len(poster) - 4):
        tweet += poster[i]
    
    # Extracting hashtags using regular expressions
    hashtagsList = get_pattern_match(r'#\w+', tweet)
    if hashtagsList:
        hashtags = " ".join(hashtagsList)
        for hashtag in hashtagsList:
            tweet = tweet.replace(hashtag, "")
        language_code = detect_language(tweet)
        
    else:
        hashtags = ""
        language_code = detect_language(tweet)

    data.append([username, tweet.strip(), hashtags, language_code])

# Creating a DataFrame
df = pd.DataFrame(data, columns=['Username', 'Tweet', 'Hashtags', 'Language'])

# Saving the DataFrame to a CSV file
df.to_csv('tweets_dataset.csv', index=False)

print("Dataset saved to tweets_dataset.csv")


# print(labels, tweets)
# # Splitting the data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(labels, tweets, test_size = 0.2, random_state = 42)
 
# # Save training and testing data to files (required by FastText)
# with open('train.txt', 'w', encoding='utf-8') as f:
#     for tweet, label in zip(X_train, y_train):
#         f.write(f'__label__{label} {tweet}\n')

# with open('test.txt', 'w', encoding='utf-8') as f:
#     for tweet, label in zip(X_test, y_test):
#         f.write(f'__label__{label} {tweet}\n')


# # Create DataFrame for training data
# train_df = pd.DataFrame({'tweet': X_train, 'label': y_train})

# # Save training dataset to CSV
# train_df.to_csv('train.csv', index=False)

# # Create DataFrame for testing data
# test_df = pd.DataFrame({'tweet': X_test, 'label': y_test})

# # Save testing dataset to CSV
# test_df.to_csv('test.csv', index=False)
# # Train the FastText classifier
# #model = fasttext.train_supervised(input='train.txt', epoch=25, lr=1.0, wordNgrams=2, verbose=2)

# # Evaluate the model
# # result = model.test('test.txt')
# # print('Precision:', result[1])
# # print('Recall:', result[2])
# # print('F1-score:', result[3])

# # # Predict on new data
# # # For example:
# # text = "This is a new tweet about #UkraineWar"
# # predicted_label = model.predict(text)
# # print('Predicted label:', predicted_label)

