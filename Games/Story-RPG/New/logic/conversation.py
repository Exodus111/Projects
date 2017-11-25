
class Conversation():
    def __init__(self, id_tag, data, master):
        self.type = "conversation"
        self.master = master
        self.id_tag = id_tag
        self.data = {i["id"]:{h:j for h,j in i.items() if h != "id"} for i in data}
        self.npc = data[0]["npc"]
        self.current_node = None
        self.top_text = "No Text"
        self.callback_list = []
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
                self._set_tags_and_cards(self.data[node])
        if self.current_node == None:
            raise Exception("No greeting found, here is the node list: \n" + str(self.data.keys()))

    def question_picked(self, question_text):
        """
            This Method starts the chain of moving further in the conversation.
            It is activated by the player.
        """
        if "Continue..." not in question_text:
            node = self._find_node(question_text)
            self._set_tags_and_cards(self.data[node])
            self.callback_list.append(node)
            if self.data[node]["links"] != []:
                answernode = self._check_nodes_for_block(self.data[node]["links"])
                if answernode != []:
                    self._setup_answer_node(self.data[answernode[0]])
                    self._setup_bottom_list(self.data[answernode[0]])
                    self._check_for_callback()
                else:
                    self.end_conversation = True
            else:
                self.end_conversation = True
        else:
            if self.current_node["links"] != []:
                answernode = self._check_nodes_for_block(self.current_node["links"])
                if answernode != []:
                    self._setup_answer_node(self.data[answernode[0]])
                    self._setup_bottom_list(self.data[answernode[0]])
                    self._check_for_callback()
                else:
                    self.end_conversation = True
            else:
                self.end_conversation = True

    def _check_nodes_for_block(self, nodelist):
        passed = []
        for node in nodelist:
            if self._check_tag_in_node(node, "a"):
                passed.append(node)
        return passed

    def _find_node(self, question):
        if question[1] not in (str(i) for i in range(10)):
            number = int(question[0])
        else:
            number = int(question[0:2])
        return self.question_ids[number-1]

    def _setup_answer_node(self, node):
        self._set_tags_and_cards(node)
        self.callback_list.append([k for k,v in self.data.items() if v == self.current_node][0])
        self.current_node = node
        self.top_text = node["text"]

    def _set_tags_and_cards(self, node):
        for tag in node["tags"]:
            if tag[0:4] == "flag":
                self.master.set_flag(tag)
            if tag[0:4] == "card":
                self.master.add_card_to_inventory(tag)

    def _retire_card(self, card):
        self.master.retired_cards.append(card)

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

    def _check_for_callback(self):
        for tag in self.current_node["tags"]:
            if tag[:4] == "back":
                tag_id = tag[5:]
                save_list = self._find_nodes_with_tag("save_"+tag_id)
                if save_list != []:
                    for node in save_list:
                        if node not in self.callback_list:
                            if self._check_tag_in_node(node, "q"):
                                if len(self.bottom_question_list) == 1 and self.bottom_question_list[0] == "Continue...":
                                    del(self.bottom_question_list[0])
                                self.bottom_question_list.append(self.data[node]["text"])
                                self.question_ids.append(node)

    def _find_nodes_with_tag(self, tag):
        temp_list = []
        for node in self.data:
            for t in self.data[node]["tags"]:
                if t == tag:
                    temp_list.append(node)
        return temp_list

    def _check_tag_in_node(self, node, _type):
        tag_dict = {"q":("question", "reply"), "a":("answer", "greeting")}
        passed = False
        for tag in self.data[node]["tags"]:
            if tag in tag_dict[_type]:
                passed = True
        if passed:
            for tag in self.data[node]["tags"]:
                if tag[0:5] == "block":
                    if self.master.check_flag(tag[6:]):
                        self._check_card_name(tag)
                        if "once" in self.data[node]["tags"]:
                            self.master.set_flag(tag[6:], False)
                        return True
                    else:
                        return False
            else:
                return True
        else:
            return False

    def _check_card_name(self, tag):
        if "block" in tag and "card" in tag:
            self.master.check_card_npc(tag, self.npc)
