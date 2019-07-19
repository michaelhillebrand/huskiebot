import os
from os.path import abspath, join, dirname, exists

BASE_PATH = dirname(dirname(abspath(__file__)))
MEDIA_PATH = join(BASE_PATH, 'media/')
if not exists(MEDIA_PATH):
    os.makedirs(MEDIA_PATH)
