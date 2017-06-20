#!/usr/bin/python3
import kivy
kivy.require("1.9.0")

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics import Rectangle
from kivy.clock import Clock
from kivy.properties import ObjectProperty

# Need to bring in Game Files now.

class Main(Widget):
    foreground = ObjectProperty(None)
    background = ObjectProperty(None)

    def setup(self):
        mn = Image(source="imgs/main.png").texture
        #fg = Image(source="imgs/foreground_.png").texture
        bg = Image(source="imgs/background_.png").texture
        with self.canvas:
            Rectangle(texture=mn, pos=[0,200], size=mn.size)
            Rectangle(texture=bg, pos=[0,200], size=bg.size)
        #    Rectangle(texture=fg, pos=[0,200], size=fg.size)

    def update(self, dt):
        pass

class ImageCheckApp(App):
    def build(self):
        game = Main()
        game.setup()
        Clock.schedule_interval(game.update, 1/60)
        return game

if __name__ == "__main__":
    app = ImageCheckApp()
    app.run()
