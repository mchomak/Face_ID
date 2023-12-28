import os
import cv2
from config import Path
import tools


def video_2_photo(user_name, i_path, video_num=1, koef=5):
    """
    Эта функция смотрит видео по кадрам и сохраняет определенный из них
    Input:
        user_name: (str) имя пользователя видео которого надо обработать
        i_path: (str) абсолютный путь до папки, в которую надо сохранять фото
        koef: (int) коэффициент сохранения, чем выше тем меньше кадров сохраняется
        video_num: (int) number of video in dir
    Output:
        Save the video frames
    """
    user_path=os.path.join(i_path,user_name)
    video_path=tools.find_file(user_name, video_num)
    if video_path!=False:
        capture=cv2.VideoCapture(video_path)
        tools.check_dir(user_name, i_path)

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
        os.remove(video_path)
        print(f"[INFO] Видео {video_path} было удалено")


def main(user_name, ImgPath):
    tools.remove_files(user_name, ImgPath)
    video_2_photo(user_name, ImgPath)
    
if __name__ == '__main__':
    main("Kaneeva_Evelina", Path["circle_image"])