#!/usr/bin/python3
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import DictProperty
import json

def import_json(filename):
    with open(filename, "r+") as f:
        return json.load(f)


# Finish this class.
# Every node should know its own next node and previous node.
# Dialogue handles player choice, and passes it on.
# Remember to save the passage of nodes in Dialogue, a list should do.
# Need to fix Text management.

class Node(Widget):
    npcname = StringProperty("")
    name = StringProperty("")
    text = StringProperty("")
    tags = ListProperty([])
    links = ListProperty([])
    next_nodes = ListProperty([])
    previous_nodes = ListProperty([])

    def next_node(self):
        pass

    def question_nodes(self):
        pass

class Dialogue(Widget):
    dialogue_dict = DictProperty(None)
    def __init__(self):
        super(Dialogue, self).__init__()
        self.dialogue_dict = import_json("./data/Dialogue_file_x2")
        self.current_name = None # <-- Set bind to load name dict.
        self.top_node = None
        self.bottom_nodes = None
        self.last_node = None
        self.top_text = ""
        self.bottom_text = ""
        self.conversation = False
        self.start = True

    def update(self, dt):
        if self.conversation:
            if self.start:
                if self.top_node == None:
                    self.start_convo()
                self.start = False
        else:
            if not self.start:
                self.parent.end_conversation()
                self.start = True

    def start_convo(self):
        nodes = self.dialogue_dict["nodes"][self.current_name]
        node = None
        for n in nodes:
            node = Nodes()
            node.npcname = self.current_name
            node.name = n
            node.text = self.dialogue_dict["text"][n]
            node.tags = self.dialogue_dict["tags"][n]
            node.links = self.dialogue_dict["links"][n]
            if self.dialogue_dict["tags"][n][0].lower() == "greeting.":
                node = n
        if node != None:
            self.top_node = n
            self.top_text = self.fix_str(self.dialogue_dict["text"][self.top_node])
            links = self.dialogue_dict["links"][self.top_node]
            self.bottom_nodes = self.find_question_nodes(links)
            self.bottom_text = self.assemble_bottom_text()
            self.parent.start_conversaton([self.top_text, self.bottom_text])
        else:
            raise Exception("The Node Returned as None!!!")

    def assemble_bottom_text(self):
        textlist = [self.dialogue_dict["text"][node] for node in self.bottom_nodes]
        textlist = [self.fix_str(line) for line in textlist]
        return "\n\n".join(textlist)

    def fix_str(self, text):
        textlist = text.split("\n")
        textlist = [line.rstrip('\n') for line in textlist]
        return " ".join(textlist)

    def find_question_nodes(self, links):
        current_x = self.dialogue_dict["coords"][self.top_node][0]
        question_nodes = []
        for link in links:
            if self.dialogue_dict["coords"][link][0] > current_x:
                question_nodes.append(link)
        return question_nodes
