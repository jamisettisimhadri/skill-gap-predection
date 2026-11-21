import sys
import os
from werkzeug.security import generate_password_hash, check_password_hash

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from firebase_db import firebase_user_manager
    print("Firebase User Manager imported successfully")
except Exception as e:
    print(f"Failed to import firebase_user_manager: {e}")
    sys.exit(1)

# Mock User class from app.py
class User:
    def __init__(self, user_data):
        self.id = user_data.get('student_id')
        self.student_id = user_data.get('student_id')
        self.email = user_data.get('email')
        self.password_hash = user_data.get('password_hash')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

def test_registration():
    print("\nTesting Registration Logic...")
    student_id = "TEST_001"
    email = "test@example.com"
    password = "password123"
    
    try:
        # Check existence
        if firebase_user_manager.user_exists(student_id=student_id):
            print(f"User {student_id} already exists. Deleting...")
            firebase_user_manager.delete_user(student_id)
        
        user_data = {
            'student_id': student_id,
            'email': email,
            'fullname': "Test User",
            'age': 20
        }
        
        # Hashing
        temp_user = User(user_data)
        temp_user.set_password(password)
        user_data['password_hash'] = temp_user.password_hash
        print(f"Password hash generated: {user_data['password_hash'][:10]}...")
        
        # Create
        created_id = firebase_user_manager.create_user(user_data)
        print(f"User created with ID: {created_id}")
        
    except Exception as e:
        print(f"Registration Failed: {e}")
        import traceback
        traceback.print_exc()

def test_login():
    print("\nTesting Login Logic...")
    email = "test@example.com"
    password = "password123"
    
    try:
        user_data = firebase_user_manager.get_user_by_email(email)
        if not user_data:
            print("User not found by email")
            return
            
        print(f"User found: {user_data['student_id']}")
        
        if check_password_hash(user_data.get('password_hash'), password):
            print("Password check passed!")
            user = User(user_data)
            print(f"User object created: {user.id}")
        else:
            print("Password check failed!")
            
    except Exception as e:
        print(f"Login Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_registration()
    test_login()
