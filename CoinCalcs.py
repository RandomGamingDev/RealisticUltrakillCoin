import math

in_range = lambda n, l, h: l <= n <= h or h <= n <= l

# quick 'n dirty vec class
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

class Coin:
	def __init__(
			self,
			gravity: float, # m/s^2
			starting_pos: Vec2, # Vec2<m>
			starting_vel: Vec2, # Vec2<m/s>
			starting_angle: Vec2, # r
			shooter_pos: Vec2, # Vec2<m>
			coin_reflection_x: float, # m
			target_pos: Vec2 # Vec2<m>
	) -> None:
		self.gravity = gravity
		self.i_pos = starting_pos
		self.i_vel = starting_vel
		self.i_angle = starting_angle
		self.shooter_pos = shooter_pos
		self.reflection_x = coin_reflection_x
		self.target_pos = target_pos

	# Projectile Motion

	def get_starting_pot_y_energy(self) -> float: # J
		return self.i_pos.y * self.gravity + self.i_vel.y ** 2 / 2

	def get_max_y(self) -> float: # m
		return self.get_starting_pot_y_energy() / self.gravity

	def get_time_in_air(self) -> float: # s
		return self.i_vel.y / self.gravity + math.sqrt(2 * self.get_max_y() / self.gravity)

	def get_x_traveled(self) -> float: # m
		return self.i_vel.x * self.get_time_in_air()

	def get_coin_y_at_time(self, t) -> float: # m
		return self.i_pos.y + self.i_vel.y * t - 0.5 * self.gravity * t ** 2

	def get_coin_y_at_x(self, x) -> float: # m
		return self.get_coin_y_at_time((x - self.i_pos.x) / self.i_vel.x)
	
	def get_coin_y_at_reflection(self) -> float: # m
		return self.get_coin_y_at_x(self.reflection_x)
	
	def get_coin_reflection_pos(self) -> Vec2: # m
		return Vec2(self.reflection_x, self.get_coin_y_at_reflection())

	# Mirror Reflection
	def get_laser_in_angle(self): # r
		return (self.get_coin_reflection_pos() - self.shooter_pos).get_angle()

	def get_laser_out_angle(self): # r
		return (self.target_pos - self.get_coin_reflection_pos()).get_angle()
	
	def get_coin_reflection_angle(self): #r
		return (self.get_laser_out_angle() + self.get_laser_in_angle()) / 2
	
	def get_i_angular_vel(self):
		return self.i_vel.x ** 2 * (self.get_coin_reflection_angle() - self.i_angle) / (self.reflection_x - self.i_pos.x)

# Projectile Motion Test Based on https://www.desmos.com/calculator/sxqlmsnuoi
"""
coin = Coin(9.8, Vec2(1, 2), Vec2(2.34, 3.015), 0, Vec2(0, 0), 0, Vec2(0, 0))
print(coin.i_pos)
print(coin.i_vel)
print(coin.gravity)
print(coin.get_starting_pot_y_energy())
print(coin.get_max_y())
print(coin.get_time_in_air())
print(coin.get_coin_y_at_time(1))
print(coin.get_coin_y_at_x(2))
print(coin.get_coin_y_at_x(1.5))
"""

#

# Mirror Reflection Based on https://www.desmos.com/calculator/ztofhfnz61
"""
coin = Coin(9.8, Vec2(0.555, 1.964), Vec2(2.47, 3.062), -4.5, Vec2(0.403, 1.438), 2.12, Vec2(3.83, 1.425))
print(coin.get_coin_reflection_pos())
print(coin.get_laser_in_angle())
print(coin.get_laser_out_angle())
print(coin.get_coin_reflection_angle())
print(coin.get_i_angular_vel())
"""