import bpy
import math
import mathutils

# Create a new coin object (a simple cylinder)
bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=0.1, location=(0, 0, 0))
coin = bpy.context.active_object
coin.name = "Coin"

# Function to rotate the coin using quaternions
def rotate_coin(obj, axis, angle_degrees):
    angle_radians = math.radians(angle_degrees)
    rotation_quaternion = mathutils.Quaternion(axis, angle_radians)
    obj.rotation_quaternion = rotation_quaternion + obj.rotation_quaternion # @

# Initialize the coin's rotation quaternion (identity quaternion)
coin.rotation_mode = 'QUATERNION'
coin.rotation_quaternion = mathutils.Quaternion((1, 0, 0, 0))

# Rotate the coin around the x-axis by 45 degrees
rotate_coin(coin, (1, 0, 0), 45)

# Rotate the coin around the y-axis by 30 degrees
#rotate_coin(coin, (0, 1, 0), 30)

# Rotate the coin around the z-axis by 60 degrees
#rotate_coin(coin, (0, 0, 1), 60)

# Update the scene to see the changes
bpy.context.view_layer.update()