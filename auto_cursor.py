# coding: utf-8
bl_info = {
    "name": "Auto-Cursor",
    "description": "Make 3D cursor follow parented object/bone of active Grease Pencil layer (background Modal operator)",
    "author": "Samuel Bernou",
    "version": (0, 0, 1),
    "blender": (2, 79, 0),
    "location": "View3D > Toolbar > Grease Pencil > Auto Cursor",
    "warning": "",
    "wiki_url": "",
    "category": "Object" }


import bpy
import os
import re, fnmatch, glob
from mathutils import Matrix
from bpy.app.handlers import persistent

def getMatrix (layer) :
    matrix = Matrix.Identity(4)

    if layer.is_parented:
        if layer.parent_type == 'BONE':

            object = layer.parent
            bone = object.pose.bones[layer.parent_bone]
            matrix = bone.matrix * object.matrix_world
            matrix = matrix.copy()# * layer.matrix_inverse
        else :
            matrix = layer.parent.matrix_world

    return matrix.copy()


class gpTools_AC_props(bpy.types.PropertyGroup):
    auto_cursor = bpy.props.BoolProperty(name="Auto Cursor", description="Cursor follow parented object/bones", default=False)
    auto_track_loc_only = bpy.props.BoolProperty(name="Track translate only", description="Follow location only", default=False)

class AutoCursor(bpy.types.Operator):
    """Move cursor automagically when changing frame with parented layer selected"""
    bl_idname = "gptools.auto_cursor"
    bl_label = "Auto cursor"

    #bpy.types.Scene.auto_track_loc_only = bpy.props.BoolProperty(name="Track translate only", description="Deplace le curseur seulement en translation (ne tient pas compte de rotations/echelle)", default=False)

    def modal(self, context, event):

        gp = context.scene.grease_pencil
        settings = context.scene.gptoolset
        if event.type == "F9" : #(F8 : stop, next press reload all-addons) #F9 best for test
            print('Auto-cursor Modal stopped')
            return {'CANCELLED'}

        if not settings.auto_cursor or not gp or not gp.layers.active or not gp.layers.active.parent:# or bpy.context.screen.is_animation_playing:
            self.pre = None
            return {'PASS_THROUGH'}

        parent = gp.layers.active.parent

        if gp.layers.active != self.current_layer :#update on active layer change
            self.pre = cur =  getMatrix(gp.layers.active)
            self.current_layer = gp.layers.active
            return {'PASS_THROUGH'}

        if parent:#if no parent, do nothing
            if context.scene.frame_current != self.current_frame :#update on frame change
                cur = getMatrix(gp.layers.active)

                if self.pre:
                    if self.pre != cur:
                        if settings.auto_track_loc_only:#translation only
                            context.scene.cursor_location += (cur - self.pre).to_translation()
                        else:#full matrix
                            context.scene.cursor_location = cur * (self.pre.inverted() * context.scene.cursor_location)

                        self.pre = cur

                else:
                    self.pre = getMatrix(self.current_layer)

                self.current_frame = context.scene.frame_current
                return {'PASS_THROUGH'}

        return {'PASS_THROUGH'}


    def invoke(self, context, event):
        print('Auto-cursor Modal launched')
        gp = context.scene.grease_pencil
        if gp and gp.layers and gp.layers.active and gp.layers.active.parent:
            self.current_layer = gp.layers.active
            self.pre = gp.layers.active.parent.matrix_world.copy()

        else :
            self.current_layer = None
            self.pre = None
        self.current_frame = context.scene.frame_current

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}



class AutoCursor_PT(bpy.types.Panel):
    bl_idname = "auto_cursor_panel"
    bl_label = "Auto Cursor"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Grease Pencil"

    def draw(self, context):
        layout = self.layout
        #layout.operator("gptools.auto_cursor", text = "Start auto cursor modal", icon = 'PLAY')
        row = layout.row(align = True)
        row.prop(context.scene.gptoolset, "auto_cursor", text = "Auto Cursor", icon = "CURSOR")
        #row.prop(context.scene.gptoolset, "auto_track_loc_only", text = "Location only")
        row.prop(context.scene.gptoolset, "auto_track_loc_only", text = "Location only", icon = "NDOF_DOM")

@persistent
def load_handler(dummy):
    bpy.ops.gptools.auto_cursor('INVOKE_DEFAULT')

def register():
    bpy.utils.register_module(__name__)

    # bpy.utils.register_class(gpTools_AC_props)
    bpy.types.Scene.gptoolset = bpy.props.PointerProperty(type=gpTools_AC_props)
    # bpy.utils.register_class(AutoCursor)
    # bpy.utils.register_class(AutoCursor_PT)
    bpy.app.handlers.load_post.append(load_handler)

def unregister():

    bpy.app.handlers.load_post.remove(load_handler)
    # bpy.utils.unregister_class(AutoCursor_PT)
    # bpy.utils.unregister_class(AutoCursor)
    del bpy.types.Scene.gptoolset
    # bpy.utils.unregister_class(gpTools_AC_props)

    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
