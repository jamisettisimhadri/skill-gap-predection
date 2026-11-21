import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from firebase_db import firebase_user_manager

print("Listing all users in Firestore...")
users = firebase_user_manager.users_ref.stream()

count = 0
for user in users:
    data = user.to_dict()
    print(f"ID: {user.id} | Email: {data.get('email')} | Name: {data.get('fullname')}")
    count += 1

print(f"\nTotal Users: {count}")
