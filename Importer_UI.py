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


import importlib
import bpy.utils.previews

import sys
import bpy
import os
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, PointerProperty

from bpy.types import Panel, PropertyGroup


class MyProperties(PropertyGroup):
	filePath: StringProperty(
					name="name", 
					description="descrp", 
					default="",
					maxlen=0, 
					subtype='FILE_PATH'
	)



# ------------------------------------------------------------------------
#    Panel in Object Mode
# ------------------------------------------------------------------------



class DSIMPORTER_PT_DsInterface(Panel):
    bl_idname = "DSIMPORTER_PT_DataPathSettings"
    bl_label = "Dark Souls Import"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "Dark Souls Import"
    bl_context = "objectmode"

    def draw(self, context):


        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        layout.separator()
        layout.label(text = "praise the sun!", icon_value=custom_icons["custom_icon"].icon_id)
        layout.operator("dsimporter.importdsdata", text="Import")




 

# ------------------------------------------------------------------------
#    Operator
# ------------------------------------------------------------------------

# class DSIMPORTER_OT_ImportDsData(bpy.types.Operator, ImportHelper):
    # bl_idname = "dsimporter.importdsdata"
    # bl_name = "Import DS Data"
    # bl_label = "Import Mesh"
    # bl_options = {"PRESET"}

    # # filename_ext = ".flver"

    # filter_glob : StringProperty(
        # default="*.flver;*.objbnd;*.partsbnd;*.chrbnd",
        # options={'HIDDEN'},
        # maxlen=255,
        # )

    # filepath: StringProperty(subtype="FILE_PATH")
    
    # def execute(self, context):
        # file = open(self.filepath, 'rb')
        # print(file.name)
        # return {'FINISHED'}

    # def invoke(self, context, event):
        # print(os.path.join(os.path.dirname(__file__)))
        # context.window_manager.fileselect_add(self)
        # return {'RUNNING_MODAL'}

# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

classes = (
    MyProperties,
    DSIMPORTER_PT_DsInterface,
)

def register():
    # load custom icon
    global custom_icons
    custom_icons = bpy.utils.previews.new()
    icons_dir = os.path.join(os.path.dirname(__file__), "icons")
    custom_icons.load("custom_icon", os.path.join(icons_dir, "icon.png"), 'IMAGE')

    # register classes
    from bpy.utils import register_class
    for cls in classes:
        print(cls)
        register_class(cls)

    bpy.types.Scene.my_tool = PointerProperty(type=MyProperties)

def unregister():
    global custom_icons
    bpy.utils.previews.remove(custom_icons)

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    del bpy.types.Scene.my_tool


if __name__ == "__main__":
    register()