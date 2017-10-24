
class Conversation():
    def __init__(self, id_tag, data, master):
        self.type = "conversation"
        self.master = master
        self.id_tag = id_tag
        self.data = {i["id"]:{h:j for h,j in i.items() if h != "id"} for i in data}
        self.npc = data[0]["npc"]
        self.current_node = None
        self.top_text = "No Text"
        self.bottom_question_list = ["Empty List"]
        self.master.set_flag("flag_start_"+self.npc, False)
        self.end_conversation = False

    def __repr__(self):
        return "< {}, {} >".format(self.id_tag, self.npc)

    def nodes(self):
        for _id, node in self.data.items():
            yield _id, node

    def tags(self):
        for node in self.data.keys():
            for tag in self.data[node]["tags"]:
                yield tag

    def find_start(self):
        for node in self.data.keys():
            if "greeting" in self.data[node]["tags"]:
                self.current_node = self.data[node]
                self.top_text = self.data[node]["text"]
                self._setup_bottom_list(self.data[node])
                self._check_tag_in_answer(self.data[node])
        if self.current_node == None:
            raise Exception("No greeting found, here is the node list: \n" + str(self.data.keys()))

    def question_picked(self, question_text):
        """
            This Method starts the chain of moving further in the conversation.
            It is activated by the player.
        """
        if "Continue..." not in question_text:
            node = self._find_node(question_text)
            if self.data[node]["links"] != []:
                answernode = self.check_nodes_for_block(self.data[node]["links"])
                if answernode != []:
                    self._setup_answer_node(self.data[answernode[0]])
                    self._setup_bottom_list(self.data[answernode[0]])
                else:
                    self._check_for_callback(node) #<--- Working on this !!
            else:
                self.end_conversation = True
        else:
            if self.current_node["links"] != []:
                answernode = self.check_nodes_for_block(self.current_node["links"])
                if answernode != []:
                    self._setup_answer_node(self.data[answernode[0]])
                    self._setup_bottom_list(self.data[answernode[0]])
                else:
                    self.end_conversation = True
            else:
                self.end_conversation = True

    def _check_for_callback(self, node): #<------- Working on this!!
        tag_found = None                 # Needs Testing data.
        save_node = []
        for tag in self.data[node]["tags"]:
            if tag[:4] == "back":
                tag_found = tag

        if tag_found != None:
            for _id in self.data:
                for tag in self.data[_id]["tags"]:
                    if tag[5:] == tag_found[5:]:
                        save_node.append(_id)
            checked_nodes = []
            for n in save_node:
                if node not in self.check_future_nodes(n):
                    checked_nodes.append(n)
            return checked_nodes
        else:
            self.end_conversation = True







    def check_nodes_for_block(self, nodelist):
        passed = []
        for node in nodelist:
            if self._check_tag_in_node(node, "a"):
                passed.append(node)
        if len(passed) > 1:
            #Now what?
            pass

        return passed

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

    def _check_tag_in_answer(self, node):
        for tag in node["tags"]:
            if tag[0:4] == "flag":
                self.master.set_flag(tag)
            if tag[0:4] == "card":
                self.master.add_card_to_inventory(tag)

    def _setup_bottom_list(self, node):
        questions = []
        self.question_ids = []
        for link in node["links"]:
            if self._check_tag_in_node(link, "q"):
                questions.append(self.data[link]["text"])
                self.question_ids.append(link)
        if questions == []:
            questions.append("Continue...")
        self.bottom_question_list = questions

    def _check_tag_in_node(self, node, _type):
        tag_dict = {"q":["question", "reply"], "a":["answer", "greeting"]}
        passed = False
        for tag in self.data[node]["tags"]:
            if tag in tag_dict[_type]:
                passed = True
        if passed:
            for tag in self.data[node]["tags"]:
                if tag[0:5] == "block":
                    if self.master.check_flag(tag[6:]):
                        self.master.set_flag(tag[6:], False)
                        return True
                    else:
                        return False
            else:
                return True
        else:
            return False