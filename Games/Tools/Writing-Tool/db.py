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
        self.links = defaultdict(dict)           # node_ids paired with a dict of string keys and int/str values.
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
        The node should be a dict, the node id as key, containing 4 more dicts.
        The first has the key 'tags', and its value should be a list containing strings.
        The second has the key 'text', its value should be a string.
        The third dict has the key links and contains another dictionary.
        The fourth...
        """
        node_id = [i for i, j in node.items()][0]
        if node_id not in self.nodes[npc]:
            self.nodes[npc].append(node_id)
        self.tags[node_id] = node[node_id]["tags"].copy()
        self.text[node_id] = node[node_id]["text"]
        self.links[node_id] = node[node_id]["links"].copy()
        self.coords[node_id] = node[node_id]["coords"]

    def update_links(self, node, l):
        for t in l:
            if t not in self.links[node]:
                self.links[node].append(t)

    def delete_node(self, npc, node_id):
        self.nodes[npc].remove(node_id)
        del self.tags[node_id]
        del self.text[node_id]
        del self.links[node_id]
        del self.coords[node_id]
        for n in self.links:
            for link in self.links[n]:
                if link == node_id:
                    self.links[n].remove(link)

    def delete_link(self, origin, target):
            for link in self.links[origin]:
                if link == target:
                    self.links[origin].remove(link)

    def save(self, fname):
        """
        Saves everything to files.
        """
        data = OrderedDict()
        data["names"] = self.names
        data["nodes"] = self.nodes
        data["text"] = self.text
        data["tags"] = self.tags
        data["links"] = self.links
        data["coords"] = self.coords

        self.save_file(data, fname)

    def save_file(self, data, fname):
        """
        Save method. Called from self.save.
        """
        print("writing data...")
        with open(fname, "w") as f:
            json.dump(data, f, indent=4, sort_keys=True)

    def load(self, fname):
        """
        Loads everything from files.
        """
        data = self.load_file(fname)
        self.names = data["names"]
        self.nodes = data["nodes"]
        self.text = data["text"]
        self.tags = data["tags"]
        self.links = data["links"]
        self.coords = data["coords"]

    def load_file(self, fname):
        """
        Load method. Called from self.load.
        """
        with open(fname, "r") as f:
            data = json.load(f)
        return data
