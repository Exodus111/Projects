#!/usr/bin/python3
from kivy.uix.relativelayout import RelativeLayout
from kivy.vector import Vector
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.properties import ObjectProperty, ListProperty, StringProperty, NumericProperty, DictProperty, BooleanProperty

from tools import circle_collide

class WorldElement(Image):
    name = StringProperty("")

class World(RelativeLayout):
    home = StringProperty("")
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
                          "to_thack_room":(146, 858),
                          "to_priest_room":(1496, 855),
                          "to_tower":(0,0),
                          "out":(830, 72)},

                          "basement":{
                          "from_basement":(1583, 192)},

                          "priest_room":{
                          "from_priest_room":(248, 84)},

                          "tower":{
                          "from_tower":(0,0)},

                          "thack_room":{
                          "from_thack_room":(248, 93)}}})

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
        self.home = "church main"

    def load_scene(self, scene, part):
        self.bg.source = self.worlddict[scene][part]["bg"]
        self.bg_clutter.source = self.worlddict[scene][part]["clutter"]
        doorlist = []
        for door in self.doors[scene][part]:
            w = Widget(pos=self.doors[scene][part][door], size=(64,64))
            w.name = door
            doorlist.append(w)
        self.poi = doorlist
        self.home = scene + " " + part
        self.add_npcs(self.parent.npcs.npcgroup)

    def add_npcs(self, npcs):
        self.in_world = []
        for child in self.children:
            if hasattr(child, "etype"):
                if child.name != "Thack":
                    self.remove_widget(child)
        for npc in npcs:
            if npc.home == self.home:
                self.in_world.append(npc.name)
                self.add_widget(npc)



    def move_world(self, direction):
        if direction == "left":
            self.worldcenter[0] -= self.worldspeed
        if direction == "right":
            self.worldcenter[0] += self.worldspeed
        if direction == "up":
            self.worldcenter[1] -= self.worldspeed
        if direction == "down":
            self.worldcenter[1] += self.worldspeed

    def center_screen(self, dt):
        pos = self.parent.player.pos
        pwin = self.parent.player.to_window(pos[0], pos[1])
        offset = Vector(self.parent.center) - Vector(pwin)
        self.worldcenter = (self.worldcenter[0]+offset[0], self.worldcenter[1]+offset[1])

    def move_player(self, pos):
        self.parent.player.pos = pos
        self.parent.center_screen(0.1)

    def collide_poi(self, w):
        poilist = [poi for poi in self.poi if circle_collide(w, poi)]
        if poilist != []:
            if self.once:
                for p in poilist:
                    if p.name == "to_basement":
                        self.load_scene("church", "basement")
                        self.size = (640*3, 416*3)
                        new_pos = self.doors["church"]["basement"]["from_basement"]
                        self.move_player(new_pos)
                        self.once = False
                        break
                    elif p.name == "to_thack_room":
                        self.load_scene("church", "thack_room")
                        self.size = (192*3, 256*3)
                        new_pos = self.doors["church"]["thack_room"]["from_thack_room"]
                        self.move_player(new_pos)
                        self.once = False
                        break
                    elif p.name == "to_priest_room":
                        self.load_scene("church", "priest_room")
                        self.size = (192*3, 256*3)
                        new_pos = self.doors["church"]["priest_room"]["from_priest_room"]
                        self.move_player(new_pos)
                        self.once = False
                        break
                    elif p.name == "to_tower":
                        self.load_scene("church", "tower")
                        self.size = (192*3, 256*3)
                        break
                    elif p.name == "from_basement":
                        self.load_scene("church", "main")
                        self.size = (768*3, 608*3)
                        new_pos = self.doors["church"]["main"]["to_basement"]
                        self.move_player(new_pos)
                        self.once = False
                        break
                    elif p.name == "from_thack_room":
                        self.load_scene("church", "main")
                        self.size = (768*3, 608*3)
                        new_pos = self.doors["church"]["main"]["to_thack_room"]
                        self.move_player(new_pos)
                        self.once = False
                        break
                    elif p.name == "from_priest_room":
                        self.load_scene("church", "main")
                        self.size = (768*3, 608*3)
                        new_pos = self.doors["church"]["main"]["to_priest_room"]
                        self.move_player(new_pos)
                        self.once = False
                        break
                    elif p.name == "from_tower":
                        self.load_scene("church", "main")
                        self.size = (768*3, 608*3)
                        new_pos = self.doors["church"]["main"]["to_tower"]
                        self.move_player(new_pos)
                        self.once = False
                        break
        else:
            self.once = True
