# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; version 2
#  of the License.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Dark Souls Importer",
    "description": "Imports Dark Souls environment, character, and object models from unpacked game data files",
    "author": "Nathan Grubbs",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "3D View > Tools",
    "warning": "",
    "wiki_url": "",
    "category": "Import-Export",
}

import bpy

from bpy.props import (
                        StringProperty,
                        BoolProperty,
                        PointerProperty,
                       )

from bpy.types import (Panel, PropertyGroup)


# ------------------------------------------------------------------------
#    Scene Properties
# ------------------------------------------------------------------------

class MyProperties(PropertyGroup):

    tpfPath : bpy.props.StringProperty(
        name="",
        description="The directory in the unpacked Dark Souls data where .tpf files are stored\n(e.g. '[DARK SOULS DATA]/map/tx/')",
        default="C:\\Users\\", # todo: Pull value from config
        maxlen=1024,
        subtype='DIR_PATH')

    ddsPath : bpy.props.StringProperty(
        name="",
        description="The directory .dds textures will be stored as they are unpacked\n(create a new or use and existing directory)",
        default="C:\\Users\\", # todo: Pull value from config
        maxlen=1024,
        subtype='DIR_PATH')



# ------------------------------------------------------------------------
#    Panel in Object Mode
# ------------------------------------------------------------------------


class OBJECT_PT_DataPathSettings(Panel):
    bl_idname = "OBJECT_PT_DataPathSettings"
    bl_label = "Dark Souls Import"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "Dark Souls Import"
    bl_context = "objectmode"

    def draw(self, context):


        layout = self.layout
        scene = context.scene



        layout.label(text = ".TPF data input path:")
        colTPF = layout.column()
        colTPF.prop(scene.my_tool, "tpfPath", text="")
        layout.separator()


        layout.label(text = ".DDS data output path:")
        colDDS = layout.column()
        colDDS.prop(scene.my_tool, "ddsPath", text="")

        layout.separator()
        colSaveDef = layout.column()
        layout.operator("mesh.import", text="Select File")

        layout.separator()
        layout.separator()

        # ImportDsData.getDataPath(scene.my_tool.tpfPath)
        layout.operator("mesh.import", text="Select File")

 

# ------------------------------------------------------------------------
#    Operator
# ------------------------------------------------------------------------

# class ImportDsData(bpy.types.Operator):
#     bl_label = "This label do anything?"
#     bl_name = "Import DS Data"
#     bl_idname = "mesh.import"
#     bl_options = {"PRESET"}

#     dataPath = ""

#     @staticmethod
#     def getDataPath(dataPath):
#         ImportDsData.dataPath = dataPath

#     def execute(self, context):
#         print("Importing DS Data")
#         print(ImportDsData.dataPath)
#         return {"FINISHED"}

# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

classes = (
    MyProperties,
    OBJECT_PT_DataPathSettings,
    # ImportDsData
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.my_tool = PointerProperty(type=MyProperties)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.my_tool


if __name__ == "__main__":
    register()