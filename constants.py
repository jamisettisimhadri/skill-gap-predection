
# Market Skill Model
MARKET_SKILL_MODEL = {
    "High_Demand_Skills": [
        "Python", "SQL", "Machine Learning", "AI",
        "Cloud Computing", "DevOps",
        "Full Stack Development",
        "Cybersecurity",
        "Data Analytics", "Power BI"
    ]
}

# Skill Categories
SKILL_CATEGORIES = {
    "Technical": [
        "Python", "SQL", "Machine Learning", "AI", "Cloud Computing", "DevOps", 
        "Full Stack Development", "Cybersecurity", "Data Analytics", "Power BI",
        "Java", "C++", "React", "Node.js", "AWS", "Azure"
    ],
    "Soft": [
        "Communication", "Teamwork", "Problem Solving", "Leadership", "Time Management"
    ],
    "Domain": [
        "Finance", "Healthcare", "E-commerce", "Education"
    ]
}

# Career Paths and Required Skills (Simplified for Synthetic Data Logic)
CAREER_PATHS = {
    "Data Scientist": ["Python", "SQL", "Machine Learning", "Data Analytics"],
    "AI Engineer": ["Python", "AI", "Machine Learning", "Cloud Computing"],
    "DevOps Engineer": ["Cloud Computing", "DevOps", "Python", "Linux"],
    "Full Stack Developer": ["Full Stack Development", "JavaScript", "React", "Node.js"],
    "Cybersecurity Analyst": ["Cybersecurity", "Networking", "Python", "Linux"],
    "Data Analyst": ["Data Analytics", "SQL", "Power BI", "Python"]
}

# Baseline skills for inference when technical stack is empty
SKILL_INFERENCE_MAPPING = {
    "Data Science": ["Python", "SQL", "Data Analytics", "Machine Learning"],
    "Web Development": ["Full Stack Development", "JavaScript", "React", "HTML/CSS"],
    "Cloud Development": ["Cloud Computing", "AWS", "DevOps", "Docker"],
    "Cybersecurity": ["Cybersecurity", "Networking", "Linux", "Python"],
    "AI Engineer": ["Python", "AI", "Machine Learning", "Neural Networks"]
}

# Learning Resources (Placeholder)
LEARNING_RESOURCES = {
    "Python": {
        "Premium": "https://www.coursera.org/specializations/google-it-automation",
        "Free": "https://www.python.org/about/gettingstarted/",
        "Practice": "https://leetcode.com/problemset/all/?topicSlugs=python"
    },
    "SQL": {
        "Premium": "https://www.datacamp.com/tracks/sql-fundamentals",
        "Free": "https://www.w3schools.com/sql/",
        "Practice": "https://sqlzoo.net/"
    },
    "Machine Learning": {
        "Premium": "https://www.coursera.org/specializations/machine-learning-introduction",
        "Free": "https://developers.google.com/machine-learning/crash-course",
        "Practice": "https://www.kaggle.com/competitions"
    },
    "Cloud Computing": {
        "Premium": "https://aws.amazon.com/training/digital/aws-cloud-practitioner-essentials/",
        "Free": "https://learn.microsoft.com/en-us/training/azure/",
        "Practice": "https://github.com/donnemartin/system-design-primer"
    },
    "DevOps": {
        "Premium": "https://www.udacity.com/course/cloud-devops-engineer-nanodegree--nd9991",
        "Free": "https://roadmap.sh/devops",
        "Practice": "https://github.com/techworld-with-nana/devops-bootcamp"
    },
    "Full Stack Development": {
        "Premium": "https://www.udemy.com/course/the-complete-web-development-bootcamp/",
        "Free": "https://www.freecodecamp.org/learn/2022/responsive-web-design/",
        "Practice": "https://theodinproject.com/"
    }
}

# Government Jobs Database - Skill-Based Matching
GOVERNMENT_JOBS = {
    "SSC_CGL": {
        "name": "SSC CGL (Combined Graduate Level)",
        "conducting_body": "Staff Selection Commission",
        "required_skill_categories": ["Analytical", "Reasoning", "Quantitative"],
        "matched_skills": ["Problem Solving", "Data Analytics", "Aptitude"],
        "min_age": 18,
        "max_age": 32,
        "min_education": "Graduate",
        "preparation_focus": ["Quantitative Aptitude", "Reasoning", "English", "General Awareness"]
    },
    "IBPS_PO": {
        "name": "IBPS PO (Probationary Officer)",
        "conducting_body": "Institute of Banking Personnel Selection",
        "required_skill_categories": ["Analytical", "Communication", "Management"],
        "matched_skills": ["Problem Solving", "Leadership", "Communication", "Data Analytics"],
        "min_age": 20,
        "max_age": 30,
        "min_education": "Graduate",
        "preparation_focus": ["Banking Awareness", "Reasoning", "Quantitative Aptitude", "English"]
    },
    "IBPS_CLERK": {
        "name": "IBPS Clerk",
        "conducting_body": "Institute of Banking Personnel Selection",
        "required_skill_categories": ["Analytical", "Administrative"],
        "matched_skills": ["Problem Solving", "Communication", "Teamwork"],
        "min_age": 20,
        "max_age": 28,
        "min_education": "Graduate",
        "preparation_focus": ["Reasoning", "Numerical Ability", "English", "Computer Knowledge"]
    },
    "LIC_AAO": {
        "name": "LIC AAO (Assistant Administrative Officer)",
        "conducting_body": "Life Insurance Corporation of India",
        "required_skill_categories": ["Analytical", "Management"],
        "matched_skills": ["Problem Solving", "Leadership", "Data Analytics"],
        "min_age": 21,
        "max_age": 30,
        "min_education": "Graduate",
        "preparation_focus": ["Reasoning", "Quantitative Aptitude", "English", "Insurance Awareness"]
    },
    "PSU_IT": {
        "name": "PSU IT Officer",
        "conducting_body": "Various Public Sector Undertakings",
        "required_skill_categories": ["Technical_IT"],
        "matched_skills": ["Python", "SQL", "Cloud Computing", "DevOps", "Cybersecurity", "Full Stack Development"],
        "min_age": 18,
        "max_age": 30,
        "min_education": "B.Tech/B.E. (CS/IT)",
        "preparation_focus": ["Programming", "Database Management", "Networking", "System Design"]
    },
    "DRDO_SCIENTIST": {
        "name": "DRDO Scientist 'B'",
        "conducting_body": "Defence Research and Development Organisation",
        "required_skill_categories": ["Technical_IT", "Analytical"],
        "matched_skills": ["Python", "AI", "Machine Learning", "Data Analytics", "Cybersecurity"],
        "min_age": 18,
        "max_age": 28,
        "min_education": "B.Tech/B.E.",
        "preparation_focus": ["Technical Knowledge", "Programming", "Research Aptitude", "General Awareness"]
    },
    "ISRO_SCIENTIST": {
        "name": "ISRO Scientist/Engineer",
        "conducting_body": "Indian Space Research Organisation",
        "required_skill_categories": ["Technical_IT", "Analytical"],
        "matched_skills": ["Python", "AI", "Machine Learning", "Cloud Computing", "Data Analytics"],
        "min_age": 18,
        "max_age": 35,
        "min_education": "B.Tech/B.E.",
        "preparation_focus": ["Technical Subjects", "Programming", "Space Technology", "Aptitude"]
    },
    "NIC_SCIENTIST": {
        "name": "NIC Scientist-B",
        "conducting_body": "National Informatics Centre",
        "required_skill_categories": ["Technical_IT"],
        "matched_skills": ["Python", "SQL", "Full Stack Development", "Cloud Computing", "DevOps"],
        "min_age": 18,
        "max_age": 30,
        "min_education": "B.Tech/B.E. (CS/IT) or MCA",
        "preparation_focus": ["Programming", "Database", "Web Technologies", "Networking"]
    },
    "TET": {
        "name": "TET (Teacher Eligibility Test)",
        "conducting_body": "State Education Boards",
        "required_skill_categories": ["Teaching", "Communication"],
        "matched_skills": ["Communication", "Leadership", "Teamwork"],
        "min_age": 18,
        "max_age": 35,
        "min_education": "B.Ed or equivalent",
        "preparation_focus": ["Child Psychology", "Teaching Methodology", "Subject Knowledge", "Language"]
    },
    "LECTURER": {
        "name": "Government Lecturer/Assistant Professor",
        "conducting_body": "Various State PSCs / UGC",
        "required_skill_categories": ["Teaching", "Communication", "Analytical"],
        "matched_skills": ["Communication", "Leadership", "Problem Solving"],
        "min_age": 21,
        "max_age": 40,
        "min_education": "Post Graduate with NET/SET",
        "preparation_focus": ["Subject Expertise", "Research Methodology", "Teaching Aptitude", "General Awareness"]
    },
    "UPSC_IAS": {
        "name": "UPSC Civil Services (IAS/IPS/IFS)",
        "conducting_body": "Union Public Service Commission",
        "required_skill_categories": ["Analytical", "Management", "Communication"],
        "matched_skills": ["Problem Solving", "Leadership", "Communication", "Teamwork"],
        "min_age": 21,
        "max_age": 32,
        "min_education": "Graduate",
        "preparation_focus": ["General Studies", "Current Affairs", "Optional Subject", "Essay Writing"]
    },
    "STATE_PSC": {
        "name": "State Civil Services",
        "conducting_body": "State Public Service Commissions",
        "required_skill_categories": ["Analytical", "Management", "Administrative"],
        "matched_skills": ["Problem Solving", "Leadership", "Communication"],
        "min_age": 21,
        "max_age": 35,
        "min_education": "Graduate",
        "preparation_focus": ["General Studies", "State Affairs", "Aptitude", "Essay"]
    },
    "POLICE_SI": {
        "name": "Police Sub-Inspector",
        "conducting_body": "State Police Recruitment Boards",
        "required_skill_categories": ["Physical", "Discipline", "Analytical"],
        "matched_skills": ["Leadership", "Teamwork", "Problem Solving"],
        "min_age": 21,
        "max_age": 28,
        "min_education": "Graduate",
        "preparation_focus": ["Physical Fitness", "Law & Order", "Reasoning", "General Knowledge"]
    },
    "DEFENCE_ARMY": {
        "name": "Indian Army (CDS/NDA)",
        "conducting_body": "UPSC",
        "required_skill_categories": ["Physical", "Discipline", "Leadership"],
        "matched_skills": ["Leadership", "Teamwork", "Problem Solving"],
        "min_age": 19,
        "max_age": 24,
        "min_education": "Graduate (CDS) / 12th (NDA)",
        "preparation_focus": ["Physical Fitness", "General Knowledge", "Mathematics", "English"]
    },
    "CAPF": {
        "name": "CAPF (Central Armed Police Forces)",
        "conducting_body": "UPSC",
        "required_skill_categories": ["Physical", "Discipline"],
        "matched_skills": ["Leadership", "Teamwork"],
        "min_age": 20,
        "max_age": 25,
        "min_education": "Graduate",
        "preparation_focus": ["Physical Fitness", "General Ability", "Current Affairs", "Essay"]
    }
}

# Skill Category Classification for Job Matching
SKILL_TO_CATEGORY_MAP = {
    "Analytical": ["Problem Solving", "Data Analytics", "Aptitude", "Reasoning", "SQL"],
    "Technical_IT": ["Python", "Java", "C++", "SQL", "Machine Learning", "AI", "Cloud Computing", 
                     "DevOps", "Full Stack Development", "Cybersecurity", "React", "Node.js"],
    "Communication": ["Communication", "English", "Presentation"],
    "Teaching": ["Communication", "Leadership", "Education"],
    "Management": ["Leadership", "Teamwork", "Time Management", "Project Management"],
    "Administrative": ["Leadership", "Communication", "Teamwork"],
    "Physical": ["Fitness", "Discipline", "Endurance"],
    "Discipline": ["Leadership", "Teamwork", "Time Management"]
}
