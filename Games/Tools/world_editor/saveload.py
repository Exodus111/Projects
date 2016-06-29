import pickle, myfuncs
import pygame as pg
from path import Path


class SaveMap():
    def __init__(self, data):
        self.data = data.copy()

    def write_to_file(self, path):
        filename = Path(path)

        for d in self.data:
            if d != "Name":
                savename = "{}{}{}".format("./save/", d, ".png")
                savename = savename.lower()
                pg.image.save(self.data[d].map, savename)
                self.data[d].saved_surf = savename
                self.data[d].map = None
                for tile in self.data[d].group:
                    tile.image = None
        pickle.dump(self.data, open(filename, "wb"))


class LoadMap():
    def __init__(self):
        pass

    def load_from_file(self, filename, menu_list):
        filename = Path(filename)
        data = pickle.load(open(filename, "rb"))
        for d in data:
            if d != "Name":
                data[d].image = pg.image.load(data[d].image_string).convert_alpha()
                data[d].map = pg.image.load(data[d].saved_surf).convert_alpha()
                for tile in data[d].group:
                    if tile.filename != data[d].image_string:
                        num = int(tile.filename)
                        tile.image = menu_list[num]
                    else:
                        tile.image = data[d].image
        return data

class Export():
    def __init__(self, name, data):
        self.name = name
        self.data = data
