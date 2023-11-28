import os
import cv2
from config import Path
import tools


def remove_files(class_name, i_path, name):
    """
    Эта функция удаляет не нужные данные

        path: абсолютный пусть к папке с данными
        name: часть названия файла, который нужно удалить
    """
    class_path=os.path.join(i_path, class_name, i_path)
    if tools.check_dir(class_name, class_path, i_path):
        files=os.listdir(class_path)
        delete_list=[]
        for file in files:
            if name in file:
                os.remove(f"{class_path}/{file}")
                delete_list.append(file)
        print(f"[INFO] {len(delete_list)} - фотографий было удалено")
        del delete_list, files


def video_2_photo(user_name, i_path, video_num=1, koef=5):
    """
    Эта функция смотрит видео по кадрам и сохраняет определенный из них
        video_path: абсолютный пусть к видео
        koef: коэффициент сохранения, чем выше тем меньше фреймов сохраняется
        video_num: (int) number of video in dir
    """
    user_path=os.path.join(i_path,user_name)
    video_path=tools.find_file(user_name, video_num)
    if video_path!=False:
        capture=cv2.VideoCapture(video_path)
        tools.check_dir(user_name, user_path, i_path)

        num=0
        create_list=[]
        while True:
            isTrue, frame=capture.read()
            if isTrue:
                if num%koef==0:
                    cv2.imwrite(f"{user_path}/video_{str(num)}.jpg",frame)
                    create_list.append(f"video_{str(num)}.jpg")
                num+=1
            
            else:
                print(f"[INFO] {len(create_list)} - было создано файлов")
                break
        
        capture.release()
        cv2.destroyAllWindows()


def main(class_name):
    ImgPath=Path["circle_image"]

    remove_files(class_name, ImgPath, "video_")
    video_2_photo(class_name, ImgPath, 2, 5)


if __name__ == '__main__':
    main("Dima_Shubin")