import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cred = credentials.Certificate(os.path.join(BASE_DIR, "SecretKey.json"))

firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendancerealtime-6bb54-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')

data = {
    "035298":
    {
        "name": "Tashvi Aggarwal",
        "major": "BCA",
        "starting_year": 2023,
        "total_attendance": 15,
        "last_attendance_date": "2025-02-15",
        "grade": "G",
        "year": 3,
        "last_attendance_time": "2025-02-15 01:55:44"
    },
    "049298":
    {
        "name": "Aashi Mathur",
        "major": "BCA",
        "starting_year": 2023,
        "total_attendance": 11,
        "last_attendance_date": "2025-02-02",
        "grade": "G",
        "year": 3,
        "last_attendance_time": "2025-02-02 00:44:24"
    },
    "018298":
    {
        "name": "Priyanshi Kohli",
        "major": "BCA",
        "starting_year": 2023,
        "total_attendance": 4,
        "last_attendance_date": "2025-04-01",
        "grade": "B",
        "year": 3,
        "last_attendance_time": "2025-03-28 00:44:24"
    },
    "011298":
    {
        "name": "Khushi Aggarwal",
        "major": "Pol Sc",
        "starting_year": 2024,
        "total_attendance": 1,
        "last_attendance_date": "2025-04-01",
        "grade": "C",
        "year": 1,
        "last_attendance_time": "2025-03-28 00:44:24"
    },
    "090298":
    {
        "name": "Kashvi Mittal",
        "major": "BBA",
        "starting_year": 2023,
        "total_attendance": 0,
        "last_attendance_date": "2025-04-01",
        "grade": "D",
        "year": 2,
        "last_attendance_time": "2025-01-28 00:44:24"
    },
    "032298":
    {
        "name": "Piyush Diwan",
        "major": "BCA",
        "starting_year": 2024,
        "total_attendance": 0,
        "last_attendance_date": "2025-02-02",
        "grade": "C",
        "year": 1,
        "last_attendance_time": "2025-02-02 00:44:24"
    },
    "016298":
    {
        "name": "hriday Chabbra",
        "major": "BCA",
        "starting_year": 2024,
        "total_attendance": 20,
        "last_attendance_date": "2025-02-02",
        "grade": "C",
        "year": 1,
        "last_attendance_time": "2025-02-02 00:44:24"
    },
}
for key,value in data.items():
    ref.child(key).set(value)
