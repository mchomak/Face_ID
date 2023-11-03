import face_recognition
import tools
from config import Path
import pickle
import cv2
import time, os


def detect_person_in_video():
    data=[]
    encodings=os.listdir(Path["encod"])
    video = cv2.VideoCapture(f"{Path['video']}\\Sergey_Frolov\\video.mp4")
    print(encodings)
    for encod in encodings:
        data.append(pickle.loads(open(f'{Path["encod"]}\\{encod}', "rb").read()))

    while True:
        ret, image = video.read()
        if ret:
            locations = tools.face_detection(image, model="loc")
            encodings = face_recognition.face_encodings(image, locations)

            for face_encoding, face_location in zip(encodings, locations):
                for encod in data:
                    result = face_recognition.compare_faces(encod["encodings"], face_encoding, tolerance=0.5)
                    if True in result:
                        match = encod["name"]
                        break

                left_top = (face_location[3], face_location[0])
                right_bottom = (face_location[1], face_location[2])
                color = [0, 255, 0]
                cv2.rectangle(image, left_top, right_bottom, color, 4)

                left_bottom = (face_location[3], face_location[2])
                right_bottom = (face_location[1], face_location[2] + 20)
                cv2.rectangle(image, left_bottom, right_bottom, color, cv2.FILLED)
                cv2.putText(image, match,
                    (face_location[3] + 10, face_location[2] + 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 4)

            cv2.imshow("detect_person_in_video is running", image)

            k = cv2.waitKey(20)
            if k == ord("q"):
                print("Q pressed, closing the app")
                break


detect_person_in_video()