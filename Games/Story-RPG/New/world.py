#!/usr/bin/python3
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.properties import ObjectProperty, ListProperty, StringProperty, NumericProperty, DictProperty, BooleanProperty

from tools import circle_collide

class WorldElement(Image):
    name = StringProperty("")

class World(RelativeLayout):
    worldcenter = ListProperty([0,0])
    worldspeed = NumericProperty(5)
    in_world = ListProperty([])
    poi = ListProperty([])
    once = BooleanProperty(True)
    worlddict = DictProperty({
    "church":{"main":{"bg":"images/world/CI Main Back.png",
                      "clutter":"images/world/CI Main Obj.png"},

              "basement":{"bg":"images/world/CI Basement Back.png",
                          "clutter":"images/world/CI Basement Obj.png"},

              "thack_room":{"bg":"images/world/CI Player Room Back.png",
                            "clutter":"images/world/CI Player Room Obj.png"},

              "priest_room":{"bg":"images/world/CI Priest Room Back.png",
                             "clutter":"images/world/CI Priest Room Obj.png"},

              "tower":{"bg":"images/world/CI Tower Top Back.png",
                       "clutter":"images/world/CI Tower Top Obj.png"}}})

    doors = DictProperty({"church":{
                          "main":{
                          "to_basement":(1883, 327),
                          "to_thack_room":(140, 651),
                          "to_priest_room":(1496, 855),
                          "to_tower":(0,0),
                          "out":(830, 72)},

                          "basement":{
                          "from_basement":(1913, 375)},

                          "priest_room":{
                          "from_priest_room":(0,0)},

                          "tower":{
                          "from_tower":(0,0)},

                          "thack_room":{
                          "from_thack_room":(0,0)}}})

    def setupworld(self, size):
        self.size = size
        self.bg = WorldElement(source=self.worlddict["church"]["main"]["bg"])
        self.bg_clutter = WorldElement(source=self.worlddict["church"]["main"]["clutter"])
        self.add_widget(self.bg)
        self.add_widget(self.bg_clutter)
        for i, v in self.doors["church"]["main"].items():
            w = Widget(pos=v, size=(64, 64))
            w.name = i
            self.poi.append(w)

    def load_scene(self, scene, part):
        self.size = (800, 800)
        self.bg.source = self.worlddict[scene][part]["bg"]
        self.bg_clutter.source = self.worlddict[scene][part]["clutter"]
        doorlist = []
        for door in self.doors[scene][part]:
            w = Widget(pos=self.doors[scene][part][door], size=(64,64))
            w.name = door
            doorlist.append(w)
        self.poi = doorlist

    def move_world(self, direction):
        if direction == "left":
            self.worldcenter[0] -= self.worldspeed
        if direction == "right":
            self.worldcenter[0] += self.worldspeed
        if direction == "up":
            self.worldcenter[1] -= self.worldspeed
        if direction == "down":
            self.worldcenter[1] += self.worldspeed

    def collide_poi(self, w):
        poilist = [poi for poi in self.poi if circle_collide(w, poi)]
        if poilist != []:
            for p in poilist:
                if p.name == "to_basement":
                    self.load_scene("church", "basement")
                    break
                elif p.name == "to_thack_room":
                    self.load_scene("church", "thack_room")
                    break
                elif p.name == "to_priest_room":
                    self.load_scene("church", "priest_room")
                    break
                elif p.name == "to_tower":
                    self.load_scene("church", "tower")
                    break
