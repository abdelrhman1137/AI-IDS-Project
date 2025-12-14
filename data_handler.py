import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

class DataHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.le = LabelEncoder()

    def load_and_clean(self, sample_size=100000):
        # Task 6.3: Dataset preprocessing demonstration
        self.df = pd.read_csv(self.file_path)
        self.df = self.df.sample(n=sample_size, random_state=42)
        
        # Convert 'Attack Type' to numbers
        self.df['Attack Type'] = self.le.fit_transform(self.df['Attack Type'])
        return self.df

    def get_train_test_split(self):
        X = self.df.drop('Attack Type', axis=1)
        y = self.df['Attack Type']
        return train_test_split(X, y, test_size=0.2, random_state=42)