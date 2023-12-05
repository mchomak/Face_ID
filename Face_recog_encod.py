import face_recognition
import tools
from config import Path
import pickle
import cv2
import time, os, sys
from datetime import datetime


# в среднем 100 милисекунд на кадр то есть 10 кадров в секунду
# количесвто пользователей в общем не влияет на скорость обрабоки
# 14 кодировок- 26821.824ms (26 сек)
# 1 кодировка- 26699.574ms (26 сек)
# разница составила 122 милисекунды


def load_encodings():
    """
    Возвращает массив с найденными кодировками пользователей
    """
    data=[]
    encodings=os.listdir(Path["encod"])
    print(f"[INFO] Found encodings: {len(encodings)}")
    for encod in encodings:
        if ".pickle" in encod:
            data.append(pickle.loads(open(f'{Path["encod"]}\\{encod}', "rb").read()))
        else:
            print(f"[ERROR] '{encod}' not encoding")
    return data
    

def image_processing(image, face_location, username):
    left_top = (face_location[3], face_location[0])
    right_bottom = (face_location[1], face_location[2])
    color = [0, 255, 0]
    cv2.rectangle(image, left_top, right_bottom, color, 4)

    left_bottom = (face_location[3], face_location[2])
    right_bottom = (face_location[1], face_location[2] + 20)
    cv2.rectangle(image, left_bottom, right_bottom, color, cv2.FILLED)
    cv2.putText(image, username,
        (face_location[3] + 10, face_location[2] + 15),
        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 4)

    return image


def detect_person_in_video(name=None, tolerance=0.5, mode="camera", video_num=-1):
    """
    Detects  the user on the video and saves the result
    Input: 
        name: (str) the name of the user on the video 
        tolerance: (float) recognition threshold
        video_num: (int/str) number of video
        mode: (str) "video"--тогда идет оработка видео, "camera"--идет захват изображения с камеры
    Return:
        f_a, f_d, f_r, f_s: 
        frame_all, frame_detect, frame_ricognise, frame_sucsefull
        Save the video with the found face and username signature
        Save the report of file processing
    """
    data=load_encodings()

    if mode=="camera":
        cam = cv2.VideoCapture(0)
        print(f"[INFO] Start camera processing")

        while True:
            ret, image = cam.read()
            if ret:
                locations = tools.face_detection(image, model="loc")
                encodings = face_recognition.face_encodings(image, locations)

                for face_encoding, face_location in zip(encodings, locations):
                    username="???" 
                    for encod in data:
                        result = face_recognition.compare_faces(encod["encodings"], face_encoding, tolerance=tolerance)
                        if True in result:
                            username = encod["name"]
                            print(f"[INFO] пользователь {username} был замечен на камере")
                            image=image_processing(image=image, face_location=face_location, username=username)
                            rep_path=os.path.join(Path["cam_rep"], "Camera_report.txt")
                            with open(rep_path, "a") as file:
                                file.write(f"{username} \n")
                            break
                
            #     cv2.imshow("Detect_person_in_video is running", image)
            
            # if cv2.waitKey(1) & 0xFF == ord('q'): 
            #     break


    elif mode=="video":
        video_num=str(video_num)
        f_a, f_d, f_r, f_s=0,0,0,0
        print(f"[INFO] Now processing user: {name}, video number: {video_num}")
        vid_path=tools.find_file(name, video_num)

        if vid_path!=False:
            video = cv2.VideoCapture(vid_path)
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            output_path=os.path.join(Path["result"], f'{name}{video_num}.avi')
            out = cv2.VideoWriter(output_path, fourcc, 20.0, (384,384))   
            print(f"[INFO] Start video processing")

            while True:
                ret, image = video.read()
                if ret:
                    locations = tools.face_detection(image, model="loc")
                    encodings = face_recognition.face_encodings(image, locations)
                    username="???" 

                    for face_encoding, face_location in zip(encodings, locations):
                        for encod in data:
                            result = face_recognition.compare_faces(encod["encodings"], face_encoding, tolerance=tolerance)
                            if True in result:
                                username = encod["name"]
                                break
                        
                        if len(locations)>0:
                            f_d+=len(locations)

                        if username!="???":
                            f_r+=1
                            
                        if username==name:
                            f_s+=1

                        image=image_processing(image=image, face_location=face_location, username=username)

                    out.write(image)
                    # cv2.imshow("Detect_person_in_video is running", image)
                else:
                    print("[INFO] Video has been successfully processed")
                    break
                # if cv2.waitKey(1) & 0xFF == ord('q'):
                #     break 
                f_a+=1

            video.release()
            out.release()
            cv2.destroyAllWindows()
            return f_a, f_d, f_r, f_s
    
        print(f"[ERROR] Video not found")
        return 0, 0, 0, 0
    

    else:
        print(f"[ERROR] {mode} не существует")


def main(name):
    start = datetime.now()
    for v_num in range(1,4):
        f_a, f_d, f_r, f_s=detect_person_in_video(name=name, tolerance=0.5, mode="camera", video_num=v_num)
        if f_a!=0:
            end = datetime.now()
            td = (end - start).total_seconds() * 10**3
            tools.create_report(name, v_num, td, f_a, f_d, f_r, f_s)
            print(f"[INFO] The processing time was: {td:.03f}ms \n")

    
if __name__ == '__main__':
    files=os.listdir(Path["video"])
    for file in files:
        main(file)  