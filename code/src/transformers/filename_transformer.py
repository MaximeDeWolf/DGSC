import os

def getFilename(filepath):
    """Get the name of a file (without its extension) based on its filepath.
    """
    filename = filepath.split(os.sep)[-1]
    return filename.split('.')[0]
