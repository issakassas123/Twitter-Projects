import matplotlib.pyplot as plt
from wordcloud import WordCloud , STOPWORDS

class Cloud:
    def __init__(self, txt):
        self.wordcloud = WordCloud(width = 3000, height = 2000, stopwords = STOPWORDS, background_color = "Black", colormap = 'Set2', collocations = False).generate(txt)
        
    #function to display wordcloud
    def plot_cloud(self, wordcloud: WordCloud):
        # Set figure size
        plt.figure(figsize=(40, 30))
        # Display image
        plt.imshow(wordcloud) 
        # No axis details
        plt.axis("off")
        plt.show()