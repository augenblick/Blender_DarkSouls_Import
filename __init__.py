# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
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
    'name': 'Dark Souls Importer',
    "description": "Imports Dark Souls environment, character, and object models from unpacked game data files",
    "author": "Nathan Grubbs",
    "location": "3D Viewport > 'N' Toolbar > Dark Souls Importer",
    'category': 'Import-Export',
    'version': (0, 2, 0),
    'blender': (2, 80, 0)
}

import sys
import os
import importlib
import bpy
import bpy.utils.previews
icons_dict = bpy.utils.previews.new()


class AddDsPresets(bpy.types.AddonPreferences):
    bl_idname = __package__

    tpfPath: bpy.props.StringProperty(
        default = "",
        name = "",
        description = "The directory containing unpacked Dark Souls .tpf files.  (Typically something like 'C:\\Program Files (x86)\\Steam\\SteamApps\\common\\Dark Souls Prepare to Die Edition\\DATA\\map\\tx')",
        maxlen = 0,
        subtype = 'DIR_PATH'
        )
    ddsPath: bpy.props.StringProperty(
        default = "",
        name = "",
        description = "The directory in which .dds texture files will be extracted and stored.  This can be a newly created directory or an existing one.",
        maxlen = 0,
        subtype = 'DIR_PATH'
        #todo: fill in other info
        )

    missingTexPath: bpy.props.StringProperty(
        default = "",
        name = "",
        description = "An image file to be use in the place of missing textures. (optional)",
        maxlen = 0,
        subtype = 'FILE_PATH'
        #todo: fill in other info
        )

    # create preferences panel of addons window
    def draw(self, context):
        layout = self.layout
        layout.label(text='Directory containing .tpf files:')
        colTpf = layout.column()
        colTpf.prop(self, 'tpfPath', expand = True)

        layout.label(text='Directory in which to store .dds files:')
        colDds = layout.column()
        colDds.prop(self, 'ddsPath', expand = False)

        layout.label(text="Path to 'Missing Texture' file:")
        colTex = layout.column()
        colTex.prop(self, 'missingTexPath', expand = False)

modulesNames = ['Importer_UI', 'Importer', 'GetOffsets']


modulesFullNames = {}
for currentModuleName in modulesNames:
    if 'DEBUG_MODE' in sys.argv:
        modulesFullNames[currentModuleName] = ('{}'.format(currentModuleName))
    else:
        modulesFullNames[currentModuleName] = ('{}.{}'.format(__name__, currentModuleName))
 
for currentModuleFullName in modulesFullNames.values():
    if currentModuleFullName in sys.modules:
        importlib.reload(sys.modules[currentModuleFullName])
    else:
        globals()[currentModuleFullName] = importlib.import_module(currentModuleFullName)
        setattr(globals()[currentModuleFullName], 'modulesNames', modulesFullNames)
 
def register():
    bpy.utils.register_class(AddDsPresets)
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'register'):
                sys.modules[currentModuleName].register()

 
def unregister():
    bpy.utils.unregister_class(AddDsPresets)
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'unregister'):
                sys.modules[currentModuleName].unregister()
 
if __name__ == "__main__":
    register()