
try:
    import flask
    import pandas
    import numpy
    import sklearn
    import joblib
    import firebase_admin
    import flask_login
    print("All imports successful")
except Exception as e:
    print(f"Import failed: {e}")
