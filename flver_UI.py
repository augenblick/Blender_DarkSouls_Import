import bpy


class DSPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Dark Souls Panel"
    bl_idname = "OBJECT_PT_DS"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = ""

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.label(text="Import Dark Souls Model:", icon='WORLD_DATA')

        row = layout.row()

        row = layout.row()
        row.operator("mesh.import")


def register():
    bpy.utils.register_class(DSPanel)


def unregister():
    bpy.utils.unregister_class(DSPanel)


if __name__ == "__main__":
    register()
