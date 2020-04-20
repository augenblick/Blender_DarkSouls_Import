# helper functions for opening *.bnd files and extracting .flver and .tpf offsets

import struct
import os


def get_numberOfFiles(filePath):
    return readInt(filePath, 16)


def readInt(filePath, offset):
    fmt = "I"
    with open(filePath, 'rb') as intFile:
        intFile.seek(offset)
        integer = struct.unpack(fmt, intFile.read(4))[0]
    return integer


def get_directoryList(filePath):
    directoryfmt = "IIIIII"
    directoryList = []
    numberOfFiles = get_numberOfFiles(filePath)

    with open(filePath, 'rb') as bnd_file:
        bnd_file.seek(32)  # start of files index
        for n in range(numberOfFiles):
            thisDirectoryListing = struct.unpack(directoryfmt, bnd_file.read(24))
            directoryList.append(thisDirectoryListing)
            # print(thisDirectoryListing)
    return directoryList


def get_filePathOffsetsList(filePath):
    offsetsList = []
    directoryList = get_directoryList(filePath)
    numberOfFiles = get_numberOfFiles(filePath)

    filePathEndsList = []
    for i in range(1, len(directoryList)):
        filePathEndsList.append(directoryList[i][4])
    filePathEndsList.append(readInt(filePath, 20))

    filePathOffsetsList = []
    for directoryListing in range(len(directoryList)):
        thisFilePathOffset = (directoryList[directoryListing][4] - 1, filePathEndsList[directoryListing] - 1)
        filePathOffsetsList.append(thisFilePathOffset)
    return filePathOffsetsList


def get_filePath(BNDfilePath, pathStart, pathEnd):
    with open(BNDfilePath, 'rb') as bnd_file:
        lengthOfFileName = pathEnd - pathStart
        bnd_file.seek(pathStart)
        fullFilePath = bnd_file.read(lengthOfFileName)
        return fullFilePath


def get_flverDataOffsets(filePath):
    flverDataOffsetList = []
    offSetsList = get_filePathOffsetsList(filePath)
    for fileNum in range(get_numberOfFiles(filePath)):
        thisFilePath = get_filePath(filePath, offSetsList[fileNum][0], offSetsList[fileNum][1])
        if isFlver(thisFilePath):
            flverDataOffsetList.append(get_directoryList(filePath)[fileNum][2])
    return flverDataOffsetList


def get_tpfDataOffsets(filePath):
    tpfDataOffsetList = []
    offSetsList = get_filePathOffsetsList(filePath)
    for fileNum in range(get_numberOfFiles(filePath)):
        thisFilePath = get_filePath(filePath, offSetsList[fileNum][0], offSetsList[fileNum][1])
        if isTPF(thisFilePath):
            tpfDataOffsetList.append(get_directoryList(filePath)[fileNum][2])
    return tpfDataOffsetList


def isFlver(filePath):
    fileName = os.path.split(filePath)[1]
    fileExtension = os.path.splitext(fileName)[1]
    if fileExtension == b'.flver':
        return True
    else:
        return False


def isTPF(filePath):
    fileName = os.path.split(filePath)[1]
    fileExtension = os.path.splitext(fileName)[1]
    if fileExtension == b'.tpf':
        return True
    else:
        return False
