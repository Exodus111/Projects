#!/usr/bin/python3
from kivy.uix.widget import Widget
from kivy.properties import DictProperty, StringProperty, ListProperty, BooleanProperty

import json

def import_json(filename):
    with open(filename, "r+") as f:
        return json.load(f)

class Dialogue(Widget):
    nodes = DictProperty()
    conv = BooleanProperty(False)
    npc = StringProperty("")
    bottom_nodes = ListProperty([])
    answer_only = BooleanProperty(False)

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
        node = self._find_greeting()
        greply_nodes = self._find_next_nodes(node)
        self.assemble_top_text(node)
        if greply_nodes != []:
            self.assemble_bottom_text(greply_nodes)
        else:
            self.answer_only = True

    def continue_conv(self, obj):
        node = obj.node
        nodelist = self._find_next_nodes(node)
        if nodelist != []:
            answer_node = nodelist[0]
            question_nodes = [node for node in self._find_next_nodes(answer_node) if "question" in node.tags]
            self.assemble_top_text(answer_node)
            if question_nodes != []:
                self.assemble_bottom_text(question_nodes)
                self.answer_only = False
            else:
                question_nodes = ["", "", "", ""]
                self.parent.change_bottom_text(question_nodes)
                self.answer_only = True
        else:
            self.end_conv()

    def end_conv(self):
        self.conv = False
        self.parent.menus.menu_on = not self.parent.menus.menu_on

    def _find_next_nodes(self, node):
        x = node.coords[0]
        links = self.nodes[node.nodeid].links
        linklist = []
        for link in links:
            if self.nodes[link].coords[0] > x:
                linklist.append(self.nodes[link])
        return linklist

    def assemble_top_text(self, node):
        txt = self.fix_str(node.text)
        self.parent.menus.topbutton.node = node
        self.parent.change_top_text(txt)

    def assemble_bottom_text(self, nodelist):
        textlist = []
        self.bottom_nodes = nodelist
        for num, node in enumerate(nodelist):
            self.parent.menus.bottombuttons[num].node = node
            txt = self.fix_str(node.text)
            txt = "{}. {}".format(num+1, txt)
            textlist.append(txt)
        self.parent.change_bottom_text(textlist)

    def fix_str(self, txt):
        textlist = txt.split("\n")
        textlist = [line.rstrip("\n") for line in textlist]
        return " ".join(textlist)

    def _find_greeting(self):
        for n in self.nodes:
            if self.nodes[n].npcname == self.npc:
                if "greeting" in self.nodes[n].tags:
                    if len(self.nodes[n].tags) == 1:
                        return self.nodes[n]

class Node(Widget):
    npcname = StringProperty("")
    nodeid = StringProperty("")
    text = StringProperty("")
    tags = ListProperty([])
    links = ListProperty([])
    coords = ListProperty([])

    def fix_tags(self):
        templist = []
        for tags in self.tags:
             for tag in tags.split(","):
                 tag = tag.strip()
                 tag = tag.lower()
                 tag = tag.rstrip(".")
                 templist.append(tag)
        self.tags = templist
