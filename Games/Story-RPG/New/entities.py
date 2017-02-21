#!/usr/bin/python3
from kivy.uix.widget import Widget
from kivy.atlas import Atlas
from kivy.properties import ObjectProperty, DictProperty, StringProperty, NumericProperty

class Entity(Widget):
    frame = ObjectProperty(None)
    moving = DictProperty({"up":False,
                           "down":False,
                           "left":False,
                           "right":False})
    current = StringProperty("idle")
    framenum = NumericProperty(1)

    def entitysetup(self, atlasfile):
        self.atlas = Atlas(atlasfile)

    def update(self, dt):
        self.move()

    def _num(self):
        while True:
            for i in range(1, 5):
                yield i

    def move(self):
        self.current = "idle"
        for mov in self.moving:
            if self.moving[mov]:
                self.current = mov
                self.framenum = next(_num())
        self.set_frame("{}{}".format(self.current, self.framenum))


    def set_frame(self, f):
        self.frame = self.atlas[f]

class Player(Entity):
    def playersetup(self):
        self.entitysetup("images/player_sheet.atlas")

class NPC(Entity):
    def npcsetup(self):
        pass
