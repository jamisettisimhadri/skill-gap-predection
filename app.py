
import os
import sys
import json
import secrets
import logging
from flask import Flask, render_template, request, jsonify, url_for, redirect, session
from datetime import datetime, timedelta
from flask_mail import Mail, Message

from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import cachecontrol
import google.auth.transport.requests
from firebase_admin import auth as firebase_auth

# Add parent dir to path for package imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_processor import DataProcessor
from ml_models import ModelManager
from gap_analyzer import GapAnalyzer
from job_recommender import JobRecommender
from firebase_db import firebase_user_manager
from company_data import COMPANY_DATA
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# removed redundant app = Flask(__name__)
# Forced reload - code check 1

# Initialize System Components
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "data")
model_dir = os.path.join(base_dir, "models")
template_dir = os.path.join(base_dir, "templates")
static_dir = os.path.join(base_dir, "static")

from flask_cors import CORS

# Initialize Flask with explicit paths
app = Flask(__name__, 
            template_folder=template_dir, 
            static_folder=static_dir,
            static_url_path='/static')

# Flask needs a secret key for sessions (login, registration, Google OAuth).
# Always set SECRET_KEY in production; for local development fall back to a
# temporary random key so session-writing routes don't fail with a 500.
_secret_key = os.environ.get('SECRET_KEY')
if not _secret_key:
    _secret_key = secrets.token_hex(32)
    print("WARNING: SECRET_KEY is not set. Using a temporary random key; "
          "sessions will be invalidated on restart. Set the SECRET_KEY "
          "environment variable in production.")
app.config['SECRET_KEY'] = _secret_key

# --- FLASK-MAIL CONFIGURATION ---
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'simhadrijamisetti@gmail.com'
# To the user: You will need to replace this with your real App Password from Google settings.
# For now, it will throw an error and fallback to console printing if this password is wrong.
app.config['MAIL_PASSWORD'] =  os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = ('Skill Gap Predictor', 'simhadrijamisetti@gmail.com')

mail = Mail(app)

CORS(app, supports_credentials=True)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Simple User class for Flask-Login
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_data):
        # Critical: Flask-Login UserMixin uses 'id' by default
        self.id = user_data.get('student_id')
        self.student_id = user_data.get('student_id')
        self.email = user_data.get('email')
        self.fullname = user_data.get('fullname')
        self.age = user_data.get('age', 0)
        self.gender = user_data.get('gender')
        self.mobile = user_data.get('mobile')
        self.course = user_data.get('course')
        self.year = user_data.get('year')
        self.cgpa = user_data.get('cgpa', 0)
        self.technical_skills = user_data.get('technical_skills')
        self.skill_level = user_data.get('skill_level')
        self.projects = user_data.get('projects', 0)
        self.internships = user_data.get('internships', 0)
        self.certifications = user_data.get('certifications', 0)
        self.communication = user_data.get('communication', 0)
        self.teamwork = user_data.get('teamwork', 0)
        self.problem_solving = user_data.get('problem_solving', 0)
        self.leadership = user_data.get('leadership', 0)
        self.career_interest = user_data.get('career_interest')
        self.password_hash = user_data.get('password_hash')
        self.marks_10th = user_data.get('marks_10th')
        self.marks_inter = user_data.get('marks_inter')
        self.dob = user_data.get('dob')
    
    # Explicit override to be safe, though UserMixin provides this if self.id is set
    def get_id(self):
        return str(self.student_id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_completion_percentage(self):
        fields = [
            self.fullname, self.email, self.mobile, self.gender, 
            self.course, self.year, self.technical_skills, 
            self.career_interest, self.projects, self.internships
        ]
        filled = [f for f in fields if f]
        return int((len(filled) / len(fields)) * 100)

    def to_dict(self):
        return {
            'student_id': self.student_id,
            'email': self.email,
            'fullname': self.fullname,
            'age': self.age,
            'gender': self.gender,
            'mobile': self.mobile,
            'course': self.course,
            'year': self.year,
            'cgpa': self.cgpa,
            'technical_skills': self.technical_skills,
            'skill_level': self.skill_level,
            'projects': self.projects,
            'internships': self.internships,
            'certifications': self.certifications,
            'communication': self.communication,
            'teamwork': self.teamwork,
            'problem_solving': self.problem_solving,
            'leadership': self.leadership,
            'career_interest': self.career_interest,
            'password_hash': self.password_hash,
            'marks_10th': self.marks_10th,
            'marks_inter': self.marks_inter,
            'dob': self.dob
        }

# Initialize system components
dp = DataProcessor(data_dir)
mm = ModelManager(model_dir, data_dir)
ga = GapAnalyzer()
jr = JobRecommender()

# Ensure models are loaded
if not os.path.exists(os.path.join(model_dir, "skill_predictor.pkl")):
    print("Training models on startup...")
    mm.train_all()
else:
    mm.load_models()

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- GOOGLE OAUTH CONFIGURATION ---
GOOGLE_CLIENT_ID = "263713427800-du23m8ql80thlpjneptgtjvcrjj7vn3i.apps.googleusercontent.com" # TODO: User must set this natively
# Secure cookies are required over HTTPS (e.g. Render), but must be disabled
# for local HTTP development or the browser drops the login cookie.
_secure_cookie = os.environ.get('SESSION_COOKIE_SECURE')
if _secure_cookie is None:
    _secure_cookie = 'true' if os.environ.get('RENDER') == 'true' else 'false'
app.config['SESSION_COOKIE_SECURE'] = _secure_cookie.lower() in ('1', 'true', 'yes')
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax' # Recommended for CSRF protection

@login_manager.user_loader
def load_user(student_id):
    user_data = firebase_user_manager.get_user_by_id(student_id)
    if user_data:
        return User(user_data)
    return None

@app.route('/api/me')
@login_required
def get_me():
    return jsonify({"status": "success", "user": current_user.to_dict()})

@app.route('/')
def index():
    if current_user.is_authenticated:
        if request.headers.get('Accept') == 'application/json':
             return jsonify({"status": "authenticated", "user": current_user.to_dict()})
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle both form and JSON data
        if request.is_json:
            data = request.json
            email = data.get('email')
            password = data.get('password')
        else:
            email = request.form.get('email')
            password = request.form.get('password')
            
        print(f"DEBUG: Login attempt for {email}")
        
        try:
            user_data = firebase_user_manager.get_user_by_email(email)
            if not user_data:
                print("DEBUG: User not found in Firebase")
                if request.is_json:
                     return jsonify({"status": "error", "message": "Invalid email or password"}), 401
                return render_template('login.html', error="Invalid email or password")
            
            print(f"DEBUG: User found: {user_data.get('student_id')}")
            stored_hash = user_data.get('password_hash')
            if not stored_hash:
                print("DEBUG: No password hash found for user")
                if request.is_json:
                    return jsonify({"status": "error", "message": "Account error: Please reset password"}), 400
                return render_template('login.html', error="Account error: Please reset password")
                
            if check_password_hash(stored_hash, password):
                print("DEBUG: Password match! Logging in...")
                user = User(user_data)
                login_user(user)
                if request.is_json:
                    return jsonify({"status": "success", "user": current_user.to_dict()})
                return redirect(url_for('dashboard'))
            else:
                print("DEBUG: Password mismatch")
                if request.is_json:
                    return jsonify({"status": "error", "message": "Invalid email or password"}), 401
                return render_template('login.html', error="Invalid email or password")
                
        except Exception as e:
            print(f"DEBUG: Login exception: {e}")
            import traceback
            traceback.print_exc()
            if request.is_json:
                return jsonify({"status": "error", "message": "System error during login"}), 500
            return render_template('login.html', error="System error during login")

    return render_template('login.html')

# ---- Forgot Password Routes ----
from firebase_db import db as firestore_db

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        if not email:
            return render_template('forgot_password.html', error="Please enter your email address.")
        
        try:
            user_data = firebase_user_manager.get_user_by_email(email)
            if not user_data:
                return render_template('forgot_password.html', error="No account found with that email address.")
            
            # Generate a secure random token
            token = secrets.token_urlsafe(32)
            expires_at = datetime.utcnow() + timedelta(minutes=30)
            
            # Store the reset token in Firestore
            reset_ref = firestore_db.collection('password_resets').document(token)
            reset_ref.set({
                'email': email,
                'student_id': user_data.get('student_id'),
                'created_at': datetime.utcnow(),
                'expires_at': expires_at,
                'used': False
            })
            
            # Generate the reset link
            reset_link = url_for('reset_password', token=token, _external=True)
            
            return render_template('forgot_password.html',
                                   success="Reset link generated successfully!",
                                   reset_link=reset_link)
        except Exception as e:
            print(f"Forgot password error: {e}")
            import traceback
            traceback.print_exc()
            return render_template('forgot_password.html', error="An error occurred. Please try again.")
    
    return render_template('forgot_password.html')

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    # Validate the token
    try:
        reset_ref = firestore_db.collection('password_resets').document(token)
        reset_doc = reset_ref.get()
        
        if not reset_doc.exists:
            return render_template('reset_password.html', error="Invalid or expired reset link. Please request a new one.", token=token)
        
        reset_data = reset_doc.to_dict()
        
        # Check if token is already used
        if reset_data.get('used', False):
            return render_template('reset_password.html', error="This reset link has already been used. Please request a new one.", token=token)
        
        # Check if token has expired
        expires_at = reset_data.get('expires_at')
        if expires_at:
            # Handle both datetime and Firestore timestamp
            if hasattr(expires_at, 'timestamp'):
                import pytz
                expires_at_dt = expires_at.replace(tzinfo=None) if expires_at.tzinfo else expires_at
            else:
                expires_at_dt = expires_at
            
            if datetime.utcnow() > expires_at_dt:
                return render_template('reset_password.html', error="This reset link has expired. Please request a new one.", token=token)
        
        if request.method == 'POST':
            password = request.form.get('password', '')
            confirm_password = request.form.get('confirm_password', '')
            
            if len(password) < 6:
                return render_template('reset_password.html', error="Password must be at least 6 characters.", token=token)
            
            if password != confirm_password:
                return render_template('reset_password.html', error="Passwords do not match.", token=token)
            
            # Update the user's password
            student_id = reset_data.get('student_id')
            new_hash = generate_password_hash(password)
            firebase_user_manager.update_user(student_id, {'password_hash': new_hash})
            
            # Mark token as used
            reset_ref.update({'used': True})
            
            return render_template('reset_password.html', success="Password reset successfully! You can now log in.", token=token)
        
        return render_template('reset_password.html', token=token)
        
    except Exception as e:
        print(f"Reset password error: {e}")
        import traceback
        traceback.print_exc()
        return render_template('reset_password.html', error="An error occurred. Please try again.", token=token)

import random
import smtplib
from email.mime.text import MIMEText

@app.route('/api/send-otp', methods=['POST'])
def send_otp():
    try:
        data = request.json
        method = data.get('method')
        target = data.get('target').strip()
        
        if method == 'email':
            user_data = firebase_user_manager.get_user_by_email(target)
            if not user_data:
                return jsonify({"status": "error", "message": "Email not found in our records."}), 404
                
            student_id = user_data.get('student_id')
        elif method == 'phone':
            # Query Firestore for a user with this exact phone number
            users_ref = firestore_db.collection('users')
            query = users_ref.where('mobile', '==', target).limit(1)
            docs = list(query.stream())
            
            if not docs:
                return jsonify({"status": "error", "message": "Phone number not found in our records."}), 404
            
            user_data = docs[0].to_dict()
            student_id = user_data.get('student_id')
        else:
            return jsonify({"status": "error", "message": "Invalid method"}), 400

        # Generate 6 digit OTP
        otp_code = str(random.randint(100000, 999999))
        
        # Save to Firestore (expires in 10 minutes)
        expires_at = datetime.utcnow() + timedelta(minutes=10)
        otp_ref = firestore_db.collection('otps').document(target)
        otp_ref.set({
            'code': otp_code,
            'student_id': student_id,
            'expires_at': expires_at,
            'used': False
        })
        
        # --- Send Email Logic using Flask-Mail ---
        if method == 'email':
            try:
                msg = Message(
                    subject="Your Password Recovery Code",
                    recipients=[target],
                    body=f"""Hello,

You requested a password reset for your Skill Gap Predictor account.

Your 6-digit recovery code is: {otp_code}

This code will expire in 10 minutes. If you did not request this, please ignore this email.

Best regards,
The Skill Gap Predictor Team"""
                )
                mail.send(msg)
                print(f"SUCCESS: OTP Email sent to {target} with code {otp_code}")
            except Exception as e:
                print(f"--------------------------------------------------")
                print(f"ERROR: Email could not be sent (SMTP authentication failed).")
                print(f"Details: {str(e)}")
                print(f"DEVELOPMENT OTP CODE FOR {target} IS: {otp_code}")
                print(f"--------------------------------------------------")
                return jsonify({"status": "success", "message": f"Email failed but development code generated in server console."}), 200
                
        # --- Send SMS Logic ---
        # DEMO MODE: Since Twilio and Firebase SMS are unconfigured/billing locked,
        # we will simply print the OTP securely to the terminal console so the user
        # can practice and test the frontend flow!
        elif method == 'phone':
            print(f"==================================================")
            print(f" DEMO MODE SMS MOCK ")
            print(f" Simulated text message sent to: {target}")
            print(f" OTP CODE: {otp_code}")
            print(f"==================================================")
            return jsonify({"status": "success", "message": "Demo Mode: Check your server terminal console for the verification code!"}), 200
        
        return jsonify({"status": "success", "message": "OTP Sent successfully!"})
        
    except Exception as e:
        print(f"Send OTP Error: {e}")
        return jsonify({"status": "error", "message": "Server error generating OTP"}), 500

@app.route('/api/verify-otp', methods=['POST'])
def verify_otp():
    try:
        data = request.json
        target = data.get('target').strip()
        code = data.get('code').strip()
        
        otp_ref = firestore_db.collection('otps').document(target)
        otp_doc = otp_ref.get()
        
        if not otp_doc.exists:
            return jsonify({"status": "error", "message": "No OTP found or it has expired. Request a new one."}), 400
            
        otp_data = otp_doc.to_dict()
        
        if otp_data.get('used'):
            return jsonify({"status": "error", "message": "This code has already been used."}), 400
            
        # Check Expiry
        expires_at = otp_data.get('expires_at')
        if expires_at:
            if hasattr(expires_at, 'timestamp'):
                expires_at_dt = expires_at.replace(tzinfo=None) if expires_at.tzinfo else expires_at
            else:
                expires_at_dt = expires_at
                
            if datetime.utcnow() > expires_at_dt:
                return jsonify({"status": "error", "message": "Code has expired. Please request a new one."}), 400
                
        # Check Code match
        if otp_data.get('code') != code:
            return jsonify({"status": "error", "message": "Invalid code."}), 400
            
        # Code is valid, generate a password reset token and return it
        reset_token = secrets.token_urlsafe(32)
        reset_ref = firestore_db.collection('password_resets').document(reset_token)
        reset_ref.set({
            'email': target,
            'student_id': otp_data.get('student_id'),
            'created_at': datetime.utcnow(),
            'expires_at': datetime.utcnow() + timedelta(minutes=15),
            'used': False
        })
        
        # Mark OTP as used
        otp_ref.update({'used': True})
        
        return jsonify({
            "status": "success", 
            "message": "OTP Verified", 
            "reset_url": url_for('reset_password', token=reset_token, _external=True)
        })
        
    except Exception as e:
        print(f"Verify OTP Error: {e}")
        return jsonify({"status": "error", "message": "Server error verifying OTP"}), 500

@app.route('/api/verify-firebase-phone', methods=['POST'])
def verify_firebase_phone():
    """
    Called by the frontend after Firebase JS SDK successfully verifies an SMS OTP.
    It passes the Firebase Authentication ID token containing the verified phone number.
    """
    try:
        data = request.json
        id_token = data.get('id_token')
        
        if not id_token:
            return jsonify({"status": "error", "message": "Missing ID Token."}), 400
            
        # Verify the Firebase ID Token
        decoded_token = firebase_auth.verify_id_token(id_token)
        phone_number = decoded_token.get('phone_number')
        
        if not phone_number:
            return jsonify({"status": "error", "message": "Phone number not found in token."}), 400
            
        # Query Firestore for a user with this exact phone number
        users_ref = firestore_db.collection('users')
        query = users_ref.where('mobile', '==', phone_number).limit(1)
        docs = list(query.stream())
        
        if not docs:
            return jsonify({"status": "error", "message": "Phone number not registered to any account."}), 404
        
        user_data = docs[0].to_dict()
        student_id = user_data.get('student_id')
        
        # Phone verified! Generate a password reset URL
        reset_token = secrets.token_urlsafe(32)
        reset_ref = firestore_db.collection('password_resets').document(reset_token)
        reset_ref.set({
            'phone': phone_number,
            'student_id': student_id,
            'created_at': datetime.utcnow(),
            'expires_at': datetime.utcnow() + timedelta(minutes=15),
            'used': False
        })
        
        return jsonify({
            "status": "success", 
            "message": "Phone Verified", 
            "reset_url": url_for('reset_password', token=reset_token, _external=True)
        })
        
    except ValueError as e:
        # Invalid Auth Token
        return jsonify({"status": "error", "message": "Invalid Firebase Authentication Token."}), 401
    except Exception as e:
        print(f"Firebase Phone Verify Error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

# Helper functions for safe conversion
def safe_int(value, default=0):
    try:
        if not value: return default
        return int(value)
    except (ValueError, TypeError):
        return default

def safe_float(value, default=0.0):
    try:
        if not value: return default
        return float(value)
    except (ValueError, TypeError):
        return default

@app.route('/register')
def register():
    # Redirect to step 1
    return redirect(url_for('register_step1'))

@app.route('/register/step1', methods=['GET', 'POST'])
def register_step1():
    if request.method == 'POST':
        data = request.form.to_dict()
        # Basic validation
        if not data.get('fullname') or not data.get('email') or not data.get('student_id'):
            return render_template('register_step1.html', error="Please fill in all required fields.")
        
        # Check if email/student_id already exists early
        if firebase_user_manager.user_exists(email=data.get('email')):
            return render_template('register_step1.html', error="Email already registered")
        if firebase_user_manager.user_exists(student_id=data.get('student_id')):
            return render_template('register_step1.html', error="Student ID already registered")

        if 'reg_data' not in session:
            session['reg_data'] = {}
        
        # Update session data
        current_data = session['reg_data']
        current_data.update(data)
        session['reg_data'] = current_data
        
        return redirect(url_for('register_step2'))
        
    return render_template('register_step1.html')

@app.route('/register/step2', methods=['GET', 'POST'])
def register_step2():
    if 'reg_data' not in session:
        return redirect(url_for('register_step1'))
        
    if request.method == 'POST':
        data = request.form.to_dict()
        current_data = session['reg_data']
        current_data.update(data)
        session['reg_data'] = current_data
        return redirect(url_for('register_step3'))
        
    return render_template('register_step2.html')

@app.route('/register/step3', methods=['GET', 'POST'])
def register_step3():
    if 'reg_data' not in session:
        return redirect(url_for('register_step1'))
        
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            current_data = session['reg_data']
            current_data.update(data)
            
            # Final validation: check password
            password = data.get('password')
            confirm_password = data.get('confirm_password')
            if not password or password != confirm_password:
                return render_template('register_step3.html', error="Passwords do not match")

            # Prepare final user data
            new_user_data = {
                'student_id': current_data.get('student_id'),
                'fullname': current_data.get('fullname'),
                'email': current_data.get('email'),
                'age': safe_int(current_data.get('age')),
                'gender': current_data.get('gender'),
                'mobile': current_data.get('mobile'),
                'course': current_data.get('course'),
                'year': current_data.get('year'),
                'cgpa': safe_float(current_data.get('cgpa')),
                'technical_skills': current_data.get('skills'),
                'skill_level': current_data.get('skill_level'),
                'projects': safe_int(current_data.get('projects')),
                'internships': safe_int(current_data.get('internships')),
                'certifications': safe_int(current_data.get('certifications')),
                'career_interest': current_data.get('career_interest'),
                'communication': 0,
                'teamwork': 0,
                'problem_solving': 0,
                'leadership': 0,
                'marks_10th': 0,
                'marks_inter': 0,
                'dob': current_data.get('dob')
            }
            
            # Helper User object for hashing
            temp_user = User(new_user_data)
            temp_user.set_password(password)
            new_user_data['password_hash'] = temp_user.password_hash

            # Save to Firebase
            firebase_user_manager.create_user(new_user_data)
            
            # Clear session
            session.pop('reg_data', None)
            
            # Log them in
            login_user(User(new_user_data))
            return redirect(url_for('dashboard'))
            
        except Exception as e:
            print(f"Registration error: {e}")
            return render_template('register_step3.html', error=f"Registration failed: {str(e)}")
            
    return render_template('register_step3.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('index.html', user=current_user)

@app.route('/profile')
@login_required
def profile():
    completion = current_user.get_completion_percentage()
    return render_template('profile.html', user=current_user, completion=completion)

@app.route('/companies')
@login_required
def companies():
    user_skills = [s.strip().lower() for s in (current_user.technical_skills or "").split(',') if s.strip()]
    enriched_companies = []
    
    for comp in COMPANY_DATA:
        company = comp.copy()
        
        # Smart Matching Logic
        required_skills = [s.lower() for s in company.get('skills_required', [])]
        if not required_skills:
            match_score = 0
            matched_skills = []
            missing_skills = []
        else:
            matched_skills = [s for s in required_skills if any(us in s or s in us for us in user_skills)]
            missing_skills = [s for s in required_skills if s not in matched_skills]
            match_score = int((len(matched_skills) / len(required_skills)) * 100)
        
        company['match_score'] = match_score
        company['matched_skills'] = [s.capitalize() for s in matched_skills]
        company['missing_skills'] = [s.capitalize() for s in missing_skills]
        
        # Recommendation Logic
        if match_score >= 80:
            company['recommendation'] = "Excellent fit – Apply now!"
        elif match_score >= 50:
            company['recommendation'] = f"Good fit – Consider improving: {', '.join(company['missing_skills'][:2])}"
        else:
            company['recommendation'] = f"Learning path required – focus on {', '.join(company['missing_skills'][:2])}"
            
        enriched_companies.append(company)
        
    # Sort by match score descending
    enriched_companies.sort(key=lambda x: x['match_score'], reverse=True)
    
    return render_template('companies.html', user=current_user, companies=enriched_companies)

@app.route('/api/profile/update', methods=['POST'])
@login_required
def update_profile():
    try:
        data = request.form
        # Update editable fields
        current_user.fullname = data.get('fullname', current_user.fullname)
        current_user.age = int(data.get('age', 0)) if data.get('age') else current_user.age
        current_user.gender = data.get('gender', current_user.gender)
        current_user.mobile = data.get('mobile', current_user.mobile)
        current_user.dob = data.get('dob', current_user.dob)
        
        current_user.course = data.get('course', current_user.course)
        current_user.year = data.get('year', current_user.year)
        
        # Numeric validation for marks
        try:
            current_user.marks_10th = float(data.get('marks_10th', 0)) if data.get('marks_10th') else current_user.marks_10th
            current_user.marks_inter = float(data.get('marks_inter', 0)) if data.get('marks_inter') else current_user.marks_inter
            current_user.cgpa = float(data.get('cgpa', 0)) if data.get('cgpa') else current_user.cgpa
            
            if current_user.cgpa > 10.0 or current_user.cgpa < 0:
                raise ValueError("CGPA must be between 0 and 10")
        except ValueError as ve:
            return jsonify({"status": "error", "message": str(ve)}), 400

        # Validate and save
        try:
            # Update local object
            current_user.projects = int(data.get('projects', 0)) if data.get('projects') else current_user.projects
            current_user.internships = int(data.get('internships', 0)) if data.get('internships') else current_user.internships
            current_user.certifications = int(data.get('certifications', 0)) if data.get('certifications') else current_user.certifications
            
            current_user.technical_skills = data.get('technical_skills', current_user.technical_skills)
            current_user.skill_level = data.get('skill_level', current_user.skill_level)
            current_user.career_interest = data.get('career_interest', current_user.career_interest)
            
            # Soft skills mapping
            current_user.communication = int(data.get('communication', 70))
            current_user.teamwork = int(data.get('teamwork', 70))
            current_user.problem_solving = int(data.get('problem_solving', 70))
            current_user.leadership = int(data.get('leadership', 70))

            # Save to Firebase
            update_data = current_user.to_dict()
            firebase_user_manager.update_user(current_user.student_id, update_data)
            
            return jsonify({
                "status": "success", 
                "message": "Profile updated successfully",
                "completion": current_user.get_completion_percentage()
            })
        except ValueError:
             return jsonify({"status": "error", "message": "Invalid numeric input"}), 400
             
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
@login_required
def analyze():
    try:
        data = request.json
        print("Received Data:", data)
        
        # Extract features
        name = data.get('name', 'Student')
        gpa = float(data.get('gpa', 7.0))
        projects = int(data.get('projects', 0))
        internships = int(data.get('internships', 0))
        certs = int(data.get('certifications', 0))
        
        # Skills handling: input is comma separated or list
        skills_input = data.get('skills', [])
        if isinstance(skills_input, str):
            skills_list = [s.strip() for s in skills_input.split(',') if s.strip()]
        else:
            skills_list = skills_input
            
        if not skills_list:
            # AUTO-SUGGEST skills if empty
            career_interest = data.get('career_interest', 'AI Engineer')
            skills_dict = ga.infer_skills(career_interest)
            print(f"Inferred skills for {career_interest}:", skills_dict)
        else:
            skills_dict = {s: 8 for s in skills_list} # Default high score for listed skills
        
        # Scores
        aptitude = int(data.get('aptitude', 70))
        soft_skills = int(data.get('soft_skills', 70))
        tech_skills = int(data.get('tech_skills', 70))
        
        # New Inputs for Roadmap
        pace = data.get('pace', 'Normal')
        daily_time = data.get('daily_time', 1.0) # Default 1 hour

        # 1. Predict Level
        pred_level = mm.skill_predictor.predict(gpa, projects, internships, certs)
        
        # 2. Recommend Career
        top_careers = mm.career_recommender.predict_top_n(skills_dict, n=3)
        pred_career = top_careers[0]['career'] if top_careers else "Full Stack Developer"
        
        # 3. Performance / Hireability
        hiring_prob = mm.perf_analyzer.predict_probability(aptitude, soft_skills, tech_skills, projects)
        
        # 4. Gap Analysis (with personalized roadmap settings)
        analysis_results = ga.analyze_gaps(skills_dict, pred_career, pace=pace, daily_hours=daily_time)
        
        # Standardize structure for frontend
        gaps_list = analysis_results.get("gaps", [])
        stats_dict = analysis_results.get("skill_stats", {})
        
        # 5. Government Job Recommendations (NEW)
        user_age = current_user.age or 22  # Default age if not set
        user_education = current_user.course or "Graduate"  # Default education
        government_jobs = jr.match_jobs(skills_dict, soft_skills, aptitude, user_age, user_education)
        
        response = {
            "status": "success",
            "name": name,
            "predicted_level": pred_level,
            "recommended_career": pred_career,
            "all_recommendations": top_careers,  # Multiple suggestions
            "hiring_probability": round(hiring_prob * 100, 1),
            "hiring_status": "High" if hiring_prob > 0.6 else "Needs Improvement",
            "gaps": gaps_list,
            "skill_stats": stats_dict,
            "government_jobs": government_jobs  # NEW: Skill-based job matches
        }
        
        return jsonify(response)
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/track_apply', methods=['POST'])
@login_required
def track_apply():
    try:
        data = request.json
        data['timestamp'] = datetime.utcnow().isoformat() + 'Z'
        data['user_id'] = current_user.student_id
        
        # Ensure data directory exists
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            
        tracking_file = os.path.join(data_dir, 'apply_tracking.json')
        
        events = []
        if os.path.exists(tracking_file):
            with open(tracking_file, 'r') as f:
                try:
                    events = json.load(f)
                except json.JSONDecodeError:
                    events = []
        
        events.append(data)
        
        with open(tracking_file, 'w') as f:
            json.dump(events, f, indent=2)
            
        return jsonify({"status": "success"})
    except Exception as e:
        print(f"Error checking email existence: {e}")
        return jsonify({'status': 'error', 'message': 'Internal Server Error'}), 500

@app.route('/login/google', methods=['POST'])
def google_auth():
    """
    Endpoint receives the id_token from the Google Sign-In button on the frontend.
    Verifies it, finds the user, or creates one, then logs them in.
    """
    token = request.json.get('credential')
    try:
        # Verify Token
        idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), GOOGLE_CLIENT_ID)

        user_email = idinfo['email']
        user_name = idinfo.get('name', '')
        
        # Check if user exists in Firestore
        user_data = firebase_user_manager.get_user_by_email(user_email)
        
        if not user_data:
            # For simplicity, if they authenticate with Google but don't exist in DB:
            # We can either create an account instantly or tell them to register
            return jsonify({
                'status': 'error', 
                'message': 'No account found for this Google email. Please register first.'
            }), 404
            
        # Log User In
        user_obj = User(user_data)
        login_user(user_obj)
        session['user_id'] = user_data['student_id']

        return jsonify({'status': 'success', 'redirect': '/dashboard'})

    except ValueError as e:
        print(f"Google OAuth Verification Failed: {e}")
        return jsonify({'status': 'error', 'message': 'Invalid token'}), 401
    except Exception as e:
        print(f"Google OAuth Error: {e}")
        return jsonify({'status': 'error', 'message': 'Authentication failed'}), 500


@app.route('/analytics')
@login_required
def analytics():
    try:
        tracking_file = os.path.join(data_dir, 'apply_tracking.json')
        if not os.path.exists(tracking_file):
            return jsonify({
                "top_companies": [],
                "top_skills_applied": [],
                "job_type_distribution": {}
            })
            
        with open(tracking_file, 'r') as f:
            events = json.load(f)
            
        company_counts = {}
        skill_counts = {}
        job_type_counts = {"fresher": 0, "internship": 0, "experienced": 0}
        
        for event in events:
            comp = event.get('company_name')
            if comp:
                company_counts[comp] = company_counts.get(comp, 0) + 1
            
            job_type = str(event.get('job_type', '')).lower()
            if job_type in job_type_counts:
                job_type_counts[job_type] += 1
                
            skills = event.get('user_skills', [])
            if isinstance(skills, str):
                skills = [s.strip() for s in skills.split(',') if s.strip()]
            
            for s in skills:
                skill_counts[s] = skill_counts.get(s, 0) + 1
                
        top_companies = sorted(company_counts, key=company_counts.get, reverse=True)[:5]
        top_skills = [s.capitalize() for s in sorted(skill_counts, key=skill_counts.get, reverse=True)[:5]]
        
        total_clicks = len(events)
        job_dist = {k: f"{int((v/total_clicks)*100)}%" if total_clicks > 0 else "0%" for k, v in job_type_counts.items()}
        
        # --- PERSONALIZED INDUSTRY PROBABILITY ---
        user_skills = [s.strip().lower() for s in (current_user.technical_skills or "").split(',') if s.strip()]
        industry_scores = {}
        industry_counts = {}
        
        for comp in COMPANY_DATA:
            ind = comp.get('industry', 'Other')
            req_skills = [s.lower() for s in comp.get('skills_required', [])]
            
            if not req_skills:
                m_score = 0
            else:
                m_skills = [s for s in req_skills if any(us in s or s in us for us in user_skills)]
                m_score = (len(m_skills) / len(req_skills)) * 100
            
            industry_scores[ind] = industry_scores.get(ind, 0) + m_score
            industry_counts[ind] = industry_counts.get(ind, 0) + 1
            
        industry_probabilities = []
        for ind in industry_scores:
            avg_score = industry_scores[ind] / industry_counts[ind]
            # Add some randomness or weights if needed, but average match is a good proxy
            industry_probabilities.append({
                "name": ind,
                "score": int(avg_score)
            })
            
        # Sort by score descending
        industry_probabilities.sort(key=lambda x: x['score'], reverse=True)
        # Take top 5 or 6
        industry_probabilities = industry_probabilities[:6]

        return render_template('analytics.html', 
                               companies=top_companies, 
                               skills=top_skills, 
                               distribution=job_dist,
                               total_applications=total_clicks,
                               industry_chances=industry_probabilities)
    except Exception as e:
        print(f"Analytics error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
