import joblib
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, accuracy_score

class IDSModel:
    def __init__(self):
        # We use an Ensemble: Combining two powerful models for better accuracy
        self.rf = RandomForestClassifier(n_estimators=50, random_state=42)
        self.xgb = XGBClassifier(n_estimators=50, random_state=42)
        
        # The Voting Classifier takes the 'best of both worlds'
        self.ensemble = VotingClassifier(
            estimators=[('rf', self.rf), ('xgb', self.xgb)],
            voting='soft'
        )
        print("Model Manager initialized with RF and XGBoost Ensemble.")

    def train(self, X_train, y_train):
        print("Training Ensemble Model (This may take a moment)...")
        self.ensemble.fit(X_train, y_train)
        # We save the model so we can use it later in our Web App without retraining
        joblib.dump(self.ensemble, 'trained_ids_model.pkl')
        print("Model trained and saved as 'trained_ids_model.pkl'")

    def evaluate(self, X_test, y_test, target_names):
        predictions = self.ensemble.predict(X_test)
        print(f"\n--- 10/10 Project Performance ---")
        print(f"Final Ensemble Accuracy: {accuracy_score(y_test, predictions) * 100:.2f}%")
        print("\nDetailed Attack Analysis:")
        print(classification_report(y_test, predictions, target_names=target_names))
        return predictions