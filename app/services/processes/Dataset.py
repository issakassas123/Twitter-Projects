import os
import json
import pandas as pd

class Dataset:
    def __init__(self, file) -> None:
        self.file = file
   
    def createDataset(self):
        # Load the JSON data
            with open(self.file, encoding='utf-8') as json_file:
                data = json.load(json_file)

            # Convert JSON to DataFrame
            dataframe = pd.DataFrame(data)
            directory_path = os.path.join(os.getcwd(), "Dataset")
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)

            dataset_file = os.path.join(directory_path, 'Tweets_Dataset.csv')

            # Save DataFrame to CSV file
            dataframe.to_csv(dataset_file, index=False, encoding='utf-8')