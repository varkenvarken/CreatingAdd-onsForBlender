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
	"version": (0, 0, 201607271133),
	"blender": (2, 76, 0),
	"location": "View3D > Add > Mesh > Ladder",
	"description": "Adds a ladder mesh object to the scene",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Add Mesh"}

import bpy
import bmesh
from bpy.props import FloatProperty, IntProperty, BoolProperty
from bpy.app.handlers import persistent

from mathutils import Vector

vertsStile = [(-0.07573,0.03,-0.05),(-0.07573,0.03,0.05),(-0.04975,0.015,-0.05),(-0.04975,0.015,0.05),(-0.04975,-0.015,-0.05),(-0.04975,-0.015,0.05),(-0.07573,-0.03,-0.05),(-0.07573,-0.03,0.05),(-0.1017,-0.015,-0.05),(-0.1017,-0.015,0.05),(-0.1017,0.015,-0.05),(-0.1017,0.015,0.05),(-0.07573,0.03,-0.01667),(-0.07573,0.03,0.01667),(-0.04975,0.015,0.01667),(-0.04975,0.015,-0.01667),(-0.04975,-0.015,0.01667),(-0.04975,-0.015,-0.01667),(-0.07573,-0.03,0.01667),(-0.07573,-0.03,-0.01667),(-0.1017,-0.015,0.01667),(-0.1017,-0.015,-0.01667),(-0.1017,0.015,0.01667),(-0.1017,0.015,-0.01667),]

facesStile = [(13, 1, 3, 14),(14, 3, 5, 16),(16, 5, 7, 18),(18, 7, 9, 20),(20, 9, 11, 22),(22, 11, 1, 13),(10, 23, 12, 0),(23, 22, 13, 12),(8, 21, 23, 10),(21, 20, 22, 23),(6, 19, 21, 8),(19, 18, 20, 21),(4, 17, 19, 6),(17, 16, 18, 19),(2, 15, 17, 4),(0, 12, 15, 2),(12, 13, 14, 15),]

edgesStile = [(2, 0),(13, 1),(1, 3),(15, 2),(4, 2),(3, 5),(17, 4),(6, 4),(5, 7),(19, 6),(8, 6),(7, 9),(21, 8),(10, 8),(9, 11),(23, 10),(0, 10),(11, 1),(0, 12),(12, 13),(3, 14),(14, 15),(5, 16),(16, 17),(7, 18),(18, 19),(9, 20),(20, 21),(11, 22),(22, 23),(23, 12),(22, 13),(21, 23),(20, 22),(19, 21),(18, 20),(17, 19),(16, 18),(15, 17),(14, 16),(12, 15),(13, 14),]

creaseStile = {0: 0.0,1: 0.0,2: 0.0,3: 0.0,4: 0.0,5: 0.0,6: 0.0,7: 0.0,8: 0.0,9: 0.0,10: 0.0,11: 0.0,12: 0.0,13: 0.0,14: 0.0,15: 0.0,16: 0.0,17: 0.0,18: 0.0,19: 0.0,20: 0.0,21: 1.0,22: 0.0,23: 1.0,24: 0.0,25: 0.0,26: 0.0,27: 0.0,28: 0.0,29: 0.0,30: 0.0,31: 0.0,32: 0.0,33: 0.0,34: 0.0,35: 0.0,36: 0.0,37: 0.0,38: 1.0,39: 1.0,40: 0.0,41: 0.0,}

selectedStile = {0: True,1: False,2: True,3: False,4: True,5: True,6: False,7: True,8: True,9: False,10: True,11: True,12: False,13: True,14: True,15: False,16: True,17: True,18: False,19: False,20: False,21: False,22: False,23: False,24: False,25: False,26: False,27: False,28: False,29: False,30: False,31: False,32: False,33: False,34: False,35: False,36: False,37: False,38: False,39: False,40: False,41: False,}

vertsRung = [(0,0.0187,0.01781),(0,0.0187,-0.01552),(0,-0.0113,0.01781),(0,-0.0113,-0.01552),]

edgesRung = [(0, 1),(2, 3),(1, 3),(0, 2),]

def geometry(unit_height, unit_width, repetitions, taper):
	# create a new bmesh
	bm = bmesh.new()

	maxx =  max(v[0] for v in vertsStile)
	offset = unit_width/2 - abs(maxx)
	height = max(v[2] for v in vertsStile) - min(v[2] for v in vertsStile)
	max_height = repetitions * unit_height
	hscale = unit_height / height

	# first the stile segment
	edge_loops = []
	stile_select = set()
	for v in vertsStile:
		bm.verts.new((v[0] - offset, v[1], v[2]))
	bm.verts.ensure_lookup_table()
	bm.verts.index_update()

	for n,e in enumerate(edgesStile):
		edge = bm.edges.new([bm.verts[e[0]],bm.verts[e[1]]])
		edge.select = selectedStile[n] # actually there's no need to keep these edges selected
		if edge.select:
			stile_select.add(e[0])
			stile_select.add(e[1])
		if creaseStile[n]>0 :
			edge_loops.append(n)
	bm.edges.ensure_lookup_table()
	bm.edges.index_update()

	# add a crease layer
	cl = bm.edges.layers.crease.new()
	for n,e in enumerate(bm.edges):
		e[cl] = creaseStile[n] # note the counter intuitive indexing the edge is indexed by the layer

	for f in facesStile:
		bm.faces.new([bm.verts[fi] for fi in f])

	for v in stile_select:
		bm.verts[v].co.z *= hscale

	# then the rung segment, which is just a square of 4 edges with no face
	start_rung_verts = len(bm.verts)
	start_rung_edges = len(bm.edges)

	for v in vertsRung:
		bm.verts.new(v)
	bm.verts.ensure_lookup_table()
	bm.verts.index_update()

	for n,e in enumerate(edgesRung):
		edge = bm.edges.new([bm.verts[e[0]+start_rung_verts], bm.verts[e[1]+start_rung_verts]])
		edge_loops.append(n+start_rung_edges)
	bm.edges.ensure_lookup_table()
	bm.edges.index_update()

	# bridge the 4 edges on the stile with those on the run 
	bmesh.ops.bridge_loops(bm, edges=[bm.edges[e] for e in edge_loops])

	bm.verts.ensure_lookup_table()
	bm.edges.ensure_lookup_table()
	bm.faces.ensure_lookup_table()

	# copying will copy creases as well so we don't have to look at that
	geom_orig = bm.verts[:] + bm.edges[:] + bm.faces[:]
	for rep in range(1,repetitions):
		ret = bmesh.ops.duplicate(bm, geom=geom_orig) # dest param not implemented in 2.76
		for ele in ret["geom"]:
			 if isinstance(ele, bmesh.types.BMVert):
				 ele.co.z += unit_height * rep

	# I am pretty sure that the duplicate bmop has taken care of this but just to be sure
	bm.verts.ensure_lookup_table()
	bm.edges.ensure_lookup_table()
	bm.faces.ensure_lookup_table()

	# make all faces appear smooth
	for f in bm.faces:
		f.smooth = True

	# finally we skew the vertices, but only those that belong to the stiles
	for v in bm.verts:
		vtaper = (v.co.z / max_height) * (taper * 0.01)
		if v.co.x < -0.001:
			v.co.x += vtaper * unit_width/2

	return bm

def updateLadderObject(ob):

	me = ob.data

	# add some geometry. we refer to different prop locations now!
	bm = geometry(	ob.ladder.height,
					ob.ladder.width,
					ob.ladder.rungs,
					ob.ladder.taper)

	# remove doubles (using a 'bmop' saves us from having to switch to edit mode and back later on)
	# we pass a list of all vertices here
	bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.001)

	# write the bmesh to the mesh
	bm.to_mesh(me)
	me.update()
	bm.free()  # free and prevent further access

	# mark object as smooth (example of using ops on active object)
	#bpy.ops.object.shade_smooth()
	
	
	# add mirror modifier and subsurface modifier if needed
	mods = ob.modifiers
	if 'Mirror' not in mods:
		m = mods.new('Mirror','MIRROR')
		m.use_x = True
		m.use_y = False
		m.use_z = False
	if 'Subsurf' not in mods:
		m = mods.new('Subsurf','SUBSURF')
		m.levels = 2
		m.render_levels = 2

def updateLadder(self, context):
	# this function is called from the operator or it is called if the redraw value changes in the panel
	# when called from the panel, self is the active object, otherwise self is the operator but to prevent confusion 
	# we explicitely retrieve the active object 

	ob = context.active_object
	updateLadderObject(ob)

class LadderPropertyGroup(bpy.types.PropertyGroup):
	ladder= BoolProperty(	name="Ladder", default=False)

	taper = FloatProperty(	name="Taper",
							description="Perc. tapering towards top",
							default=0, min=0, max=100,
							subtype='PERCENTAGE',
							update=updateLadder)
	width = FloatProperty(	name="Width",
							description="Width of the ladder",
							default=0.5, min=0.3, soft_max=.6,
							unit='LENGTH',
							update=updateLadder)
	height= FloatProperty(	name="Height",
							description="Step height",
							default=0.3, min=0.1, soft_max=.5,
							unit='LENGTH',
							update=updateLadder)
	rungs = IntProperty(	name="# Rungs",
							description="Number of rungs",
							default=12, min=1, soft_max=30,
							update=updateLadder)

class LadderPropsPanel(bpy.types.Panel):
	bl_label = "Ladder"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"
	bl_category = "Ladder"
	bl_options = set()
	
	@classmethod
	def poll(self, context):
		# Check if we are in object mode (and we are dealing with a ladder object)
		return (	context.mode == 'OBJECT'
				and	(context.active_object is not None)
				and	(context.active_object.ladder is not None)
				and	context.active_object.ladder.ladder	)

	def draw(self, context):
		layout = self.layout
		ob = context.active_object.ladder
		layout.prop(ob, 'width')
		layout.prop(ob, 'height')
		layout.prop(ob, 'rungs')
		layout.prop(ob, 'taper')


class Ladder(bpy.types.Operator):
	"""Add a ladder mesh object to the scene"""
	bl_idname = "mesh.ladder05"
	bl_label = "Ladder"
	bl_options = {'REGISTER', 'UNDO', 'PRESET'}

	@classmethod
	def poll(cls, context):
		return context.mode == 'OBJECT'

	def execute(self, context):
		# create a new empty mesh
		me = bpy.data.meshes.new(name='Ladder')

		# create a new object and identify it as a ladder object
		ob = bpy.data.objects.new('Ladder', me)
		ob.ladder.ladder = True

		# associate the mesh with the object
		ob.data = me

		# link the object to the scene & make it active and selected
		context.scene.objects.link(ob)
		context.scene.update()
		context.scene.objects.active = ob
		ob.select = True

		# create the geometry based on properties in the Ladder panel
		updateLadder(self, context)

		return {'FINISHED'}

@persistent
def update_ladders(scene):
	print("update_ladders", scene, scene.frame_current)
	for ob in scene.objects:
		if hasattr(ob,'ladder'):
			if ob.ladder.ladder:
				print(ob)
				updateLadderObject(ob)
	scene.update()

def register():
	bpy.utils.register_module(__name__)
	# adding a pointer to a propertygroup will cause *every* object in the scene to have a pointer to a possibly empty propertygroup
	# only when assigning to a member of this property group will this propertygroup itself be instantiated
	bpy.types.Object.ladder = bpy.props.PointerProperty(type=LadderPropertyGroup)
	bpy.types.INFO_MT_mesh_add.append(menu_func)
	# add a post frame change handler to update all ladder objects.
	# w.o. it object properties can be animated but will not result in actual changes to the object.
	# (this is a known issue https://developer.blender.org/T48285 )
	bpy.app.handlers.frame_change_post.append(update_ladders)

def unregister():
	bpy.utils.unregister_module(__name__)
	bpy.types.INFO_MT_mesh_add.remove(menu_func)
	bpy.app.handlers.frame_change_post.remove(update_ladders)
	bpy.utils.unregister_module(__name__)
	
def menu_func(self, context):
	self.layout.operator(Ladder.bl_idname, icon='PLUGIN')
