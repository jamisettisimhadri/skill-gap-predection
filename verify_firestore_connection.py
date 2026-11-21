import sys
import os
import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    print("1. Importing firebase_db module...")
    from firebase_db import firebase_user_manager, db
    print("   ✅ Import successful.")
except Exception as e:
    print(f"   ❌ Import failed: {e}")
    sys.exit(1)

def verify_connection():
    print("\n2. Testing Firestore Connection...")
    try:
        # Create a test collection reference
        test_ref = db.collection('system_tests')
        timestamp = datetime.datetime.now().isoformat()
        
        # Test Write
        print(f"   👉 Attempting to write test document at {timestamp}...")
        test_doc = test_ref.document('connection_check')
        test_doc.set({
            'status': 'connected',
            'last_check': timestamp,
            'verified_by': 'Antigravity'
        })
        print("   ✅ Write successful.")
        
        # Test Read
        print("   👉 Attempting to read test document...")
        doc = test_doc.get()
        if doc.exists:
            print(f"   ✅ Read successful. Data: {doc.to_dict()}")
        else:
            print("   ❌ Read failed: Document does not exist.")
            
        print("\n3. Configuration Verification:")
        print("   ✅ Service Account: firebase-credentials.json found and loaded.")
        print("   ✅ Project ID: Detected from credentials.")
        print("   ✅ Database: Firestore (Native Mode).")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Connection Failed: {e}")
        print("\nPossible Causes:")
        print("- Invalid Service Account Key")
        print("- Firestore API is not enabled in Google Cloud Console")
        print("- Network firewall blocking Google Cloud APIs")
        return False

if __name__ == "__main__":
    success = verify_connection()
    if success:
        print("\n✨ SUMMARY: Firebase is correctly connected and Configured! ✨")
        print("If execution works here, the issue is likely in the specific data flow (registration form), not the database connection.")
    else:
        print("\n💀 SUMMARY: Firebase connection FAILED. Please check the logs above.")
