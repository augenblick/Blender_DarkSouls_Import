import os
import sys
import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector



# Globals
filepathImport = ""
pathTPFs = ""
pathDDSs = ""



def read_some_data(context, filepath, use_some_setting):

    print(filepath)
    sourceDirectory = "D:/DATA/map/tx/"  # directory .tpf files are found in
    destination = "D:/DATA/map/dds_files/"  # directory .dds textures export to

    fileExtension = os.path.splitext(os.path.split(filepath)[1])[1]

    if not fileExtension == '.flver':

        flverDataOffsets = get_flverDataOffsets(filepath)

        tpfDataOffsets = get_tpfDataOffsets(filepath)
        # extract all .dds textures
        for TPFOffset in tpfDataOffsets:
            DDS_extract.write_DDSFilesFromOffsets(filepath, sourceDirectory, destination, TPFOffset)

    else:
        flverDataOffsets = [0]

    for offset in flverDataOffsets:
        thisFile = flver.flv_file(filepath, sourceDirectory, destination, offset)
        meshInfo = thisFile.get_meshInfo()
        faceTotal = 0
        materialList = thisFile.get_MaterialsForBlender()

        for m in range(thisFile.get_meshCount()):
            # print(m)

            verts = [Vector(v) for v in thisFile.get_VertsForBlender(m)]
            edges = []
            properFaceSet = []
            for f in range(meshInfo[m][8]):

                faces = thisFile.get_FacesForBlender(faceTotal)
                faceTotal = faceTotal + 1
                if len(properFaceSet) == 0:
                    properFaceSet = faces
                elif len(faces) > len(properFaceSet):
                    properFaceSet = faces

            #faces = ProperFaceSet
            mesh = bpy.data.meshes.new(name="New Object Mesh")
            mesh.from_pydata(verts, edges, properFaceSet)

            object_data_add(context, mesh)  # , operator=self)

            # vertex index : vertex value pair
            vi_uv = {i: uv for i, uv in enumerate(thisFile.get_UVsForBlender(m))}

            # initialize an empty list
            per_loop_list = [0.0] * len(mesh.loops)

            for loop in mesh.loops:
                per_loop_list[loop.index] = vi_uv.get(loop.vertex_index)

            per_loop_list = [uv for pair in per_loop_list for uv in pair]

            # creating the uvs
            mesh.uv_textures.new("test")
            mesh.uv_layers[0].data.foreach_set("uv", per_loop_list)

            # adding textures-----------------------------
            nameString = ""

            try:
                diffuse_path = materialList[m]['d1']
                nameString += "d1"
            except:
                diffuse_path = "D:/DATA/Missing Image.png"
                nameString += "err1"

            try:
                normal_path = materialList[m]['n1']
                nameString += "n1"
            except:
                normal_path = ""
                # print(materialList)

            try:
                specular_path = materialList[m]['s1']
                # print(specular_path)
                nameString += "s1"
            except:
                specular_path = ""

            try:
                mat_name = os.path.splitext(os.path.split(diffuse_path)[1])[0] + "_" + nameString
            except:
                mat_name = "Missing_image_" + nameString

            if bpy.data.materials.get(mat_name):
                bpy.context.active_object.data.materials.append(bpy.data.materials.get(mat_name))
            else:
                if not (diffuse_path == ".TPL TEXTURE MISSING"):

                    mat = (bpy.data.materials.get(mat_name) or bpy.data.materials.new(mat_name))

                    mat.use_nodes = True
                    nt = mat.node_tree
                    nodes = nt.nodes
                    links = nt.links

                    # clear
                    while(nodes):
                        nodes.remove(nodes[0])

                    output = nodes.new("ShaderNodeOutputMaterial")
                    transparent = nodes.new("ShaderNodeBsdfTransparent")
                    diffuse = nodes.new("ShaderNodeBsdfDiffuse")
                    alphaMix = nodes.new("ShaderNodeMixShader")

                    diffTexture = nodes.new("ShaderNodeTexImage")
                    diffTexture.image = bpy.data.images.load(diffuse_path)

                    if normal_path != "":
                        normTexture = nodes.new("ShaderNodeTexImage")
                        normTexture.image = bpy.data.images.load(normal_path)
                        normTexture.color_space = 'NONE'
                        normalMapNode = nodes.new("ShaderNodeNormalMap")

                    '''
                    if specular_path != "":
                        specTexture = nodes.new("ShaderNodeTexImage")
                        specTexture.image = bpy.data.images.load(specular_path)
                        glossy = nodes.new("ShaderNodeBsdfGlossy")
                        glossMix = nodes.new("ShaderNodeMixShader")
                    '''

                    if specular_path == "":
                        links.new(diffuse.inputs['Color'], diffTexture.outputs['Color'])
                        links.new(alphaMix.inputs[0], diffTexture.outputs[1])
                        links.new(output.inputs['Surface'], alphaMix.outputs['Shader'])
                        links.new(alphaMix.inputs[1], transparent.outputs['BSDF'])
                        links.new(alphaMix.inputs[2], diffuse.outputs['BSDF'])
                        if normal_path != "":
                            links.new(normalMapNode.inputs[1], normTexture.outputs[0])
                            links.new(diffuse.inputs[2], normalMapNode.outputs[0])

                    if specular_path != "":
                        links.new(diffuse.inputs['Color'], diffTexture.outputs['Color'])
                        links.new(alphaMix.inputs[0], diffTexture.outputs[1])
                        links.new(output.inputs['Surface'], alphaMix.outputs['Shader'])
                        links.new(alphaMix.inputs[1], transparent.outputs['BSDF'])
                        links.new(alphaMix.inputs[2], diffuse.outputs['BSDF'])
                        if normal_path != "":
                            links.new(normalMapNode.inputs[1], normTexture.outputs[0])
                            links.new(diffuse.inputs[2], normalMapNode.outputs[0])

                    # distribute nodes along the x axis
                    for index, node in enumerate((diffTexture, diffuse, output)):
                        node.location.x = 200.0 * index
                        node.location.y = 100.0 * index
                    print("adding " + mat_name + " texture to " + str(bpy.context.active_object))
                    bpy.context.active_object.data.materials.append(mat)

                else:
                    print("Textures missing")

    return {'FINISHED'}


# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class ImportDSModel(Operator, ImportHelper):
    #Import Dark Souls model from file of type .flver, .objbnd, .partsbnd, or .chrbnd

    bl_label = ""
    bl_name = "Import DS Data"
    bl_idname = "mesh.import"
    bl_options = {"PRESET"}

    # ImportHelper mixin class uses this
    filename_ext = ".flver"

    filter_glob = StringProperty(
        default="*.flver;*.objbnd;*.partsbnd;*.chrbnd",
        options={'HIDDEN'},
        maxlen=255,
    )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    use_setting = BoolProperty(
        name="Example Boolean",
        description="Example Tooltip",
        default=True,
    )

    type = EnumProperty(
        name="Example Enum",
        description="Choose between two items",
        items=(('OPT_A', "First Option", "Description one"),
               ('OPT_B', "Second Option", "Description two")),
        default='OPT_A',
    )

    def execute(self, context):
        print(self.filepath)
        return read_some_data(context, self.filepath, self.use_setting)


def register():
    bpy.utils.register_class(ImportDSModel)


def unregister():
    bpy.utils.unregister_class(ImportDSModel)



if __name__ == "__main__":
    register()
