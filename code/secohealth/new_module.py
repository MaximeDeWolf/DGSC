import os
SHORT_NAME = 'NM'

def removePrefix(string, prefix):
    return string.replace(prefix, "")

def filename(filepath):
    return filepath.split(os.sep)[-1]
