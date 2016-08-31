from collections import defaultdict


class DataBase():
    def __init__(self):
        self.npcs = []
        self.quests = defaultdict(list)
        self.dialogue = defaultdict(list)

    def add_info(self, info):
        for npc in info:
            if "quest" in npc["Header"]:
                pass
            elif "question" in npc["Header"]:
                pass
