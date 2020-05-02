from typing import Type
import model
from binary_reader import BinaryReader
from errors import UnreadableFormatError
import os
from collections import namedtuple
import struct

test_file_path = "D:\\DATA\\map\\m10_01_00_00\\m3210B1A10.flver"

class FlverExtractor:

    # define namedtuples
    material_info = namedtuple("material_data", ["name_offset", "path_offset", "param_count", "param_start_index", "flags", "unknown1", "unknown2", "unknown3"])
    mesh_info = namedtuple("mesh_info", ["is_dynamic", "material_index", "unknown1", "unknown2", "bone_index", "bone_index_count", "unknown3", "bone_indices_offset",
                                        "faceset_count", "faceset_index_offset", "vertex_info_count", "vertex_info_offset"])
    faceset_info = namedtuple("faceset_info", ["flags", "topology", "cull_backfaces", "unknown1", "unknown2",
                                               "index_count", "buffer_offset", "buffer_size", "unknown3", "unknown4", "unknown5"] )
    vertex_info = namedtuple("vertex_info", ["unknown1", "vertex_struct_formats_index", "per_vertex_size", "vertex_count",
                                             "unknown2", "unknown3", "buffer_size", "buffer_offset"])
    vertex_description_info = namedtuple("vertex_description_info", ["datatype_count", "unknown1", "unknown2", "description_offset"])

    material_parameters = namedtuple("material_parameters", ["name_offset1", "name_offset2", "unknown1", "unknown2", "unknown3", "unknown4", "unknown5", "unknown6"])

    __flver_file_path = ""
    __metadata = None                   # flver file metadata-- data offset, number of meshes, bones, etc.

    __materials_info = None             # per material: offsets to material names, material paths, parameter count, etc.
    __mesh_info = None                  # per mesh: is_dynamic, material_index, bone_index, etc.
    __faceset_info = None               # per faceset: information about each faceset buffer (indices count, offset to indices, etc.)
    __vertex_info = None                # per vertex set: vertex_struct_formats_index, data size per vertex, vertices offset, vertex_count, etc.
    __vertex_description_info = None    # per vertex description: count of datapoints in this description, offset to start of description
    __material_parameters = None        # offsets to material/texture filenames(?)
    __vertex_struct_formats = None      # list of ordered dictionaries describing the vertex data layouts

    def extract_model(self):
        vert_data_dict = dict({"position":"fff",
                              "bone index":"I",
                              "normal":"BBBx",
                              "vertex color":"BBBB",
                              "bitangent":"BBBB",
                              "diffuse/lightmap UV":"HHxxxx",
                              "bone weight":"II",
                              "diffuse UV":"HH",
                              "unknown":"I"},
                              )

        with BinaryReader(self.__flver_file_path) as reader:
            # for vi in self.__vertex_info:
            vi = self.__vertex_info[3]
            print(vi.buffer_size)

            current_vertex_format = ""
            reader.seek(vi.buffer_offset + self.__metadata.data_offset)
            for datatype in self.__vertex_struct_formats[vi.vertex_struct_formats_index]:
                current_vertex_format += vert_data_dict.get(datatype)
            for vertex in range(0,vi.vertex_count):
                vert_data = reader.get_struct(current_vertex_format)
                # TODO: create vertices, meshes, model


    # "loading the file" obtains the information necessary to extract the file's payload (vertices, faces, etc.)
    def load_file(self, flver_file_path):

        self.__flver_file_path = flver_file_path

        if not self.__is_ds1_flver():
            raise UnreadableFormatError(
                "The given file '{filepath}' is not of a readable format".format(filepath=flver_file_path))

        self.__metadata = self.__FlverMetadata(flver_file_path)

        with BinaryReader(self.__flver_file_path) as reader:

            # TODO: convert flag values to booleans?

            # seek past file metadata
            reader.seek(128)

            # seek past hitbox data (64 bytes per hitbox)
            reader.seek_from_current_pos(self.__metadata.hitbox_count * 64)

            # collect material info
            self.__materials_info = \
                self.__obtain_info(reader, "IIIIIIII", self.__metadata.material_count, self.material_info)

            # seek past bone data (128 bytes per bone)
            reader.seek_from_current_pos(self.__metadata.bone_count * 128)

            # collect mesh info
            self.__mesh_info = \
                self.__obtain_info(reader, "IIIIIIIIIIII", self.__metadata.mesh_count, self.mesh_info)

            # collect faceset info
            self.__faceset_info = \
                self.__obtain_info(reader, "IBBBBIIIIII", self.__metadata.faceset_count, self.faceset_info)

            # collect vertex info
            self.__vertex_info = \
                self.__obtain_info(reader, "IIIIIIII", self.__metadata.vertex_info_count, self.vertex_info)

            # collect vertex descriptions info
            self.__vertex_description_info = \
                self.__obtain_info(reader, "IIII", self.__metadata.vertex_descr_count, self.vertex_description_info)

            # collect material parameters
            self.__material_parameters = \
                self.__obtain_info(reader, "IIffIIII", self.__metadata.material_param_count, self.material_parameters)

            self.__vertex_struct_formats = self.__define_vertset_formats()


    def __is_ds1_flver(self):

        if not os.path.isfile(self.__flver_file_path):
            raise FileNotFoundError("The file '{filepath}' could not be found".format(filepath=self.__flver_file_path))

        with BinaryReader(self.__flver_file_path) as reader:

            if reader.get_string(5) == "FLVER":         # is flver file?
                reader.seek(6)
                if reader.get_string(1) == "L":         # is little-endian?
                    reader.seek(8)
                    version_minor = reader.get_int8()
                    reader.seek(10)
                    if reader.get_int8() == 2 and version_minor == 12:      # is version 2.12?
                        return True

            return False


    def __obtain_info(self, binary_reader, struct_fmt, item_count, named_tuple):
        """
        @type named_tuple: namedtuple
        """
        info_list = []
        for x in range(0, item_count):
            info_struct = binary_reader.get_struct(struct_fmt)
            info_list.append(named_tuple._make(info_struct))
        return tuple(info_list)


    def __define_vertset_formats(self):

        vertset_formats = []
        with BinaryReader(self.__flver_file_path) as reader:
            for vert_info in self.__vertex_description_info:
                reader.seek(vert_info.description_offset)
                formats = []
                for i in range(0, vert_info.datatype_count):
                    tempStruct = reader.get_struct("IIIII")
                    typeConcat = str(tempStruct[2]) + str(tempStruct[3])


                    if typeConcat == "20":
                        formats.append("position")
                    elif typeConcat == "172":
                        formats.append("bone index")
                    elif typeConcat == "193":
                        formats.append("normal")
                    elif typeConcat == "196":
                        formats.append("vertex color")
                    elif typeConcat == "1910":
                        formats.append("bitangent")
                    elif typeConcat == "225":
                        formats.append("diffuse/lightmap UV")
                    elif typeConcat == "261":
                        formats.append("bone weight")
                    elif typeConcat == "215":
                        formats.append("diffuse UV")
                    elif typeConcat == "197":
                        formats.append("unknown")
                vertset_formats.append(formats)
        return vertset_formats






    class __FlverMetadata:

        data_offset = 0
        data_size = 0
        hitbox_count = 0
        material_count = 0
        bone_count = 0
        mesh_count = 0
        vertex_info_count = 0
        # bounding_box_1 (vec3)
        # bounding_box_2 (vec3)
        # unknown_3 (u int32)
        # unknown_4 (u int32)
        # unknown_5 (u int32)
        # unknown_6 (u int32)
        faceset_count = 0
        vertex_descr_count = 0
        material_param_count = 0

        vert_pointers = None


        def __init__(self, flver_file):

            with BinaryReader(flver_file) as reader:
                reader.seek(12)
                self.data_offset = reader.get_u_int32()
                self.data_size = reader.get_u_int32()
                self.hitbox_count = reader.get_u_int32()
                self.material_count = reader.get_u_int32()
                self.bone_count = reader.get_u_int32()
                self.mesh_count = reader.get_u_int32()
                self.vertex_info_count = reader.get_u_int32()
                reader.seek(80)
                self.faceset_count = reader.get_u_int32()
                self.vertex_descr_count = reader.get_u_int32()
                self.material_param_count = reader.get_u_int32()


