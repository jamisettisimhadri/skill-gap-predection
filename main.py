
import os
import sys
from data_processor import DataProcessor
from ml_models import ModelManager
from gap_analyzer import GapAnalyzer

def main():
    print("===========================================")
    print(" AI Skill Gap Predictor & Career Guider")
    print("===========================================")
    
    # Initialize
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    model_dir = os.path.join(base_dir, "models")
    
    dp = DataProcessor(data_dir)
    mm = ModelManager(model_dir, data_dir)
    ga = GapAnalyzer()
    
    # Check/Train Models
    if not os.path.exists(os.path.join(model_dir, "skill_predictor.pkl")):
        print("Models not found. Training now...")
        mm.train_all()
    else:
        mm.load_models()
        
    while True:
        print("\nOPTIONS:")
        print("1. Register New Student")
        print("2. Analyze Existing Student")
        print("3. Retrain Models")
        print("4. Exit")
        choice = input("Select an option: ")
        
        if choice == "1":
            register_student(dp)
        elif choice == "2":
            analyze_student(dp, mm, ga)
        elif choice == "3":
            mm.train_all()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

def register_student(dp):
    print("\n--- Student Registration ---")
    name = input("Name: ")
    try:
        gpa = float(input("GPA (0.0 - 4.0): "))
    except ValueError:
        gpa = 3.0
        
    projects = int(input("Number of Projects: ") or 0)
    internships = int(input("Number of Internships: ") or 0)
    certs = int(input("Number of Certifications: ") or 0)
    
    # Skills input
    print("Enter your top skills (comma separated, e.g., Python, SQL, Java):")
    skills_str = input("> ")
    skills_list = [s.strip() for s in skills_str.split(",") if s.strip()]
    
    # Convert to dict with default intermediate score for simplicity of CLI
    skills_dict = {s: 5 for s in skills_list} 
    
    # Basic aptitude scores (could be extended)
    aptitude = int(input("Aptitude Test Score (0-100, default 70): ") or 70)
    soft_skills = int(input("Soft Skills Score (0-100, default 70): ") or 70)
    tech_skills = int(input("Technical Assessment Score (0-100, default 70): ") or 70)
    
    profile = {
        "name": name,
        "GPA": gpa,
        "Projects": projects,
        "Internships": internships,
        "Certifications": certs,
        "Skills": skills_dict,
        "Aptitude": aptitude,
        "Soft_Skills": soft_skills,
        "Tech_Skills": tech_skills
    }
    
    path = dp.save_student_profile(profile)
    print(f"Profile saved to {path}")

def analyze_student(dp, mm, ga):
    print("\n--- Student Analysis ---")
    # List available profiles
    files = [f for f in os.listdir(dp.data_dir) if f.endswith("_profile.json")]
    if not files:
        print("No profiles found. Please register first.")
        return
        
    for i, f in enumerate(files):
        print(f"{i+1}. {f}")
        
    sel = input("Select profile number: ")
    try:
        idx = int(sel) - 1
        filepath = os.path.join(dp.data_dir, files[idx])
        profile = dp.load_student_profile(filepath)
    except (ValueError, IndexError):
        print("Invalid selection.")
        return
        
    print(f"\nAnalyzing profile for {profile['name']}...")
    
    # 1. Predict Skill Level
    pred_level = mm.skill_predictor.predict(profile["GPA"], profile["Projects"], 
                                            profile["Internships"], profile["Certifications"])
    print(f"\n[Predicted Skill Level]: {pred_level}")
    
    # 2. Recommend Career
    # Need to construct skill vector matching training features
    # Since we can't easily query the user for 50+ skills in CLI, we'll map what we have and zero the rest
    # In a real app, this would be a comprehensive form
    # We use the keys from the profile's 'Skills'
    
    pred_career = mm.career_recommender.predict(profile["Skills"])
    print(f"[Recommended Career Path]: {pred_career}")
    
    # 3. Performance Analysis
    hiring_prob = mm.perf_analyzer.predict_probability(profile["Aptitude"], 
                                                       profile["Soft_Skills"], 
                                                       profile["Tech_Skills"], 
                                                       profile["Projects"])
    print(f"[Employability Score]: {hiring_prob*100:.1f}%")
    status = "High Chance of Hire" if hiring_prob > 0.6 else "Needs Improvement"
    print(f"[Status]: {status}")
    
    # 4. Gap Analysis
    print(f"\n--- Gap Analysis for {pred_career} ---")
    gaps = ga.analyze_gaps(profile["Skills"], pred_career)
    roadmap = ga.generate_roadmap(gaps)
    print(roadmap)

if __name__ == "__main__":
    main()
