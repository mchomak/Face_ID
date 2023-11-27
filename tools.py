from config import Path
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import pickle
import cv2
import os
import time


def face_detection(img,model):
    """
    Face detection on img
    Input:
        img: a photo where you want to find the face
        model: cv2-with opencv, loc-with face recognition
    Output: 
        cv2-(x1, y1, x2, y2): facial boundary coordinates
        loc-(x, y, w, h): facial boundary coordinates
    """
    
    if model=="cv2":
        img=cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        haar_cascade=cv2.CascadeClassifier(Path["haar_face"])
        faces_rect=haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3)
        return faces_rect   
        # crop=img[x1:x2, y1:y2]
        # cv2.imwrite(Path["test"])
        # return faces_rect[0]


    if model=="loc":
        import face_recognition
        faces_rect = face_recognition.face_locations(img, model="mtcnn")  #("hog") обработка на CPU
        return faces_rect


if __name__ == '__main__':
    face_detection(f"{Path['image']}\\Anastasia_Khudyakova\\photo_1_2023-10-11_19-09-02.jpg", "cv2")