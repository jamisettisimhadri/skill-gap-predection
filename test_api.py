import requests
import json

# Test the analysis API
url = "http://127.0.0.1:5000/api/analyze"
headers = {"Content-Type": "application/json"}
data = {
    "name": "Test User",
    "gpa": "7.5",
    "projects": "2",
    "internships": "1",
    "certifications": "1",
    "skills": "Python, SQL",
    "aptitude": "75",
    "soft_skills": "70",
    "tech_skills": "65"
}

try:
    response = requests.post(url, headers=headers, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")
