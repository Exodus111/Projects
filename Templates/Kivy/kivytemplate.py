#!/usr/bin/python3
import kivy
kivy.require("1.9.0")

from kivy.config import Config
xwidth, xheight = 1024, 960
Config.set("graphics", "width", xwidth)
Config.set("graphics", "height", xheight)
Config.write()
from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.widget import Widget

class MyGame(Widget):
    pass

    def setup(self):
        pass

    def update(self, dt):
        pass

class MyApp(App):
    def build(self):
        game = MyGame()
	game.setup()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game

MyApp().run()
