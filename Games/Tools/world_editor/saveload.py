import json
import numpy as np
import pygame as pg
from load import Tile, SpriteSheet
from path import Path
from myfuncs import *

class SaveMap(object):
    def __init__(self, name, size, block, sheetfile, group, fg_group=None):
        self.name = name
        self.size = size
        self.save_dic = {"Name":name,
                         "Size":size,
                         "Block size":block,
                         "Sheet File":sheetfile,
                         "FileIDs":{}}
        self.read_sheet(sheetfile)
        self.bgmap_array = self.read_map(block, group)
        if fg_group != None:
            self.fgmap_array = self.read_map(block, fg_group)
        else:
            self.fgmap_array = None

    def read_sheet(self, sheetfile):
        sheet = SpriteSheet(sheetfile, 64, (0,0), (8,44))
        imagelist = sum(sheet.image_list, [])
        size = len(imagelist)
        image_dict = {}
        for num in xrange(size):
            num += 1
            self.save_dic["FileIDs"]["maptile{}".format(num)] = {"id":num}

    def read_map(self, block, group):
        npsize = tuple_div(self.size, block)
        nparray = np.zeros(npsize, "int16")
        for sprite in group:
            xy = tuple_div(sprite.xy, block)
            if sprite.filename in self.save_dic["FileIDs"].keys():
                nparray[xy] = self.save_dic["FileIDs"][sprite.filename]["id"]
        return nparray

    def write_to_file(self):
        savepath = Path("./save")
        filelist = [f for f in savepath.files("*.sav")]
        num = 1
        if filelist != []:
            while "./save/{}{}.sav".format(self.name, num) in filelist:
                num += 1
        self._write_array("./save/bg_{}{}.npy".format(self.name, num), self.bgmap_array)
        if self.fgmap_array != None:
            self._write_array("./save/fg_{}{}.npy".format(self.name, num), self.fgmap_array, False)
        with open("./save/{}{}.sav".format(self.name, num), "w") as outfile:
            json.dump(self.save_dic, outfile, sort_keys=True, indent=4)

    def _write_array(self, name, maparray, bg=True):
        if bg:
            suf = "bg"
        else:
            suf = "fg"
        with open(name, "w") as npfile:
            np.save(npfile, maparray)
        self.save_dic["Mapfile_{}".format(suf)] = name


class LoadMap(object):
    """Load Game Object"""
    def __init__(self, name):
        print name
        self.default = "./tiles/Empty_tile_64p.png"
        self.name = name
        self.dict = self.load_file(name)
        self.image_dict = self.read_sheet()
        if self.dict != None:
            self.bg_group = self.generate_group("bg")
            self.fg_group = self.generate_group("fg")

    def read_sheet(self):
        sheet = SpriteSheet(self.dict["Sheet File"], 64, (0,0), (8,44))
        imagelist = sum(sheet.image_list, [])
        image_dict = {}
        for num, image in enumerate(imagelist):
            name = "maptile{}".format(num)
            if name in self.dict["FileIDs"].keys():
                image_dict[self.dict["FileIDs"][name]["id"]] = image
        return image_dict

    def generate_group(self, suf):
        with open("{}".format(self.dict["Mapfile_{}".format(suf)]), "r+") as outfile:
            array = np.load(outfile)
        group = pg.sprite.LayeredDirty()
        size = tuple_div(self.dict["Size"], self.dict["Block size"])
        for x in xrange(size[0]):
            for y in xrange(size[1]):
                num = array[x][y]
                xy = tuple_mult((x,y), self.dict["Block size"])
                tile = self.make_tile(num, xy)
                group.add(tile)
        return group

    def make_tile(self, num, xy):
        if num != 0:
            image = self.image_dict[num]
            tile = Tile(None, xy)
            tile.image = image
            tile.reload()
        else:
            print "We got a Zero!"
            tile = Tile(self.default, xy)
        tile.dirty = 1
        return tile

    def load_file(self, name):
        folder = Path("./save")
        savfiles = [f for f in folder.files("*.sav")]
        if name in savfiles:
            with open(name, "r") as outfile:
                return json.loads(outfile.read())
        else:
            print "File not Found"
            return None
