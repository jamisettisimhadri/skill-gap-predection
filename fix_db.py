import sqlite3
import os

db_path = r'c:\Users\simha\skill_gap_predictor\data\database.db'

if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Check if column exists first
    cursor.execute("PRAGMA table_info(users)")
    columns = [row[1] for row in cursor.fetchall()]
    
    if 'updated_at' not in columns:
        cursor.execute('ALTER TABLE users ADD COLUMN updated_at DATETIME')
        conn.commit()
        print("Column 'updated_at' added successfully.")
    else:
        print("Column 'updated_at' already exists.")
        
except Exception as e:
    print(f"Error: {e}")
finally:
    conn.close()
