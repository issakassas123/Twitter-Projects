import pandas as pd
from os import getcwd
from os.path import join
from app.services.ML.Fast import FastText
from app.services.ML.SVM import SVM
from app.services.ML.Tokenization import Token
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from pickle import load
from sklearn.metrics import accuracy_score

# Load the dataset
csv_file = join(getcwd(), "Dataset", "israel-palestine-conflict.csv")

data = pd.read_csv(csv_file).head(399)

# Preprocessing and Tokenization
token = Token()
downloader = token.nltk_download()

#Extract tweets
tweets = data['text']

cleaned_tweets = token.preprocess_text(tweets)

token.save_to_txt('preprocessed_tweets.txt', cleaned_tweets)

#Generate FastText Embeddings
fast = FastText()
model = fast.train_supervised('preprocessed_tweets.txt')

# Combine embeddings for each tweet
tweet_embeddings = []
for tweet in cleaned_tweets:
    embedding = [model[word] for word in tweet if word in model.words]
    if embedding:
        tweet_embeddings.append(sum(embedding) / len(embedding))
    else:
        tweet_embeddings.append([0]*100)  # If tweet contains no words in vocabulary, use zero vector
        
# Convert tweet embeddings to DataFrame
X = tweet_embeddings

Y = data[['Help', 'Prayer',  'News_Updates', 'Support_Palestine', 'Support_Israel', 'Unknown']]

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.2, random_state = 3)

# Train SVM model
model = SVM()
model.train(X_train, y_train)
X_train_prediction = model.predict(X_train)
training_data_accuracy = model.accuracy(X_train_prediction, y_train)
print('Accuracy on training data = ', training_data_accuracy)


#loading the saved model
loaded_model = load(open('svm_trained_model.sav', 'rb'))

loaded_model.fit(X_train, y_train)

# Make predictions on the test set
Y_pred = loaded_model.predict(X_test)

# # Evaluate accuracy
# accuracy = accuracy_score(y_test, Y_pred)
# print("Accuracy:", accuracy)

# svm = SVM()
# start_time = svm.svm_time()
# svm_classifier = svm.svm_fit(X_train_scaled, y_train)
# svm_predictions = svm.predictions(X_test_scaled)
# # Evaluate accuracy
# accuracy = svm.svm_accuracy_score(y_test, svm_predictions)
# #Get decision function values as features
# svm_decision_values = svm.svm_decision(X_train)
# #Apply clustering on SVM decision function values
# clusters_svm = svm.kmeans_fit_pred(svm_decision_values)
# # Evaluate SVM classifier
# svm_accuracy = svm.svm_accuracy_score(y_test, svm_predictions)
# svm_report = svm.svm_report(y_test, svm_predictions)
# svm_f1_score = svm.svm_f1(y_test, svm_predictions)
# svm_precision_recall_support = svm.precision_recall_support(y_test, svm_predictions)
# # Evaluate clustering results
# silhouette_svm = svm.svm_silhouette(svm_decision_values, clusters_svm)
# svm_execution_time = svm.svm_time()
# data = {
#     "Start SVM model": start_time,
#     "End SVM model": svm_execution_time,
#     "SVM Accuracy": svm_accuracy,
#     "F1 Score": svm_f1_score,
#     "Precision": svm_precision_recall_support[0],
#     "Recall": svm_precision_recall_support[1],
#     "Support": svm_precision_recall_support[2],
#     "Silhouette Score SVM": silhouette_svm
# }

# dataframe = pd.DataFrame(data, index = [0])
# print(dataframe)




# # Calculate accuracy
# accuracy = accuracy_score(Y_test, Y_pred)

# print("Overall Accuracy:", accuracy)

# # Convert tweet embeddings to DataFrame
# X = pd.DataFrame(tweet_embeddings)
# Y_palestine = data['Support_Palestine']
# Y_israel = data['Support_Israel']

# # Split the dataset into training and testing sets
# X_train, X_test, Y_train_palestine, Y_test_palestine, Y_train_israel, Y_test_israel = train_test_split(X, Y_palestine, Y_israel, test_size=0.2, random_state=42)

# # Train SVM model for supporting Palestine
# svm_model_palestine = SVC(kernel='linear')
# svm_model_palestine.fit(X_train, Y_train_palestine)

# # Train SVM model for supporting Israel
# svm_model_israel = SVC(kernel='linear')
# svm_model_israel.fit(X_train, Y_train_israel)

# # Make predictions for each target separately
# Y_pred_palestine = svm_model_palestine.predict(X_test)
# Y_pred_israel = svm_model_israel.predict(X_test)

# # Combine predictions
# Y_pred_combined = pd.DataFrame({'Support_Palestine': Y_pred_palestine, 'Support_Israel': Y_pred_israel})

# # Evaluate the overall accuracy
# accuracy = accuracy_score(Y_test_palestine.reset_index(drop=True), Y_pred_combined['Support_Palestine']) * \
#            accuracy_score(Y_test_israel.reset_index(drop=True), Y_pred_combined['Support_Israel'])

# print("Overall Accuracy:", accuracy)