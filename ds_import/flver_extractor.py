from typing import Type
import model
from ds_import import binary_reader
from ds_import import errors
import os
from collections import namedtuple

test_file_path = "D:\\DATA\\map\\m10_01_00_00\\m3210B1A10.flver"

class FlverExtractor:

    __flver_file_path = ""

    def __is_ds1_flver(self):

        if not os.path.isfile(self.__flver_file_path):
            raise FileNotFoundError("The file '{filepath}' could not be found".format(filepath=self.__flver_file_path))

        with binary_reader.BinaryReader(self.__flver_file_path) as reader:

            if reader.get_string(5) == "FLVER":         # is flver file?
                reader.seek(6)
                if reader.get_string(1) == "L":         # is little-endian?
                    reader.seek(8)
                    version_minor = reader.get_int8()
                    reader.seek(10)
                    if reader.get_int8() == 2 and version_minor == 12:      # is version 2.12?
                        return True

            return False




    def extract_model(self, __flver_file_path):

        self.__flver_file_path = __flver_file_path

        print(self.__is_ds1_flver())



        # how many meshes
        # how many vert sets
        # where is vertex buffer(s)

        # get vertex buffer format(s)
        # get vertices


    class FlverMetadata:

        """
        # Get that sweet header data (of format '5sxsxHHIIIIIIIffffffIIIIIIII')
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
        """

        metadata_init = False
        data_offset = 0
        data_size = 0
        hitbox_count = 0
        material_count = 0
        bone_count = 0
        mesh_count = 0
        vertex_info_count = 0
        face_set_count = 0
        vertex_descr_count = 0
        texture_count = 0

        vert_pointers = None

        def __init__(self):
            vert_set_pointer = namedtuple("vert_set_pointer", "offset size")
            # self.vert_pointers = [vert_set_pointer(14, 10000)]


