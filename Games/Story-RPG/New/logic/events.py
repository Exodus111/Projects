from collections import defaultdict

class EventCreator:
	def __init__(self):

		self.flags = {}
		self.rooms = {}

		# Default Events
		self.playerwait_10 = False
		self.playerwait_20 = False
		self.playerwait_30 = False
		self.player_in_menu = False
		self.player_moving = False
		self.player_outside_bounds = False
		self.player_outside_bounds_lament = False

		# Triggers and timers.
		self.player_timer = defaultdict(float)
		self.cooldown = {}
		self.trigger = defaultdict(bool)

	def check_cooldown(self, name, duration):
		if name not in self.cooldown.keys():
			self.cooldown[name] = float(duration)
			return True
		elif self.cooldown[name] <= 0.0:
			del(self.cooldown[name])
			return True
		else:
			return False

	def insert_flags(self, flags):
		for flag in flags:
			self.flags[flag] = False

	def insert_rooms(self, rooms):
		for room in rooms:
			self.rooms[room] = False

	def is_in_room(self, room):
		self.room[room] = True

	def left_room(self, room):
		self.room[room] = False

	def update(self, dt):
		self.time_idles(dt)
		self.check_bounds(dt)
		self.timeout_cds(dt)

	def timeout_cds(self, dt):
		for cd in self.cooldown.keys():
			if self.cooldown[cd] > 0:
				self.cooldown[cd] -= dt


	def check_bounds(self, dt):
		if self.player_outside_bounds:
			self.player_timer["out of bounds"] += dt
		else:
			self.player_timer["out of bounds"] = 0.

		if self.player_timer["out of bounds"] > 10.:
			self.player_outside_bounds_lament = True

	def time_idles(self, dt):
		if not self.player_in_menu and not self.player_moving: 
			self.player_timer["player_idle"] += dt
		else:
			self.player_timer["player_idle"] = 0.

		if self.player_timer["player_idle"] > 10.:
			self.playerwait_10 = True
		if self.player_timer["player_idle"] > 20.:
			self.playerwait_20 = True
		if self.player_timer["player_idle"] > 30.:
			if not self.trigger["idle_30"]:
				self.trigger["idle_30"] = True
				self.playerwait_30 = True
			self.player_timer["player_idle"] = 0.

