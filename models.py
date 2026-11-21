
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), unique=True, nullable=False)
    fullname = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile = db.Column(db.String(20))
    dob = db.Column(db.String(20))
    
    # Academic Info
    course = db.Column(db.String(100))
    year = db.Column(db.String(20))
    marks_10th = db.Column(db.Float)
    marks_inter = db.Column(db.Float)
    cgpa = db.Column(db.Float)
    
    # Technical Skills
    technical_skills = db.Column(db.Text) # Stored as comma-separated string
    skill_level = db.Column(db.String(50)) # Beginner/Intermediate/Advanced
    
    # Professional Experience
    certifications = db.Column(db.Integer, default=0)
    internships = db.Column(db.Integer, default=0)
    projects = db.Column(db.Integer, default=0)
    
    # Soft Skills (0-100 scale)
    communication = db.Column(db.Integer, default=0)
    teamwork = db.Column(db.Integer, default=0)
    problem_solving = db.Column(db.Integer, default=0)
    leadership = db.Column(db.Integer, default=0)
    
    # Career Interest
    career_interest = db.Column(db.String(100))
    
    # Authentication
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_completion_percentage(self):
        # Fields to check for profile completion
        fields = [
            self.fullname, self.age, self.gender, self.mobile, self.dob,
            self.course, self.year, self.marks_10th, self.marks_inter, self.cgpa,
            self.technical_skills, self.career_interest
        ]
        filled = len([f for f in fields if f is not None and str(f).strip() != ""])
        return int((filled / len(fields)) * 100)

    def to_dict(self):
        # Calculate scores for analytics
        aptitude = self.problem_solving or 70
        soft = self.communication or 70
        # Calculate a baseline tech score based on existing fields
        tech = ((self.communication or 0) + (self.teamwork or 0) + (self.problem_solving or 0) + (self.leadership or 0)) // 4
        if tech == 0: tech = 70

        return {
            "name": self.fullname,
            "gpa": self.cgpa or 7.0,
            "projects": self.projects or 0,
            "internships": self.internships or 0,
            "certifications": self.certifications or 0,
            "skills": self.technical_skills or "",
            "aptitude": aptitude,
            "soft_skills": soft,
            "tech_skills": tech,
            "career_interest": self.career_interest or "AI Engineer"
        }
