from sklearn.svm import SVC
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import (classification_report, accuracy_score, f1_score,
                             precision_recall_fscore_support, silhouette_score)
from sklearn.multiclass import OneVsRestClassifier
from datetime import datetime
import numpy as np

class SVM:
    def __init__(self, kernel='linear', decision_shape='ovo', n_clusters=3, scale_data=True):
        """
        kernel: SVM kernel type
        decision_shape: 'ovo' or 'ovr' for OneVsRestClassifier
        n_clusters: number of clusters for KMeans
        scale_data: whether to standardize features
        """
        self.scale_data = scale_data
        self.scaler = StandardScaler() if scale_data else None
        self.svm_classifier = OneVsRestClassifier(SVC(kernel=kernel, decision_function_shape=decision_shape, probability=True))
        self.kmeans_svm = KMeans(n_clusters=n_clusters, random_state=42)
    
    def current_time(self):
        return datetime.now()
    
    def preprocess(self, X_train, X_test):
        """Scale features if required"""
        if self.scale_data:
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            return X_train_scaled, X_test_scaled
        return X_train, X_test
    
    def train(self,  X_train_scaled, y_train):
        self.svm_classifier.fit(X_train_scaled, y_train)
    
    def predict(self, X_test):
        return self.svm_classifier.predict(X_test)
    
    def predict_proba(self, X_test):
        if hasattr(self.svm_classifier.estimators_[0], "predict_proba"):
            return self.svm_classifier.predict_proba(X_test)
        raise AttributeError("SVM estimator does not support probability estimates")
    
    def decision_function(self, X):
        return self.svm_classifier.decision_function(X)
    
    # ----- Clustering based on decision function -----
    # Apply clustering on SVM decision function values
    def cluster_decision_function(self, svm_decision_values):
        svm_decision_values_2d = svm_decision_values.reshape(-1, 1)
        return self.kmeans_svm.fit_predict(svm_decision_values_2d)
    
    def evaluate_silhouette_score(self, svm_decision_values, clusters_svm):
        return silhouette_score(svm_decision_values.reshape(-1, 1), clusters_svm)
    
    # ----- Evaluation metrics -----
    def accuracy(self, y_true, y_pred):
        return accuracy_score(y_true, y_pred)
    
    def f1(self, y_true, y_pred, average='weighted'):
        return f1_score(y_true, y_pred, average=average)
    
    def precision_recall_support(self, y_true, y_pred, average='macro'):
        return precision_recall_fscore_support(y_true, y_pred, average=average, zero_division=0)
    
    def report(self, y_true, y_pred):
        return classification_report(y_true, y_pred, zero_division=0)
    
    # ----- Utility to split dataset -----
    @staticmethod
    def split_data(X, y, test_size=0.2, random_state=42):
        return train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y if len(np.unique(y)) > 1 else None)
