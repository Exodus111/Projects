import json

class Dialogue():
    def __init__(self, **kwargs):
        """
            kwargs is a dict, contains the keys:
            'names', 'nodes', 'links', 'tags', 'coords', 'text'
        """
        for i,j in kwargs.items():
            setattr(self, i, j)
        self.counter = 1
        self.node_list = []
        self.conversations = []
        self.clear_tags()
        self.parse_conversations()
        self.current_conv = self.conversations[0]

    def clear_tags(self):
        self.tags = {i:[tag.strip(".").lower() for tag in j] for i,j in self.tags.items()}

    def parse_conversations(self):
        for name in self.names:
            for node in self.nodes[name]:
                for tag in self.tags[node]:
                    if tag == "greeting":
                        self.create_conversation(node)

    def assemble_node(self, node):
        node_dict = {}
        name = [name for name in self.nodes if node in self.nodes[name]][0]
        node_dict["npc"] = name
        node_dict["id"] = node
        node_dict["links"] = self.check_links(node)
        node_dict["text"] = self.text[node]
        node_dict["tags"] = self.tags[node]
        return node_dict

    def check_links(self, node):
        link_nodes = []
        for n in self.links[node]:
            if self.coords[n][0] > self.coords[node][0]:
                link_nodes.append(n)
        return link_nodes

    def create_conversation(self, node):
        node = self.assemble_node(node)
        self.node_list.append(node)
        self.trace_nodes(node)
        conv = Conversation("Conv-"+str(self.counter), self.node_list)
        self.conversations.append(conv)
        self.counter += 1
        self.node_list = []

    def trace_nodes(self, node):
        """Recursive Method"""
        if node["links"] != []:
            for n in node["links"]:
                n = self.assemble_node(n)
                self.node_list.append(n)
                self.trace_nodes(n)

class Conversation():
    def __init__(self, id_tag, data):
        self.id_tag = id_tag
        self.data = {i["id"]:{h:j for h,j in i.items() if h != "id"} for i in data}
        self.npc = data[0]["npc"]
        self.current_node = data[0]
        self.greeting = data[0]["text"]
        self.top_text = self.greeting
        self.question_ids = []
        self.bottom_question_list = self.get_bottom_list(data[0])
        self.end_conversation = False

    def __repr__(self):
        return "< {}, {} >".format(self.id_tag, self.npc)

    def get_bottom_list(self, node):
        questions = []
        self.question_ids = []
        for link in node["links"]:
            for tag in self.data[link]["tags"]:
                if tag == "question" or tag == "greeting_reply":
                    questions.append(self.data[link]["text"])
                    self.question_ids.append(link)
        if questions == []:
            questions.append("Continue...")
        return questions

    def question_picked(self, question_text):
        if question_text != "1. Continue...":
            if question_text[1] not in ("0","1","2","3","4","5","6","7","8","9"):
                question_number = int(question_text[0])
            else:
                question_number = int(question_text[0:1])
            node = self.question_ids[question_number-1]
            if self.data[node]["links"] != []:
                _id = self.data[node]["links"][0]
                self.current_node = self.data[_id]
                self.top_text = self.data[_id]["text"]
                self.bottom_question_list = self.get_bottom_list(self.data[_id])
            else:
                self.end_conversation = True
        else:
            if self.current_node["links"] != []:
                self.current_node = self.data[self.current_node["links"][0]]
                self.top_text = self.current_node["text"]
                self.bottom_question_list = self.get_bottom_list(self.current_node)
            else:
                self.end_conversation = True
