import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cred = credentials.Certificate(os.path.join(BASE_DIR, "SecretKey.json"))

firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendancerealtime-6bb54-default-rtdb.firebaseio.com/"
})

def download_attendance():
    ref = db.reference('Students')
    students_data = ref.get()

    if not students_data:
        print("No attendance data found!")
        return

    data_list = []
    for student_id, student_info in students_data.items():
        data_list.append([student_id, student_info['name'], student_info['total_attendance']])

    df = pd.DataFrame(data_list, columns=['Student ID', 'Name', 'Total Attendance'])

    # Save to Excel
    file_path = os.path.join(BASE_DIR, 'attendance_report.xlsx')
    df.to_excel(file_path, index=False)
    print(f"✅ Attendance report saved as: {file_path}")


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/background.png')

# Importing the mode images into a list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = [cv2.imread(os.path.join(folderModePath, path)) for path in modePathList]

# Load the encoding file
print("Loading Encode File ...")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
print("Encode File Loaded")

modeType = 0
counter = 0
id = -1
imgStudent = []

# Start capturing video
cap = cv2.VideoCapture(0)  # Change 0 to 1 or 2 if needed
success, img = cap.read()

# Debugging Check
if not success or img is None:
    print("Error: Image not loaded. Check the camera index or file path.")
    cap.release()
    exit()

# Resize image for faster processing
imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

while True:
    success, img = cap.read()

    if not success or img is None:
        print("Error: Failed to read frame from camera.")
        break

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

            if len(faceDis) > 0:
                matchIndex = np.argmin(faceDis)  
                if matches[matchIndex]:
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                    imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                    print("✅ Known Face Detected!")
                    id = studentIds[matchIndex]

                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                    cv2.imshow("Face Attendance", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

        if counter != 0:
            if counter == 1:
                studentInfo = db.reference(f'Students/{id}').get()
                print(studentInfo)

                # Check if attendance is already taken today
                last_attendance_date = studentInfo.get('last_attendance_date', '')
                current_date = datetime.now().strftime("%Y-%m-%d")  # Get today's date

                if last_attendance_date == current_date:
                    # Attendance already marked today
                    print(f"✅ Attendance already marked for {studentInfo['name']} today.")
                    modeType = 3
                    counter = 0
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
                else:
                    # Update total attendance if not already marked today
                    datetimeObject = datetime.strptime(studentInfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
                    secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                    print(f"Seconds elapsed: {secondsElapsed}")

                    if secondsElapsed > 30:  # Check if enough time has passed to mark attendance again
                        studentInfo['total_attendance'] += 1
                        db.reference(f'Students/{id}').update({
                            'total_attendance': studentInfo['total_attendance'],
                            'last_attendance_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'last_attendance_date': current_date  # Update the attendance date
                        })
                        print(f"✅ Attendance updated for {studentInfo['name']}")

                        # Fetch and print updated data
                        updated_data = db.reference(f'Students/{id}').get()
                        print(f"📌 Updated Firebase Data: {updated_data}")

                    modeType = 2

            if modeType != 3:
                if 10 < counter < 20:
                    modeType = 2

                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if counter <= 10:
                    studentInfo = db.reference(f'Students/{id}').get()
                    if modeType !=3:
                        cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861, 125),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                        cv2.putText(imgBackground, str(studentInfo['major']), (1006, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)                
                        cv2.putText(imgBackground, str(id), (1006, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                        cv2.putText(imgBackground, str(studentInfo['grade']), (910, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                        cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                        cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                        (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                        offset = (414 - w) // 2
                        cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                    counter += 1
                    if counter >= 20:
                        counter = 0
                        modeType = 0
                        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
        else:
            modeType = 0
            counter = 0

    cv2.imshow("Face Attendance", imgBackground)
    
    key = cv2.waitKey(1)  # Capture key press
    if key == ord('d'):  # Press 'd' to download attendance
        print("📥 Downloading attendance report...")
        download_attendance()
    elif key == 27 or key == ord('q'):  # ESC or 'q' to exit
        print("Exiting loop...")
        break

cap.release()
cv2.destroyAllWindows()
