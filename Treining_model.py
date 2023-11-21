import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
from config import Path

features=[]
labels=[]

people=os.listdir(Path["image"])
print(people)

def create_train():
    for person in people:
        path=os.path.join(Path["image"],person)
        label=people.index(person)

        for img in os.listdir(path):
            img_path=os.path.join(path, img)

            img_array=cv2.imread(img_path)
            gray=cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)

            haar_cascade=cv2.CascadeClassifier(Path["haar_face"])

            faces_rect=haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(24,24))

            for (x,y,w,h) in faces_rect:
                faces_roi=gray[y:y+h, x:x+w]

                features.append(faces_roi)
                labels.append(label)

create_train()
print("Training done ------------------")

features=np.array(features, dtype="object")
labels=np.array(labels)

face_reconizer=model = cv2.face.EigenFaceRecognizer()

print(features, labels)
face_reconizer.train(features, labels)

np.save("features.npy", features)
np.save("labels.npy", labels)