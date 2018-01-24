
class Comment():
	def __init__(self, node_list):
		"""
			node_list is a list a of node dicts.
			Keys: npc, id, links, text, tags, coords
		"""
		self.type = "comment"
		self.node_db = node_list
		self.npc = node_list[0]["npc"]
		self.current_node = self.find_first()
		self.comments = []
		self.busy = self.check_for_busy()
		self.end_conversation = False
		self.append_comments()

	def __repr__(self):
		return "Comment node. Npc: {}, First comment: {}, Busy? {}.".format(self.npc, self.comments[0][0,8], self.busy)

	def check_node_for_npc(self, node):
		if "comment" in node["tags"]:
			# if npcname in tags: <-- code for more then one NPC talking.
			return self.npc
		elif "comment_reply" in node["tags"]:
			return "player"
		else:
			raise Exception("Comment node missing essetial 'comment' or 'comment_reply' tag. Not supposed to happen.") 

	def check_for_busy(self):
		for node in self.node_db:
			if "busy" in node["tags"]:
				return True
		else:
			return False

	def find_first(self):
		for node in self.node_db:
			if "start" in node["tags"]:
				return node
		else:
			raise Exception("Start not found in comments")

	def append_comments(self):
		while True:
			self.comments.append({
				"npc":self.check_node_for_npc(self.current_node).lower(), 
				"text":self.current_node["text"]})
			self.current_node = self.goto_next(self.current_node)
			if self.current_node == None:
				break

	def goto_next(self, node):
		if node["links"] != []:
			for link in self.node_db:
				if link["id"] == node["links"][0]:
					return link
			else:
				return None
		else: return None


