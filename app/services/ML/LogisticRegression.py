from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, r2_score, mean_absolute_error

class Logistic:
    def __init__(self):
        self.model = LogisticRegression()
        
    def logistic_classification(self,  X_train_scaled, y_train):
        self.model.fit(X_train_scaled, y_train)
        
    def predictions(self, X_test_scaled):
        logistic_predictions = self.model.predict(X_test_scaled)
        return logistic_predictions
    
    def logistic_accuracy_score(self, y_test, logistic_predictions):
        logistic_accuracy = accuracy_score(y_test, logistic_predictions)
        return logistic_accuracy
    
    def r2_score(self, Y_train, training_data_prediction):  
        # R squared error
        return r2_score(Y_train, training_data_prediction)

    def mean_absolute_error(self, Y_train, training_data_prediction):  
        # R squared error
        return mean_absolute_error(Y_train, training_data_prediction)