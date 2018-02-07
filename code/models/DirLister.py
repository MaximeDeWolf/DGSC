import os
import sys
import glob

def listDirectory(path, filterFunction = lambda x : True):
    files = glob.glob(path, recursive=True)
    return listFilter(files, filterFunction)

def listFilter(collection, filterFunction):
    newList = []
    for elem in collection:
        if filterFunction(elem):
            newList.append(elem)
    return newList

if __name__ == '__main__':
    print(listDirectory(sys.argv[1], lambda x : '.json' not in x ))
