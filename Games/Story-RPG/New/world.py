#!/usr/bin/python3
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.properties import ObjectProperty, ListProperty, NumericProperty

class World(RelativeLayout):
    worldcenter = ListProperty([0,0])
    worldspeed = NumericProperty(5)

    def setupworld(self):
        self.bg =  WorldElement(source="images/world/CI Main Back.png")
        self.clutter = WorldElement(source="images/world/CI Main Obj.png")
        self.add_widget(self.bg)
        self.add_widget(self.clutter)

    def move_world(self, direction):
        if direction == "left":
            self.worldcenter[0] -= self.worldspeed
        if direction == "right":
            self.worldcenter[0] += self.worldspeed
        if direction == "up":
            self.worldcenter[1] -= self.worldspeed
        if direction == "down":
            self.worldcenter[1] += self.worldspeed

class WorldElement(Image):
    pass
