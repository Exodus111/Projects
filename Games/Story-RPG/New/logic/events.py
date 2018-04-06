from collections import defaultdict
from path import Path

class EventCreator:
	def __init__(self, master):

		self.master = master
		self.flags = {}            ## All flags start as False
		self.blocks = []
		self.room = ""
		self.prev_room = "church main"
		self.poi = {"exit_poi":self.poi_exit,
					"class_poi":self.poi_class_menu}

		# Default Events
		self.playerwait_10 = False
		self.playerwait_20 = False
		self.playerwait_30 = False
		self.player_in_menu = False
		self.player_moving = False
		self.player_outside = False
		self.player_outside_bounds = False
		self.player_outside_bounds_lament = False
		self.in_conversation = False

		# Triggers and timers.
		self.uptime = 0.0 
		self.player_timer = defaultdict(float)
		self.cooldown = {}
		self.trigger = defaultdict(bool) # Defaults as False
		self.trigger["Tutorial"] = False
		self.trigger["game_started"] = False

	def setup_dialogue(self, data):
		self.data = data
		self.flags = self.get_flags()
		self.set_start_flags()

	def get_flags(self):
		flags = {}
		for node in self.data.nodes.keys():
			for tag in self.data.nodes[node].tags:
				if "flag" in tag:
					flags[tag] = False
				elif tag[:4] == "card":
					flags["flag_"+tag] = False
		return flags

	def set_start_flags(self):
		self.trigger["Tutorial"] = True
		self.flags["flag_tutorial_part1"] = True
		self.flags["flag_tutorial_part4"] = False
		self.flags["flag_tutorial_end"] = False
		self.flags["flag_book_lover"] = False
		self.flags["flag_book_liar"] = False
		self.flags["flag_book_joker"] = False
		for npc in self.data.names:
			self.flags["flag_start_"+npc.lower()] = True

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
		if self.trigger["game_started"]:
			self.uptime += dt
			if self.trigger["Tutorial"] and self.check_commenting() and (self.room_check() or self.check_uptime(10)):
				self.tutorial_event_checker()
			self.flag_activators()
		self.time_idles(dt)
		self.check_bounds(dt)

	def flag_activators(self):
		if self.flags["flag_tutorial_part3"]:
			self.flags["flag_tutorial_part3"] = False
			self.master.toggle_classmenu()
		if self.flags["flag_tutorial_part5"]:
			self.flags["flag_tutorial_part5"] = False
			self.flags["flag_tutorial_end"] = True
			self.trigger["Tutorial"] = False

	def check_commenting(self):
		if self.master.gui.commenting != self.trigger["commenting"]:
			self.trigger["commenting"] = self.master.gui.commenting
		if self.trigger["commenting"]:
			return False
		return True

	def check_uptime(self, num):
		return self.uptime > num and self.uptime < num + 1

	def room_check(self):
		if self.prev_room != self.room:
			self.prev_room = self.room
			return True
		return False

	def tutorial_event_checker(self):
		if self.flags["flag_tutorial_part1"] or self.flags["flag_tutorial_part2"]:
			self.master.begin_conv("Tutorial")

	def check_comment_tags(self, tags):
		for tag in tags:
			if tag[:4] == "flag":
				self.flags[tag] = True
			elif tag[:4] == "card":
				self.parent.diag.add_card_to_inventory(tag)

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

	def book_chosen(self, book):
		self.flags["flag_"+book] = True
		self.master.dialogue.add_card_to_inventory("card_"+book)
		self.flags["flag_tutorial_part4"] = True

	def tutorial_over(self): 
		pass