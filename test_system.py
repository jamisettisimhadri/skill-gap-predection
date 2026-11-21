
import os
import sys
import shutil

# Add parent directory to path so we can import the package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skill_gap_predictor.data_processor import DataProcessor
from skill_gap_predictor.ml_models import ModelManager
from skill_gap_predictor.gap_analyzer import GapAnalyzer

def test_system():
    print("Running System Verification...")
    
    # Setup paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "test_data")
    model_dir = os.path.join(base_dir, "test_models")
    
    # Clean up verification dirs
    if os.path.exists(data_dir): shutil.rmtree(data_dir)
    if os.path.exists(model_dir): shutil.rmtree(model_dir)
    
    try:
        # 1. Initialize Components
        print("[1/5] Initializing Components...")
        dp = DataProcessor(data_dir)
        mm = ModelManager(model_dir, data_dir)
        ga = GapAnalyzer()
        
        # 2. Train Models (Includes Data Generation)
        print("[2/5] Training Models...")
        mm.train_all()
        assert os.path.exists(os.path.join(model_dir, "skill_predictor.pkl"))
        assert os.path.exists(os.path.join(data_dir, "skill_level_train.csv"))
        
        # 3. Create Dummy Student
        print("[3/5] Simulating Student Data...")
        student_skills = {"Python": 8, "SQL": 6, "Communication": 7} # Good at Python/SQL
        
        # 4. Run Predictions
        print("[4/5] Running Predictions...")
        # Skill Level - 8.5 on 10pt scale
        level = mm.skill_predictor.predict(8.5, 3, 1, 2)
        print(f"   > Predicted Level: {level}")
        
        # Career
        career = mm.career_recommender.predict(student_skills)
        print(f"   > Recommended Career: {career}")
        
        # Performance
        prob = mm.perf_analyzer.predict_probability(80, 70, 85, 3)
        print(f"   > Hiring Probability: {prob:.2f}")
        
        # 5. Gap Analysis
        print("[5/5] Generating Roadmap...")
        gaps = ga.analyze_gaps(student_skills, career)
        roadmap = ga.generate_roadmap(gaps)
        print(roadmap)
        
        print("\n✅ System Verification PASSED!")
        
    except Exception as e:
        print(f"\n❌ System Verification FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Cleanup
        if os.path.exists(data_dir): shutil.rmtree(data_dir)
        if os.path.exists(model_dir): shutil.rmtree(model_dir)

if __name__ == "__main__":
    test_system()
