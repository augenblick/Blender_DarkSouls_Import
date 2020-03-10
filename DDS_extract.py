import struct
import os


# get the number of DDS files within this TPF file
def get_DDSCount(fileName):
    with open(fileName, 'rb') as tpf_File:
        tpf_File.seek(8)
        DDSCount = struct.unpack("I", tpf_File.read(4))[0]

    return DDSCount

# collects offset and datasize info for each DDS file within this TPF file
def get_DDSInfoList(fileName):
    numDDSFiles = get_DDSCount(fileName)
    DDSInfoFormat = "IIIII"
    DDSInfoList = []
    with open(fileName, 'rb') as tpf_File:
        tpf_File.seek(16)
        for DDSFile in range(numDDSFiles):
            thisDDSInfo = struct.unpack(DDSInfoFormat, tpf_File.read(20))
            DDSInfoList.append(thisDDSInfo)

    return DDSInfoList


def get_fileNoExtension(fileNameData):
    filePath = fileNameData[0]
    fileNoPath = (os.path.split(filePath))
    fileNoExtension = os.path.splitext(fileNoPath[1])[0]
    return (fileNoExtension, fileNameData[1])


def get_tpfPath(fileName, sourceDirectory):
    fileNoExtension = get_fileNoExtension(fileName)
    tpfFileName = "{}{}.tpf".format(sourceDirectory, fileNoExtension[0])
    return (tpfFileName, fileName[1])

# extracts every DDS file within this TPF file
def write_DDSFilesFromOffsets(fileName, sourceDirectory, destination, offset):
    DDSInfoList = []
    with open(fileName, 'rb') as bnd_file:
        bnd_file.seek(8 + offset)
        numDDSFiles = struct.unpack("I", bnd_file.read(4))[0]
        if numDDSFiles > 0:

            bnd_file.seek(offset + 16)
            for DDSFile in range(numDDSFiles):
                thisDDSInfo = struct.unpack("IIIII", bnd_file.read(20))
                DDSInfoList.append(thisDDSInfo)

            # get start/end offsets for fileNames
            filePathOffsetList = []
            count = 0

            for DDS in range(len(DDSInfoList) - 1):
                thisFilePathOffset = (DDSInfoList[DDS][3] + offset, DDSInfoList[DDS + 1][3] + offset)
                filePathOffsetList.append(thisFilePathOffset)
                count += 1
            filePathOffsetList.append((DDSInfoList[count][3] + offset, DDSInfoList[count][3] + 15 + offset))

            # get filenames
            fileNamesList = []
            for nameOffset in filePathOffsetList:
                charList = []
                nameLength = nameOffset[1] - nameOffset[0] - 1
                bnd_file.seek(nameOffset[0])
                thisFileName = bnd_file.read(nameLength).decode("utf-8")
                thisFileName = thisFileName.rstrip('\t\r\n\0')

                fileNamesList.append(thisFileName)

            count = 0
            for DDS in DDSInfoList:
                saveFileName = os.path.split(fileNamesList[count])[1].split('.')[0]

                # convention seems to be that the first .dds in a .tpf has no suffix.
                # after the first, file #N carries a suffix of N-1
                # if count == 0:
                saveFilePath = "{}{}.{}".format(destination, saveFileName, 'dds')

                count += 1

                bnd_file.seek(DDS[0] + offset)  # seek to the start of this DDS file's data
                byteBuffer = bnd_file.read(DDS[1])  # load the DDS data into a buffer
                if not (os.path.isfile(saveFilePath)):
                    with open(saveFilePath, 'wb') as dds_File:
                        dds_File.write(byteBuffer)  # write the buffer to a file
                    dds_File.closed

    bnd_file.closed


def write_DDSFiles(fileNameData, sourceDirectory, destination):
    ddsFileList = []
    count = 0
    fileName = get_tpfPath(fileNameData, sourceDirectory)[0]
    if (os.path.isfile(fileName)):
        with open(fileName, 'rb') as tpf_File:
            for DDS in get_DDSInfoList(fileName):
                
                saveFileName = os.path.split(fileName)[1].split('.')[0]

                # convention seems to be that the first .dds in a .tpf has no suffix.
                # after the first, file #N carries a suffix of N-1
                # if count == 0:

                saveFilePath = "{}{}.{}".format(destination, saveFileName, 'dds')
                ddsFileList.append((saveFilePath, fileNameData[1]))

                tpf_File.seek(DDS[0])  # seek to the start of this DDS file's data
                byteBuffer = tpf_File.read(DDS[1])  # load the DDS data into a buffer
                if not (os.path.isfile(saveFilePath)):
                    with open(saveFilePath, 'wb') as dds_File:
                        dds_File.write(byteBuffer)  # write the buffer to a file
                    dds_File.closed
    else:
        pass

    return ddsFileList
