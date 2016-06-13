


class Node():
    """docstring for Node"""
    def __init__(self, name, stages, owner=None, verbose=None):
        self.name = name
        self.verbose = verbose
        self.owner = owner
        self.event_trigger = None
        self.stages = set_stages(stages)

    def set_stages(self, stages):
        stage_dict = {}
        for i in range(stages):
            stage_dict["Stage{}".format(i+1)] = {"Done":False, "Question":"", "Answer":""}
        return stage_dict

    def add_text(self, stage, question, answer):
        self.stages["Stage{}".format(stage)]["Question"] = question
        self.stages["Stage{}".format(stage)]["Answer"] = answer

class EventManager():
    def __init__(self):
        self.events = {}
        self.m_events = {}
        self.nodes = []
        self.active_node = None

    def add_event(self, name):
        self.events[name] = False

    def select_node(self, owner, event):
        for node in self.nodes:
            if node.owner == owner:
                if node.event_trigger == event:
                    self.active_node = node

    def create_multi_event(self, name, true_list, false_list):
        self.m_events[name] = {}
        for t in true_list:
            self.m_events[name][t] = True
        for f in false_list:
            self.m_events[name][f] = False




if __name__ == "__main__":
    main()
