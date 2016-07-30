# ##### BEGIN GPL LICENSE BLOCK #####
#
#  Circle, a Blender addon
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
	"name": "CircleObjects",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 201601061418),
	"blender": (2, 76, 0),
	"location": "View3D > Object > Circle",
	"description": "Arranges selected objects in a circle",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Object"}

import bpy
from mathutils import Vector
from bpy.props import FloatProperty
from bpy.props import FloatVectorProperty
from bpy.props import EnumProperty

class CircleObjects(bpy.types.Operator):
	"""Arrange selected objects in a circle in the xy plane"""
	bl_idname = "object.circle_objects"
	bl_label = "Circle objects"
	bl_options = {'REGISTER', 'UNDO'}

	scale = 100

	@classmethod
	def poll(cls, context):
		return (	(len(context.selected_objects) > 2) 
				and (context.mode == 'OBJECT')	)

	def execute(self, context):
		xyz = [ob.location for ob in context.selected_objects]
		center = sum(xyz, Vector()) / len(xyz)
		radius = sum((loc.xy - center.xy).length for loc in xyz)
		radius /= len(xyz)
		for loc, ob in zip(xyz, context.selected_objects):
			direction = (loc.xy - center.xy).normalized().to_3d()
			ob.location = center + self.scale * 0.01 * radius * direction
		return {'FINISHED'}

preview_collections = {}

def load_icon():
	import os
	import bpy
	import bpy.utils
	
	try: # if anything goes wrong, for example because we are not running 2.75+ we just ignore it
		import bpy.utils.previews
		pcoll = bpy.utils.previews.new()
		# the path is calculated relative to this py file inside the addon folder
		my_icons_dir = os.path.join(os.path.dirname(__file__), "icons")
		# load a preview thumbnail of the circle icon
		pcoll.load("circle_icon", os.path.join(my_icons_dir, "circle32.png"), 'IMAGE')
		preview_collections['icons'] = pcoll
	except Exception as e:
		pass

def register():
	load_icon()
	bpy.utils.register_module(__name__)
	bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
	bpy.utils.unregister_module(__name__)
	bpy.types.VIEW3D_MT_object.remove(menu_func)
	for pcoll in preview_collections.values():
		bpy.utils.previews.remove(pcoll)
	preview_collections.clear()

def menu_func(self, context):
	if 'icons' in preview_collections:
		self.layout.operator(CircleObjects.bl_idname, 
			icon_value=preview_collections['icons']['circle_icon'].icon_id)
	else:
		self.layout.operator(CircleObjects.bl_idname, icon='PLUGIN')

if __name__ == "__main__":
	register()
