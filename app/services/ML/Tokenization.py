from nltk import download
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from re import sub

class Token:
    def __init__(self) -> None:
        self.stemmer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
    def nltk_download(self):
        print("NLTK resources are being downloaded. Please wait...")
        download('punkt')
        download('punkt_tab')
        download('stopwords')
        download('wordnet')
    
    def word_tokenize(self, text):
        return word_tokenize(text)
    
    def preprocess_tweet(self, tweet):
        # Remove URLs, mentions, and special characters
        tweet = sub(r'http\S+|www\S+|@[^\s]+|\W', ' ', tweet)
        # Tokenize the tweet
        words = self.word_tokenize(tweet.lower())
        # Remove stop words and apply lemmatization
        filtered_words = [self.stemmer.lemmatize(word) for word in words if word not in self.stop_words and word.isalnum()]
        return filtered_words
    
    def preprocess_text(self, text):
        preprocessed_text = text.apply(self.preprocess_tweet)
        return preprocessed_text
    
    def save_to_txt(self, file_path, cleaned_tweets):
        with open(file_path, 'w') as f:
            for tweet in cleaned_tweets:
                f.write(' '.join(tweet) + '\n')