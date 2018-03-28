#!/usr/bin/python3
import json

class Dialogue:
	"""
		Keys: names, text, nodes, links, coords, tags
	"""
	def __init__(self, dialoguedict):
		self.portraits = {
		"mrjohes":"images/portraits/Portrait Apothecary.png",
		"jarold":"images/portraits/Portrait Blacksmith.png",
		"sheila":"images/portraits/Portrait Girl.png",
		"riff":"images/portraits/Portrait Guy.png",
		"vonduren":"images/portraits/Portrait Old.png",
		"tylda":"images/portraits/Portrait Wife.png",
		"djonsiscus":"images/portraits/Portrait Priest.png",
		}		
		self.names = []
		self.nodes = self.assemble_nodes(dialoguedict)
		self.starts = self.gather_nodes("greeting")
		self.comment_starts = self.gather_nodes("start")
		self.cards = self.find_cards()

##### Init Methods.

	def assemble_nodes(self, _dict):
		node_dict = {}
		for name in _dict["names"]:
			self.names.append(name)
			for node in _dict["nodes"][name]:
				tags = self.fix_tags(_dict["tags"][node])
				portrait = "None"*(name not in self.portraits.keys()) or self.portraits[name.lower()]  
				n = Node(node, 
						name.lower(),
						portrait, 
						_dict["text"][node], 
						_dict["links"][node], 
						tags, 
						_dict["coords"][node], 
						self.set_type(tags))
				node_dict[node] = n
		return node_dict

	def set_type(self, tags):
		if tags[0] in ("comment", "comment_reply", "start"):
			return "comment"
		elif tags[0] in ("greeting", "question", "answer"):
			return "dialogue"
		elif "card" in tags[0]:
			return "card"
		else:
			return "unknown"

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

	def find_cards(self):
		cards = []
		for node in self.nodes.keys():
			if self.nodes[node].type == "card":
				cards.append(node)
		return cards

#### Public Methods.

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
	def __init__(self, node, npc, portrait, text, links, tags, coords, type_):
		self.node = node
		self.npc = npc
		self.portrait = portrait
		self.text = text
		self.links = links
		self.tags = tags
		self.coords = coords
		self.type = type_
		if self.type == "card":
			title = self.tags[0].replace("card", "")
			title = title.replace("_", " ")
			title = title.strip()
			title = title.capitalize()
			names = [t[:4] for t in tags if "name" in t]
			self.dict = {"title":title, "maintext":self.text, "tags":names}

	def __repr__(self):
		return self.text

	def remove_block(self):
		tags = []
		if "greeting" not in self.tags:
			if "start" not in self.tags:
				for tag in self.tags:
					if "block" not in tag:
						tags.append(tag)
				self.tags = tags

		
class Events:
	def __init__(self, dialogue):
		self.data = dialogue
		self.flags = self.get_flags()
		self.blocks = []
		self.playerwait_30 = False
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
		self.flags["flag_tutorial_part1"] = True
		for npc in self.data.names:
			self.flags["flag_start_"+npc.lower()] = True

	def update(self, dt):
		pass

class DialogueSystem:
	def __init__(self, parent, events, dialoguedata):
		self.parent = parent
		self.dialogue = dialoguedata
		self.events = events
		self.deck = []
		self.retired_deck = []
		self.card_changed = None
		self.callback_dict = {}
		self.once_list = []
		self.current_answer = None
		self.current_questions = []
		self.current_comment = None
		self.p_counter = 0

### Starting Conversations.
	def start_conversation(self, npc):
		node = None
		print("Starting conversation.")
		for meth in (self.find_conversation, self.find_comment, self.find_busy):
			node = meth(npc)
			if node != None:
				break
		if node != None:
			self.setup_conversation(node)

	def end_conversation(self):
		self.events.in_conversation = False
		self.parent.gui.conv_panels_toggle()

	def find_conversation(self, npc):
		for start in self.dialogue.starts:
			if start.npc.lower() == npc:
				for tag in start.tags:
					if "block" in tag:
						if not self.blocked(start):
							return start
		else:
			return None

	def find_busy(self, npc):
		for comment in self.dialogue.comment_starts:
			if npc == comment.npc and "busy" in comment.tags:
				return comment

	def find_comment(self, npc):
		for comment in self.dialogue.comment_starts:
			if npc.lower() == comment.npc:
				for tag in comment.tags:
					if "block" in tag:
						if not self.blocked(comment):
							return comment
		return None

### Setting up a conversation.
	def setup_conversation(self, node):
		"""
			Sets up the initial and following conversations.
			Takes the greeting/start node of the conversation/comment or the answer node of a dialogue. 
		"""
		if node.type == "dialogue":
			if not self.events.in_conversation:  # <-- This happens at the beginning.
				self.once_list = []
				self.events.in_conversation = True
				self.parent.gui.conv_panels_toggle()
			node, back = self.check_answer_tags(node)  # <-- Checking flag/card/back tags, can return a different node (back tag).
			self.current_questions = self.get_questions(node)  # <-- This returns a list of questions or Continue...
			if not back: # Normal.
				self.current_answer = node
			text_dict = {"top_text":str(self.current_answer),
						 "question_list":[str(n) for n in self.current_questions]}   # <-- Constructing dict for the GUI.
			self.parent.gui.add_text_to_conv_panels(text_dict, self.current_answer.portrait)
		elif node.type == "comment":
			nodelist = []
			while True:
				self.check_answer_tags(node)
				name = "player"*("comment_reply" in node.tags) or node.npc.lower() #<-- Top level coding right there.
				npc = self.parent.get_npc(name)
				nodelist.append({"entity":npc, "text":str(node), "tags":node.tags})
				next_list = self.next_nodes(node)
				if next_list == []:
					break
				else:
					node = next_list[0]
			self.parent.gui.add_comments(nodelist)

	def question_picked(self, text):
		"""
			When the player clicks on a question in a dialogue.
			The text is the string of the question. Contains numbering.
		"""
		text = text[3:]      # <-- Removes Numbering.
		if text != "Continue...":
			for node in self.current_questions:  # We find the question node.
				if text == node.text:
					self.check_question_tags(node) # Checking for save tag.
					break                          # Breaking means the node we found sticks around.
			else:
				raise Exception("Selected text not found among Questions. That is not supposed to happen. \n{}\n{}".format(text, self.current_questions))
		else:
			node = self.current_answer    # Continue means no questions, so we stick to the answer node we came from.
		next_list = self.next_nodes(node) # Get the connected nodes to the right of our node. 
		if next_list != []:
			self.setup_conversation(next_list[0])   # <-- Sending answer node to setup.
		else:
			self.end_conversation()

	def next_nodes(self, node):
		next_nodes = []
		for n in node.links:
			if node.coords[0] < self.dialogue.nodes[n].coords[0]:
				next_nodes.append(self.dialogue.nodes[n])
		return next_nodes

	def get_questions(self, node):
		"""
			Gets next question nodes.
			node is an answer node.
		"""
		nodelist = self.next_nodes(node)
		nodelist = self.check_for_blocks(nodelist)
		nodelist = [q for q in nodelist if q not in self.once_list]   # Eliminate questions we have already asked.
		if nodelist != []:
			if "question" in nodelist[0].tags:
				return nodelist
		return ["Continue..."]

	def check_for_blocks(self, nodelist):
		return [i for i in nodelist if not self.blocked(i)]

	def blocked(self, node):
		blocked = False
		for tag in node.tags:
			if "block" in tag:
				blocked = True
				if "flag" not in tag:
					flag = tag.replace("block", "flag")
				else:
					flag = tag.replace("block_", "")
				if self.events.flags[flag]:
					self.events.flags[flag] = False
					blocked = False
					if tag not in self.events.blocks:
						self.events.blocks.append(tag)
					if "card" in tag:
						node.dict["tags"] = [t for t in node.dict["tags"] if node.npc.lower() not in t]
						self.parent.gui.update_card(node.dict)
					node.remove_block()
		return blocked

	def check_answer_tags(self, node):
		back = False
		for tag in node.tags:
			if "flag" in tag:
				self.events.flags[tag] = True
			elif "card" == tag[:4]:
				self.events.flags["flag_"+tag] = True
				self.add_card_to_inventory(tag)
			elif "back" in tag:                        # The answer tag contains a back tag. We need to check to see if we need to go back. 
				saved = tag.replace("back", "save")
				if not self.last_save_tag(saved):
					if saved in self.callback_dict.keys(): # <-- THIS SHOULD WORK NOW! TEST IT!!
						node = self.callback_dict[saved]
						back = True
		return node, back

	def last_save_tag(self, tag):
		howmany = [k for k in self.dialogue.nodes.keys() if tag in self.dialogue.nodes[k].tags]
		amount = [i for i in self.once_list if tag in i.tags]
		return len(howmany) == len(amount) 

	def check_question_tags(self, question):
		for tag in question.tags:
			if "save" in tag:
				self.once_list.append(question)               # We save the question for future elimination.
				if tag not in self.callback_dict.keys(): 
					self.callback_dict[tag] = self.current_answer # We save the answer node to return to it from a back node.

#### Card Inventory

	def add_card_to_inventory(self, tag):
		for node in self.dialogue.cards:
			if tag in node.tags:
				self.parent.gui.add_card(node.dict)

	def update_card(self, tag, npc):
		for node in self.dialogue.cards:
			if tag in node.tags:
				node.dict["tags"].remove(npc)
				self.parent.gui.update_card(node.dict)

