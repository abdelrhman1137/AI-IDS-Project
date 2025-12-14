from data_handler import DataHandler
from model_manager import IDSModel

def run_project():
    print("--- Starting AI-Based IDS Project ---")
    
    # 1. Handle Data
    dh = DataHandler('cicids2017_cleaned.csv')
    dh.load_and_clean()
    X_train, X_test, y_train, y_test = dh.get_train_test_split()
    
    # 2. Handle AI Model
    ids = IDSModel()
    ids.train(X_train, y_train)
    
    # 3. Show Results
    ids.evaluate(X_test, y_test, dh.le.classes_)

if __name__ == "__main__":
    run_project()