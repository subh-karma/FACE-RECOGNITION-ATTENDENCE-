import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import numpy as np
from datetime import datetime

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':'https://faceattendancerealtime-bb55f-default-rtdb.firebaseio.com/',
    'storageBucket':'faceattendancerealtime-bb55f.appspot.com'
})

bucket= storage.bucket()


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('C:/Users/Acer/Desktop/3 SEM PROJECT/Resources/final.png')

#importing the mode imgs

folderModePath='C:/Users/Acer/Desktop/3 SEM PROJECT/Resources/Modes'
modePathList=os.listdir(folderModePath)
imgModeList=[]
#print(modePathList)
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath,path)))

#print(len(imgModeList))

#load the encoing files

print("Loading Encoding File")

file=open('EncodeFile.p','rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
#print(studentIds)

print("Encode file Loaded....")

modeType = 0
counter = 0
id = -1
#imgStudent=[]

while True:
    success, img = cap.read()

    imgS=cv2.resize(img, (0,0),None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162+480,55:55+640]=img
    imgBackground[44:44 + 633, 808:808+414] = imgModeList[modeType]

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        #print("matches", matches)
        #print("faceDis", faceDis)

        matchIndex=np.argmin(faceDis)

        if matches[matchIndex]:
            #print("Known Face Detected ")
            #print(studentIds[matchIndex])
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            bbox= 55 + x1, 162 + y1, x2-x1, y2-y1

            imgBackground= cvzone.cornerRect(imgBackground, bbox, rt=0)
            id = studentIds[matchIndex]
            print(id)
            if counter ==0:
                cvzone.putTextRect(imgBackground,"Loading",(275,400))
                cv2.imshow("Face Attendance", imgBackground)
                cv2.waitKey(1)
                counter = 1
                modeType = 1

    if counter !=0:

        if counter ==1:
            studentInfo = db.reference(f'Student/{id}').get()
            print(studentInfo)
            #img storage
            #blob = bucket.get_blob(f'Images/{id}.png')
            #array=np.frombuffer(blob.download_as_string(), np.uint8)
            #imgStudent = cv2.imdecode(array,cv2.COLOR_BGRA2BGR)

            #datetimeObject=datetime.strptime(studentInfo['last_attendance_time'],
              #                           " %Y-%m-%d %H:%M:%S" )

            #secondElapsed=(datetime.now()-datetimeObject).total_seconds()

            ref= db.reference(f'Student/{id}')
            studentInfo['total_attendence'] +=1
            ref.child('total_attendence').set(studentInfo['total_attendence'] )
            #ref.child('last_attendance_time').set(datetime.now().strftime(" %Y-%m-%d %H:%M:%S"))
        if 10<counter<20:
            modeType=2

        imgBackground[44:44+633,808:808+ 414]=imgModeList[modeType]


        if counter <=10:


             cv2.putText(imgBackground,str(studentInfo['total_attendence']),(861,125),
                         cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)

             cv2.putText(imgBackground, str(studentInfo['Major']), (1006, 550),
                         cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
             cv2.putText(imgBackground, str(id), (1006, 493),
                         cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
             cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625),
                         cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
             cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625),
                         cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
             cv2.putText(imgBackground, str(studentInfo['Starting_year']), (1125, 625),
                         cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

             (w,h),_ =cv2.getTextSize(studentInfo['Name'],cv2.FONT_HERSHEY_COMPLEX,1,1)
             offset=(414-w)//2
             cv2.putText(imgBackground, str(studentInfo['Name']), (808+offset, 445),
                         cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

        #imgBackground[175:175+216,909:909+260]=imgStudent




        counter+=1

        if counter>=20:
            counter =0
            modeType=0
            studentInfo=[]
            imgStudent=[]
            imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]





    #cv2.imshow("Webcam", img)
    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)