# ##### BEGIN GPL LICENSE BLOCK #####
#
#  Ladder, a Blender addon
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
	"name": "Ladder",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 201601071058),
	"blender": (2, 76, 0),
	"location": "View3D > Add > Mesh > Ladder",
	"description": "Adds a ladder mesh object to the scene",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Add Mesh"}

import bpy
import bmesh
from bpy.props import FloatProperty, IntProperty
from mathutils import Vector

verts = [
(1.0000, -2.0000, -3.0000),
(1.0000, -4.0000, -3.0000),
(-1.0000, -4.0000, -3.0000),
(-1.0000, -2.0000, -3.0000),
(1.0000, -2.0000, -1.0000),
(1.0000, -4.0000, -1.0000),
(-1.0000, -4.0000, -1.0000),
(-1.0000, -2.0000, -1.0000),
(1.0000, -4.0000, 1.0000),
(1.0000, -2.0000, 1.0000),
(-1.0000, -2.0000, 1.0000),
(-1.0000, -4.0000, 1.0000),
(1.0000, -4.0000, 3.0000),
(1.0000, -2.0000, 3.0000),
(-1.0000, -2.0000, 3.0000),
(-1.0000, -4.0000, 3.0000),
(0.0000, -2.0000, -3.0000),
(0.0000, -4.0000, -3.0000),
(0.0000, -2.0000, -1.0000),
(0.0000, -4.0000, -1.0000),
(0.0000, -2.0000, 1.0000),
(0.0000, -4.0000, 1.0000),
(0.0000, -2.0000, 3.0000),
(0.0000, -4.0000, 3.0000),
(1.0000, -4.0000, 0.0000),
(-1.0000, -4.0000, 0.0000),
(-1.0000, -2.0000, 0.0000),
(1.0000, -2.0000, 0.0000),
(0.0000, -4.0000, 0.0000),
(1.0000, 0.0000, 0.0000),
(0.0000, 0.0000, 1.0000),
(0.0000, 0.0000, -1.0000),
(-1.0000, 0.0000, 0.0000)]

faces = [( 28,24,8,21 ),
( 0,4,5,1 ),
( 17,19,6,2 ),
( 2,6,7,3 ),
( 18,16,3,7 ),
( 10,11,15,14 ),
( 27,4,18 ),
( 26,25,11,10 ),
( 24,27,9,8 ),
( 8,9,13,12 ),
( 21,8,12,23 ),
( 20,10,14,22 ),
( 9,20,22,13 ),
( 11,21,23,15 ),
( 10,20,26 ),
( 4,0,16,18 ),
( 1,5,19,17 ),
( 25,28,21,11 ),
( 6,19,28,25 ),
( 20,9,27 ),
( 5,4,27,24 ),
( 7,6,25,26 ),
( 26,20,30,32 ),
( 19,5,24,28 ),
( 18,7,26 ),
( 20,27,29,30 ),
( 27,18,31,29 ),
( 18,26,32,31 ) ]

def geometry(verts, faces, unit_height, unit_width, repetitions, taper):
	# create a new bmesh
	bm = bmesh.new()

	width =  max(v[1] for v in verts) - min(v[1] for v in verts)
	height = max(v[2] for v in verts) - min(v[2] for v in verts)
	max_height = repetitions * unit_height
	wscale = unit_width / (width/2)
	hscale = unit_height / height

	start_index = 0
	for rep in range(repetitions):
		for v_co in verts:
			h = (v_co[2] + rep * height) * hscale
			vtaper = 1 - (h / max_height) * (taper * 0.01)
			bm.verts.new((v_co[0]*hscale, v_co[1]*wscale*vtaper, h))

		bm.verts.ensure_lookup_table()
		for f_idx in faces:
			bm.faces.new([bm.verts[i + start_index] for i in f_idx])

		start_index = len(bm.verts)

	return bm

class Ladder(bpy.types.Operator):
	"""Add a ladder mesh object to the scene"""
	bl_idname = "mesh.ladder"
	bl_label = "Ladder"
	bl_options = {'REGISTER', 'UNDO', 'PRESET'}

	taper = FloatProperty(name="Taper", description="Perc. tapering towards top", default=0, min=0, max=100, subtype='PERCENTAGE')
	width = FloatProperty(name="Width", description="Width of the ladder", default=0.5, min=0.3, soft_max=.6, unit='LENGTH')
	height= FloatProperty(name="Height", description="Step height", default=0.3, min=0.1, soft_max=.5, unit='LENGTH')
	rungs = IntProperty(name="# Rungs", description="Number of rungs", default=12, min=1, soft_max=30)

	@classmethod
	def poll(cls, context):
		return context.mode == 'OBJECT'

	def execute(self, context):
		# create a new empty mesh
		me = bpy.data.meshes.new(name='Ladder')

		# create a new object
		ob = bpy.data.objects.new('Ladder', me)

		# add some geometry
		bm = geometry(	verts, faces,
						self.height,
						self.width,
						self.rungs,
						self.taper)

		# remove doubles (using a 'bmop' saves us from having to switch to edit mode and back later on)
		# we pass a list of all vertices here
		bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.001)

		# TODO add a uv-map (two ways: mark seams and unwrap, or DIY layer
		
		# write the bmesh to the mesh
		bm.to_mesh(me)
		me.update()
		bm.free()  # free and prevent further access

		# associate the mesh with the object
		ob.data = me

		# link the object to the scene & make it active and selected
		context.scene.objects.link(ob)
		context.scene.update()
		context.scene.objects.active = ob
		ob.select = True

		# mark object as smooth (example of using ops on active object)
		bpy.ops.object.shade_smooth()

		# add mirror modifier and subsurface modifier
		mods = ob.modifiers
		m = mods.new('Mirror','MIRROR')
		m.use_x = False
		m.use_y = True
		m.use_z = False
		m = mods.new('Subsurf','SUBSURF')
		m.levels = 2
		m.render_levels = 2

		# TODO add material

		return {'FINISHED'}

def register():
	bpy.utils.register_module(__name__)
	bpy.types.INFO_MT_mesh_add.append(menu_func)

def unregister():
	bpy.utils.unregister_module(__name__)
	bpy.types.INFO_MT_mesh_add.remove(menu_func)

def menu_func(self, context):
	self.layout.operator(Ladder.bl_idname, icon='PLUGIN')
