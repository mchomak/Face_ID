import os
import pickle
import sys
import face_recognition
from config import Path
import tools

def train_model_by_img(file_name, user_name, im_path):
    """
    Функция создает кодировку лица человека по его фотографиям
    Input:
        file_name: (str) name of the directory that stores the user's photos
        user_name: (str) name of the user 
    Return:
        (str) Program operation result (error/success)
        save ("nsme"_encodings.pickle) file 
    """

    if not os.path.exists("data"):
        print("[ERROR] there is no directory 'dataset'")
        sys.exit()

    known_encodings = []
    images = os.listdir(f'{im_path}\\{file_name}')


    for(i, image) in enumerate(images):
        print(f"[+] processing img {i + 1}/{len(images)}")

        face_img = face_recognition.load_image_file(f'{im_path}\\{file_name}\\{image}')
        if len(face_recognition.face_encodings(face_img))>0:
            face_enc = face_recognition.face_encodings(face_img)[0]

            # print("Face sucseful detected")

            if len(known_encodings) == 0:
                known_encodings.append(face_enc)
            else:
                for item in range(0, len(known_encodings)):
                    result = face_recognition.compare_faces([face_enc], known_encodings[item])

                    if result[0]:
                        known_encodings.append(face_enc)
                    break
        
        else:
            print("[ERROR] Face didnt detected")

    # print(f"Length {len(known_encodings)}")

    data = {
        "name": user_name,
        "encodings": known_encodings
    }

    with open(f'{Path["encod"]}\\{file_name}_encodings.pickle', "wb") as file:
        file.write(pickle.dumps(data))

    return f"[INFO] File {file_name}_encodings.pickle successfully created"


def main(user_count=1, mode="photo", file_name=None, user_name=None):
    """
    Input:
        user_count: (int) количество пользователей, которое должно быть обработано, 1 или all (все)
        mode: (str) "photo"--работаем с фото, "video"--работаем с видео
        file_name: (str) название файла кодировки
        user_name: (str) имя пользователя, оно также будет выводится на ПО охранника
    Output:
        Создается кодировка лица пользователя    
    """

    if mode=="photo":
        i_path=Path["image"]

    elif mode=="video":
        i_path=Path["circle_image"]
    
    else:
        print(f"[INFO] {mode} Такого мода работы нет")
        sys.exit()

    if user_count==1:
        print(train_model_by_img(file_name, user_name, i_path))
        tools.remove_files(user_name, i_path)

    elif user_count=="all":
        files=os.listdir(Path["image"])
        count_user=len(files)
        print(f"[INFO] Total number of users {count_user}")

        ready_user=0
        for file in files:
            print(f"[INFO] Now processing user: {file}")
            print(train_model_by_img(file, user_name, i_path))
            tools.remove_files(user_name, i_path)
            ready_user+=1
            left=round((count_user-ready_user)*100/count_user)
            print(f"[INFO] {left}% left \n")


if __name__ == '__main__':
    main(1, "video", "Kaneeva_Evelina", "Kaneeva_Evelina")