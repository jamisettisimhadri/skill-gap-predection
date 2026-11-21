from constants import GOVERNMENT_JOBS, SKILL_TO_CATEGORY_MAP

class JobRecommender:
    def __init__(self):
        self.jobs = GOVERNMENT_JOBS
        self.skill_categories = SKILL_TO_CATEGORY_MAP
    
    def classify_user_skills(self, user_skills, soft_skills_score, aptitude_score):
        """
        Classify user skills into categories for job matching
        user_skills: dict of {skill_name: proficiency_score}
        """
        user_categories = set()
        
        # Technical IT skills
        for skill in user_skills.keys():
            for category, category_skills in self.skill_categories.items():
                if skill in category_skills:
                    user_categories.add(category)
        
        # Analytical skills (based on aptitude and problem solving)
        if aptitude_score >= 60:
            user_categories.add("Analytical")
        
        # Communication skills
        if soft_skills_score >= 60:
            user_categories.add("Communication")
            user_categories.add("Teaching")
        
        # Management/Leadership
        if soft_skills_score >= 70:
            user_categories.add("Management")
            user_categories.add("Administrative")
        
        return user_categories
    
    def match_jobs(self, user_skills, soft_skills_score, aptitude_score, age, education_level):
        """
        Match user to government jobs based on skills
        Returns list of matched jobs with eligibility status
        """
        user_categories = self.classify_user_skills(user_skills, soft_skills_score, aptitude_score)
        matched_jobs = []
        
        for job_id, job_data in self.jobs.items():
            # Check if user has required skill categories
            required_categories = set(job_data["required_skill_categories"])
            category_match = bool(user_categories & required_categories)
            
            if not category_match:
                continue  # Skip jobs that don't match user's skill categories
            
            # Check skill alignment
            matched_skills = []
            for skill in job_data["matched_skills"]:
                if skill in user_skills or skill.lower() in [s.lower() for s in user_skills.keys()]:
                    matched_skills.append(skill)
            
            # Check eligibility
            eligibility_status = self._check_eligibility(job_data, age, education_level)
            
            # Calculate skill gaps
            skill_gaps = [s for s in job_data["matched_skills"] if s not in matched_skills]
            
            matched_jobs.append({
                "job_name": job_data["name"],
                "conducting_body": job_data["conducting_body"],
                "matched_skills": matched_skills if matched_skills else ["General Aptitude"],
                "eligibility_status": eligibility_status,
                "skill_gaps": skill_gaps,
                "preparation_focus": job_data["preparation_focus"],
                "age_limit": f"{job_data['min_age']}-{job_data['max_age']} years",
                "education": job_data["min_education"]
            })
        
        return matched_jobs
    
    def _check_eligibility(self, job_data, user_age, user_education):
        """Check if user meets age and education criteria"""
        age_eligible = job_data["min_age"] <= user_age <= job_data["max_age"]
        
        # Simplified education check
        education_levels = {
            "12th": 1,
            "Graduate": 2,
            "B.Tech": 2,
            "B.E.": 2,
            "Post Graduate": 3,
            "M.Tech": 3,
            "MCA": 3
        }
        
        user_level = education_levels.get(user_education, 2)
        required_level = 1  # Default
        
        if "B.Tech" in job_data["min_education"] or "B.E." in job_data["min_education"]:
            required_level = 2
        elif "Post Graduate" in job_data["min_education"]:
            required_level = 3
        elif "Graduate" in job_data["min_education"]:
            required_level = 2
        
        education_eligible = user_level >= required_level
        
        if age_eligible and education_eligible:
            return "Eligible"
        elif age_eligible or education_eligible:
            return "Partial"
        else:
            return "Not Eligible"
