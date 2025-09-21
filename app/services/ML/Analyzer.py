from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import numpy as np
from re import findall, sub

class Analyzer:
    def __init__(self, ) -> None:
        self.analyzer = SentimentIntensityAnalyzer()
        
    def readCSV(self, filePath: str):
        dataframe = pd.read_csv(filePath)
        return dataframe
    
    #cleaning the tweets
    def remove_pattern(self, input_txt: str, pattern: str):
        r = findall(pattern, input_txt)  
        for i in r: input_txt = sub(i, '', input_txt)        
        return input_txt
    
    def clean_tweets(self, tweets: str):
        #remove twitter Return handles (RT @xxx:)
        tweets = np.vectorize(self.remove_pattern)(tweets, "RT @[\\w]*:") 
        
        #remove twitter handles (@xxx)
        tweets = np.vectorize(self.remove_pattern)(tweets, "@[\\w]*")
        
        #remove URL links (httpxxx)
        tweets = np.vectorize(self.remove_pattern)(tweets, "https?://[A-Za-z0-9./]*")
        
        #remove special characters, numbers, punctuations (except for #)
        tweets = np.core.defchararray.replace(tweets, "[^a-zA-Z]", " ")
        
        return tweets
     
    def Scores(self, df: pd.DataFrame) -> list:
        scores = []
        for i in range(df.shape[0]):
            compound = self.analyzer.polarity_scores(df[i])["compound"]
            pos = self.analyzer.polarity_scores(df[i])["pos"]
            neu = self.analyzer.polarity_scores(df[i])["neu"]
            neg = self.analyzer.polarity_scores(df[i])["neg"]
            
            scores.append({
                "Compound": compound, 
                "Positive": pos,
                "Negative": neg,
                "Neutral": neu
            }) 
        
        return scores

    def joinScores(self, df: pd.DataFrame, scores : list) -> pd.DataFrame:
        sentiments_score = pd.DataFrame.from_dict(scores)
        dataframe = df.join(sentiments_score)
        return dataframe
    
    def SelectByConditions(self, conditions: list, values: list, default = "-"):
        return np.select(conditions, values, default)
    
    def GroupBy(self, df: pd.DataFrame, by: str) -> pd.DataFrame:
        return  df.groupby([by])[by].count()
    
    def PercentageDataFrame(self, counts_score: pd.DataFrame):
        return pd.DataFrame(counts_score).rename(columns = {
            "Category": "Counts"
        }).assign(Percentage = lambda per: (per.Counts / per.Counts.sum()) * 100)
        
    def AverageLength(self, df: pd.DataFrame):
        df['text_len'] = df.astype(str).apply(len)
        return round(np.mean(df['text_len']))
    
    def AverageWordCount(self, df: pd.DataFrame):
        df['text_word_count'] = df.apply(lambda x: len(str(x).split()))
        return round(np.mean(df['text_word_count']))
    
    def Top(self, n: int, df: pd.DataFrame, columns: list, column: str):
        return df.nlargest(n = n, columns=columns)[column]
    
    def Small(self, n: int, df: pd.DataFrame, columns: list, column: str):
        return df.nsmallest(n = n, columns=columns)[column]
    
    def Retweets(self, n: int, df: pd.DataFrame, column: str):
        return df.sort_values('Retweets', ascending = False)[column].drop_duplicates().head(n)
    
    def hashtag_extract(self, tags):
        hashtags = []
        # Loop over the words in the tweet
        for i in tags:
            ht = findall(r"#(\w+)", i)
            hashtags.append(ht)
            
        return hashtags