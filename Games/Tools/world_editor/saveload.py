#!/usr/bin/python3
from collections import defaultdict
from path import Path
import json

class SaveMap():
    def __init__(self, empty):
        self.maps = defaultdict(dict)
        self.empty = empty
        self.savefolder = Path("./save")

    def add_map(self, mymap):
        self.maps[mymap.name]["tiles"] = defaultdict(list)
        self.maps[mymap.name]["info"] = {
            "name":mymap.name,
            "size":mymap.screen_size,
            "grid":mymap.grid,
            "block":mymap.block,
            "color":mymap.color
        }
        for tile in mymap.group:
            if self.empty != tile.filename:
                self.maps[mymap.name]["tiles"][tile.filename].append(tile.rect.topleft)

    def write_to_file(self):
        num = len(self.savefolder.files("*.sav"))
        with open("./save/savefile{}.sav".format(num), "w+") as f:
            json.dump(self.maps, f, indent=4, sort_keys=True)
        print("Writing Save file...")

class LoadMap():
    def __init__(self, filename):
        fullpath = Path("./save/") + filename
        with open(fullpath, "r+") as f:
            self.maps = json.load(f)

    def extract_map(self, mymap):
        pass
