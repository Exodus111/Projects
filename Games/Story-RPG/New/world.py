#!/usr/bin/python3
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, DictProperty, BooleanProperty

from tools import circle_collide

class WorldElement(Image):
    pass

class World(RelativeLayout):
    worldcenter = ListProperty([0,0])
    worldspeed = NumericProperty(5)
    in_world = ListProperty([])
    poi_points = ListProperty([])
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

    def setupworld(self):
        self.bg = WorldElement(source=self.worlddict["church"]["main"]["bg"])
        self.bg_clutter = WorldElement(source=self.worlddict["church"]["main"]["clutter"])
        self.add_widget(self.bg)
        self.add_widget(self.bg_clutter)
        w = Widget(pos=(1883, 327), size=(64, 64))
        w.name = "basement"
        self.poi_points.append(w)
        for poi in self.poi_points:
            self.add_widget(poi)

    def load_scene(self, scene, part):
        self.bg.source = self.worlddict[scene][part]["bg"]
        self.bg_clutter.source = self.worlddict[scene][part]["clutter"]


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
        poilist = [poi for poi in self.poi_points if circle_collide(w, poi)]
        if poilist != []:
            if self.once:
                for p in poilist:
                    if p.name == "basement":
                        self.load_scene("church", "basement")
                        for w in self.parent.npcs.npcgroup:
                            if w.name == "Djonsiscus":
                                self.in_world.remove(w.name)
                                self.remove_widget(w)
                                self.once = False
                                break
                                break
