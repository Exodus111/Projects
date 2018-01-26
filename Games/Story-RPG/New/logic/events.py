from collections import defaultdict
from path import Path

class EventCreator:
	def __init__(self, master):

		self.master = master
		self.flags = {}
		self.room = ""
		self.prev_room = ""
		self.poi = {"exit_poi":self.poi_exit,
					"class_poi":self.poi_class_menu,
					"start_poi":self.poi_start
					}

		# Default Events
		self.playerwait_10 = False
		self.playerwait_20 = False
		self.playerwait_30 = False
		self.player_in_menu = False
		self.player_moving = False
		self.player_outside = False
		self.player_outside_bounds = False
		self.player_outside_bounds_lament = False

		# Triggers and timers.
		self.uptime = 0.0 
		self.player_timer = defaultdict(float)
		self.cooldown = {}
		self.trigger = defaultdict(bool) # Defaults as False
		self.trigger["Tutorial"] = True		

	def save(self, player_pos): # Not tested, should work.
		savedict = {"player_pos":player_pos, "flags":[]}
		for flag in self.flags.keys():
			if self.flags[flag]:
				savedict["flags"].append(flag)
		counter = len(Path("/saves").files("savefile*.*"))
		counter += 1
		with open("/saves/savefile{}.json".format(counter), "w+") as f:
			json.dump(f, savedict)

	def check_cooldown(self, name, duration):
		if name not in self.cooldown.keys():
			self.cooldown[name] = self.uptime + float(duration)
			self.trigger[name] = True
			return True
		elif self.cooldown[name] < self.uptime and self.trigger[name]:
			self.trigger[name] = not self.trigger[name]
			return True
		elif self.cooldown[name] < self.uptime - float(duration):
			del(self.cooldown[name])
		else:
			return False

	def add_cooldown(self, name, duration):
		self.cooldown[name] = self.uptime + float(duration)

	def if_cooldown(self, name):
		if name in self.cooldown.keys():
			return self.cooldown[name] < self.uptime
		else:
			return False

	def reset_cooldown(self, name):
		if name in self.cooldown.keys():
			del(self.cooldown[name])

	def insert_flags(self, flags):
		for flag in flags:
			self.flags[flag] = False

	def update(self, dt):
		self.uptime += dt
		if self.prev_room != self.room:
			if self.trigger["Tutorial"]:
				if self.room == "church main" and self.playerwait_10:
					self.tutorial_start(1)
				elif self.room == "church thack_room":
					self.tutorial_start(2)
			self.prev_room = self.room
		self.time_idles(dt)
		self.check_bounds(dt)

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

	def activate_poi(self, poi):
		if poi.name in self.poi.keys():
			self.poi[poi.name]()

	def poi_class_menu(self):
		if self.trigger["class_menu"]:
			self.master.toggle_classmenu()
			self.trigger["class_menu"] = False

	def poi_exit(self):
		pass

	def tutorial_start(self, section):  ## DONE. Now write the rest of the tutorial!
		if section == 1:
			self.master.begin_conv("Tutorial")  ## Opening.
		elif section == 2:
			pass ## Expostion and class selection.
		elif section == 3:
			pass ## Turn Tutorial off.

