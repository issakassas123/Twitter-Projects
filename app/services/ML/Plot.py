import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

class Plot:
    def __init__(self):
        pass
    
    def pie(self, title: str, labels: list, sizes: list, colors: list, startangle: float):        
        plt.pie(sizes, colors = colors, startangle = startangle)
        plt.style.use('default')
        plt.legend(labels)
        plt.title(title)
        plt.title( '#Number of Tweets (Positive, Negative, Neutral)' )
        plt.axis('equal')

    def distplot(self, df: pd.DataFrame, color, hist: dict, kde: dict ):
        sns.distplot(df, hist = False, kde = True, bins = int(180/5), color = color, hist_kws = hist, kde_kws = kde)    
        
    def plot_cloud(self, wordcloud):
        # Set figure size
        plt.figure(figsize = (40, 30))
        # Display image
        plt.imshow(wordcloud) 
        # No axis details
        plt.axis("off")