import struct
import binascii
import os
from . import DDS_extract

# a script to provide Blender with the data it needs to create a 3D model from Dark Souls data
# author: Nathan Grubbs

# a python representation of the Dark Souls flver file


class flv_file:

    def __init__(self, fileName, sourceDirectory, destination, masterOffset):
        self.fileName = fileName
        self.sourceDirectory = sourceDirectory
        self.destination = destination

        self.masterOffset = masterOffset

        self.header_data = self.header_parse(self.fileName)

        # obtain separate header elements from the header data
        self.data_offset = self.header_data[4] + self.masterOffset          # offset to start of data
        self.data_length = self.header_data[5]                              # size of data in bytes
        self.hitbox_count = self.header_data[6]                             # count of hitboxes
        self.mater_count = self.header_data[7]                              # count of materials
        self.bone_count = self.header_data[8]                               # count of bones
        self.mesh_count = self.header_data[9]                               # count of meshes in this file

        self.vertInfo_count = self.header_data[10]                          # count of vertex infos TODO: Is this ever different from mesh count?
        # 6 unknown floats here                                             # bounding box info?
        # 4 unknown ints here
        self.faceSet_count = self.header_data[21]                           # count of face sets
        self.vertDesc_count = self.header_data[22]                          # count of vertex descriptions TODO: explain this

        self.texture_count = self.header_data[23]                           # count of textures
        # 9 unknown ints here

        self.UVInfoList = []
        self.vertDataDescriptionPointers = self.get_vertDataDescriptionPointers()           # contains two values per vertex set: number of datapoints per vertex,
                                                                                            # and offset to location that describes datapoints

        self.vertStructFormats = self.get_vertStructFormats()               # struct formats for vertex data in this file

        self.MeshVert_info = self.get_MeshVert_info()                       # info about vertices in each mesh (offset, format, total size, etc.)

        self.meshInfo = self.get_meshInfo()

        self.allVerts = []

        for m in range(0, self.mesh_count):
            Verts = self.get_Vertices(self.vertStructFormats[self.MeshVert_info[m][1]], self.data_offset + self.MeshVert_info[m][7], self.MeshVert_info[m][3])
            self.allVerts.append(Verts)

        self.allFaceSets = self.get_faceSets()
        self.get_MaterialsForBlender()

        self.get_TexturePathList()

    # parses the header of the flver file
    def header_parse(self, fileName):

        # common struct types specified as follows:
            # x = pad byte
            # c = char
            # h = short (2 bytes)
            # H = unsigned short (2 bytes)
            # i = int (4 bytes)
            # I = unsigned int (4 bytes)
            # f = float
            # s = string (prefixed with length - defaults to '1')

        # define struct format
        header_fmt = "5sxsxHHIIIIIIIffffffIIIIIIII"
        head_length = struct.calcsize(header_fmt)

        with open(self.fileName, 'rb') as flver_file:
            flver_file.seek(self.masterOffset)
            top_data = struct.unpack(header_fmt, flver_file.read(head_length))
        return top_data

    # retrieves list of information on every Material in this file
    def get_MaterialAddressList(self):
        materialAddress_fmt = "IIIIIIII"
        materialAddressList = []
        with open(self.fileName, 'rb') as flver_file:
            flver_file.seek(128 + (self.hitbox_count * 64) + self.masterOffset)
            for material in range(self.mater_count):
                thisMaterialAddress = struct.unpack(materialAddress_fmt, flver_file.read(32))
                materialAddressList.append(thisMaterialAddress)
        flver_file.close()
        return materialAddressList

    # retrieves the paths/filenames for this file's textures
    def get_TexturePathList(self):
        texturePathList = []
        textureCount = 0
        char_fmt = 'bx'
        with open(self.fileName, 'rb') as flver_file:
            for materialAddress in self.get_MaterialAddressList():
                for texture in range(materialAddress[2]):
                    charList = []
                    thisTextureAddress = self.get_TextureAddressList()[textureCount]
                    flver_file.seek(thisTextureAddress[0] + self.masterOffset)
                    textureStringLength = thisTextureAddress[1] - thisTextureAddress[0]
                    for i in range(textureStringLength // 2):
                        thisByte = struct.unpack(char_fmt, flver_file.read(2))
                        thisChar = chr(thisByte[0])
                        if thisChar == "\\":
                            thisChar = "/"

                        charList.append(thisChar[0])
                        textureString = ''.join(charList)
                        textureString = textureString.rstrip()

                    charList = []
                    flver_file.seek(thisTextureAddress[1] + self.masterOffset)
                    for i in range(10):
                        thisByte = struct.unpack(char_fmt, flver_file.read(2))
                        thisChar = chr(thisByte[0])
                        if thisChar == "\\":
                            thisChar = "/"

                        charList.append(thisChar[0])
                        textureName = ''.join(charList)
                        textureName = textureName.rstrip()
                    textureCount += 1
                    if len(textureString) > 3:
                        texturePathList.append((textureString, textureName))
            return texturePathList

        flver_file.close()
        return

    # retrieves list of information on every texture in this file
    # TODO: explain in more detail
    def get_TextureAddressList(self):
        textureAddressList = []
        textureAddress_fmt = "IIffIIII"
        textureAddressOffset = 128 + (self.hitbox_count * 64) + (128 * self.bone_count) + (32 * self.mater_count) + (80 * self.mesh_count) + (32 * self.faceSet_count) + (16 * self.vertDesc_count)
        with open(self.fileName, 'rb') as flver_file:
            flver_file.seek(textureAddressOffset + self.masterOffset)
            for texture in range(self.texture_count):
                thisTextureAddress = struct.unpack(textureAddress_fmt, flver_file.read(32))
                textureAddressList.append(thisTextureAddress)
        flver_file.close()
        return textureAddressList

    # extracts required DDS files and returns a dictionary
    # containing paths to extract location as values
    # and texture type and number as key
    def get_MaterialsForBlender(self):
        materialList = []
        unsortedTextures = []
        textureCount = 0
        TexturePathList = self.get_TexturePathList()
        for material in range(self.mater_count):
            thisMaterial = {}
            diffuseCount = 0
            specularCount = 0
            normalCount = 0
            lightMapCount = 0
            detailBumpCount = 0

            # for every texture in this material...
            for textureNum in range(self.get_MaterialAddressList()[material][2] - 1):

                # the following line both extracts the .dds file and gets the filepath to said file
                thisTexture = DDS_extract.write_DDSFiles(TexturePathList[textureCount], self.sourceDirectory, self.destination)

                if len(thisTexture) == 0:
                    OGFilePath = TexturePathList[textureNum][0]  # get texture filepath from .flver
                    fileNameNoExt = os.path.splitext(os.path.split(OGFilePath)[1])[0]
                    if fileNameNoExt.endswith('n'):
                        textureType = "g_bumpmap"
                    elif fileNameNoExt.endswith('s'):
                        textureType = "g_specular"
                    else:
                        textureType = "g_diffuse"

                    # do checks for existing texture image here
                    if os.path.isfile(self.destination + fileNameNoExt + '.dds'):
                        thisTexture = [(self.destination + fileNameNoExt + '.dds', textureType)]

                for texture in thisTexture:
                    fileNoExtension = DDS_extract.get_fileNoExtension(texture)
                    currentFileName = fileNoExtension[1]
                    if currentFileName[4] == 'e':
                        specularCount += 1
                        thisMaterial['s' + str(specularCount)] = texture[0]
                    elif currentFileName[4] == 'm':
                        normalCount += 1
                        thisMaterial['n' + str(normalCount)] = texture[0]
                    elif currentFileName[4] == 'f':
                        diffuseCount += 1
                        thisMaterial['d' + str(diffuseCount)] = texture[0]
                    elif currentFileName[4] == 'g':
                        lightMapCount += 1
                        thisMaterial['lm' + str(lightMapCount)] = texture[0]
                    elif currentFileName[4] == 't':
                        detailBumpCount += 1
                        thisMaterial['db' + str(detailBumpCount)] = texture[0]

                textureCount += 1

            materialList.append(thisMaterial)
        return materialList

    # returns count of highest face in a given set of faces
    def get_HighestFace(self, faceset):
        highest = 0
        for face in faceset:
            for vertex in face:
                if vertex > highest:
                    highest = vertex
        return highest

    def get_materialNumber(self, VertSet):
        return meshInfo[VertSet][1]

    # returns number of meshes in flver file
    def get_meshCount(self):
        return self.mesh_count

    # retrieves list of information on every mesh in this file
    def get_meshInfo(self):

        meshInfo_offset = 128 + (self.hitbox_count * 64) + (128 * self.bone_count) + (32 * self.mater_count)
        fmt = "IIIIIIIIIIII"
        fmt_length = struct.calcsize(fmt)
        self.meshInfo = []

        with open(self.fileName, 'rb') as flver_file:
            flver_file.seek(meshInfo_offset + self.masterOffset)
            for info in range(self.mesh_count):
                thisMeshInfo = struct.unpack(fmt, flver_file.read(fmt_length))
                self.meshInfo.append(thisMeshInfo)
        return self.meshInfo

    # returns info on the vertex structs in this file
    # contains two values per vertex set:
        # 1 - number of datapoints included in each vertex set
        # 2 - offset (from data_offset) of the data that describes the type and format of each datapoint
    def get_vertDataDescriptionPointers(self):

        fmt = "IxxxxxxxxI"
        vertInfo_length = struct.calcsize(fmt)
        offset = 128 + (self.hitbox_count * 64) + (128 * self.bone_count) + (80 * self.mesh_count) + (32 * self.mater_count) + (32 * self.faceSet_count)  # offset of the vert. struct info
        vertDataDescriptionPointers = []

        with open(self.fileName, 'rb') as flver_file:
            flver_file.seek(offset + self.masterOffset)  # seek to the offset of the vert. struct info

            for i in range(0, self.vertDesc_count):
                thisvertDataDescriptionPointers = struct.unpack(fmt, flver_file.read(vertInfo_length))
                vertDataDescriptionPointers.append(thisvertDataDescriptionPointers)

        return vertDataDescriptionPointers

    # retrieves list of information on every set of Vertices in this file
    # there are 8 values per vertex set stored in MesVert_info.
    # The values are as follows:
        # 1 - unknown
        # 2 - vertex format (an index into self.vertStructFormats).
        # 3 - byte size of data for each vertex in this set
        # 4 - number of vertices in this vertex set
        # 5 - unknown
        # 6 - unknown
        # 7 - total byte size of this vertex set
        # 8 - offset to start of the data for this vertex set (starting from self.data_offset)
    def get_MeshVert_info(self):
        fmt = "IIIIIIII"
        fmt_size = struct.calcsize(fmt)
        mesh_infoList = []
        MVInfo_offset = 128 + (self.hitbox_count * 64) + (128 * self.bone_count) + (48 * self.mesh_count) + (32 * self.mater_count) + (32 * self.faceSet_count)

        with open(self.fileName, 'rb') as flver_file:
            flver_file.seek(MVInfo_offset + self.masterOffset)
            for i in range(0, self.mesh_count):
                thisMeshVert_info = struct.unpack(fmt, flver_file.read(fmt_size))
                mesh_infoList.append(thisMeshVert_info)
        return mesh_infoList

    # TODO: determine if this is in use anywhere
    # NOTE: this returns the same thing as self.get_MeshVert_info() with the unknown/unused values discarded
    def get_vertInfo(self):
        fmt = "xxxxxxxxIIxxxxxxxxII"
        vertInfo_length = struct.calcsize(fmt)
        offset = 128 + (self.hitbox_count * 64) + (128 * self.bone_count) + (80 * self.mesh_count) + (32 * self.faceSet_count)  # offset of the vert. struct info
        vertInfo = []

        with open(self.fileName, 'rb') as flver_file:
            flver_file.seek(offset + self.masterOffset)  # seek to the offset of the vert. struct info

            for i in range(0, self.mesh_count):
                thisVertInfo = struct.unpack(fmt, flver_file.read(vertInfo_length))
                vertInfo.append(thisVertInfo)

        return vertInfo

    # defines the vertex structs used in this file
    # Checks 5 ints to determine what the structure of the vertex data for each set is.
    def get_vertStructFormats(self):

        fmt = "IIIII"
        fmt_length = struct.calcsize(fmt)
        tempList = []
        UVInfoList = []
        VertNormalInfoList = []

        with open(self.fileName, 'rb') as flver_file:
            count = 0
            vertStructFormats = []

            for currentvertDataDescriptionPointers in self.get_vertDataDescriptionPointers():
                # (self.get_vertDataDescriptionPointers() returns a collection that contains the number of
                # datapoints and the offset to type and format of each datapoint for each vertex set

                thisDiffUVInfo = [0, -1]  # (exists?, position in struct)
                thisLMUVInfo = [0, -1]  # (exists?, position in struct)
                thisUVInfoGroup = []
                currentPosition = -1
                currentVertStruct = ""

                # unpack
                flver_file.seek(currentvertDataDescriptionPointers[1] + self.masterOffset)
                for j in range(0, currentvertDataDescriptionPointers[0]):
                    thisVertInfo = struct.unpack(fmt, flver_file.read(fmt_length))
                    if thisVertInfo[2] == 2:  # position
                        currentPosition += 3
                        currentVertStruct += "fff"
                    elif thisVertInfo[2] == 17:  # bone index
                        currentPosition += 1
                        currentVertStruct += "I"
                    elif thisVertInfo[2] == 21:  # diffuse UV coords
                        currentPosition += 1
                        thisDiffUVInfo[0] = 1
                        thisDiffUVInfo[1] = currentPosition  # save position of Diffuse UV in struct
                        currentPosition += 1
                        currentVertStruct += "HH"
                    elif thisVertInfo[2] == 22:  # diffuse/lightmap UV coords
                        currentPosition += 1
                        thisLMUVInfo[0] = 1
                        thisLMUVInfo[1] = currentPosition  # save position of Diffuse/LM UV in struct
                        currentPosition += 1
                        currentVertStruct += "HHxxxx"
                    elif thisVertInfo[2] == 26:  # bone weights
                        currentPosition += 2
                        currentVertStruct += "II"
                    elif thisVertInfo[2] == 19:
                        if thisVertInfo[3] == 3:  # normal
                            currentPosition += 1
                            VertNormalInfoList.append(currentPosition)
                            currentPosition += 2
                            currentVertStruct += "BBBx"

                        elif thisVertInfo[3] == 10:  # bitangent
                            currentPosition += 4
                            currentVertStruct += "BBBB"
                        elif thisVertInfo[3] == 6:  # vertex color
                            currentPosition += 4
                            currentVertStruct += "BBBB"
                        elif thisVertInfo[3] == 7:
                            currentPosition += 1
                            currentVertStruct += "I"  # don't know what this one is yet! (4 bytes in size)

                    tempList.append(thisVertInfo)

                count += 1
                vertStructFormats.append(currentVertStruct)
                thisUVInfoGroup.append(thisDiffUVInfo)
                thisUVInfoGroup.append(thisLMUVInfo)
                UVInfoList.append(thisUVInfoGroup)

        self.UVInfoList = UVInfoList
        self.VertNormalInfoList = VertNormalInfoList
        return vertStructFormats

    # returns a list of all vertex info for every vertex in a given set of vertices
    def get_Vertices(self, VertFmt, offset, count):

        fmt_size = struct.calcsize(VertFmt)
        vertList = []

        with open(self.fileName, 'rb') as flver_file:
            flver_file.seek(offset)
            for i in range(0, count):
                thisVertInfo = struct.unpack(VertFmt, flver_file.read(fmt_size))
                vertList.append(thisVertInfo)
        return vertList

    def get_faceSetsInfo(self):

        fmt = "IIIIIIII"
        fmt_size = struct.calcsize(fmt)
        faceSet_infoList = []
        faceSetsInfo_offset = 128 + (self.hitbox_count * 64) + (128 * self.bone_count) + (32 * self.mater_count) + (48 * self.mesh_count)

        with open(self.fileName, 'rb') as flver_file:
            flver_file.seek(faceSetsInfo_offset + self.masterOffset)
            for i in range(0, self.faceSet_count):
                thisFaceSet_info = struct.unpack(fmt, flver_file.read(fmt_size))
                faceSet_infoList.append(thisFaceSet_info)
        return faceSet_infoList

    # returns a list of every faceset in this file
    def get_faceSets(self):
        faceSet_info = self.get_faceSetsInfo()
        face_struct = "H"
        face_size = struct.calcsize(face_struct)

        thisFaceSet = []
        all_faceSets = []

        with open(self.fileName, 'rb') as flver_file:
            all_faceSets = []
            shortList = []
            # once for each mesh...
            for faceSet in range(self.faceSet_count):
                # go to the start location of this mesh's faceset buffer
                flver_file.seek(faceSet_info[faceSet][3] + self.data_offset)

                # do the following once for each face in this mesh's faceset
                shortList = []
                for face in range(faceSet_info[faceSet][2]):
                    thisShort = struct.unpack(face_struct, flver_file.read(face_size))

                    shortList.append(thisShort[0])

                thisFaceSet = self.sortFaces(shortList)
                all_faceSets.append(thisFaceSet)
        return all_faceSets

    # sorts a given faceset into an order that Blender can use
    def sortFaces(self, faces):
        faceslist = []
        StartDirection = -1
        f1 = faces[0]
        f2 = faces[1]
        FaceDirection = StartDirection
        counter = 2
        while counter < len(faces):

            f3 = faces[counter]
            FaceDirection *= -1
            if (f1 != f2) and (f2 != f3) and (f3 != f1):
                if FaceDirection > 0:
                    faceslist.append(f1)
                    faceslist.append(f2)
                    faceslist.append(f3)
                else:
                    faceslist.append(f1)
                    faceslist.append(f3)
                    faceslist.append(f2)
            counter = counter + 1
            f1 = f2
            f2 = f3

        return faceslist

    # retrieves x,y,z coordinates for every vertex in a given set of vertices
    def get_VertsForBlender(self, whichVertSet):

        vertSet = self.allVerts[whichVertSet]
        vertList = []

        for vert in (vertSet):

            thisVert = []
            # y and z axes transposed to match Blender's axis orientation (z = up/down)
            thisVert.append(vert[0])  # append x
            thisVert.append(vert[2])  # append z
            thisVert.append(vert[1])  # append y
            vertList.append(thisVert)

        return vertList

    # returns face indices for a given faceset
    def get_FacesForBlender(self, whichFaceSet):

        faceList = []
        currentFaceSet = self.allFaceSets[whichFaceSet]
        faceCount = 0
        for k in range(len(currentFaceSet) // 3):
            thisFace = []
            thisFace.append(currentFaceSet[faceCount])
            thisFace.append(currentFaceSet[faceCount + 1])
            thisFace.append(currentFaceSet[faceCount + 2])

            faceList.append(thisFace)

            faceCount = faceCount + 3

        return faceList

    # returns a list of UV data from this file
    def get_UVsForBlender(self, whichVertGroup):
        UVList = []
        tripFlag = 0
        # check that the required struct has UVs
        whichUVSet = self.MeshVert_info[whichVertGroup][1]

        if self.UVInfoList[whichUVSet][1][0] != 0:
            UVLocation = self.UVInfoList[whichUVSet][1][1]
            highest_v = None
            lowest_v = None
            for vertInfo in self.allVerts[whichVertGroup]:
                [u, v] = vertInfo[UVLocation], vertInfo[UVLocation + 1]
                if u > 32767:
                    u = u - 65536
                u = u / 1024

                if v > 32767:
                    v = v - 65536
                v = v / 1024
                v = ((v - 0.5) * -1) + 0.5

                UVList.append([u, v])

            return UVList

        elif self.UVInfoList[whichUVSet][0][0] != 0:
            UVLocation = self.UVInfoList[whichUVSet][0][1]
            for vertInfo in self.allVerts[whichVertGroup]:
                [u, v] = vertInfo[UVLocation], vertInfo[UVLocation + 1]
                if u > 32767:
                    u = ((u) - 65536)

                    u = u / 1024
                else:
                    u = u / 1024

                if v > 32767:
                    v = ((v) - 65536)

                    v = v / 1024
                else:
                    v = v / 1024
                v = ((v - 0.5) * -1) + 0.5

                UVList.append((u, v))

            greatest = 0
            total = 0
            count = 0
            return UVList

    # this 'works', though the values haven't been thoroughly tested
    # I'm not certain how correct they are.
    def get_VertNormsForBlender(self, whichVertSet):
        vertNormList = []
        vertSet = self.allVerts[whichVertSet]
        vertStructNumber = self.MeshVert_info[whichVertSet][1]
        VNPosition = self.VertNormalInfoList[vertStructNumber]
        for vert in vertSet:
            thisVertNorm = ((vert[VNPosition] - 127) / 127, (vert[VNPosition + 1] - 127) / 127, (vert[VNPosition + 2] - 127) / 127)
            vertNormList.append(thisVertNorm)
        return vertNormList

    # returns a list of all edges that are outermost or innermost (are only a part of one face)
    def get_OuterEdgeSet(self, faceList):

        outerEdgeSet = set([])
        for face in faceList:
            edge1 = (face[0], face[1])
            edge2 = (face[1], face[2])
            edge3 = (face[2], face[0])

            # check edge1
            if (edge1 in outerEdgeSet):
                newSet.remove(edge1)
            elif (edge1[1], edge1[0]) in outerEdgeSet:
                outerEdgeSet.remove((edge1[1], edge1[0]))
            else:
                outerEdgeSet.add(edge1)

            # check edge2
            if (edge2 in outerEdgeSet):
                newSet.remove(edge2)
            elif (edge2[1], edge2[0]) in outerEdgeSet:
                outerEdgeSet.remove((edge2[1], edge2[0]))
            else:
                outerEdgeSet.add(edge2)

            # check edge3
            if (edge3 in outerEdgeSet):
                newSet.remove(edge3)
            elif (edge3[1], edge3[0]) in outerEdgeSet:
                outerEdgeSet.remove((edge3[1], edge3[0]))
            else:
                outerEdgeSet.add(edge3)

        return outerEdgeSet
