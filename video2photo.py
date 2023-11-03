import os
import cv2
import tensorflow as tf

ImgPath=f"./data/images/"
VidPath=f"./data/videos/"


def remove_files(class_name,name):
    """
    Эта функция удаляет не нужные данные

        path: абсолютный пусть к папке с данными
        name: часть названия файла, который нужно удалить
    """
    class_path=os.path.join(ImgPath,class_name)
    files=os.listdir(class_path)
    delete_list=[]

    for file in files:
        if name in file:
            os.remove(f"{class_path}/{file}")
            delete_list.append(file)
    print(f"{len(delete_list)} - фотографий было удалено")
    del delete_list, files


def video_2_photo(class_name,koef=3):
    """
    Эта функция смотрит данное видио по кадрам и сохраняет определенный из них
        video_path: абсолютный пусть к видео
        koef: коэффициент сохранения, чем выше тем меньше фреймов сохраняется
    """
    class_path=os.path.join(ImgPath,class_name)
    video_path=os.path.join(VidPath,class_name,"video.mp4")
    capture=cv2.VideoCapture(video_path)
    have_dir=(class_name in  os.listdir(ImgPath))
    if have_dir==False:
        os.mkdir(class_path)
        print(f"Папка {class_name} была создана")


    num=0
    create_list=[]
    while True:
        isTrue, frame=capture.read()
        if isTrue:
            if num%koef==0:
                cv2.imwrite(f"{class_path}/video_{str(num)}.jpg",frame)
                create_list.append(f"video_{str(num)}.jpg")
            num+=1
        
        else:
            print(f"{len(create_list)} - было создано файлов")
            break
    
    capture.release()
    cv2.destroyAllWindows()


class_name="Sergey_Frolov"
remove_files(class_name,"video_")
video_2_photo(class_name)