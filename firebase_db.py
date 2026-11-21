
import os
from pathlib import Path
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore

BASE_DIR = Path(__file__).resolve().parent

# Render secret file location
render_cred = Path("/etc/secrets/firebase-credentials.json")

# Local development file location
local_cred = BASE_DIR / "firebase-credentials.json"

# Select available credentials
cred_path = render_cred if render_cred.exists() else local_cred

if not cred_path.exists():
    raise FileNotFoundError(
        "Firebase credentials not found. "
        "Add firebase-credentials.json to Render Secret Files."
    )

# Initialize Firebase
try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate(str(cred_path))
    firebase_admin.initialize_app(cred)

# Firestore database
db = firestore.client()


class FirebaseUserManager:
    def __init__(self):
        self.users_ref = db.collection("users")

    def create_user(self, user_data):
        user_data["created_at"] = datetime.utcnow()
        user_data["updated_at"] = datetime.utcnow()

        doc_ref = self.users_ref.document(user_data["student_id"])
        doc_ref.set(user_data)

        return user_data["student_id"]

    def get_user_by_id(self, student_id):
        doc = self.users_ref.document(student_id).get()

        if doc.exists:
            data = doc.to_dict()
            data["id"] = doc.id
            return data

        return None

    def get_user_by_email(self, email):
        users = self.users_ref.where(
            "email", "==", email
        ).limit(1).stream()

        for user in users:
            data = user.to_dict()
            data["id"] = user.id
            return data

        return None

    def update_user(self, student_id, update_data):
        update_data["updated_at"] = datetime.utcnow()

        self.users_ref.document(student_id).update(update_data)

        return True

    def delete_user(self, student_id):
        self.users_ref.document(student_id).delete()
        return True

    def user_exists(self, student_id=None, email=None):
        if student_id:
            return self.users_ref.document(student_id).get().exists

        if email:
            users = self.users_ref.where(
                "email", "==", email
            ).limit(1).stream()

            return len(list(users)) > 0

        return False


firebase_user_manager = FirebaseUserManager()
