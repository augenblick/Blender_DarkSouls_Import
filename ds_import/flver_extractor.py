from collections import namedtuple
from ds_import.face import Face
from ds_import.vertex import Vertex
from ds_import.mesh import Mesh
from ds_import.vector2 import Vector2
from ds_import.vector3 import Vector3
from ds_import.binary_reader import BinaryReader
from ds_import.errors import UnreadableFormatError


# TODO: add docstring comments throughout
class FlverExtractor:

    # namedtuple definitions ===========================================================================================

    # material_info - information about each material associated with the model in this flver file.
    #       > name_offset - offset to the material name
    #       > path_offset - offset to the material's path within the Dark Souls data (external to this .flver file)
    #       > param_count - number of inputs (textures) for this material
    #       > param_start_index - index into the list of texture files for the first texture associated with this material
    #       > flags - single-bit flags (stored currently as a integer).  I haven't deduced their specific purpose yet-- presumably material settings
    material_info = namedtuple("material_data", ["name_offset", "path_offset", "param_count", "param_start_index", "flags", "unknown1", "unknown2", "unknown3"])

    # material_parameters - information about each material parameter (texture)
    #       > name_offset1 - offset to the path of the parameter within the Dark Souls data (external to this .flver file)
    #                       These come in groups, with the last member in each group being a name (of some sort) rather than a path.
    #                                for example:   <Path to first texture>
    #                                               <Path to second texture>
    #                                               <Path to third texture>
    #                                               g_DetailBumpmap
    #                       The size of each group corresponds with material_info.param_count (see previous namedtuple)
    #       > name_offset2 - offset to, presumptively, the name of the field the given parameter is assigned to.  e.g. "g_Diffuse", "g_Bumpmap", etc.
    material_parameters = namedtuple("material_parameters", ["name_offset1", "name_offset2", "unknown1", "unknown2", "unknown3", "unknown4", "unknown5", "unknown6"])

    # mesh_info - information related to each mesh in this flver file.  It seems that a mesh will have one vertset, but may have multiple facesets.
    #       > is_dynamic -
    #       > material_index -
    #       > bone_index -
    #       > bone_index_count -
    #       > bone_indices_offset -
    #       > faceset_count -
    #       > faceset_index_offset -
    #       > vertset_info_count -
    #       > vertset_info_offset - 
    mesh_info = namedtuple("mesh_info", ["is_dynamic", "material_index", "unknown1", "unknown2", "bone_index", "bone_index_count", "unknown3", "bone_indices_offset",
                                        "faceset_count", "faceset_index_offset", "vertset_info_count", "vertset_info_offset"])

    # faceset_info - information about each faceset in this file, including information needed to obtain actual face data
    #       > flags - flags for this faceset (specific purpose yet unknown)
    #       > topology - yet unknown
    #       > cull_backfaces - presumably information about whether or not to cull the backfaces of faces in this faceset
    #       > index_count - number of vertex indices in this faceset
    #       > buffer_offset - offset to this faceset buffer (relative to the mater data offset, self.__metadata.data_offset)
    #       > buffer_size - total size in bytes of this faceset buffer
    faceset_info = namedtuple("faceset_info", ["flags", "topology", "cull_backfaces", "unknown1", "unknown2",
                                               "index_count", "buffer_offset", "buffer_size", "unknown3", "unknown4", "unknown5"] )

    # vertset_info - information about each set of vertices (one vertex set per mesh)
    #       > vertset_struct_formats_index - index telling which vertex structure to use for this vertex set
    #       > per_vertex_size - the size, in bytes, of each vertex in this set
    #       > vertex_count - number of vertices in this set
    #       > buffer_size - total vertex buffer size for this set (per_vertex_size * vertex_count)
    #       > buffer_offset - offset to the start of the vertex data for this set (relative to the master data offset, self.__metadata.data_offset)
    vertset_info = namedtuple("vertset_info", ["unknown1", "vertset_struct_formats_index", "per_vertex_size", "vertex_count",
                                             "unknown2", "unknown3", "buffer_size", "buffer_offset"])

    # vertset_description_info - A section of the flver data contains 'vertset_descriptions', which describe possible 
    #   layouts of vertset data (which vertex data is stored in a vertex buffer-- position, vert color, bone weight, etc.).
    #   vertset_description_info holds information used to locate and read each of these 'vertset_descriptions'.
    #       > datatype_count - Number of vertex data types in this vertset description
    #       > description_offset - offset to the start of this vertset description
    vertset_description_info = namedtuple("vertset_description_info", ["datatype_count", "unknown1", "unknown2", "description_offset"])


    # verset_struct_formats - an list holding lists of the possible vertex data structures in this flver file
    #       for example:
    #                   ['position', 'bone index', 'normal', 'vertex color', 'bitangent', 'diffuse/lightmap UV']
    #                   ['position', 'bone index', 'bone weight', 'normal', 'vertex color', 'bitangent', 'diffuse/lightmap UV']
    #                   ['position', 'bone index', 'normal', 'bitangent', 'diffuse/lightmap UV']
    #                   ['position', 'bone index', 'bone weight', 'normal', 'bitangent', 'diffuse/lightmap UV']
    #
    #       Each vertset will reference an index into vertset_struct_formats (index found at vertset_info.vertset_struct_formats_index),
    #       which in turn reveals the structure of the data in that vertset.


    # vert_data_dict is a dictionary used to reference the underlying data structure for each possible data type in a vertset.
    #       > key = vertex data type
    #       > value = struct format for that data type
    vert_data_dict = dict({"position": "fff",
                           "bone index": "I",
                           "normal": "BBBx",
                           "vertex color": "BBBB",
                           "bitangent": "BBBB",
                           "diffuse/lightmap UV": "HHxxxx",
                           "bone weight": "II",
                           "diffuse UV": "HH",
                           "unknown": "I"},)

    def __init__(self):

        self.__flver_file_path = ""
        self.__metadata = None  # flver file metadata-- data offset, number of meshes, bones, etc.

        self.__materials_info = None  # per material: offsets to material names, material paths, parameter count, etc.
        self.__mesh_info = None  # per mesh: is_dynamic, material_index, bone_index, etc.
        self.__faceset_info = None  # per faceset: information about each faceset buffer (indices count, offset to indices, etc.)
        self.__vertset_info = None  # per vertex set: vertset_struct_formats_index, data size per vertex, vertices offset, vertex_count, etc.
        self.__vertset_description_info = None  # per vertex description: count of datapoints in this description, offset to start of description
        self.__material_parameters = None  # per material?: offsets to material/texture filenames(?)
        self.__vertset_struct_formats = None  # list of ordered dictionaries describing the vertex data layouts


    def extract_model(self):
        """
        Extracts the loaded Dark Souls flver file and returns as a Model

        :return: A Dark Souls Model
        """

        if self.__flver_file_path == "":
            raise Exception("A file must be loaded before extraction.  Use FlverExtractor.load_file(flver_filepath)")


        with BinaryReader(self.__flver_file_path) as reader:

            # add vertex sets to model
            mesh_list = []
            for vi in self.__vertset_info:

                current_vertex_format = ""
                reader.seek(vi.buffer_offset + self.__metadata.data_offset)
                for datatype in self.__vertset_struct_formats[vi.vertset_struct_formats_index]:
                    current_vertex_format += FlverExtractor.vert_data_dict.get(datatype)
                vert_list = []
                new_vert = Vertex()
                for vertex in range(0,vi.vertex_count):
                    vert_data = reader.get_struct(current_vertex_format)
                    new_vert.uv = None
                    new_vert.normal = None
                    new_vert.lightmap_uv = None
                    new_vert.bone_weight = None

                    data_index = 0

                    for data_type in self.__vertset_struct_formats[vi.vertset_struct_formats_index]:
                        if data_type == "position":
                            new_vert.position = Vector3(vert_data[data_index], vert_data[data_index + 1], vert_data[data_index + 2])
                            data_index += 3

                        elif data_type == "bone index":
                            # TODO: handle "bone_index" case
                            data_index += 1

                        elif data_type == "normal":
                            # TODO: confirm that normals are correct
                            new_vert.normal = Vector3(((vert_data[data_index] - 127) / 127) * -1, ((vert_data[data_index + 1] - 127) / 127) * -1, ((vert_data[data_index + 2] - 127) / 127) * -1)
                            data_index += 3

                        elif data_type == "vertex color":
                            # TODO: handle "vert_color" case
                            data_index += 4

                        elif data_type == "bitangent":
                            # TODO: handle "bitangent" case
                            data_index += 4

                        elif data_type == "diffuse/lightmap UV":

                            [u,v] = vert_data[data_index], vert_data[data_index + 1]
                            if u > 32767:
                                u = u - 65536
                            u = u / 1024

                            if v > 32767:
                                v = v - 65536
                            v = v / 1024
                            v = ((v - 0.5) * -1) + 0.5
                            new_vert.lightmap_uv = Vector2(u,v)
                            data_index += 2

                        elif data_type == "bone weight":
                            # TODO: handle "bone_weights" case
                            data_index += 2

                        elif data_type == "diffuse UV":
                            [u, v] = vert_data[data_index], vert_data[data_index + 1]
                            if u > 32767:
                                u = u - 65536
                            u = u / 1024

                            if v > 32767:
                                v = v - 65536
                            v = v / 1024
                            v = ((v - 0.5) * -1) + 0.5
                            new_vert.uv = Vector2(u, v)
                            data_index += 2

                        elif data_type == "unknown":
                            # TODO: handle "unknown" case
                            data_index += 1
                            pass

                    vert_list.append(new_vert)
                mesh_list.append(Mesh(vert_list))

            # create facesets
            temp_face_sets = []
            for face_data in self.__faceset_info:
                reader.seek(self.__metadata.data_offset + face_data.buffer_offset)
                face_set = []
                for face_index in range(0, face_data.index_count):
                    face_set.append(reader.get_u_int16())

                temp_face_sets.append(self.__sort_faces_vertex_list(face_set))    # re-order faceset

            # break facesets into faces
            face_sets = []
            for f_set in temp_face_sets:
                curr_set = []
                for i in range(0, len(f_set), 3):
                     curr_set.append(Face(f_set[i:i + 3]))      # create Face objects
                face_sets.append(curr_set)

            start_set = 0
            for mesh_counter, mesh in enumerate(mesh_list):
                mesh.face_sets = face_sets[start_set:self.__mesh_info[mesh_counter].faceset_count + start_set]
                start_set += self.__mesh_info[mesh_counter].faceset_count


        return Model(mesh_list)


    # "loading the file" obtains the information necessary to extract the file's payload (vertices, faces, etc.)
    def load_file(self, flver_file_path):

        self.__flver_file_path = flver_file_path

        if not self.__is_ds1_flver():
            raise UnreadableFormatError(
                "The given file '{filepath}' is not of a readable format".format(filepath=flver_file_path))

        self.__metadata = self.__FlverMetadata(flver_file_path)

        with BinaryReader(self.__flver_file_path) as reader:

            # TODO: convert flag values to boolean?

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

            # collect vertset info
            self.__vertset_info = \
                self.__obtain_info(reader, "IIIIIIII", self.__metadata.vertset_info_count, self.vertset_info)

            # collect vertex descriptions info
            self.__vertset_description_info = \
                self.__obtain_info(reader, "IIII", self.__metadata.vertex_descr_count, self.vertset_description_info)

            # collect material parameters
            self.__material_parameters = \
                self.__obtain_info(reader, "IIffIIII", self.__metadata.material_param_count, self.material_parameters)

            self.__vertset_struct_formats = self.__define_vertset_formats()



    # check to see whether the file is a readable format
    def __is_ds1_flver(self):
        """return true if the given file is of a supported format

        Currently support are v2.12 .flver files with little-endian byte order.
        """

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

    @staticmethod
    def __obtain_info(binary_reader, struct_fmt, item_count, named_tuple):
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
            for vert_info in self.__vertset_description_info:
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


    # sorts a given list of vertex indices defining a set of faces into an order that Blender can use
    @staticmethod
    def __sort_faces_vertex_list(faces_vertex_list):
        # TODO: figure out why this works
        sorted_faces_vertex_list = []
        StartDirection = -1
        face_vertex1 = faces_vertex_list[0]
        face_vertex2 = faces_vertex_list[1]
        FaceDirection = StartDirection
        counter = 2
        while counter < len(faces_vertex_list):
            face_vertex3 = faces_vertex_list[counter]

            # For each vertex in the list, reverse the order of the vertices,
            # effectively reversing the normal of the face.
            FaceDirection *= -1
            # If any of the three vertices in this set are duplicates,
            # do not append, effectively skipping one vertex.
            if (face_vertex1 != face_vertex2) and (face_vertex2 != face_vertex3) and (face_vertex3 != face_vertex1):
                if FaceDirection > 0:
                    sorted_faces_vertex_list.append(face_vertex1)
                    sorted_faces_vertex_list.append(face_vertex2)
                    sorted_faces_vertex_list.append(face_vertex3)
                else:
                    sorted_faces_vertex_list.append(face_vertex1)
                    sorted_faces_vertex_list.append(face_vertex3)
                    sorted_faces_vertex_list.append(face_vertex2)

            counter = counter + 1

            # Shift the set of vertices down the list by one
            face_vertex1 = face_vertex2
            face_vertex2 = face_vertex3
        return sorted_faces_vertex_list


    class __FlverMetadata:

        def __init__(self, flver_file):

            with BinaryReader(flver_file) as reader:
                reader.seek(12)     # seek past file header (filetype, endianness, version info)
                self.data_offset = reader.get_u_int32()
                self.data_size = reader.get_u_int32()
                self.hitbox_count = reader.get_u_int32()
                self.material_count = reader.get_u_int32()
                self.bone_count = reader.get_u_int32()
                self.mesh_count = reader.get_u_int32()
                self.vertset_info_count = reader.get_u_int32()
                reader.seek(80)     # seek past bounding box definition and 4 other currently unused ints
                self.faceset_count = reader.get_u_int32()
                self.vertex_descr_count = reader.get_u_int32()
                self.material_param_count = reader.get_u_int32()


