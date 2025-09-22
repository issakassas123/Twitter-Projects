from fasttext import train_supervised, load_model, train_unsupervised
from sklearn.metrics import classification_report

class FastText:
    def fast_model(self, path):
        return load_model(path)
    
    # Prepare training data in FastText format
    
    def prepare_data(self, data, label_prefix='__label__'):
        return [f"{label_prefix}{row['label']} {row['tweet']}" for index, row in data.iterrows()]
    
    def trainFormat(self, training_testing):
        training_testing[0]['fasttext_format'] = training_testing[0].apply(lambda row: f'__label__{row['label']} - {row['tweet']}', axis=1)
        return training_testing[0]['fasttext_format']
    
    # Write FastText training data to a text file
    def save_to_csv(self, data, file_path):
        data.to_csv(file_path, index=False, header=False, sep=' ')
                
    def train_unsupervised(self, file_path, model='skipgram'):
        # Train FastText model
        return train_unsupervised(file_path, model=model)

    # Train FastText classifier
    def train_supervised(self, file_path, epoch=25, lr=1.0, wordNgrams=2):
        return train_supervised(input=file_path, epoch=epoch, lr=lr, wordNgrams=wordNgrams, verbose=2)

    # Prepare testing data in FastText format
    def testFormat(self, training_testing):
        training_testing[1]['fasttext_format'] = training_testing[1].apply(lambda row: '__label__' + str(row['label']) + ' ' + row['tweet'], axis=1)
        return training_testing[1]['fasttext_format']
    
    # Make predictions on the test set
    def predict(self, model, data):
        predictions = model.predict(data)
        return [label[0] for label in predictions[0]]
    
    # Evaluate the performance of the model
    def evaluate(self, predicted_labels, true_labels):
        return classification_report(true_labels, predicted_labels)
    
    def save_model(self, model, file_path):
        model.save_model(file_path)