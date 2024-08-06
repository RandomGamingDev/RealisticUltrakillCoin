# give Python access to Blender's functionality
import bpy
import math
import mathutils
from mathutils import Euler, Vector

in_range = lambda n, l, h: l <= n <= h or h <= n <= l

def f_range(start, stop, increment):
	while start <= stop + 1e-4:
		yield start
		start += increment

# quick 'n dirty vec classes
class Vec2:
	def __init__(self, x: float, y: float) -> None:
		self.x = x
		self.y = y

	def __add__(self, o):
		return Vec2(self.x + o.x, self.y + o.y)

	def __sub__(self, o):
		return Vec2(self.x - o.x, self.y - o.y)
	
	def get_angle(self) -> float:
		return math.atan2(self.y, self.x)
	
	def __str__(self) -> str:
		return f"({ self.x }, { self.y })"
class Vec3:
	def __init__(self, x: float, y: float, z: float) -> None:
		self.x = x
		self.y = y
		self.z = z

	def get_xy(self):
		return Vec2(self.x, self.y)

	def get_yz(self):
		return Vec2(self.y, self.z)
	
	def get_xz(self):
		return Vec2(self.x, self.z)

	def get_zy(self):
		return Vec2(self.z, self.y)

	def __add__(self, o):
		return Vec3(self.x + o.x, self.y + o.y, self.z + o.z)

	def __sub__(self, o):
		return Vec3(self.x - o.x, self.y - o.y, self.z - o.z)
	
	def __str__(self) -> str:
		return f"({ self.x }, { self.y }, { self.z })"

class Coin:
	def __init__(
			self,
			gravity: float, # m/s^2
			starting_pos: Vec3, # Vec3<m>
			starting_vel: Vec3, # Vec3<m/s>
			starting_angle: Vec3, # r
			shooter_pos: Vec3, # Vec3<m>
			coin_reflection_x: float, # m
			target_pos: Vec3 # Vec3<m>
	) -> None:
		self.gravity = gravity
		self.i_pos = starting_pos
		self.i_vel = starting_vel
		self.i_angle = starting_angle
		self.shooter_pos = shooter_pos
		self.reflection_x = coin_reflection_x
		self.target_pos = target_pos

	# Projectile Motion

	def get_starting_y_energy(self) -> float: # J
		return self.i_pos.y * self.gravity + self.i_vel.y ** 2 / 2

	def get_max_y(self) -> float: # m
		return self.get_starting_y_energy() / self.gravity

	def get_time_in_air(self) -> float: # s
		return self.i_vel.y / self.gravity + math.sqrt(2 * self.get_max_y() / self.gravity)

	def get_x_traveled(self) -> float: # m
		return self.i_vel.x * self.get_time_in_air()

	def get_z_traveled(self) -> float: # m
		return self.i_vel.z * self.get_time_in_air()

	def get_x_at_time(self, t) -> float: # m
		return t * self.i_vel.x + self.i_pos.x

	def get_z_at_time(self, t) -> float: # m
		return t * self.i_vel.z + self.i_pos.z

	def get_y_at_time(self, t) -> float: # m
		return self.i_pos.y + self.i_vel.y * t - 0.5 * self.gravity * t ** 2

	def get_time_at_x(self, x) -> float: # m
		return (x - self.i_pos.x) / self.i_vel.x

	def get_time_at_z(self, z) -> float: # m
		return (z - self.i_pos.z) / self.i_vel.z

	def get_y_at_x(self, x) -> float: # m
		return self.get_y_at_time(self.get_time_at_x(x))
	
	def get_y_at_z(self, z) -> float: # m
		return self.get_y_at_time(self.get_time_at_z(z))

	def get_z_at_x(self, x) -> float: # m
		return self.get_z_at_time(self.get_time_at_x(x))

	def get_y_at_reflection(self) -> float: # m
		return self.get_y_at_x(self.reflection_x)
	
	def get_z_at_reflection(self) -> float: # m
		return self.get_z_at_x(self.reflection_x)

	def get_reflection_pos(self) -> Vec3: # m
		return Vec3(self.reflection_x, self.get_y_at_reflection(), self.get_z_at_reflection())

	# Mirror Reflection
	def get_laser_in_x_angle(self) -> float: # r
		return (self.get_reflection_pos() - self.shooter_pos).get_xy().get_angle()

	def get_laser_in_z_angle(self) -> float: # r
		return (self.get_reflection_pos() - self.shooter_pos).get_zy().get_angle()

	def get_laser_out_x_angle(self) -> float: # r
		return (self.target_pos - self.get_reflection_pos()).get_xy().get_angle()
	
	def get_laser_out_z_angle(self) -> float: # r
		return (self.target_pos - self.get_reflection_pos()).get_zy().get_angle()

	def get_reflection_x_angle(self) -> float: # r
		return (self.get_laser_out_x_angle() + self.get_laser_in_x_angle()) / 2
	
	def get_reflection_z_angle(self) -> float: # r
		return (self.get_laser_out_z_angle() + self.get_laser_in_z_angle()) / 2

	def get_i_x_angular_vel(self) -> float: # r / s
		return self.i_vel.x ** 2 * (self.get_reflection_x_angle() - self.i_angle.x) / (self.reflection_x - self.i_pos.x)

	def get_i_z_angular_vel(self) -> float: # r / s
		return self.i_vel.z ** 2 * (self.get_reflection_z_angle() - self.i_angle.z) / (self.get_z_at_reflection() - self.i_pos.z)
	
	# Combined
	def get_x_rotation_at_time(self, t) -> float: # r
		return self.i_angle.x + t * self.get_i_x_angular_vel() / self.i_vel.x

	def get_z_rotation_at_time(self, t) -> float: # r
		return self.i_angle.z + t * self.get_i_z_angular_vel() / self.i_vel.z



coin = Coin(9.8, Vec3(0.555, 1.964, 0.555), Vec3(2.47, 3.062, 2.47), Vec3(-4.5, 0, -4.5), Vec3(0.403, 1.438, 0.403), 2.12, Vec3(3.83, 1.425, 3.83))
#print(coin.get_x_rotation_at_time(1))
#print(coin.get_z_rotation_at_time(1))

# get a reference to the currently active object
obj = bpy.context.active_object.copy()
bpy.context.collection.objects.link(obj)

i = 1
num_steps = 30
for t in f_range(0, coin.get_time_in_air(), coin.get_time_in_air() / (num_steps - 1)):
	#obj.location.x = coin.get_x_at_time(t)
	#obj.location.z = coin.get_y_at_time(t)
	obj.location = Vector((coin.get_x_at_time(t), coin.get_z_at_time(t), coin.get_y_at_time(t)))
	obj.keyframe_insert("location", frame=i)
	#obj.rotation_euler.y = coin.get_rotation_at_time(t)
	obj.rotation_euler = Euler((coin.get_x_rotation_at_time(t), 0, coin.get_z_rotation_at_time(t)), 'YZX')
	obj.keyframe_insert("rotation_euler", frame=i)

	i += 1

# x and y rotation