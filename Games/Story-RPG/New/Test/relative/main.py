#!/usr/bin/python3
from screeninfo import get_monitors
_M = [m for m in get_monitors()][0]
SIZE = (_M.width, _M.height)

import kivy
kivy.require("1.9.0")

from kivy.config import Config
Config.set("graphics", "width", SIZE[0])
Config.set("graphics", "height", SIZE[1])
Config.write()
from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Line, Color, Rectangle
from kivy.properties import *

class MyBackground(Widget):
    def setup(self):
        pass

class MyForeground(Widget):
    def setup(self):
        pass

class MyController(Widget):
    move = ListProperty([SIZE[0]/4, SIZE[1]/4])

    def setup(self):
        widget_size = (50, 50)
        self.collider = Widget(size_hint=(None, None), size=widget_size, pos=self.pos2center(widget_size)) # Move this to the center!!
        self.add_widget(self.collider)

    def show_rect(self):
        self.collider.canvas.clear()
        with self.collider.canvas:
            Color(rgba=[0.,1.,0.,.5])                          # <-- Green !!
            Rectangle(pos=self.pos, size=self.size)

    def update(self, dt):
        self.collider.pos = self.pos2center(self.collider.size)
        self.show_rect()

    def pos2center(self, size):
        return (self.pos[0] + self.size[0]/2 - size[0]/2, self.pos[1] + self.size[1]/2 - size[1]/2)

class MyGame(RelativeLayout):
    bg = ObjectProperty()
    fg = ObjectProperty()
    controller = ObjectProperty()

    def setup(self):
        self.keyboard = Window.request_keyboard(lambda : None, self)
        self.keyboard.bind(on_key_down=self.keydown)
        self.keyboard.bind(on_key_up=self.keyup)
        self.controller.setup()

    def keydown(self, *args):
        if args[1][1] == "w":
            self.controller.move[1] += 4
        if args[1][1] == "a":
            self.controller.move[0] -= 4
        if args[1][1] == "s":
            self.controller.move[1] -= 4
        if args[1][1] == "d":
            self.controller.move[0] += 4

    def keyup(self, key, *_):
        pass

    def update(self, dt):
        self.controller.update(dt)

class MyApp(App):
    def build(self):
        game = MyGame(size=SIZE)
        game.setup()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game

MyApp().run()
