import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import os

# Initialize Firebase Admin SDK
cred_path = os.path.join(os.path.dirname(__file__), 'firebase-credentials.json')
cred = credentials.Certificate(cred_path)

try:
    firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()

class FirebaseUserManager:
    """Manages user operations in Firebase Firestore"""
    
    def __init__(self):
        self.users_ref = db.collection('users')
    
    def create_user(self, user_data):
        """Create a new user in Firestore"""
        user_data['created_at'] = datetime.utcnow()
        user_data['updated_at'] = datetime.utcnow()
        
        # Use student_id as document ID
        doc_ref = self.users_ref.document(user_data['student_id'])
        doc_ref.set(user_data)
        return user_data['student_id']
    
    def get_user_by_id(self, student_id):
        """Get user by student ID"""
        doc = self.users_ref.document(student_id).get()
        if doc.exists:
            data = doc.to_dict()
            data['id'] = doc.id
            return data
        return None
    
    def get_user_by_email(self, email):
        """Get user by email"""
        users = self.users_ref.where('email', '==', email).limit(1).stream()
        for user in users:
            data = user.to_dict()
            data['id'] = user.id
            return data
        return None
    
    def update_user(self, student_id, update_data):
        """Update user data"""
        update_data['updated_at'] = datetime.utcnow()
        self.users_ref.document(student_id).update(update_data)
        return True
    
    def delete_user(self, student_id):
        """Delete a user"""
        self.users_ref.document(student_id).delete()
        return True
    
    def user_exists(self, student_id=None, email=None):
        """Check if user exists by student_id or email"""
        if student_id:
            return self.users_ref.document(student_id).get().exists
        if email:
            users = self.users_ref.where('email', '==', email).limit(1).stream()
            return len(list(users)) > 0
        return False

# Global instance
firebase_user_manager = FirebaseUserManager()
