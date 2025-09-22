from nltk import *
from app.services.ML.Analyzer import Analyzer
from app.services.ML.Plot import Plot
from app.services.ML.Cloud import Cloud
import matplotlib.pyplot as plt
from os import getcwd
from os.path import join
import warnings
warnings.filterwarnings('ignore')

analyzer = Analyzer()
file  = join(getcwd(), "Dataset", "tweets_Dataset.csv")
dataframe = analyzer.readCSV(file)

dataframe['tweet'] = analyzer.clean_tweets(dataframe['tweet'])
dataframe['tweet'].head()
print(dataframe['tweet'])

scores = analyzer.Scores(dataframe['tweet'])
print(scores)
# Declare variables for scores
compound_list, positive_list, negative_list, neutral_list = [], [], [], []

sentiments_score = analyzer.joinScores(dataframe, scores)

# create a list of our conditions
conditions = [
    (sentiments_score['Compound'] <= -0.5),
    (sentiments_score['Compound'] > -0.5) & (sentiments_score['Compound'] < 0.5),
    (sentiments_score['Compound'] > 0.5)
]

# create a list of the values we want to assign for each condition
values = ['Negative', 'Neutral', 'Positive']

# create a new column and use np.select to assign values to it using our lists as arguments
sentiments_score["Category"] = analyzer.SelectByConditions(conditions, values)
print(sentiments_score)

# Group by 'Category' and count occurrences
counts_score = analyzer.GroupBy(sentiments_score, "Category")
percentage = analyzer.PercentageDataFrame(counts_score)
negative, neutral, positive = percentage["Counts"][0], percentage["Counts"][1], percentage["Counts"][2]

#Creating PieChart
labels = [f'Positive [{positive}]', f'Neutral [{neutral}]', f'Negative [{negative}]']
sizes = [positive, neutral, negative]
colors = ["#81F495", "#A9E4EF", "#FF3C38"]

plot = Plot()
# plot.pie('#Number of tweets (Positive, Negative, Neutral)', labels, sizes, colors = colors, startangle = 90)
# plt.show()

#Average Length & Word Counts of tweets
text_len = analyzer.AverageLength(sentiments_score['tweet'])
text_word_count = analyzer.AverageWordCount(sentiments_score['tweet'])

print("Average length of tweets ", text_len)
print("Average word counts of tweets", text_word_count)

# Top 50 positive tweets
top = analyzer.Top(50, sentiments_score, ['Compound'], 'tweet')

# Top 50 negative tweets
small = analyzer.Small(50, sentiments_score, ['Compound'], 'tweet')

# # Top 50 tweets with maximum numbers of retweets
# retweets = analyzer.Retweets(50, sentiments_score, 'tweet')

# Visualization of the Sentiment Scores of Positive, Neutral & Negative tweets
plot.distplot(sentiments_score["Positive"], 'green', {'edgecolor':'black'}, {'shade': True, 'linewidth': 2})
plot.distplot(sentiments_score["Negative"], 'red', {'edgecolor':'black'}, {'shade': True, 'linewidth': 2})
plot.distplot(sentiments_score["Neutral"], 'yellow', {'edgecolor':'black'}, {'shade': True, 'linewidth': 2})
plt.show()

#Visualization of the Sentiment Scores
plot.distplot(sentiments_score["Compound"], 'green', {'edgecolor':'black'}, {'shade': True,'linewidth': 2})
plt.show()

### Word Cloud of mostly used word in tweets
txt = " ".join(review for review in sentiments_score.tweet)
cloud = Cloud(txt)
wordcloud = cloud.wordcloud
cloud.plot_cloud(wordcloud)

#wordcloud for Negative tweets 
## Word Cloud of mostly used word in tweets
txt = " ".join(review for review in sentiments_score[sentiments_score['Category'] == 'Negative'].tweet)
cloud = Cloud(txt)
wordcloud = cloud.wordcloud
cloud.plot_cloud(wordcloud)

#wordcloud for Neutral tweets 
## Word Cloud of mostly used word in tweets
txt = " ".join(review for review in sentiments_score[sentiments_score['Category'] == 'Neutral'].tweet)
cloud = Cloud(txt)
wordcloud = cloud.wordcloud
cloud.plot_cloud(wordcloud)

#wordcloud for Positive tweets 
### Word Cloud of mostly used word in tweets
txt = " ".join(review for review in sentiments_score[sentiments_score['Category'] == 'Positive'].tweet)
cloud = Cloud(txt)
wordcloud = cloud.wordcloud
cloud.plot_cloud(wordcloud)

#Collect the positive hashtags from the tweets data
# extracting hashtags from  tweets
HT_positive = analyzer.hashtag_extract(sentiments_score['tweet'][sentiments_score['Compound'] > 0.5])

# unnesting list
HT_positive  = sum(HT_positive,[])
HT_positive = HT_positive[0:10]
print(HT_positive)
# # extracting hashtags from  tweets
HT_negative  = analyzer.hashtag_extract(sentiments_score['tweet'][sentiments_score['Compound'] < -0.5])
# unnesting list
HT_negative = sum(HT_negative,[])
HT_negative = HT_negative[0:10]

# #Comparison of Sentiment Score of tweets by Indian and from Other Country
# sentiments_score[['Location']] = sentiments_score[['Location']].fillna('')

# plot.distplot(sentiments_score[~sentiments_score["Location"].str.contains('India')]["Compound"], 'r', 
# {'edgecolor':'black'}, {'shade': True,'linewidth': 2})

# plot.distplot(sentiments_score[sentiments_score['Location'].str.contains("India")]["Compound"], 'g', 
# {'edgecolor':'black'}, {'shade': True,'linewidth': 2})

# plt.show()