from curriculum_data import TECHNOLOGY_ROADMAPS

class StudyPlanner:
    def __init__(self):
        self.time_allocation = {
            "theory": 0.25,      # 25% theory
            "practice": 0.55,    # 55% practice
            "revision": 0.20     # 20% revision
        }
        
    def generate_full_roadmap(self, skill_name, current_level, pace="Normal", daily_hours=1):
        """
        Generates a complete multi-level roadmap for a skill
        """
        # specialized or generic map
        tech_key = skill_name if skill_name in TECHNOLOGY_ROADMAPS else "Generic"
        roadmap_data = TECHNOLOGY_ROADMAPS.get(tech_key, TECHNOLOGY_ROADMAPS["Generic"])
        
        # Pace multiplier (Fast = less time needed? No, Fast means doing it in fewer days, 
        # but user input is 'learning pace'. 
        # Slow Pace = Relaxed deadline (more weeks). Intensive = Tight deadline (fewer weeks).
        # Actually easier to think of it as: 
        # Slow: Take 1.5x expected hours (more thorough)
        # Normal: 1.0x expected hours
        # Intensive: 0.8x expected hours (cramming)
        pace_multiplier = {"Slow": 1.5, "Normal": 1.0, "Intensive": 0.8}.get(pace, 1.0)
        
        levels = ["Beginner", "Intermediate", "Advanced", "Industry-Ready"]
        full_plan = []
        
        # Determine starting index based on current level
        start_index = 0
        if current_level == "Intermediate": start_index = 1
        elif current_level == "Advanced": start_index = 2
        
        for i in range(len(levels)):
            level_name = levels[i]
            if i < start_index:
                # Mark as completed
                full_plan.append({
                    "level": level_name,
                    "status": "Completed",
                    "duration": "0 Weeks",
                    "details": roadmap_data.get(level_name, {})
                })
                continue
                
            level_data = roadmap_data.get(level_name, TECHNOLOGY_ROADMAPS["Generic"]["Beginner"])
            
            # Calculate dynamic duration
            base_hours = level_data.get("duration_hours", 40)
            adjusted_total_hours = base_hours * pace_multiplier
            
            # Daily hours determines weeks. (Hours / Daily = Days. Days / 7 = Weeks)
            # Avoid division by zero
            safe_daily_hours = max(0.5, float(daily_hours)) 
            total_days = adjusted_total_hours / safe_daily_hours
            weeks = max(1, round(total_days / 7))
            
            full_plan.append({
                "level": level_name,
                "status": "Pending",
                "duration": f"{weeks} Weeks ({int(adjusted_total_hours)} Hours)",
                "daily_time": f"{safe_daily_hours} hrs/day",
                "details": level_data
            })
            
        return full_plan

    def generate_daily_plan(self, skill_name, current_level, target_level, duration_weeks, daily_minutes=60):
        """
        Legacy support for gap analyzer daily plan (simple version)
        """
        # ... (Keep existing logic if needed or redirect to new logic)
        # For now, simplifying to avoid breaking existing calls
        return [] 
