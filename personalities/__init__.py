from os.path import abspath, join, dirname

BASE_PATH = dirname(dirname(abspath(__file__)))
STATIC_PATH = join(BASE_PATH, 'static/')
IMAGES_PATH = join(BASE_PATH, 'images/')
