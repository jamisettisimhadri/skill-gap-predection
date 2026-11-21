import sqlite3
import os

db_path = r'c:\Users\simha\skill_gap_predictor\data\database.db'

# Define all current expected columns for the 'users' table
expected_columns = {
    'id': 'INTEGER PRIMARY KEY',
    'student_id': 'VARCHAR(50)',
    'fullname': 'VARCHAR(100)',
    'age': 'INTEGER',
    'gender': 'VARCHAR(20)',
    'email': 'VARCHAR(120)',
    'mobile': 'VARCHAR(20)',
    'dob': 'VARCHAR(20)',
    'course': 'VARCHAR(100)',
    'year': 'VARCHAR(20)',
    'marks_10th': 'FLOAT',
    'marks_inter': 'FLOAT',
    'cgpa': 'FLOAT',
    'technical_skills': 'TEXT',
    'skill_level': 'VARCHAR(50)',
    'certifications': 'INTEGER',
    'internships': 'INTEGER',
    'projects': 'INTEGER',
    'communication': 'INTEGER',
    'teamwork': 'INTEGER',
    'problem_solving': 'INTEGER',
    'leadership': 'INTEGER',
    'career_interest': 'VARCHAR(100)',
    'password_hash': 'VARCHAR(200)',
    'created_at': 'DATETIME',
    'updated_at': 'DATETIME'
}

if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.execute("PRAGMA table_info(users)")
    existing_columns = {row[1]: row[2] for row in cursor.fetchall()}
    
    for col_name, col_type in expected_columns.items():
        if col_name not in existing_columns:
            print(f"Adding missing column: {col_name} ({col_type})")
            cursor.execute(f'ALTER TABLE users ADD COLUMN {col_name} {col_type}')
            
    conn.commit()
    print("Database schema synchronization complete.")
        
except Exception as e:
    print(f"Error: {e}")
finally:
    conn.close()
