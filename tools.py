from config import Path
import cv2
import os


def remove_files(user_name, i_path):
    """
    Эта функция удаляет не user_pathнужные данные
        user_name: (str) имя пользователя фото которого надо удалить
        user_path: (str) абсолютный путь к папке с фото пользователя
    """
    if check_dir(user_name, i_path):
        i_path=os.path.join(i_path, user_name)
        files=os.listdir(i_path)
        delete_list=[]
        for file in files:
            os.remove(os.path.join(i_path, file))
            delete_list.append(file)
        print(f"[INFO] {len(delete_list)} - фотографий было удалено")
        del delete_list, files


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


def find_file(user_name, video_num):
    """
    Searching for the right file
    Input:
        user_name: (str) имя пользователя видео которого надо обработать
        video_num: (int) number of video in dir
    Output:
        vid_path: (str) full video path
    """
    video_num=str(video_num)
    videos=os.listdir(os.path.join(Path['video'], user_name))
    vid_path=False
    for vid in videos:
        if video_num in vid:
            vid_path=os.path.join(Path['video'], user_name, vid)
            break
    
    return vid_path


def check_dir(user_name, i_path):
    """
    Checks for a directory 
    Input:
        user_name: (str) имя пользователя видео которого надо обработать
        i_path: (str) абсолютный путь до папки, где храянтся фото пользователя
    Output:
        vid_path: (str) full video path
    """
    have_dir=(user_name in  os.listdir(i_path))
    if have_dir==False:
        os.mkdir(os.path.join(i_path, user_name))
        print(f"[INFO] Папка {user_name} была создана")
        return False 
    else:
        return True


def create_report(name, v_num, time, frame_all, frame_detect, frame_ricognise, frame_sucsefull):
    """
    Create the report file with model precision and processing time
    Input:
        name: (str) the name of the user on the video
        time: (float) program runtime
    Output:
        Save the report file
    """
    with open(f"Report_{name}_{v_num}.txt", "w") as report:
        report.writelines([
            f"[INFO] Total number of frames: {frame_all} \n",
            f"[INFO] Number of frames with people: {frame_detect} \n",
            f"[INFO] Number of frames with user: {frame_ricognise} \n",
            f"[INFO] Total number of correctly processed frames: {frame_sucsefull} \n",
            f"[INFO] Number of frames with faces: {round(frame_detect/frame_all*100)}% \n",
            f"[INFO] Of these, users recognized: {round(frame_ricognise/frame_detect*100)}% \n",
            f"[INFO] Of these, users were correctly recognized: {round(frame_sucsefull/frame_ricognise*100)}% \n",
            f"[INFO] Final precision is {round(frame_sucsefull/frame_all*100)}% \n",
            f"[INFO] The processing time was: {time:.03f}ms \n",
        ])



if __name__ == '__main__':
    face_detection(f"{Path['image']}\\Anastasia_Khudyakova\\photo_1_2023-10-11_19-09-02.jpg", "cv2")