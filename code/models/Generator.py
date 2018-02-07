import sys
import FileLoader
import JsonRenderer
import DirLister

def chooseLoaderFromExtension(filename):
    print(filename[-5:])
    if filename[-5:] == '.json':
        return lambda path: FileLoader.jsonLoader(path)
    elif filename[-5:] == '.yaml':
        return lambda path: FileLoader.yamlLoader(path)

def generateFromFileList(fileList, templatePath, outputPath):
    for file_ in fileList:
        loader = chooseLoaderFromExtension(file_)
        data = loader(file_)
        content = JsonRenderer.renderContent('.', data, templatePath)
        outputFile = open(outputPath, 'a')
        outputFile.write(content + "\n\n")

def generateWithDict(fileList, nameList, templatePath, outputPath):
    dataDict = {}
    for file_, name in zip(fileList, nameList):
        loader = chooseLoaderFromExtension(file_)
        data = loader(file_)
        dataDict[name] = data
    print(dataDict)
    content = JsonRenderer.renderContent('.', dataDict, templatePath)
    outputFile = open(outputPath, 'w')
    outputFile.write(content)

if __name__ == '__main__':
    fileList = DirLister.listDirectory('res/players.*')
    nameList = ['json', 'yaml']
    templatePath = 'res/mixedTemplate.j2'
    outputPath = 'res/out.txt'
    #generateFromFileList(fileList, templatePath, outputPath)
    generateWithDict(fileList, nameList, templatePath, outputPath)
