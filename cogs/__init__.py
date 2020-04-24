import os
from os.path import abspath, join, dirname, exists

BASE_PATH = dirname(dirname(abspath(__file__)))
MEDIA_PATH = join(BASE_PATH, 'media/')
STATIC_PATH = join(BASE_PATH, 'static/')
IMAGES_PATH = join(STATIC_PATH, 'images/')
if not exists(MEDIA_PATH):
    os.makedirs(MEDIA_PATH)
