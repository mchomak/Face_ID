import os
# место для хранения необходимых данных

Dir=os.getcwd()

Path={
    "face":os.path.join(Dir, "data", "faces"),
    "data":os.path.join(Dir, "data"),
    "video":os.path.join(Dir, "data", "videos"),
    "image":os.path.join(Dir, "data", "simple_images"),
    "circle_image":os.path.join(Dir, "data", "circle_images"),
    "models":os.path.join(Dir, "models"),
    "encod":os.path.join(Dir, "data", "encodings"),
    "test":os.path.join(Dir, "data", "test"),
    "haar_face":os.path.join(Dir, "data", "models", "haarcascade_frontalface_default.xml"),
    "result":os.path.join(Dir, "docks", "results"),
}
