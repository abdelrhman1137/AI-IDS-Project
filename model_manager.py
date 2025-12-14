import joblib
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, accuracy_score

class IDSModel:
    def __init__(self):
        # We use an Ensemble: Combining two powerful models
        self.rf = RandomForestClassifier(n_estimators=50, random_state=42)
        # XGBoost is very efficient for limited IoT resources [cite: 13]
        self.xgb = XGBClassifier(n_estimators=50, random_state=42, use_label_encoder=False, eval_metric='mlogloss')
        
        # The Voting Classifier takes the best decision from both models
        self.ensemble = VotingClassifier(
            estimators=[('rf', self.rf), ('xgb', self.xgb)],
            voting='soft'
        )

    def train(self, X_train, y_train):
        print("Training Upgraded Ensemble Model...")
        self.ensemble.fit(X_train, y_train)
        # We save the model for the Web App phase
        joblib.dump(self.ensemble, 'trained_ids_model.pkl')
        print("Model saved as 'trained_ids_model.pkl'")

    def evaluate(self, X_test, y_test, target_names):
        predictions = self.ensemble.predict(X_test)
        print(f"\nEnsemble Accuracy: {accuracy_score(y_test, predictions) * 100:.2f}%")
        print(classification_report(y_test, predictions, target_names=target_names))