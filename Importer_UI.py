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

import bpy

from bpy.props import (
                        StringProperty,
                        BoolProperty,
                        PointerProperty,
                       )

from bpy.types import (Panel, PropertyGroup)


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

        layout.separator()
        colSaveDef = layout.column()
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
    # MyProperties,
    OBJECT_PT_DataPathSettings
    # ImportDsData
)

def register():
    from bpy.utils import register_class
    # for cls in classes:
    #     register_class(cls)
    register_class(OBJECT_PT_DataPathSettings)

    # bpy.types.Scene.my_tool = PointerProperty(type=MyProperties)

def unregister():
    from bpy.utils import unregister_class
    # for cls in reversed(classes):
    #     unregister_class(cls)
    unregister_class(OBJECT_PT_DataPathSettings)
    # del bpy.types.Scene.my_tool


if __name__ == "__main__":
    register()