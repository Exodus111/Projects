#!/usr/bin/python3
from kivy.uix.widget import Widget
from kivy.properties import DictProperty, StringProperty, ListProperty, BooleanProperty

import json

def import_json(self, filename):
    with open(filename, "r+") as f:
        return json.load(f)

class Dialogue(Widget):
    nodes = DictProperty()
    conv = BooleanProperty(False)
    npc = StringProperty("")

    def dialoguesetup(self):
        d_dict = import_json("./data/Dialogue_file_x4")
        for name in d_dict["names"]:
            for n in d_dict["nodes"][name]:
                node = Node()
                node.nodeid = n
                node.npcname = name
                node.text = d_dict["text"][n]
                node.tags = d_dict["tags"][n]
                node.links = d_dict["links"][n]
                node.coords = d_dict["coords"][n]
                node.fix_tags()
                self.nodes[n] = node

    def update(self, dt):
        if self.conv:
            pass

    def start_conv(self):
        """
         Starts Conversation.
         The property self.npc needs to be filled first.
        """
        self.conv = True
        node = self.find_greeting()
        greply_nodes = self.find_next_nodes(node)
        self.assemble_top_text(node)
        self.assemble_bottom_text(greply_nodes)

    def continue_conv(self, nodeid):
        if nodeid  == "answer":
            pass
        else:
            pass

    def find_next_nodes(self, node):
        x = node.coords[0]
        links = self.nodes[node.nodeid].links
        return [link for links if x < link.coords[0]]

    def assemble_top_text(self, node):
        txt = self.fix_str(node.text)
        txt = "[ref=answer]{}[/ref]".format(txt)
        self.parent.change_top_text(txt)

    def assemble_bottom_text(self, nodelist):
        textlist = []
        for num, node in enumerate(nodelist):
            txt = self.fix_str(node.text)
            txt = "[ref={}]{}. {}[/ref]".format(node.nodeid, num, txt)
            textlist.append(txt)
        self.parent.change_bottom_text(textlist)

    def fix_str(self, txt):
        textlist = txt.split("\n")
        textlist = [line.rstrip("\n") for line in textlist]
        return " ".join(textlist)

    def find_greeting(self):
        nodes = []
        for n in self.nodes:
            if self.nodes[n].npcname == self.npc:
                if "greeting" in self.nodes[n]["tags"]:
                    if len(self.nodes[n]["tags"]) == 1:
                        return self.nodes[n]

class Node(Widget):
    npcname = StringProperty("")
    nodeid = StringProperty("")
    text = StringProperty("")
    tags = ListProperty([])
    links = ListProperty([])
    coords = ListProperty([])
    question_nodes = ListProperty([])
    answer_node = StringProperty("")

    def fix_tags(self):
        templist = []
        for tags in self.tags:
             for tag in tags.split(","):
                 tag = tag.strip()
                 tag = tag.lower()
                 tag = tag.rstrip(".")
                 templist.append(tag)
        self.tags = templist
