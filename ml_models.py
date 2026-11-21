
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os
import os
import sys

# Ensure local imports work regardless of execution context
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from data_processor import DataProcessor

class SkillLevelPredictor:
    def __init__(self):
        self.model = DecisionTreeClassifier()

    def train(self, data_path):
        df = pd.read_csv(data_path)
        X = df[["GPA", "Projects", "Internships", "Certifications"]]
        y = df["Skill_Level"]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        
        preds = self.model.predict(X_test)
        print(f"Skill Level Predictor Accuracy: {accuracy_score(y_test, preds):.2f}")
        
    def predict(self, gpa, projects, internships, certs):
        input_data = pd.DataFrame([[gpa, projects, internships, certs]], 
                                  columns=["GPA", "Projects", "Internships", "Certifications"])
        return self.model.predict(input_data)[0]

class CareerRecommender:
    def __init__(self):
        self.model = RandomForestClassifier()
        self.feature_names = None

    def train(self, data_path):
        df = pd.read_csv(data_path)
        y = df["Target_Career"]
        X = df.drop("Target_Career", axis=1)
        self.feature_names = X.columns.tolist()
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        
        preds = self.model.predict(X_test)
        print(f"Career Recommender Accuracy: {accuracy_score(y_test, preds):.2f}")

    def predict(self, skill_vector):
        """
        skill_vector: dict mapping skill name to level (0-10)
        """
        # Create input array based on feature_names order
        input_data = []
        for feature in self.feature_names:
            input_data.append(skill_vector.get(feature, 0))
            
        return self.model.predict([input_data])[0]

    def predict_top_n(self, skill_vector, n=3):
        """
        skill_vector: dict mapping skill name to level (0-10)
        Returns top N career classes and their probabilities
        """
        if not self.feature_names:
            return [{"career": "Full Stack Developer", "probability": 1.0}]

        input_data = []
        for feature in self.feature_names:
            input_data.append(skill_vector.get(feature, 0))
            
        probas = self.model.predict_proba([input_data])[0]
        # Get indices of top probabilities
        top_indices = np.argsort(probas)[-n:][::-1]
        
        results = []
        for idx in top_indices:
            results.append({
                "career": self.model.classes_[idx],
                "probability": float(probas[idx])
            })
        return results

class PerformanceAnalyzer:
    def __init__(self):
        self.model = LogisticRegression()

    def train(self, data_path):
        df = pd.read_csv(data_path)
        X = df[["Aptitude", "Soft_Skills", "Tech_Skills", "Projects"]]
        y = df["Hired"]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        
        preds = self.model.predict(X_test)
        print(f"Performance Analyzer Accuracy: {accuracy_score(y_test, preds):.2f}")

    def predict_probability(self, aptitude, soft_skills, tech_skills, projects):
        input_data = pd.DataFrame([[aptitude, soft_skills, tech_skills, projects]],
                                  columns=["Aptitude", "Soft_Skills", "Tech_Skills", "Projects"])
        return self.model.predict_proba(input_data)[0][1] # Probability of Class 1 (Hired)

class ModelManager:
    def __init__(self, model_dir="models", data_dir="data"):
        self.model_dir = model_dir
        self.data_dir = data_dir
        if not os.path.exists(self.model_dir):
            os.makedirs(self.model_dir)
            
        self.skill_predictor = SkillLevelPredictor()
        self.career_recommender = CareerRecommender()
        self.perf_analyzer = PerformanceAnalyzer()
 
    def train_all(self):
        print("Training models...")
        # Ensure data exists
        dp = DataProcessor(self.data_dir)
        if not os.path.exists(os.path.join(self.data_dir, "skill_level_train.csv")):
            dp.generate_synthetic_data()
            
        self.skill_predictor.train(os.path.join(self.data_dir, "skill_level_train.csv"))
        self.career_recommender.train(os.path.join(self.data_dir, "career_train.csv"))
        self.perf_analyzer.train(os.path.join(self.data_dir, "performance_train.csv"))
        
        # Save models
        joblib.dump(self.skill_predictor, os.path.join(self.model_dir, "skill_predictor.pkl"))
        joblib.dump(self.career_recommender, os.path.join(self.model_dir, "career_recommender.pkl"))
        joblib.dump(self.perf_analyzer, os.path.join(self.model_dir, "perf_analyzer.pkl"))
        print("Models trained and saved.")

    def load_models(self):
        try:
            self.skill_predictor = joblib.load(os.path.join(self.model_dir, "skill_predictor.pkl"))
            self.career_recommender = joblib.load(os.path.join(self.model_dir, "career_recommender.pkl"))
            self.perf_analyzer = joblib.load(os.path.join(self.model_dir, "perf_analyzer.pkl"))
            print("Models loaded successfully.")
            return True
        except FileNotFoundError:
            print("Models not found. Please train them first.")
            return False
