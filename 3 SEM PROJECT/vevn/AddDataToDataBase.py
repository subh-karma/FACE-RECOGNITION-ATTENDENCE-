import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':'https://faceattendancerealtime-bb55f-default-rtdb.firebaseio.com/'
})

ref =db.reference('Student')

data = {
    "1":
        {
            "Name":"NAYAN KANPILE",
            "Major":"MSc.CA-1",
            "Starting_year":2022,
            "total_attendence":7,
            "standing":"G",
            "year":2,
            "last_attendance_time":"2023-12-11 00:55:34"


        },
    "2":
        {
            "Name":"RUSHI MOHITE",
            "Major":"MSc.CA-1",
            "Starting_year":2022,
            "total_attendence":5,
            "standing":"G",
            "year":2,
            "last_attendance_time":"2023-12-11 00:54:34"


        },
    "3":
        {
            "Name":"SHANTANU PANDIT",
            "Major":"MSc.CA-1",
            "Starting_year":2022,
            "total_attendence":8,
            "standing":"G",
            "year":2,
            "last_attendance_time":"2023-12-11 00:53:34"


        },
    "4":
        {
            "Name":"SHRIKANT KAILKHERE",
            "Major":"MSc.CA-1",
            "Starting_year":2022,
            "total_attendence":7,
            "standing":"G",
            "year":2,
            "last_attendance_time":"2023-12-11 00:52:34"


        },
    "5":
        {
            "Name":"VICTOR BEEMER",
            "Major":"MSc.CA-1",
            "Starting_year":2022,
            "total_attendence":7,
            "standing":"G",
            "year":2,
            "last_attendance_time":"2023-12-11 00:51:34"


        },

}

for key,value in data.items():
    ref.child(key).set(value)