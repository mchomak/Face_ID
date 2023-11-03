import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

path=os.getcwd()
name="Mikhail_Kobozev/3.jpg"
ImgPath=f"./data/images/"
VidPath=f"./data/videos/"
haar_face_path=os.path.join(path, "models", "haarcascade_frontalface_default.xml")


def rescale_img(img,scale=0.75):
    width=int(img.shape[1]*scale)
    height=int(img.shape[0]*scale)
    dimensions=(width,height)

    return cv2.resize(img, dimensions, interpolation=cv2.INTER_AREA)


def reading_video(video_path=0):
    # Если передать значение 0, то будет считываться изображение с камеры
    capture=cv2.VideoCapture(video_path)

    while True:
        isTrue, frame=capture.read()
        if isTrue:
            # "Video" - название окна, frame - то что нужно вывести на экран
            cv2.imshow("Video",frame)
        
        # если нажать кнопку d то прерветься показ видео
        if cv2.waitKey(20) & 0xFF==ord("d"):
            break

    capture.release()
    cv2.destroyAllWindows()
    

def reading_img(img_path):
    img=cv2.imread(img_path)
    # "Man" - название окна, img - то что нужно вывести на экран
    cv2.imshow("Man",img)
    # бесконечное ожидание нажатия любой кнопки, после нажатия окно уничтожиться
    cv2.waitKey(0)


def paint_img():
    # все картинки являются массивом пикселей
    # поэтому с помощью numpy мы можем создать пустое изображение просто заполнив массив нулями
    blank=np.zeros((500,500,3), dtype="uint8")

    # blank[:] для выбора всех пикселей изображения
    blank[:]=255,255,255
    blank[200:300,200:300]=0,255,0

    # рисование прямоугольника функцией
    # (0,0)-пиксель начала, (250,250)-пиксель конца, thickness-толщина, thickness=-1 -заливка прямоголника цветом
    cv2.rectangle(blank, (200,200), (300,300), (0,0,255), thickness=3)

    # кружок
    cv2.circle(blank,(blank.shape[1]//2, blank.shape[0]//2),radius=70,color=(255,0,0),thickness=3 )

    # линия
    cv2.line(blank, (100,250), (blank.shape[1]//2, blank.shape[0]//2), (0,0,0), thickness=2)

    # добавим текста
    cv2.putText(blank, "Hello", (100,100), cv2.FONT_HERSHEY_COMPLEX, thickness=2, color=(0,0,0), fontScale=1)


    cv2.imshow("blank",blank)
    cv2.waitKey(0)


def gray_img(img):
    img=cv2.imread(img)
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # размытие по гауссу
    blur=cv2.GaussianBlur(img, (5,5), cv2.BORDER_DEFAULT)

    # ищем края изображения
    canny=cv2.Canny(img, 125, 175)

    
    dilated=cv2.dilate(canny, (7,7), iterations=3)

    eroded=cv2.erode(dilated, (7,7), iterations=3)

    # изменение размера, если уменьшаем INTER_AREA, если увеличиваем INTER_CUBIC
    resized=cv2.resize(img, (500,500), interpolation=cv2.INTER_AREA)

    # обрезка 
    cropped=img[100:400, 50:500]

    cv2.imshow("cropped",cropped)
    cv2.waitKey(0)


def contours_img(img):
    img=cv2.imread(img)
    blank=np.zeros(img.shape, dtype="uint8")

    gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # # 1-ый вариант через блюр и кенни
    # blur=cv2.GaussianBlur(gray, (5,5), cv2.BORDER_DEFAULT)

    # canny=cv2.Canny(blur,125,175)

    # 2-ой вариант через треш и инверсию цвета
    ret, tresh=cv2.threshold(gray, 125, 255, cv2.THRESH_BINARY)
    
    # возвращает все координаты контуров и их иерархию
    contours, hierarchies=cv2.findContours(tresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    print(len(contours))

    # рисуем контуры на пустом поле
    cv2.drawContours(blank, contours, -1, (0,0,255), 1)

    cv2.imshow("tresh",tresh)
    cv2.imshow("blank",blank)
    cv2.waitKey(0)


def colors_img(img):
    img=cv2.imread(img)
    
    # BGR to HSV
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    # BGR to L*a*b
    lab=cv2.cvtColor(img,cv2.COLOR_BGR2LAB)

    # другие библиотеки не знают что изображение в BGR поэтому инвертируют его
    plt.imshow(img)
    plt.show()

    # BGR to RGB
    rgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    # HSV to BGR
    hsv_bgr=cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    cv2.imshow("img",hsv_bgr)
    cv2.waitKey(0)


def colors_channels_img(img):
    img=cv2.imread(img)
    
    blank=np.zeros(img.shape[:2], dtype="uint8")

    # разделение картинки на цветовые каналы, чем белее область тем больше там данного цвета
    # каждая из картинок является матрицей 2 на 2, поскольку там только один канал
    b, g, r=cv2.split(img)

    blue=cv2.merge([b,blank,blank])
    green=cv2.merge([blank,g,blank])
    red=cv2.merge([blank,blank,r])

    cv2.imshow("blue",blue)
    cv2.imshow("green",green)    
    cv2.imshow("red",red)

    # объеденение каналов
    sumed=cv2.merge([b,g,r])

    cv2.imshow("img",sumed)
    cv2.waitKey(0)


def massking(img):
    img=cv2.imread(img)
    blank=np.zeros(img.shape[:2], dtype="uint8")


    mask =cv2.circle(blank, (img.shape[1]//2, img.shape[0]//2), 100, 255, -1)

    masked=cv2.bitwise_and(img, img, mask=mask)

    cv2.imshow("blank", masked)
    cv2.waitKey(0)


def binarizing_img(img):
    img=cv2.imread(img)

    gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # черно-белая картинка
    threshold, thresh=cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    
    #инвертированная черно-белая картинка
    threshold, thresh_inv=cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)

    # адаптивное инвертирование
    adaptive_thresh=cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 11)

    cv2.imshow("thresh", adaptive_thresh)
    cv2.waitKey(0)


def edge_detection(img):
    img=cv2.imread(img)

    gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    lap=cv2.Laplacian(gray, cv2.CV_64F)
    lap=np.uint8(np.absolute(lap))

    sobelx=cv2.Sobel(gray, cv2.CV_64F, 1, 0)
    sobely=cv2.Sobel(gray, cv2.CV_64F, 0, 1)
    combined_sobel=cv2.bitwise_or(sobelx, sobely)

    canny=cv2.Canny(gray,150, 175)

    cv2.imshow("thresh", canny)
    cv2.waitKey(0)


def face_detection(img):
    img=cv2.imread(img)

    gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    haar_cascade=cv2.CascadeClassifier(haar_face_path)

    faces_rect=haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6)

    for (x,y,w,h) in faces_rect:
        cv2.rectangle(img, (x,y), (x+w, y+h), (0,255, 0), thickness=2)

    cv2.imshow("img", img)
    cv2.waitKey(0)

face_detection(ImgPath+name)