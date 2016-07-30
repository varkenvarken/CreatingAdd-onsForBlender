# ##### BEGIN GPL LICENSE BLOCK #####
#
#  Move, a Blender addon
#  (c) 2016 Michel J. Anders (varkenvarken)
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
	"name": "MoveObject",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 20160104121212),
	"blender": (2, 76, 0),
	"location": "View3D > Object > Move",
	"description": "Moves and object",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Object"}

import bpy


class MoveObject(bpy.types.Operator):
    """Moves an object"""
    bl_idname = "object.move_object"
    bl_label = "Move an object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.active_object.location.x += 1
        return {'FINISHED'}


# registering an operator is necessary so the user can find it
# we create a wrapper function here so that we have a single
# point where we can register multiple operators if needed and
# and add operator to menus if desired.
 
def register():
    bpy.utils.register_module(__name__)
    bpy.types.VIEW3D_MT_object.append(menu_func)

# the unregister() function is needed for deinstalling add-ons
def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.VIEW3D_MT_object.remove(menu_func)

def menu_func(self, context):
	self.layout.operator(MoveObject.bl_idname, icon='MESH_CUBE')

if __name__ == "__main__":
    register()
