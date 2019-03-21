import json
from path import Path

def main(filename):
	with open(filename, "r+") as f:
		filedict = json.load(f)
	# Flags first
	flags = fetch_items(filedict, "flag")
	display_item(flags)
	# Second Cards.
	cards = fetch_items(filedict, "card")
	display_item(cards)

def display_item(itemdict):
	for name in itemdict.keys():
		print("\n", name, "\n")
		mylist = list(set(itemdict[name]))
		for flag in mylist:
			print(flag)

def fetch_items(filedict, t):
	flagdict = {}
	for name in filedict["names"]:
		flaglist = []
		for node in filedict["nodes"][name]:
			flags_in_node = [tag for tag in filedict["tags"][node] if t in tag]
			flaglist += flags_in_node
		flagdict[name] = flaglist
	return flagdict

if __name__ == "__main__":
	main("/home/aurelio/Projects/Games/Story-RPG/New/data/dialogue/dialogue.json")



