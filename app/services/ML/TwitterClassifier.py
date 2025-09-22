import pandas as pd
from difflib import get_close_matches

class TweetClassifier:
    def __init__(self):
        self.data = None
        self.labels = None

    def load_data(self, tweet_data):
        # Convert tweet data to pandas DataFrame
        self.data = pd.DataFrame(tweet_data)
        return self.data

    def load_csv(self, file):
        self.data = pd.read_csv(file, header=None, skiprows=1, names=['username', 'text', 'likes', 'date', 'Help', 'Prayer', 'News_Updates', 'Support_Palestine', 'Support_Israel', 'Unknown'])
        self.data.columns = self.data.columns.str.strip()
        return self.data
    
    def describe(self):
        return self.data.describe()
    
    def getXY(self, dataframe, tweet_embeddings):
        # Get features and labels for machine learning.
        # Convert tweet embeddings to DataFrame
        X = tweet_embeddings
        Y = dataframe[['Help', 'Prayer', 'News_Updates', 'Support_Palestine', 'Support_Israel']]
        return X, Y
    
    def label_num(self):
        self.data['label_num'] = self.data.label.map({
            'Help':0,
            'Prayer':1,
            'New_Updates':2,
            'Support_Palestine' :3,
            'Support_Israel': 4,
            'Unknown': 5
        })
             
    def get_close_match(self, search, column):
        list_of_all = self.data[column].tolist()
        find_close_match = get_close_matches(search, list_of_all)
        return find_close_match
