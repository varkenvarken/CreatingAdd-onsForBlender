from random import random
import bpy
import bmesh

C = bpy.context

bm = bmesh.new()

bm.from_mesh(C.object.data)
bm.faces.ensure_lookup_table()

vcolor = bm.loops.layers.color.active
if vcolor is None:
    vcolor = bm.loops.layers.color.new()
    
for face in bm.faces:
    color = (random(), random(), random())
    for loop in face.loops:
        loop[vcolor] = color

bm.to_mesh(C.object.data)
bm.free()

for w in C.window_manager.windows:
    for a in w.screen.areas:
        if a.type == 'VIEW_3D':
            a.tag_redraw()