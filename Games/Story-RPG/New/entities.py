#!/usr/bin/python3
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.atlas import Atlas
from kivy.properties import ListProperty, ObjectProperty, DictProperty, StringProperty, NumericProperty

from tools import *

class Entity(Widget):
    frame = ObjectProperty(None)
    dirs = DictProperty({"up":(0, 3),
            "down":(0, -3),
            "left":(-3, 0),
            "right":(3, 0)})
    moving = DictProperty({"up":False,
                           "down":False,
                           "left":False,
                           "right":False})
    current = StringProperty("idle")
    framenum = NumericProperty(1)
    counter = NumericProperty(0)
    name = StringProperty("")
    collided_with = StringProperty("")

    def place(self, x, y):
        self.pos = self.to_widget(x, y)

    def entitysetup(self, atlasfile):
        self.atlas = Atlas(atlasfile)
        self.set_frame("idle", 1)
        self.gen = self._num()

    def update(self, dt):
        if self.counter > 8: # <--Animation speed.
            self.framenum = next(self.gen)
            self.counter = 0
        self.counter += 1
        self.move()
        self.collide_world()

    def move(self):
        self.current = "idle"
        for mov in self.moving:
            if self.moving[mov]:
                # Movement Code.
                self.pos = Vector(self.pos) + Vector(self.dirs[mov])

                # Collision Code.
                self.collide_npcs(mov)

                # Animation Code.
                if self.moving["right"] or self.moving["left"]:
                    if mov == "up" or mov == "down":
                        pass
                    else:
                        self.current = "walk{}".format(mov)
                else:
                    self.current = "walk{}".format(mov)
        self.set_frame(self.current, self.framenum)

    def set_frame(self, pose, num):
        if pose == "idle":
            num = 1
        self.frame = self.atlas["{}{}".format(pose, num)]

    def _num(self):
        while True:
            for i in range(1, 5):
                yield i

    def collide_world(self):
        pass

    def collide_npcs(self, mov):
        if self.name != "Thack":
            collidelist = self.parent.parent.coll_childs(self)
        else:
            collidelist = self.parent.parent.npcs.coll_childs(self)
        if collidelist != []:
            if collidelist[0].name in self.parent.in_world:
                self.collided_with = collidelist[0].name
            if mov == "up":
                self.pos = Vector(self.pos) + Vector(self.dirs["down"])
            elif mov == "down":
                self.pos = Vector(self.pos) + Vector(self.dirs["up"])
            elif mov == "left":
                self.pos = Vector(self.pos) + Vector(self.dirs["right"])
            elif mov == "right":
                self.pos = Vector(self.pos) + Vector(self.dirs["left"])

class Player(Entity):
    screen_size = ListProperty([0,0])
    def playersetup(self, screen_size):
        self.screen_size = screen_size
        self.entitysetup("images/player_sheet.atlas")
        self.name = "Thack"
        self.bind(collided_with=lambda x, y: self.parent.parent.begin_conv(y))

    def collide_world(self):
        ws = 500
        window_pos = self.to_window(self.pos[0], self.pos[1])
        if window_pos[0] < ws:
            self.parent.move_world("right")
        if window_pos[0] > self.screen_size[0]-ws:
            self.parent.move_world("left")
        if window_pos[1] < ws:
            self.parent.move_world("down")
        if window_pos[1] > self.screen_size[1]-ws:
            self.parent.move_world("up")
        self.parent.collide_poi(self)

    def keydown(self, key):
        if key in ("up", "w"):
            self.moving["up"] = True
        if key in ("down", "s"):
            self.moving["down"] = True
        if key in ("left", "a"):
            self.moving["left"] = True
        if key in ("right", "d"):
            self.moving["right"] = True

    def keyup(self, key):
        if key in ("up", "w"):
            self.moving["up"] = False
        if key in ("down", "s"):
            self.moving["down"] = False
        if key in ("left", "a"):
            self.moving["left"] = False
        if key in ("right", "d"):
            self.moving["right"] = False

class NPC(Entity):
    def npcsetup(self, atlasfile):
        self.entitysetup(atlasfile)

class NPCController(Widget):
    npcs = ListProperty(["Djonsiscus",
                         "Jarod",
                         "Tylda Travisteene",
                         "Sheila Travisteene",
                         "Mr Johes",
                         "Riff Danner"])
    npcgroup = ListProperty([])

    def controllersetup(self):
        x, y = (80, 250)
        for name in self.npcs:
            if name == "Djonsiscus":
                npc = NPC()
                npc.name = name
                npc.npcsetup("images/{}.atlas".format(name))
                npc.pos = (1955, 735)
                x += 130
                self.npcgroup.append(npc)

    def update(self, dt):
        for npc in self.npcgroup:
            npc.update(dt)

    def coll_childs(self, w):
        return [child for child in self.npcgroup if circle_collide(child, w)]
