#!/usr/bin/python3
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import DictProperty, StringProperty, ListProperty
import json

def import_json(filename):
    with open(filename, "r+") as f:
        return json.load(f)


# Playthrough class, records playthough.
# Comment system.
#
# Need to fix Text management.

class PlayThrough(Widget):
    visited_nodes = ListProperty()

    def check_list(self, w):
        if w in self.visited_nodes:
            return True
        else:
            return False

class Node(Widget):
    npcname = StringProperty("")
    name = StringProperty("")
    text = StringProperty("")
    tags = ListProperty([])
    links = ListProperty([])
    question_nodes = ListProperty([])
    answer_node = StringProperty("")

    def fix_tags(self):
        self.tags = [tag.lower().rstrip(".") for tag in self.tags]

class Dialogue(Widget):
    dialogue_dict = DictProperty(None)
    def __init__(self):
        super(Dialogue, self).__init__()
        self.dialogue_dict = import_json("./data/Dialogue_file_x2")
        self.playthrough = PlayThrough()
        self.nodes = {}
        self.current_name = None
        self.greeting_nodes = {}
        self.top_node = None
        self.bottom_nodes = None
        self.last_node = None
        self.selected_node = None
        self.old_selection = None
        self.top_text = ""
        self.bottom_text = ""
        self.conversation = False
        self.start = True

    def play_comment(self, node):
        node = self.nodes[node]
        text1 = node.text
        text2 = self.nodes[node.links[0]].text
        self.parent.npcs.comment(self.current_name, text2)
        self.parent.player.comment(text1)


    def key_up(self, key):
        if key == "spacebar":
            self.line_clicked("answer")
        else:
            if int(key) <= len(self.bottom_nodes):
                self.line_clicked(self.bottom_nodes[int(key)-1])

    def key_down(self, key):
        pass

    def update(self, dt):
        if self.conversation:
            if self.start:
                self.start_convo()
                self.start = False
            else:
                if self.selected_node != self.old_selection:
                    self.old_selection = self.selected_node
                    self.continue_conv()
        else:
            if not self.start:
                self.parent.end_conversation()
                self.start = True

    def line_clicked(self, value):
        if value != "answer":
            self.selected_node = value
        else:
            if self.bottom_text == " ":
                self.selected_node = self.nodes[self.selected_node].answer_node
        self.playthrough.visited_nodes.append(self.selected_node)

    def setup_nodes(self):
        for name in self.dialogue_dict["names"]:
            nodes = self.dialogue_dict["nodes"][name]
            current = None
            for n in nodes:
                node = Node()
                node.npcname = name
                node.name = n
                node.text = self.dialogue_dict["text"][n]
                node.tags = self.dialogue_dict["tags"][n]
                node.links = self.dialogue_dict["links"][n]
                node.fix_tags()
                self.nodes[node.name] = node
        for nod in self.nodes:
            self.check_tags(nod, self.nodes[nod])

    def check_tags(self, name, node):
        if node.tags[0] in ("answer", "greeting"):
            find_next_nodes = self.find_next_nodes(name, node.links)
            if len(find_next_nodes) > 0:
                if self.nodes[find_next_nodes[0]].tags[0] != "answer":
                    node.question_nodes = find_next_nodes
                else:
                    node.answer_node = find_next_nodes[0]
            else:
                node.answer_node = "end_node"
        elif node.tags[0] in ("question", "greeting_reply"):
            node.answer_node = self.find_next_nodes(name, node.links)[0]
        if node.tags[0] == "greeting":
            self.greeting_nodes[node.npcname] = node
        return node

    def continue_conv(self):
        question_node = self.nodes[self.selected_node]
        if question_node.answer_node == "end_node":
            self.parent.change_top_text(" ")
            self.parent.change_bot_text(" ")
            self.parent.end_conversation()
        else:
            self.top_node = question_node.answer_node
            self.top_text = self.assemble_top_text()

            self.bottom_nodes = self.nodes[self.top_node].question_nodes
            if self.bottom_nodes != []:
                self.bottom_text = self.assemble_bottom_text()
            else:
                self.bottom_text = " "
            self.parent.change_top_text(self.top_text)
            self.parent.change_bot_text(self.bottom_text)


    def start_convo(self):
        current = None
        current = self.greeting_nodes[self.current_name]
        if current != None:
            if not self.playthrough.check_list(current.name):
                self.playthrough.visited_nodes.append(current.name)
                self.top_node = current.name
                top_text = self.fix_str(self.dialogue_dict["text"][self.top_node])
                self.top_text = self.assemble_top_text()

                self.bottom_nodes = current.question_nodes
                self.bottom_text = self.assemble_bottom_text()
                self.parent.start_conversaton([self.top_text, self.bottom_text])
            else:
                nodes = self.dialogue_dict["nodes"][self.current_name]
                mynode = [node for node in nodes if "comment" in self.nodes[node].tags][0]
                self.play_comment(mynode)

    def assemble_top_text(self):
        top_text = self.fix_str(self.dialogue_dict["text"][self.top_node])
        return "[ref=answer]{}[/ref]".format(top_text)


    def assemble_bottom_text(self):
        textlist = [self.dialogue_dict["text"][node] for node in self.bottom_nodes]
        textlist = [self.fix_str(line) for line in textlist]
        textlist = ["[ref={}]{}. {}[/ref]".format(self.bottom_nodes[n], str(n+1), line) for n, line in enumerate(textlist)]
        return "\n\n".join(textlist)

    def fix_str(self, text):
        textlist = text.split("\n")
        textlist = [line.rstrip('\n') for line in textlist]
        return " ".join(textlist)

    def find_next_nodes(self, current, links):
        current_x = self.dialogue_dict["coords"][current][0]
        question_nodes = []
        for link in links:
            if self.dialogue_dict["coords"][link][0] > current_x:
                question_nodes.append(link)
        return question_nodes
