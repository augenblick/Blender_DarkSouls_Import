from model import Model

def write_obj(model: Model, filepath: str):
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
            # for faceset in mesh.face_sets:
            faceset = mesh.face_sets[0]
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
