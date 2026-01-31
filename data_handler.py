import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

class DataHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.all_labels = [
            'Normal Traffic', 'DoS', 'DDoS', 'Port Scanning', 
            'Brute Force', 'Web Attacks', 'Bots'
        ]
        self.le = LabelEncoder()
        self.le.fit(self.all_labels)

    def load_and_clean(self, sample_size=100000):
        self.df = pd.read_csv(self.file_path)
        self.df = self.df.sample(n=sample_size, random_state=42)
        self.df['Attack Type'] = self.le.transform(self.df['Attack Type'])
        return self.df

    def get_train_test_split(self):
        X = self.df.drop('Attack Type', axis=1)
        y = self.df['Attack Type']
        return train_test_split(X, y, test_size=0.2, random_state=42)