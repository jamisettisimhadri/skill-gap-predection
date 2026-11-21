import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from firebase_db import firebase_user_manager

print("Deleting ALL users from Firestore...")
users = firebase_user_manager.users_ref.stream()

count = 0
for user in users:
    print(f"Deleting user: {user.id}")
    firebase_user_manager.delete_user(user.id)
    count += 1

print(f"\nDeleted {count} users.")
