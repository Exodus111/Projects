import json
from logic.conversation import Conversation
from logic.comment import Comment

class Dialogue():
    def __init__(self, events, **kwargs):
        """
            kwargs contains the Keys:
            'names', 'nodes', 'links', 'tags', 'coords', 'text'
        """
        for i,j in kwargs.items(): setattr(self, i, j)
        self.counter = 1
        self.button_cooldown = True
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
        self.retired_cards = []
        self.card_changed = None
        self.portraits = {
        "apothecary":"images/portraits/Portrait Apothecary.png",
        "blacksmith":"images/portraits/Portrait Blacksmith.png",
        "girl":"images/portraits/Portrait Girl.png",
        "guy":"images/portraits/Portrait Guy.png",
        "old_lady":"images/portraits/Portrait Old.png",
        "wife":"images/portraits/Portrait Wife.png",
        "Djonsiscus":"images/portraits/Portrait Priest.png",
        }

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
                    break   #<--- This works because Question/Answer always comes first.
                elif tag[0:4] == "card":
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

###################### Activated Methods #################################################################################

    def check_links(self, node):
        link_nodes = []
        for n in self.links[node]:
            if self.coords[n][0] > self.coords[node][0]:
                link_nodes.append(n)
        return link_nodes

    def add_card_to_inventory(self, tag):
        for card in self.cards.keys():
            if card == tag:
                title = self.tag_strip(card, "card")
                text = self.text[self.cards[card]]
                names = [self.tag_strip(i, "name") for i in self.tags[self.cards[card]] if i[0:4] == "name"]
                card_dict = {"id":card, "title":title, "maintext":text, "tags":{k:True for k in names}}
                self.card_inventory.append(card_dict)

    def tag_strip(self, tag, _id):
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
                                        if "card" not in flag:
                                            if not self.check_flag(flag[6:]):
                                                self.set_flag(flag[6:])
                                                greeting_list.append(convs)
                                        else:
                                            if self.check_card_npc(flag, convs.npc):
                                                self.set_card_npc(flag, convs.npc)
                                                greeting_list.append(convs)
        if len(greeting_list) > 1:
            num = 0
            conv = None
            for c in greeting_list:
                c.find_start()
                if c.current_node["coords"][0] < num:
                    num = c.current_node["coords"][0]
                    conv = c
            self.current_conv = conv
            self.current_conv.find_start()
        elif greeting_list != []:
            self.current_conv = greeting_list[0]
            self.current_conv.find_start()

    def check_flag(self, flag):
        return self.events.flags[flag]

    def set_flag(self, flag, truefalse=True):
        self.events.flags[flag] = truefalse

    def set_card_npc(self, tag, npc, truefalse=False):
        for t in ("card_", "flag_", "block_"):
            tag = tag.replace(t, "")
        for card in self.card_inventory:
            if card["id"] == "card_"+tag:
                for k in card["tags"]:
                    if k.lower() == npc.lower():
                        card["tags"][k] = truefalse
                        self.card_changed = card

    def check_card_npc(self, tag, npc):
        for t in ("card_", "flag_", "block_"):
            tag = tag.replace(t, "")
        for card in self.card_inventory:
            if card["id"] == "card_"+tag:
                for k in card["tags"]:
                    if k.lower() == npc.lower():
                        return card["tags"][k]
                else:
                    return False
        else:
            return False

    def find_comment(self, name):
        comment_list = []
        for comment in self.comments:
            if comment.npc.lower() == name.lower():
                if "start_"+ name.lower() in comment.current_node["tags"]:
                    if not self.check_flag("start_"+ name.lower()):
                        self.set_flag("start_"+ name.lower())
                        self.current_conv = comment
                        return
                elif "start" in comment.current_node["tags"]:
                    for tags in commment.current_node["tags"]:
                        if tag[0:5] == "block":
                            if self.check_flag(flag[6:]):
                                self.set_flag(flag[6:], False)
                                comment_list.append(comment)
                                break
                            else:
                                break
        num = 999999
        conv = None
        for com in comment_list:
            if com.current_node["coords"][0] < num:
                num = com.current_node["coords"][0]
                conv = com
        self.current_conv = conv
            
    def pick_busy(self, name):
        self.current_conv = self.busy_nodes[name]

########## Public Methods.

    def start_conversation(self, name):
        for func in (self.find_conversation, self.find_comment, self.pick_busy):
            if self.current_conv != None:
                break
            func(name)
        if self.current_conv.npc.lower() == name.lower():
            if self.current_conv.type == "comment":
                self.manage_comments()
                return
        conv = self.current_conv
        portrait = self.portraits[name]
        self.master.gui.add_text_to_conv_panels({"top_text":conv.top_text, "question_list":conv.bottom_question_list}, portrait)
        self.master.gui.conv_panels_toggle()

    def question_picked(self, text):
        if self.button_cooldown:      #<-- Needed because Kivy sometimes presses a button multiple times.
            self.current_conv.question_picked(text)
            conv = self.current_conv
            self.master.gui.add_text_to_conv_panels({"top_text":conv.top_text, "question_list":conv.bottom_question_list})
            self.cooldown_flipper()
            self.master.cooldown(self.cooldown_flipper, 0.1)

    def manage_comments(self, commentlist=None):
        if commentlist == None:
            commentlist = self.current_conv.comments
        for comment in commentlist:
            comment["entity"] = self.get_npc_pos(comment["npc"])
        self.master.gui.add_comments(commentlist)

    def get_npc_pos(self, name):
        if name in ("player", "Thack"):
            return self.master.player
        else:
            for npc in self.master.npcs.npcgroup:
                if name == npc.name.lower():
                    return npc
            else:
                return self.master.player

    def cooldown_flipper(self, *_):
        self.button_cooldown = not self.button_cooldown




