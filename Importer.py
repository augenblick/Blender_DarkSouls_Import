import os
import sys
import bpy

from bpy.types import Operator
from bpy.props import FloatVectorProperty, StringProperty, BoolProperty, EnumProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from bpy_extras.io_utils import ImportHelper
from mathutils import Vector
from .GetOffsets import(get_flverDataOffsets, get_tpfDataOffsets)
from .DDS_extract import write_DDSFilesFromOffsets
from .flver import *
from .Importer_UI import MyProperties


def read_some_data(context, filepath):

    # Load values set in addon preferences
    pathTPFs = bpy.context.preferences.addons[__package__].preferences.tpfPath
    pathDDSs = bpy.context.preferences.addons[__package__].preferences.ddsPath
    pathMissingTex = bpy.context.preferences.addons[__package__].preferences.missingTexPath

    useCollections = bpy.context.scene.my_tool.useCollections
    useLegacyNodes = bpy.context.scene.my_tool.useLegacyNodes
    matSpecular = bpy.context.scene.my_tool.specular
    matRoughness = bpy.context.scene.my_tool.roughness

    fileExtension = os.path.splitext(os.path.split(filepath)[1])[1]
    meshName = os.path.splitext(os.path.split(filepath)[1])[0]

    if not fileExtension == '.flver':
        flverDataOffsets = get_flverDataOffsets(filepath)

        tpfDataOffsets = get_tpfDataOffsets(filepath)
        # extract all .dds textures
        for TPFOffset in tpfDataOffsets:
            write_DDSFilesFromOffsets(filepath, pathTPFs, pathDDSs, TPFOffset)

    else:
        flverDataOffsets = [0]

    if (useCollections):
        # create collection for object
        currentCollection = bpy.context.view_layer.active_layer_collection.collection
        newCollection = bpy.data.collections.new(meshName)
        currentCollection.children.link(newCollection)

    for offset in flverDataOffsets:
        thisFile = flv_file(filepath, pathTPFs, pathDDSs, offset)
        meshInfo = thisFile.get_meshInfo()
        faceTotal = 0
        materialList = thisFile.get_MaterialsForBlender()



        for m in range(thisFile.get_meshCount()):

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
            mesh = bpy.data.meshes.new(name=meshName)
            mesh.from_pydata(verts, edges, properFaceSet)
            
            newObj = object_data_add(context, mesh)

            if (useCollections):
                # Link object to new collection
                oldObjCollection = newObj.users_collection[0]
                newCollection.objects.link(newObj)

                # Unlink object from old collection
                oldObjCollection.objects.unlink(newObj)
            

            # vertex index : vertex value pair
            vi_uv = {i: uv for i, uv in enumerate(thisFile.get_UVsForBlender(m))}

            # initialize an empty list
            per_loop_list = [0.0] * len(mesh.loops)

            for loop in mesh.loops:
                per_loop_list[loop.index] = vi_uv.get(loop.vertex_index)

            per_loop_list = [uv for pair in per_loop_list for uv in pair]

            # creating the uvs
            mesh.uv_layers.new(name="UVMap", do_init=True)
            mesh.uv_layers[0].data.foreach_set("uv", per_loop_list)

            # adding textures-----------------------------
            nameString = ""

            try:
                diffuse_path = materialList[m]['d1']
                nameString += "d1"
            except:
                if os.path.isfile(pathMissingTex):
                    diffuse_path = pathMissingTex
                else:
                    print("No default 'missing texture' image set.  Check add-on preferences")
                    diffuse_path = ".TPF TEXTURE MISSING"
                nameString += "err1"

            try:
                normal_path = materialList[m]['n1']
                nameString += "n1"
            except:
                normal_path = ""

            try:
                specular_path = materialList[m]['s1']
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
                if not (diffuse_path == ".TPF TEXTURE MISSING"):

                    mat = (bpy.data.materials.get(mat_name) or bpy.data.materials.new(mat_name))

                    mat.use_nodes = True
                    nt = mat.node_tree
                    nodes = nt.nodes
                    links = nt.links

                    # clear any existing nodes
                    while(nodes):
                        nodes.remove(nodes[0])

                    if (useLegacyNodes):

                    # Create materials without use of the Principled BSDF node

                        # create shader nodes for transparency
                        output = nodes.new("ShaderNodeOutputMaterial")
                        transparent = nodes.new("ShaderNodeBsdfTransparent")
                        diffuse = nodes.new("ShaderNodeBsdfDiffuse")
                        alphaMix = nodes.new("ShaderNodeMixShader")

                        # set up diffuse texture
                        diffTexture = nodes.new("ShaderNodeTexImage")
                        diffTexture.image = bpy.data.images.load(diffuse_path)

                        # set up normal map
                        if normal_path != "":
                            normTexture = nodes.new("ShaderNodeTexImage")
                            normTexture.image = bpy.data.images.load(normal_path)
                            normalMapNode = nodes.new("ShaderNodeNormalMap")

                        # set up transparency
                        links.new(diffuse.inputs['Color'], diffTexture.outputs['Color'])
                        links.new(alphaMix.inputs[0], diffTexture.outputs[1])
                        links.new(output.inputs['Surface'], alphaMix.outputs['Shader'])
                        links.new(alphaMix.inputs[1], transparent.outputs['BSDF'])
                        links.new(alphaMix.inputs[2], diffuse.outputs['BSDF'])
                        if normal_path != "":
                            links.new(normalMapNode.inputs[1], normTexture.outputs[0])
                            links.new(diffuse.inputs[2], normalMapNode.outputs[0])

                        # distribute nodes along the x axis (crude method)
                        for index, node in enumerate((diffTexture, diffuse, output, alphaMix)):
                            node.location.x = 200.0 * index
                            node.location.y = 100.0 * index
                        # print("adding " + mat_name + " texture to " + str(bpy.context.active_object))
                        bpy.context.active_object.data.materials.append(mat)

                        try:
                            bpy.context.object.active_material.blend_method = 'HASHED'
                            bpy.context.object.active_material.shadow_method = 'HASHED'
                        except:
                            print("Unable to set transparency")



                    else:

                        # create nodes
                        output = nodes.new("ShaderNodeOutputMaterial")
                        transparent = nodes.new("ShaderNodeBsdfTransparent")
                        principled = nodes.new("ShaderNodeBsdfPrincipled")
                        alphaMix = nodes.new("ShaderNodeMixShader")

                        # set up diffuse texture and alpha
                        diffTexture = nodes.new("ShaderNodeTexImage")
                        diffTexture.image = bpy.data.images.load(diffuse_path)
                        links.new(principled.inputs['Base Color'], diffTexture.outputs['Color']) # diffuse color to principled
                        links.new(diffTexture.outputs['Alpha'], alphaMix.inputs[0])              # diffuse alpha to mix factor
                        links.new(principled.outputs['BSDF'], alphaMix.inputs[2])                # principled to mix
                        links.new(transparent.outputs['BSDF'], alphaMix.inputs[1])               # transparent to mix
                        links.new(alphaMix.outputs['Shader'], output.inputs['Surface'])          # Mixed Shader to output node

                        # set up normal map
                        if normal_path != "":
                            normTexture = nodes.new("ShaderNodeTexImage")
                            normTexture.image = bpy.data.images.load(normal_path)
                            normalMapNode = nodes.new("ShaderNodeNormalMap")
                            links.new(normalMapNode.inputs[1], normTexture.outputs[0])
                            links.new(principled.inputs['Normal'], normalMapNode.outputs[0])

                        # set up specular map
                        if specular_path != "":
                            specTexture = nodes.new("ShaderNodeTexImage")
                            specTexture.image = bpy.data.images.load(specular_path)
                            links.new(principled.inputs['Specular'], specTexture.outputs['Color'])

                        # spread out the nodes a bit (not working well in most cases)

                        principled.location.x = 740
                        principled.location.y = 200
                        output.location.x = 925
                        output.location.y = 200
                        transparent.location.x = 800
                        transparent.location.y = 185
                        alphaMix.location.x = 850
                        alphaMix.location.y = 225
                        diffTexture.location.x = 640
                        diffTexture.location.y = 230

                        if 'normTexture' in locals():
                            normTexture.location.x = 590
                            normTexture.location.y = 85

                        if 'specTexture' in locals():
                            specTexture.location.x = 560
                            specTexture.location.y = 160

                        # set Specular and Roughness values on the Principled BSDF node
                        principled.inputs[5].default_value = matSpecular
                        principled.inputs[7].default_value = matRoughness

                        bpy.context.active_object.data.materials.append(mat)

                        try:
                            bpy.context.object.active_material.blend_method = 'HASHED'
                            bpy.context.object.active_material.shadow_method = 'HASHED'
                        except:
                            print("Unable to set transparency")



                    

                else:
                    print("Textures missing")

    return {'FINISHED'}

def AutoImport_Folder(context, filePath, file):
    print("full name : ")
    print(filePath)
    path_to_obj_dir = os.path.dirname(filePath)

    file_list = sorted(os.listdir(path_to_obj_dir))

    obj_list = [item for item in file_list if item.endswith('.flver')]
    print("number of file founded:")
    print(len(obj_list))

    for item in obj_list:
        path_to_file = os.path.join(path_to_obj_dir, item)
        print(path_to_file)
        read_some_data(context, path_to_file)

    return {'FINISHED'}

class DSIMPORTER_OT_ImportDsData(bpy.types.Operator, ImportHelper):
    bl_idname = "dsimporter.importdsdata"
    bl_name = "Import DS Data"
    bl_label = "Import Mesh"
    bl_options = {"PRESET"}

    # filename_ext = ".flver"

    filter_glob : StringProperty(
        default="*.flver;*.objbnd;*.partsbnd;*.chrbnd",
        options={'HIDDEN'},
        maxlen=255,
        )

    filepath: StringProperty(subtype="FILE_PATH")
    
    # def execute(self, context):
    #     file = open(self.filepath, 'rb')
    #     read_some_data(context, file.name)
    #     return {'FINISHED'}
    def execute(self, context):
        file = open(self.filepath, 'rb')
        importFolder = bpy.context.scene.my_tool.importFolder

        if not importFolder:
            read_some_data(context, file.name)
        else:
            AutoImport_Folder(context, file.name, file)
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

classes = (
    DSIMPORTER_OT_ImportDsData,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
