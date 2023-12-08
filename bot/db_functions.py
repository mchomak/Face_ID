import os
import shutil
import sqlite3
from os import listdir
from config import Path

db_path = "db_bot"


def delete_user(user_id):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("DELETE FROM main WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()


def get_names():
    encodings_path = Path['encod']
    onlyfiles = [f for f in listdir(encodings_path)]
    return list(map(lambda x: x.replace("_encodings.pickle", ""), onlyfiles))


# проверяет есть ли пользователь в БД
def check_name(name, user_id):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('SELECT user_id FROM main;')
    res = cur.fetchall()
    res = list(map(lambda x: x[0], res))
    print(user_id, res)
    if user_id in res:
        return True
    cur.execute("INSERT INTO main VALUES(?, ?);", (user_id, name))
    conn.commit()
    conn.close()


# возращает имя из БД по id
def get_user_name(user_id):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('SELECT user_name FROM main WHERE user_id = ?', (user_id,))
    name = cur.fetchone()
    conn.close()
    return name[0]


# возращает фото из БД по id
def get_photo(user_id):
    name = get_user_name(user_id)
    encodings_path = Path["image"]
    onlyfiles = [f for f in listdir(encodings_path)]
    print(onlyfiles)
    if name in onlyfiles and len(listdir(encodings_path + '/' + name)):
        return f"{Path['image']}/{name}/{listdir(encodings_path + '/' + name)[0]}"
    return False


def get_circle_photo(user_id):
    name = get_user_name(user_id)
    encodings_path = Path['circle_image']
    onlyfiles = [f for f in listdir(encodings_path)]
    if name in onlyfiles:
        return f"{Path['circle_image']}/{name}/{listdir(encodings_path + '/' + name)[0]}"
    return False


# удаляет фото и видео
def delete_photo(user_id):
    name = get_user_name(user_id)
    dirs = [Path['circle_image'], Path['image'], Path['video']]
    try:
        for dir in dirs:
            list_d = listdir(dir)
            if name in list_d:
                list_file = listdir(f'{dir}/{name}')
                for f in list_file:
                    os.remove(f'{dir}/{name}/{f}')
        return True
    except Exception as e:
        print(e)
        return False


def delete_dirs(user_id):
    name = get_user_name(user_id)
    dirs = [Path['circle_image'], Path['image'], Path['video']]
    try:
        for dir in dirs:
            list_d = listdir(dir)
            if name in list_d:
                shutil.rmtree(f"{dir}/{name}")
        delete_user(user_id)
        os.remove(Path['encod'] + '/' + name + '_encodings.pickle')
        return True
    except Exception as e:
        print(e)
        return False


# изменение фото
def change_photo(user_id, photo):
    delete_photo(user_id)
    return True


# создание папок в data
def make_dirs(name):
    dirs = [Path['circle_image'], Path['image'], Path['video']]
    for dir in dirs:
        list_d = listdir(dir)
        if name not in list_d:
            os.makedirs(dir + '/' + name)


# получение кол-ва видео в папке
def get_num_videos(name):
    list_d = listdir(Path['circle_image'] + '/' + name)
    return len(list_d)


def get_num_photos(name):
    list_d = listdir(Path['image'] + '/' + name)
    return len(list_d)


if __name__ == '__main__':
    delete_photo(1267141705)
    make_dirs('Makar_Averkin')
