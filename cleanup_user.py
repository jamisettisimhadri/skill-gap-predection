import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from firebase_db import firebase_user_manager

email_to_check = "raji3yoy@gmail.com"

print(f"Checking for user: {email_to_check}")
user = firebase_user_manager.get_user_by_email(email_to_check)

if user:
    print(f"User found: {user['student_id']}")
    print("Deleting user to allow re-registration...")
    firebase_user_manager.delete_user(user['student_id'])
    print("User deleted successfully.")
else:
    print("User not found.")
