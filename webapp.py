import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from pickle import load, dump
from app.services.ML.TwitterClassifier import TweetClassifier
from app.services.ML.Tokenization import Token
from app.services.ML.SVM import SVM
from app.services.ML.Forest import Forest
from app.services.ML.Fast import FastText
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from streamlit_option_menu import option_menu
import os

# getting the working directory of the main.py
working_dir = os.path.dirname(os.path.abspath(__file__))

# Create a Streamlit app
st.set_page_config(page_title="Palestine & Israel War", layout="wide", page_icon="💉")

st.title("""
    # Data Analysis Dashboard
    **Isreal** & **Palestine** Conflict Analysis
    """)

# Sidebar for data upload
st.sidebar.header("Upload Data")

tweet_classifier = TweetClassifier()
token = Token()
fast = FastText()

uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])
if uploaded_file is not None:
    tweet_classifier.data = tweet_classifier.load_csv(uploaded_file)
    # replace the null values with a null string
    tweet_classifier.data = tweet_classifier.data.where((pd.notnull(tweet_classifier.data)),'')
    dataframe = tweet_classifier.data
     
    with st.sidebar:
        selected = option_menu('Multiple Predictions System', ['Support Vector Machine', 'Random Forest'],
        menu_icon='Models', icons=['tools', 'tree'], default_index=0)
      
    # Extract tweets
    tweets = dataframe['text']

    cleaned_tweets = token.preprocess_text(tweets)

    filename = f'{working_dir}/preprocessed_tweets.txt'
    token.save_to_txt(filename, cleaned_tweets)

    # Generate FastText Embeddings
    model = fast.train_unsupervised(filename)

    # Combine embeddings for each tweet
    tweet_embeddings = []
    for tweet in cleaned_tweets:
        embedding = [model[word] for word in tweet if word in model.words]
        if embedding: tweet_embeddings.append(sum(embedding) / len(embedding))
        else: tweet_embeddings.append([0] * 100)  # If tweet contains no words in vocabulary, use zero vector

    X = tweet_embeddings

    Y = dataframe[['Help', 'Prayer', 'News_Updates', 'Support_Palestine', 'Support_Israel']]

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.2, random_state = 42)
    
    # Number of events
    num_events = len(dataframe)
    st.sidebar.write("No  of Events", num_events)
    
    if selected == 'Support Vector Machine':
        # page title SVM
        st.title('SVM Prediction using ML')
        st.subheader("SVM Values")
        svm = SVM()
        
        start_time = svm.current_time()
        svm_classifier = svm.train(X_train, y_train)
        svm_predictions = svm.predict(X_train)

        #Get decision function values as features
        svm_decision_values = svm.decision_function(X_train)

        #Apply clustering on SVM decision function values
        clusters_svm = svm.cluster_decision_function(svm_decision_values)

        # Evaluate SVM classifier
        svm_accuracy = svm.accuracy(svm_predictions, y_train)
        svm_report = svm.report(y_train, svm_predictions)
        svm_f1_score = svm.f1(y_train, svm_predictions)
        svm_precision_recall_support = svm.precision_recall_support(y_train, svm_predictions)
        
        # Evaluate clustering results
        silhouette_svm = svm.evaluate_silhouette_score(svm_decision_values, clusters_svm)
        svm_execution_time = svm.current_time()

        data = {
            "Start SVM model": start_time,
            "SVM Accuracy": svm_accuracy,
            "F1 Score": svm_f1_score,
            "Precision": svm_precision_recall_support[0],
            "Recall": svm_precision_recall_support[1],
            "Support": svm_precision_recall_support[2],
            "Silhouette Score SVM": silhouette_svm,
            "End SVM model": svm_execution_time
        }

        data = pd.DataFrame(data, index = [0])
        st.write(data)
        st.sidebar.write(svm_report)

        filename = f'{working_dir}/save_models/svm_trained_model.sav'
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))

        dump(svm.svm_classifier, open(filename, 'wb'))

    if selected == 'Random Forest':
        # page title RandomForest
        st.title('RandomForest Prediction using ML')
        st.subheader("RandomForest Values")

        rf = Forest()
        start_time = rf.rf_time()
        rf_classifier = rf.rf_classification(X_train, y_train)
        rf_predictions = rf.predictions(X_train)

        # Get leaf indices as features
        rf_leaf_indices = rf.rf_indices(X_train)

        # Apply clustering on Random Forest leaf indices
        clusters_rf = rf.kmeans_fit_pred(rf_leaf_indices)

        # Evaluate Random Forest classifier
        rf_accuracy = rf.rf_accuracy_score(rf_predictions, y_train)
        rf_report = rf.rf_report(y_train, rf_predictions)
        rf_f1_score = rf.rf_f1(y_train, rf_predictions)
        rf_precision_recall_support = rf.precision_recall_support(y_train, rf_predictions)

        # Evaluate clustering results
        silhouette_rf = rf.rf_silhouette(rf_leaf_indices, clusters_rf)
        rf_execution_time = rf.rf_time()

        data = {
            "Start RF model": start_time,
            "RF Accuracy": rf_accuracy,
            "F1 Score": rf_f1_score,
            "Precision": rf_precision_recall_support[0],
            "Recall": rf_precision_recall_support[1],
            "Support": rf_precision_recall_support[2],
            "Silhouette Score SVM": silhouette_rf,
            "End RF model": rf_execution_time
        }

        data = pd.DataFrame(data, index = [0])
        st.write(data)
        st.sidebar.write(rf_report)
        
        filename = f'{working_dir}/rf_trained_model.sav'
        dump(rf.rf_classifier, open(filename, 'wb'))

    dataframe = dataframe[['username', 'text', 'likes']]
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Users")
        users_counts = dataframe['username'].value_counts()
        st.bar_chart(users_counts)
    with col2:
        st.subheader("Tweets")
        labels_counts = dataframe['text'].value_counts()
        st.bar_chart(labels_counts, color='#FF0000')

    dataframe = dataframe.head(25)
    col1, col2 = st.columns(2)
    with col1:
        tweetsbyusers = dataframe.groupby('username')['text'].nunique()
        st.subheader("Percentage of tweets group By users")
        fig, ax = plt.subplots()
        ax.pie(tweetsbyusers, labels = tweetsbyusers.index, autopct='%1.1f%%')
        st.pyplot(fig)
    with col2:
        labelsbyusers = dataframe.groupby('username')['likes'].nunique()
        st.subheader("Percentage of labels group By users")
        fig,ax = plt.subplots()
        ax.pie(labelsbyusers, labels = labelsbyusers.index, autopct='%1.1f%%')
        st.pyplot(fig)

    st.sidebar.text("Data analysis dashboard by Issa Kassas")