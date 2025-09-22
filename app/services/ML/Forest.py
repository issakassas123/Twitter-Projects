from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.metrics import classification_report, accuracy_score, f1_score, precision_recall_fscore_support, silhouette_score
from datetime import datetime
from numpy import errstate

class Forest:
    def __init__(self):
        # RF classifier
        self.rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.kmeans_rf = KMeans(n_clusters = 3)
    
    def rf_time(self):
        return datetime.now()
    
    def rf_classification(self,  X_train_scaled, y_train):
        self.rf_classifier.fit(X_train_scaled, y_train)
        
    def predictions(self, X_test_scaled):
        rf_predictions = self.rf_classifier.predict(X_test_scaled)
        return rf_predictions
    
    def rf_indices(self, X_train):
        # Get leaf indices as features
        rf_leaf_indices = self.rf_classifier.apply(X_train)
        return rf_leaf_indices
    
    # Apply clustering on SVM decision function values
    def kmeans_fit_pred(self, rf_leaf_indices):
        clusters_rf = self.kmeans_rf.fit_predict(rf_leaf_indices)
        return clusters_rf
    
    def rf_silhouette(self, rf_leaf_indices, clusters_rf):
        silhouette_rf = silhouette_score(rf_leaf_indices, clusters_rf)
        return silhouette_rf
    
    def rf_accuracy_score(self, rf_predictions, y_test):
        rf_accuracy = accuracy_score(rf_predictions, y_test)
        return rf_accuracy
    
    def rf_report(self, y_test, rf_predictions):
        with errstate(divide='ignore', invalid='ignore'):
            rf_report = classification_report(y_test, rf_predictions, zero_division=0)
        return rf_report

    def rf_f1(self, y_test, rf_predictions):
        rf_f1_score = f1_score(y_test, rf_predictions, average = "weighted")
        return rf_f1_score
    
    def precision_recall_support(self, y_test, rf_predictions):
        with errstate(divide='ignore', invalid='ignore'):
            rf_precision_recall_support = precision_recall_fscore_support(y_test, rf_predictions, average='macro', zero_division=0)
        return rf_precision_recall_support
        