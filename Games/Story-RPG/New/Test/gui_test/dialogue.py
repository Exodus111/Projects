import json

class Dialogue():
    def __init__(self, **kwargs):
        """
            kwargs is a dict, contains the keys:
            'names', 'nodes', 'links', 'tags', 'coords', 'text'
        """
        for i,j in kwargs.items(): setattr(self, i, j)
        self.counter = 1
        self.node_list = []
        self.conversations = []
        self.clear_tags()
        self.flags = self.create_flags()                      #<-- Dict
        self.cards = self.assemble_cards()                    #<-- Dict
        self.parse_conversations()
        self.current_conv = None
        self.card_inventory = []

    def assemble_node(self, node):
        node_dict = {}
        name = [name for name in self.nodes if node in self.nodes[name]][0]
        node_dict["npc"] = name
        node_dict["id"] = node
        node_dict["links"] = self.check_links(node)
        node_dict["text"] = self.text[node]
        node_dict["tags"] = self.tags[node]
        return node_dict

    def find_conversation(self, npc):
        npc = npc.lower()
        for convs in self.conversations:
            if convs.npc.lower() == npc:
                self.current_conv = convs
                self.current_conv.find_start()

    def create_flags(self):
        flags = []
        for taglist in self.tags.values():
            for tag in taglist:
                if tag[0:4] == "flag":
                    flags.append(tag)
        flags = {i:False for i in list(set(flags))}
        return flags

    def assemble_cards(self):
        cards = {}
        for node, taglist in self.tags.items():
            for tag in taglist:
                if tag in ("question", "answer", "greeting", "greeting_reply"):
                    break
                elif tag[0:4] == "card": # This works because Question/Answer always comes first.
                    cards[tag] = node
        return cards

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
        tag = tag.strip()
        tag = tag.capitalize()
        return tag

    def check_flag(self, flag):
        return self.flags[flag]

    def set_flag(self, flag, truefalse=True):
        self.flags[flag] = truefalse

    def clear_tags(self):
        self.tags = {i:[tag.strip(".").lower() for tag in j] for i,j in self.tags.items()}

    def parse_conversations(self):
        for name in self.names:
            for node in self.nodes[name]:
                for tag in self.tags[node]:
                    if tag == "greeting":
                        self.create_conversation(node)

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
        conv = Conversation("Conv-"+str(self.counter), self.node_list, self)
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
    def __init__(self, id_tag, data, master):
        self.master = master
        self.id_tag = id_tag
        self.data = {i["id"]:{h:j for h,j in i.items() if h != "id"} for i in data}
        self.npc = data[0]["npc"]
        self.current_node = None
        self.top_text = "No Text"
        self.bottom_question_list = ["Empty List"]
        self.greeting_nodes = self.assemble_greeting_nodes()
        self.master.set_flag("flag_start_"+self.npc, False)
        self.end_conversation = False

    def __repr__(self):
        return "< {}, {} >".format(self.id_tag, self.npc)

    def assemble_greeting_nodes(self):
        greeting_nodes = []
        for node in self.data.keys():
            for tag in self.data[node]["tags"]:
                if tag == "greeting":
                    greeting_nodes.append(node)
        return greeting_nodes

    def find_start(self):
        if not self.master.check_flag("flag_start_"+self.npc):
            for node in self.greeting_nodes:
                if "flag_start" in self.data[node]["tags"]:
                    self.current_node = self.data[node]
                    self.top_text = self.data[node]["text"]
                    self.bottom_question_list = self.get_bottom_list(self.data[node])
                    self.master.set_flag("flag_start_"+self.npc)
                    self._check_tag_in_answer(self.data[node])
        else:
            for node in self.greeting_nodes:
                for tag in self.data[node]["tags"]:
                    if tag[0:4] == "flag":
                        if self.master.check_flag(tag):
                            self.current_node = self.data[node]
                            self.top_text = self.data[node]["text"]
                            self.bottom_question_list = self.get_bottom_list(self.data[node])
                            self._check_tag_in_answer(self.data[node])
                            self.master.set_flag(tag, False)
        if self.current_node == None:
            raise Exception("No greeting found, here is the greeting list: \n" + str(self.greeting_nodes))


    def get_bottom_list(self, node):
        questions = []
        self.question_ids = []
        for link in node["links"]:
            if self._check_tag_in_question(link):
                questions.append(self.data[link]["text"])
                self.question_ids.append(link)
        if questions == []:
            questions.append("Continue...")
        return questions

    def _check_tag_in_question(self, node):
        question = False
        for tag in self.data[node]["tags"]:
            if tag == "question" or tag == "reply":
                question = True
        if question:
            for tag in self.data[node]["tags"]:
                if tag[0:4] == "flag":
                    if self.master.check_flag(tag):
                        return True
                    else:
                        return False
            else:
                return True
        else:
            return False

    def question_picked(self, question_text):
        if "Continue..." not in question_text:
            node = self._find_node(question_text)
            if self.data[node]["links"] != []:
                self._setup_answer_node(self.data[self.data[node]["links"][0]])   # Questions always have one linked node.
            else:
                self.end_conversation = True
        else:
            if self.current_node["links"] != []:
                self._setup_answer_node(self.data[self.current_node["links"][0]])
            else:
                self.end_conversation = True

    def _find_node(self, question):
        if question[1] not in (str(i) for i in range(10)):
            number = int(question[0])
        else:
            number = int(question[0:2])
        return self.question_ids[number-1]

    def _setup_answer_node(self, node):
        self._check_tag_in_answer(node)
        self.current_node = node
        self.top_text = node["text"]
        self.bottom_question_list = self.get_bottom_list(node)

    def _check_tag_in_answer(self, node):
        for tag in node["tags"]:
            if tag[0:4] == "flag":
                self.master.set_flag(tag)
            if tag[0:4] == "card":
                self.master.add_card_to_inventory(tag)
