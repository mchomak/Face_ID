import face_recognition
import tools
from config import Path
import pickle
import cv2
import time, os, sys
from datetime import datetime
from statistics import median

# в среднем 100 милисекунд на кадр то есть 10 кадров в секунду
# количесвто пользователей в общем не влияет на скорость обрабоки
# 14 кодировок- 26821.824ms (26 сек)
# 1 кодировка- 26699.574ms (26 сек)
# разница составила 122 милисекунды


def detect_person_in_video(name, tolerance):
    buf=[]
    """
    Detects  the user on the video and saves the result
    Input: 
        name: (str) the name of the user on the video 
        tolerance: (float) recognition threshold
    Return:
        f_a, f_d, f_r, f_s
        frame_all, frame_detect, frame_ricognise, frame_sucsefull
        Save the video with the found face and username signature
        Save the report of file processing
    """
    data=[]
    f_a, f_d, f_r, f_s=0,0,0,0
    encodings=os.listdir(Path["encod"])
    print(f"[INFO] Found encodings: {len(encodings)}")
    print(f"[INFO] Now processing user: {name}")

    video = cv2.VideoCapture(f"{Path['video']}\\{name}\\video.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output_path=os.path.join(Path["result"], f'{name}1.avi')
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (384,384))   

    for encod in encodings:
        if ".pickle" in encod:
            data.append(pickle.loads(open(f'{Path["encod"]}\\{encod}', "rb").read()))
        else:
            print(f"[ERROR] '{encod}' not encoding")
            sys.exit()

    print(f"[INFO] Start video processing")
    while True:
        ret, image = video.read()
        if ret:
            locations = tools.face_detection(image, model="loc")
            encodings = face_recognition.face_encodings(image, locations)

            if len(locations)>0:
                f_d+=len(locations)

            username="???" 
            for face_encoding, face_location in zip(encodings, locations):
                for encod in data:
                    result = face_recognition.compare_faces(encod["encodings"], face_encoding, tolerance=tolerance)
                    if True in result:
                        username = encod["name"]
                        break
                
                if username!="???":
                    f_r+=1
                    
                if username==name:
                    f_s+=1

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


def create_report(name, time, frame_all, frame_detect, frame_ricognise, frame_sucsefull):
    """
    Create the report file with model precision, processing time
    Input:
        name: (str) the name of the user on the video
        time: (float) program runtime
    """
    with open(f"Report_{name}.txt", "w") as report:
        report.writelines([
            f"[INFO] Total number of frames: {frame_all} \n",
            f"[INFO] Number of frames with people: {frame_detect} \n",
            f"[INFO] Number of frames with user: {frame_ricognise} \n",
            f"[INFO] Total number of correctly processed frames: {frame_sucsefull} \n",
            f"[INFO] Number of frames with faces: {round(frame_detect/frame_all*100)}% \n",
            f"[INFO] Of these, users recognized: {round(frame_ricognise/frame_detect*100)}% \n",
            f"[INFO] Of these, users were correctly recognized: {round(frame_sucsefull/frame_ricognise*100)}% \n",
            f"[INFO] Final precision is {round(frame_sucsefull/frame_detect*100)}% \n",
            f"[INFO] The processing time was: {time:.03f}ms \n",
        ])


def main():
    start = datetime.now()
    name="Nikita_Kholodarev"

    f_a, f_d, f_r, f_s=detect_person_in_video(name, 0.5)

    end = datetime.now()
    td = (end - start).total_seconds() * 10**3
    create_report(name, td, f_a, f_d, f_r, f_s)
    print(f"[INFO] The processing time was: {td:.03f}ms")

    
if __name__ == '__main__':
    main()