import os

def getFilename(filepath):
    filename = filepath.split(os.sep)[-1]
    return filename.split('.')[0]
