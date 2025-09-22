from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import accuracy_score, r2_score, mean_absolute_error

class Lasso:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators = 100)
        
    def lasso_classification(self,  X_train_scaled, y_train):
        self.model.fit(X_train_scaled, y_train)
        
    def predictions(self, X_test_scaled):
        lasso_predictions = self.model.predict(X_test_scaled)
        return lasso_predictions
    
    def lasso_accuracy_score(self, y_test, lasso_predictions):
        lasso_accuracy = accuracy_score(y_test, lasso_predictions)
        return lasso_accuracy
    
    def r2_score(self, Y_train, training_data_prediction):  
        # R squared error
        return r2_score(Y_train, training_data_prediction)

    def mean_absolute_error(self, Y_train, training_data_prediction):  
        # R squared error
        return mean_absolute_error(Y_train, training_data_prediction)