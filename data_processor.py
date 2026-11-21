
import pandas as pd
import numpy as np
import os
import json
import random
from constants import CAREER_PATHS, SKILL_CATEGORIES

class DataProcessor:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            
    def generate_synthetic_data(self):
        """Generates synthetic datasets for training models."""
        print("Generating synthetic data...")
        self._generate_skill_level_data()
        self._generate_career_recommendation_data()
        self._generate_performance_data()
        print(f"Data generated in {self.data_dir}/")

    def _generate_skill_level_data(self):
        # Logic: GPA, Projects, Internships -> Skill Level
        data = []
        for _ in range(1000):
            gpa = round(random.uniform(5.0, 10.0), 2) # Assuming 10.0 scale
            projects = random.randint(0, 5)
            internships = random.randint(0, 3)
            certs = random.randint(0, 5)
            
            # Simple heuristic for label - adjusted for 10.0 scale
            score = (gpa * 6) + (projects * 5) + (internships * 10) + (certs * 2)
            if score > 80:
                level = "Advanced"
            elif score > 50:
                level = "Intermediate"
            else:
                level = "Beginner"
                
            data.append([gpa, projects, internships, certs, level])
            
        df = pd.DataFrame(data, columns=["GPA", "Projects", "Internships", "Certifications", "Skill_Level"])
        df.to_csv(os.path.join(self.data_dir, "skill_level_train.csv"), index=False)

    def _generate_career_recommendation_data(self):
        # Logic: Skills -> Career
        # We'll treat this as a multi-class classification
        # Features: Proficiency in specific key skills (0-10)
        # Target: Career Path
        
        roles = list(CAREER_PATHS.keys())
        all_skills = set()
        for skills in CAREER_PATHS.values():
            all_skills.update(skills)
        all_skills = sorted(list(all_skills))
        
        data = []
        for _ in range(1000):
            # Pick a target role to bias the generation so we have clear patterns
            target_role = random.choice(roles)
            required_skills = CAREER_PATHS[target_role]
            
            row = {}
            for skill in all_skills:
                if skill in required_skills:
                    row[skill] = random.randint(6, 10) # Good at required skills
                else:
                    row[skill] = random.randint(0, 5) # Average/Poor at others
            
            row["Target_Career"] = target_role
            data.append(row)
            
        df = pd.DataFrame(data)
        df.to_csv(os.path.join(self.data_dir, "career_train.csv"), index=False)

    def _generate_performance_data(self):
        # Logic: Overall attributes -> Employability Score (0 or 1 for hired)
        data = []
        for _ in range(1000):
            aptitude_test = random.randint(0, 100)
            soft_skill_score = random.randint(0, 100)
            tech_skill_score = random.randint(0, 100)
            projects = random.randint(0, 5)
            
            # Composite score
            total = (aptitude_test * 0.3) + (soft_skill_score * 0.2) + (tech_skill_score * 0.4) + (projects * 2)
            hired = 1 if total > 60 else 0
            
            data.append([aptitude_test, soft_skill_score, tech_skill_score, projects, hired])
            
        df = pd.DataFrame(data, columns=["Aptitude", "Soft_Skills", "Tech_Skills", "Projects", "Hired"])
        df.to_csv(os.path.join(self.data_dir, "performance_train.csv"), index=False)

    def save_student_profile(self, profile):
        """Saves a single student profile to JSON."""
        # Use name or ID for filename
        filename = f"{profile['name'].replace(' ', '_').lower()}_profile.json"
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(profile, f, indent=4)
        return filepath
            
    def load_student_profile(self, filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
