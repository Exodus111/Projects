from datetime import datetime
import json

class WorkTimer:
	def __init__(self, title="No title"):
		self.title = title
		self.primary_timer = 0.0
		self.secondary_timer = 0.0
		self.tertiary_timer = 0.0
		self.start_date = datetime.now()
		self.paused_date = datetime.now()
		self.current_date = datetime.now()
		self.state = "off"
		self.once = True

	def __repr__(self):
		first = "Timer: {}".format(self.primary_timer)
		secondary = "Paused Timer: {}".format(self.secondary_timer)
		third = "Total Pause: {}".format(self.tertiary_timer)
		return "\n".join([self.title, first, second, third])

	def start(self):
		self.state = "on"

	def pause(self):
		if self.state != "paused":
			self.state = "paused"
		else:
			self.state = "on"
			self.tertiary_timer += self.secondary_timer
			self.secondary_timer = 0.0

	def stop(self):
		self.state = "off"
		self.current_date = datetime.now()

	def save(self, directory):
		savedict = {"title":self.title,
					"primary_timer":self.primary_timer,
					"secondary_timer":self.secondary_timer,
					"tertiary_timer":self.tertiary_timer,
					"start_date":self.start_date,
					"current_date":self.current_date}
		with open(directory + self.title, "w+") as outfile:
			json.dump(outfile, savedict)

	def load(self, directory):
		with open(directory + self.title, "r+") as infile:
			loaddict = json.load(infile)
		self.title = loaddict["title"]
		self.primary_timer = loaddict["primary_timer"]
		self.secondary_timer = loaddict["secondary_timer"]
		self.tertiary_timer = loaddict["tertiary_timer"]
		self.current_date = loaddict["current_date"]

	def run(self):
		if self.state == "on":
			self.primary_timer += 1
		elif self.state == "paused":
			self.secondary_timer += 1
