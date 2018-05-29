from os import listdir, unlink
from os.path import join, dirname, abspath

ALLOWED_EXTENSIONS = set(['rgb', 'gif', 'pbm', 'pgm', 'ppm', 'tiff', 'rast', 'xbm', 'jpeg', 'bmp', 'png', 'webp', 'exr', 'jpg'])


def is_allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_images(folder):
    return [('/' + join(folder, file), file.split('.')[0]) for file in listdir(folder) if is_allowed_file(file)]


def delete_images(folder):
    [unlink(dirname(abspath(file)) + '/' + join(folder, file)) for file in listdir(folder) if is_allowed_file(file)]


def get_filepath(folder, filename):
    try:
        return [join(folder, file) for file in listdir(folder) if file.split('.')[0] == filename][0]
    except Exception:
        return None


def count_folders(folder):
    return len(listdir(folder))
