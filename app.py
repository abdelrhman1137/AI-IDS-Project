import json
from data_handler import DataHandler
from model_manager import IDSModel
from sklearn.metrics import accuracy_score

def run_project():
    print("--- Starting AI-Based IDS Project (Dynamic Mode) ---")
    
    # 1. Handle Data
    dh = DataHandler('cicids2017_cleaned.csv')
    dh.load_and_clean(sample_size=100000)
    X_train, X_test, y_train, y_test = dh.get_train_test_split()
    
    # 2. Handle AI Model
    ids = IDSModel()
    ids.train(X_train, y_train)
    
    # 3. Evaluation & Saving Dynamic Accuracy
    # Predict to get the actual score
    predictions = ids.ensemble.predict(X_test)
    acc_score = accuracy_score(y_test, predictions)
    
    # Save the score for the Dashboard to read
    accuracy_data = {"accuracy": round(acc_score * 100, 2)}
    with open('accuracy_metric.json', 'w') as f:
        json.dump(accuracy_data, f)
    
    print(f"✅ Training Complete. Accuracy saved: {accuracy_data['accuracy']}%")
    
    # Standard terminal report
    ids.evaluate(X_test, y_test, dh.le.classes_)

if __name__ == "__main__":
    run_project()