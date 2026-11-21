
from constants import CAREER_PATHS, LEARNING_RESOURCES, MARKET_SKILL_MODEL
from study_planner import StudyPlanner

class GapAnalyzer:
    def __init__(self):
        pass

    def analyze_gaps(self, student_skills, target_career, pace="Normal", daily_hours=1):
        """
        student_skills: dict {skill_name: level_str or score}
        target_career: str
        pace: str (Slow, Normal, Intensive)
        daily_hours: float
        """
        # Get career specific skills
        career_skills = list(CAREER_PATHS.get(target_career, []))
        
        # Get market-wide high demand skills
        market_skills = MARKET_SKILL_MODEL.get("High_Demand_Skills", [])
        
        # Combine them (removing duplicates)
        required_skills = sorted(list(set(career_skills + market_skills)))
        
        gaps = []
        all_skill_stats = {}

        # Create a lowercase map for efficient lookup
        student_skills_lower = {str(k).lower(): v for k, v in student_skills.items()}
        
        # FIRST: Add all user skills to stats (so they show as Strong/Weak)
        for skill_name, skill_value in student_skills.items():
            if isinstance(skill_value, str):
                level_map = {"none": 0, "beginner": 3, "intermediate": 6, "advanced": 9}
                score = level_map.get(skill_value.lower(), 0)
            else:
                score = float(skill_value)
            all_skill_stats[skill_name] = score
        
        # THEN: Check required skills and find gaps
        for skill in required_skills:
            # Case-insensitive lookup
            skill_lower = skill.lower()
            current_value = 0
            already_tracked = False
            
            if skill_lower in student_skills_lower:
                current_value = student_skills_lower[skill_lower]
                already_tracked = True
            else:
                # Partial match logic (e.g. "Python" in "Python Programming")
                for sk_key, val in student_skills_lower.items():
                    if skill_lower in sk_key or sk_key in skill_lower:
                        current_value = val
                        already_tracked = True
                        break

            # Convert string levels to scores for the graph
            if isinstance(current_value, str):
                level_map = {"none": 0, "beginner": 3, "intermediate": 6, "advanced": 9}
                curr_score = level_map.get(current_value.lower(), 0)
            else:
                curr_score = float(current_value)

            # Only add to stats if not already tracked from user skills
            if not already_tracked:
                all_skill_stats[skill] = curr_score

            # Logic: If level is low (less than 7/10 for high demand), it's a gap
            if curr_score < 7: 
                current_level = self._get_level_name(curr_score)
                duration_str = self._estimate_duration(curr_score)
                
                # Generate FULL multi-level roadmap (NEW)
                planner = StudyPlanner()
                full_roadmap = planner.generate_full_roadmap(
                    skill_name=skill,
                    current_level=current_level,
                    pace=pace,
                    daily_hours=daily_hours
                )
                
                gap_info = {
                    "Skill": skill,
                    "Category": self._get_category(skill),
                    "Current_Level": current_level,
                    "Target_Level": "Advanced Mastery",
                    "Duration": duration_str,
                    "Resources": LEARNING_RESOURCES.get(skill, {
                        "Premium": f"https://www.coursera.org/search?query={skill}", 
                        "Free": f"https://github.com/topics/{skill}", 
                        "Practice": f"https://www.hackerrank.com/domains/{skill.lower().replace(' ', '-')}"
                    }),
                    "Roadmap": full_roadmap # NEW: Complete roadmap
                }
                gaps.append(gap_info)
                
        return {"gaps": gaps, "skill_stats": all_skill_stats}
    
    def _parse_duration_weeks(self, duration_str):
        """Convert duration string to weeks"""
        if "4-6 Months" in duration_str:
            return 20  # 5 months average
        elif "3-4 Months" in duration_str:
            return 14  # 3.5 months
        elif "1-2 Months" in duration_str:
            return 6   # 1.5 months
        else:
            return 3   # 3 weeks

    def infer_skills(self, career_interest):
        """Returns a baseline skill dictionary if input is empty"""
        from constants import SKILL_INFERENCE_MAPPING
        skills = SKILL_INFERENCE_MAPPING.get(career_interest, ["Python", "SQL", "Communication"])
        return {s: 0 for s in skills} # Start from level 0 for suggested skills

    def _get_level_name(self, score):
        if score == 0: return "None"
        elif score < 5: return "Beginner"
        elif score < 8: return "Intermediate"
        return "Advanced"

    def _get_category(self, skill):
        from constants import SKILL_CATEGORIES
        for cat, skills in SKILL_CATEGORIES.items():
            if skill in skills:
                return cat
        return "Technical"

    def _estimate_duration(self, current_score):
        if current_score == 0:
            return "4-6 Months (Deep Dive)"
        elif current_score < 5:
            return "3-4 Months (Bridge Gap)"
        elif current_score < 8:
            return "1-2 Months (Focused)"
        else:
            return "2-4 Weeks (Elite Polish)"

    def generate_roadmap(self, gaps):
        if not gaps:
            return "Great job! You match the requirements for this role."
            
        roadmap = "--- Personalized Learning Roadmap ---\n"
        for i, gap in enumerate(gaps, 1):
            roadmap += f"{i}. **{gap['Skill']}** ({gap['Category']})\n"
            roadmap += f"   - Current: {gap['Current_Level']} -> Target: {gap['Required_Level']}\n"
            roadmap += f"   - Estimated Time: {gap['Duration']}\n"
        return roadmap
