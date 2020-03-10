import importlib
import bpy.utils.previews

import sys
import bpy
import os
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, PointerProperty, BoolProperty

from bpy.types import Panel, PropertyGroup


class MyProperties(PropertyGroup):
	filePath: StringProperty(
					name="name", 
					description="descrp", 
					default="",
					maxlen=0, 
					subtype='FILE_PATH'
	)

	useCollections: BoolProperty(
					name="Use Collections?", 
					description="Move each imported mesh into its own collection", 
					default=True
	)
	
	useLegacyNodes: BoolProperty(
					name="Use Legacy Nodes?", 
					description="Use legacy nodes in shader graph (as opposed to Principled BSDF)", 
					default=False
	)


# custom GUI element
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
        
        colOpts = layout.column()
        colOpts.prop(scene.my_tool, "useCollections")
        colOpts.prop(scene.my_tool, "useLegacyNodes")
        layout.separator()
        layout.label(text = "Praise the Sun!", icon_value=custom_icons["custom_icon"].icon_id)
        layout.operator("dsimporter.importdsdata", text="Import")


# register everything ------------------------------------

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