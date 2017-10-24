import json
from logic.conversation import Conversation
from logic.comment import Comment

class Dialogue():
    def __init__(self, events, **kwargs):
        """
            kwargs contains the Key:Values:
            'names', 'nodes', 'links', 'tags', 'coords', 'text'"""
        for i,j in kwargs.items(): setattr(self, i, j)
        self.counter = 1
        self.node_list = []
        self.conversations = []
        self.comments = []
        self.busy_nodes = {}
        self.clear_tags()
        self.events = events
        self.events.insert_flags(self.create_flags())
        self.cards = self.assemble_cards()                       #<-- Dict
        self.parse_conversations()
        self.assemble_commentary()
        self.current_conv = None
        self.card_inventory = []

#############################  Loading Methods ######################################################

    def clear_tags(self):
        self.tags = {i:[tag.strip(".").lower() for tag in j] for i,j in self.tags.items()}

    def create_flags(self):
        flags = []
        for taglist in self.tags.values():
            for tag in taglist:
                if tag[0:4] == "flag" or tag[0:5] == "start":
                    flags.append(tag)
        return list(set(flags))

    def assemble_cards(self):
        cards = {}
        for node, taglist in self.tags.items():
            for tag in taglist:
                if tag in ("question", "answer", "greeting", "reply"):
                    break
                elif tag[0:4] == "card": # This works because Question/Answer always comes first.
                    cards[tag] = node
        return cards

    def parse_conversations(self):
        for name in self.names:
            for node in self.nodes[name]:
                for tag in self.tags[node]:
                    if tag == "greeting":
                        self.conversations.append(self.create_conversation(node))

    def assemble_commentary(self):
        for name in self.nodes.keys():
            for node in self.nodes[name]:
                if ("comment" in self.tags[node] or "comment_reply" in self.tags[node]) and "start" in self.tags[node]:
                    node = self.assemble_node(node)
                    self.node_list.append(node)
                    self.trace_nodes(node)
                    comment = Comment(self.node_list)
                    self.node_list = []
                    self.comments.append(comment)
        for com in self.comments:
            if com.busy:
                self.busy_nodes[com.npc.lower()] = com

    def create_conversation(self, node):
        node = self.assemble_node(node)
        self.node_list.append(node)
        self.trace_nodes(node)
        conv = Conversation("Conv-"+str(self.counter), self.node_list, self)
        self.counter += 1
        self.node_list = []
        return conv

    def assemble_node(self, node):
        node_dict = {}
        name = [name for name in self.nodes if node in self.nodes[name]][0]
        node_dict["npc"] = name
        node_dict["id"] = node
        node_dict["links"] = self.check_links(node)
        node_dict["text"] = self.text[node]
        node_dict["tags"] = self.tags[node]
        node_dict["coords"] = self.coords[node]
        return node_dict

    def trace_nodes(self, node):
        """Recursive Method"""
        if node["links"] != []:
            for n in node["links"]:
                n = self.assemble_node(n)
                self.node_list.append(n)
                self.trace_nodes(n)

###################### Active Methods #################################################################################

    def check_links(self, node):
        link_nodes = []
        for n in self.links[node]:
            if self.coords[n][0] > self.coords[node][0]:
                link_nodes.append(n)
        return link_nodes

    def add_card_to_inventory(self, tag):
        for card in self.cards.keys():
            if card == tag:
                title = self._tag_strip(card, "card")
                text = self.text[self.cards[card]]
                names = [self._tag_strip(i, "name") for i in self.tags[self.cards[card]] if i[0:4] == "name"]
                card_dict = {"id":card, "title":title, "maintext":text, "tags":names}
                self.card_inventory.append(card_dict)

    def _tag_strip(self, tag, _id):
        tag = tag.replace("_", " ")
        tag = tag.strip(_id)
        tag = tag.strip(" ")
        tag = tag.capitalize()
        return tag

    def find_conversation(self, npc):
        npc = npc.lower()
        greeting_list = []
        for convs in self.conversations:
            if convs.npc.lower() == npc:
                if not self.check_flag("start_"+npc):
                    for tag in convs.tags():
                        if tag == "start_"+npc:
                            self.set_flag("start_"+npc)
                            self.current_conv = convs
                            self.current_conv.find_start()
                            return
                else:
                    for _id, node in convs.nodes():
                        if "greeting" in node["tags"]:
                            if "start_"+npc not in node["tags"]:
                                for flag in node["tags"]:
                                    if flag[0:5] == "block":
                                        if self.check_flag(flag[6:]):
                                            self.set_flag(flag[6:], False)
                                            greeting_list.append(convs)
                                            break
        if len(greeting_list) > 1:
            num = 0
            conv = None
            for c in greeting_list:
                if c.data["coords"][0] > num:
                    num = c.data["coords"][0]
                    conv = c
            self.current_conv = conv
            self.current_conv.find_start()
        elif len(greeting_list) == 0:
            self.current_conv = self.busy_nodes[npc]
        else:
            self.current_conv = greeting_list[0]
            self.current_conv.find_start()

    def check_flag(self, flag):
        return self.events.flags[flag]

    def set_flag(self, flag, truefalse=True):
        self.events.flags[flag] = truefalse
