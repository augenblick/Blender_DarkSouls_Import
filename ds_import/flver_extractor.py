import os
import typing
from collections import namedtuple
from face import Face
from face_set import FaceSet
from model import Model
from vertex import Vertex
from mesh import Mesh
from vector2 import Vector2
from vector3 import Vector3
from binary_reader import BinaryReader
from errors import UnreadableFormatError



# TODO: add docstring comments throughout
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
    __material_parameters = None        # per material?: offsets to material/texture filenames(?)
    __vertex_struct_formats = None      # list of ordered dictionaries describing the vertex data layouts

    def extract_model(self):
        """
        Extracts the loaded Dark Souls flver file and returns as a Model

        :return: A Dark Souls Model
        """

        if self.__flver_file_path == "":
            raise Exception("A file must be loaded before extraction.  Use FlverExtractor.load_file(flver_filepath)")


        # TODO: fix bug occurring when there is more than one faceset per mesh.  There is a "faceset_count" parameter stored in self.__mesh_info that probably should be referenced
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

            # add vertex sets to model
            mesh_list = []
            for vi in self.__vertex_info:

                current_vertex_format = ""
                reader.seek(vi.buffer_offset + self.__metadata.data_offset)
                for datatype in self.__vertex_struct_formats[vi.vertex_struct_formats_index]:
                    current_vertex_format += vert_data_dict.get(datatype)
                vert_list = []
                for vertex in range(0,vi.vertex_count):
                    vert_data = reader.get_struct(current_vertex_format)
                    new_vert = Vertex()
                    new_vert.uv = None
                    new_vert.normal = None
                    new_vert.lightmap_uv = None
                    new_vert.bone_weight = None

                    data_index = 0

                    for data_type in self.__vertex_struct_formats[vi.vertex_struct_formats_index]:
                        if data_type == "position":
                            new_vert.position = Vector3(vert_data[data_index], vert_data[data_index + 1], vert_data[data_index + 2])
                            data_index += 3

                        elif data_type == "bone index":
                            # TODO: handle "bone_index" case
                            data_index += 1

                        elif data_type == "normal":
                            # TODO: confirm that normals are correct
                            new_vert.normal = Vector3(((vert_data[data_index] - 127) / 127) * 1, ((vert_data[data_index + 1] - 127) / 127) * 1, ((vert_data[data_index + 2] - 127) / 127) * 1)
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
                new_mesh = Mesh(vert_list)
                mesh_list.append(new_mesh)

            # create facesets
            temp_face_sets = []
            for face_data in self.__faceset_info:
                reader.seek(self.__metadata.data_offset + face_data.buffer_offset)
                face_set = []
                for face_index in range(0, face_data.index_count):
                    face_set.append(reader.get_u_int16())

                temp_face_sets.append(self.__sort_faces(face_set))    # re-order faceset

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

    # check to see whether the file is a readable format
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


    def output_obj(self, model: Model, filepath: str):
        """
        Outputs an obj model given a dark souls model and destination path.

        :param model: a dark souls model
        :param filepath: the path/filename for the resulting obj file
        """

        # model = self.extract_model()

        vertcount_this_set = 1
        vertcount_prev_set = 1
        normcount_this_set = 1
        normcount_prev_set = 1
        uvcount_this_set = 1
        uvcount_prev_set = 1
        if filepath[-4:] != ".obj":
            filepath += ".obj"
        with open(filepath, "w") as writer:
            for mesh in model.meshes:

                normals_exist = mesh.vertices[0].normal is not None
                uvs_exist = mesh.vertices[0].uv is not None
                lm_uvs_exist = mesh.vertices[0].lightmap_uv is not None
                writer.write("\no {}\n".format(mesh) )
                for vertex in mesh.vertices:
                    vertcount_this_set += 1
                    writer.write("v {} {} {}\n".format(str(vertex.position.x), str(vertex.position.y), str(vertex.position.z)))

                if lm_uvs_exist:
                    writer.write("\n")
                    for vertex in mesh.vertices:
                        uvcount_this_set += 1
                        writer.write("vt {} {}\n".format(str(vertex.lightmap_uv.x), str(vertex.lightmap_uv.y)))

                elif uvs_exist:
                    writer.write("\n")
                    for vertex in mesh.vertices:
                        uvcount_this_set += 1
                        writer.write("vt {} {}\n".format(str(vertex.uv.x), str(vertex.uv.y)))

                if normals_exist:
                    writer.write("\n")
                    for vertex in mesh.vertices:
                        normcount_this_set += 1
                        writer.write("vn {} {} {}\n".format(str(vertex.normal.x), str(vertex.normal.y), str(vertex.normal.z)))

                writer.write("\n")
                for faceset in mesh.face_sets:
                    for face in faceset:
                        pos1 = face.vertices[0] + vertcount_prev_set
                        pos2 = face.vertices[1] + vertcount_prev_set
                        pos3 = face.vertices[2] + vertcount_prev_set
                        uv1 = face.vertices[0] + uvcount_prev_set
                        uv2 = face.vertices[1] + uvcount_prev_set
                        uv3 = face.vertices[2] + uvcount_prev_set
                        norm1 = face.vertices[0] + normcount_prev_set
                        norm2 = face.vertices[1] + normcount_prev_set
                        norm3 = face.vertices[2] + normcount_prev_set

                        if lm_uvs_exist:
                            uvs_exist = True
                        # writer.write("f {} {} {}\n".format(pos1, pos2, pos3))
                        # normals_exist = False
                        writer.write("f {}/{}/{} {}/{}/{} {}/{}/{}\n".format(pos1,uv1 if uvs_exist else "", norm1 if normals_exist else "",
                                                                    pos2,uv2 if uvs_exist else "", norm2 if normals_exist else "",
                                                                    pos3,uv3 if uvs_exist else "", norm3 if normals_exist else ""))
                vertcount_prev_set = vertcount_this_set
                uvcount_prev_set = uvcount_this_set
                normcount_prev_set = normcount_this_set


    # sorts a given faceset into an order that Blender can use
    def __sort_faces(self, faces):
        # TODO: figure out why this works
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


    def get_materials(self):

        with BinaryReader(self.__flver_file_path) as reader:
            mat_info = self.__material_parameters
            for counter in range (0, len(mat_info)):
                reader.seek(mat_info[counter].name_offset1)
                print(reader.get_string(mat_info[counter].name_offset2 - mat_info[counter].name_offset1))
                if counter < len(mat_info) - 1:
                    print(reader.get_string(mat_info[counter + 1].name_offset1 - mat_info[counter].name_offset2))

                # print("-----------------")
                # reader.seek(material.name_offset1)
                # print(reader.get_string((material.name_offset2 - material.name_offset1)))
                # print(reader.get_string((material.path_offset - material.name_offset)))

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


