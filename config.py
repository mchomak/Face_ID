import os
# место для хранения необходимых данных

Dir=os.getcwd()

Path={
    "data":os.path.join(Dir, "data"),
    "video":os.path.join(Dir, "data", "videos"),
    "image":os.path.join(Dir, "data", "images"),
    "models":os.path.join(Dir, "models"),
    "encod":os.path.join(Dir, "encodings"),
    "test":os.path.join(Dir, "data", "images","test"),
    "haar_face":os.path.join(Dir, "models", "haarcascade_frontalface_default.xml"),
}
