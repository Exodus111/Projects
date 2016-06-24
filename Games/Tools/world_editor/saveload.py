import pickle, myfuncs
import pygame as pg
from path import Path


class SaveMap():
    def __init__(self, data):
        self.data = data

    def write_to_file(self, path):
        filename = Path(path)

        for d in self.data:
            if d != "Name":
                savename = "{}{}{}".format("./save/", d, ".bmp")
                savename = savename.lower()
                pg.image.save(self.data[d].map, savename)
                self.data[d].saved_surf = savename
        pickle.dump(self.data, open(filename, "wb"))


class LoadMap():
    def __init__(self):
        pass

    def load_from_file(self, filename):
        filename = Path(filename)
        data = pickle.load(open(filename, "rb"))
        for d in data:
            if d != "Name":
                data[d].image = pg.image.load(data[d].image_string).convert_alpha()
                data[d].group = data[d].make_grid()
                data[d].map = pg.image.load(data[d].saved_surf).convert_alpha()
        return data

class Export():
    def __init__(self, name, data):
        self.name = name
        self.data = data
