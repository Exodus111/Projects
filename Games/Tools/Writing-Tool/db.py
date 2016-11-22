from collections import defaultdict, OrderedDict
from path import Path
import json, os

#This is a hack for Atom, since it doesn't run your file from the files own directory.
here = Path(__file__).abspath().parent
if here != os.getcwd():
    print("Changing dir")
    here.chdir()

class DataBase():
    """ Simple JSON DB class """
    def __init__(self):
        self.names = []                           # List of NPC names.
        self.nodes = defaultdict(list)            # npc name paired with a list of node_ids.
        self.tags = defaultdict(list)             # node_ids paired with a list of tags.
        self.p_tags = defaultdict(dict)           # node_ids paired with a dict of string keys and int/str values.
        self.coords = defaultdict(tuple)          # node_ids paired with tuple of x,y coordinates.
        self.text = defaultdict(str)              # node_ids paired with String of text.
        self.data_path = Path("./data")

    def add_npc(self, npc):
        """
        Saves one NPC name to the db.
        npc strings should be a string, that is saved to a list.
        """
        self.names.append(npc)

    def add_node(self, npc, node):
        """
        Saves one node to the db.
        The node should be a dict, the node id as key, containing 3 more dicts.
        The first has the key 'tags', and its value should be a list containing strings.
        The second has the key 'text', its value should be a string.
        The third dict has the key p_tags and contains another dictionary.
        """
        node_id = [i for i, j in node.items()][0]
        self.nodes[npc].append(node_id)
        self.tags[node_id].append(node[node_id]["tags"])
        self.text[node_id] = node[node_id]["text"]
        self.p_tags[node_id] = node[node_id]["p_tags"]
        self.coords[node_id] = node[node_id]["coords"]

    def add_nodes(self, npc, nodes):
        """
        Adds multiple nodes to the same npc.
        """
        for node in nodes:
            self.add_node(npc, nodes[node])

    def add_data(self, data):
        for i in data.keys():
            self.add_npc(i)
            self.add_nodes(i, data[i])

    def save(self, fname):
        """
        Saves everything to files.
        """
        data = OrderedDict()
        data["names"] = self.names,
        data["nodes"] = self.nodes,
        data["text"] = self.text,
        data["tags"] = self.tags,
        data["p_tags"] = self.p_tags,
        data["coords"] = self.coords

        self.save_file(data, fname)

    def load(self, fname):
        """
        Loads everything from files.
        """
        data = self.load_file(fname)
        self.names = data["names"]
        self.nodes = data["nodes"]
        self.text = data["text"]
        self.tags = data["tags"]
        self.p_tags = data["p_tags"]
        self.coords = data["coords"]

    def save_file(self, data, fname):
        """
        Save method. Called from self.save.
        """
        print("writing data...")
        with open(fname, "w") as f:
            json.dump(data, f)

    def load_file(self, fname):
        """
        Load method. Called from self.load.
        """
        with open(fname, "r") as f:
            data = json.load(f)
        return data
