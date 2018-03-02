#!/usr/bin/python3
import json

class Dialogue:
	"""
		Keys: names, text, nodes, links, coords, tags
	"""
	def __init__(self, dialoguedict):
		self.nodes = self.assemble_nodes(dialoguedict)
		self.starts = self.gather_nodes("greeting")
		self.comment_starts = self.gather_nodes("start")

##### Init Methods.

	def assemble_nodes(self, _dict):
		node_dict = {}
		for name in _dict["names"]:
			for node in _dict["nodes"][name]:
				tags = self.fix_tags(_dict["tags"][node])
				n = Node(node, name, _dict["text"][node], _dict["links"][node], tags, _dict["coords"])
				n.type = "comment"*any([(t in ("comment", "comment_reply", "start")) for t in tags]) or "dialogue"
				node_dict[node] = n
		return node_dict

	def fix_tags(self, tags):
		taglist = []
		for tag in tags:
			tag = tag.lower()
			tag = tag.strip()
			taglist.append(tag)
		return taglist

	def gather_nodes(self, pat):
		nodelist = []
		for node in self.nodes.keys():
			if pat in self.nodes[node].tags:
				nodelist.append(self.nodes[node])
		return nodelist

#### Public Methods.

	def next_nodes(self, node):
		next_nodes = []
		for n in node.links:
			if node.coords[0] < self.nodes[n].coords[0]:
				next_nodes.append(self.nodes[n])
		return next_nodes

	def find_node(self, node_id=None, text=None):
		if node_id:
			return self.nodes[node_id]
		elif text:
			for node in self.nodes.keys():
				if text == self.nodes[node].text:
					return self.nodes[node]
		else:
			return None

class Node():
	def __init__(self, node, npc, text, links, tags, coords):
		self.node = node
		self.npc = npc
		self.text = text
		self.links = links
		self.tags = tags
		self.coords = coords

	def __repr__(self):
		return self.text
		
class Events:
	def __init__(self, dialogue):
		self.data = dialogue
		self.flags = self.get_flags()
		self.blocks = []
		self.set_start_flags()

	def get_flags(self):
		flags = {}
		for node in self.data.nodes.keys():
			for tag in self.data.nodes[node].tags:
				if "flag" in tag:
					flags[tag] = False
		return flags

	def set_start_flags(self):
		self.flags["flag_tutorial"] = True
		for npc in self.data.names:
			self.flags["flag_start_"+npc] = True

class DialogueSystem:
	def __init__(self, events, dialoguedata):
		self.dialogue = dialoguedata
		self.events = events
		self.callback_list = []
		self.current_answer = None
		self.current_questions = None
		self.current_comment = None

### Starting Conversations.
	def start_conversation(self, npc):
		node = None
		for meth in (find_conversation, find_comment, find_busy):
			node = meth(npc)
			if node != None:
				break
		self.setup_conversation(node)

	def find_conversation(self, npc):
		for start in self.dialogue.starts:
			if start.npc.lower() == npc.lower():
				for tag in start.tags:
					if "block" in tag:
						if not self.blocked(tag):
							return start
		else:
			return None

	def find_busy(self, npc):
		for comment in self.dialogue.comment_starts:
			if npc == comment.npc and "busy" in comment.tags:
				return comment
		raise Exception("Busy comment missing. Something went wrong. NPC: "+npc)

	def find_comment(self, npc):
		for comment in self.dialogue.comment_starts:
			if npc == comment.npc:
				for tag in comment.tags:
					if "block" in tag:
						if not self.blocked(tag):
							return comment
		return None 

### Setting up a conversation.
	def setup_conversation(self, node):
		if node.type == "dialogue":
			self.current_answer = node
			self.current_questions = self.get_questions(node)
		elif node.type == "comment":
			self.current_comment = node

	def get_questions(self, node):
		nodelist = self.dialogue.next_nodes(node)
		nodelist = self.check_for_blocks(nodelist)
		if len(nodelist) == 1:
			if "question" in nodelist[0].tags:
				return nodelist
		elif len(nodelist) > 1:
			return nodelist
		return None

	def check_for_blocks(self, nodelist):
		return [i for i in nodelist if not self.blocked(i)]

	def blocked(self, tag):
		flag = tag.replace("block", "flag")
		if self.events.flags[flag]:
			if tag not in self.events.blocks:
				self.events.blocks.append(tag)
				return False
		return True

	def next_step(self, next_type, text=None):
		if next_type == "question":
			node = self.dialogue.find_node(text=text)
			node = self.check_tags(node)
		elif next_type == "answer":
			node = self.current_answer
		elif next_type == "comment":
			node = self.current_comment
		next_node = self.dialogue.next_nodes(node)[0]
		self.check_tags(next_node)
		self.setup_conversation(next_node)

	def check_tags(self, node):
		for tag in node.tags:
			if "flag" in tag:
				self.events.flags[tag] = True
			elif "card" in tag:
				self.add_card_to_inventory(tag) # To be continued.
			elif "save" in tag:
				self.callback_list.append(node)
			elif "back" in tag:
				saved = tag.replace("back", "save")
				for saved_node in self.callback_list: 
					if saved in saved_node.tag:
						self.callback_list.pop(saved_node)
						return saved_node
			return node

	def add_card_to_inventory(self, tag):
		# Find which card the tag names.
		# Add it to some kind of inventory.
		pass

class Main:
	def setup(self):
		pass