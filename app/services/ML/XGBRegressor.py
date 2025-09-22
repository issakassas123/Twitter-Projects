from xgboost import XGBRegressor
from sklearn.metrics import accuracy_score, r2_score, mean_absolute_error

class Xgboost:
    def __init__(self):
        self.model = XGBRegressor()
        
    def xgb_classification(self,  X_train_scaled, y_train):
        self.model.fit(X_train_scaled, y_train)
        
    def predictions(self, X_test_scaled):
        training_data_prediction = self.model.predict(X_test_scaled)
        return training_data_prediction
    
    def xgb_accuracy_score(self, y_test, xgb_predictions):
        xgb_accuracy = accuracy_score(y_test, xgb_predictions)
        return xgb_accuracy
    
    def r2_score(self, Y_train, training_data_prediction):  
        # R squared error
        return r2_score(Y_train, training_data_prediction)

    def mean_absolute_error(self, Y_train, training_data_prediction):  
        # R squared error
        return mean_absolute_error(Y_train, training_data_prediction)