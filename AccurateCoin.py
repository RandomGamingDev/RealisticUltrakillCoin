# give Python access to Blender's functionality
import bpy
import math

# add a cube into the scene
bpy.ops.mesh.primitive_cube_add()
# get a reference to the currently active object
cube = bpy.context.active_object

for i in range(1, 180):
	cube.location.z = math.sin(i / 50)
	cube.keyframe_insert("location", frame=i)

"""
# insert keyframe at frame one
start_frame = 1
cube.keyframe_insert("location", frame=start_frame)

# change the location of the cube on the z-axis
cube.location.z = 5

# insert keyframe at the last frame
end_frame = 180
cube.keyframe_insert("location", frame=end_frame)
"""