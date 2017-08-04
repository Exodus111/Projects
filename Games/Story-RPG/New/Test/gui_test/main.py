#!/usr/bin/python3
import kivy
kivy.require("1.9.0")

from kivy.config import Config
xwidth, xheight = 1024, 768
Config.set("graphics", "width", xwidth)
Config.set("graphics", "height", xheight)
Config.write()
from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.widget import Widget

from gui_test import GUI

class MyGame(Widget):

    def setup(self):
        self.keyboard = Window.request_keyboard(lambda : None, self)
        self.keyboard.bind(on_key_down=self.keydown)
        self.gui = GUI(size=(xwidth, xheight))
        self.gui.setup()
        self.add_widget(self.gui)

    def update(self, dt):
        self.gui.update(dt)

    def keydown(self, *e):
        if e[1][1] == "spacebar":
            self.gui.toggle_menu()
        if e[1][1] == "c":
            pass

class MainApp(App):
    def build(self):
        game = MyGame()
        game.setup()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game

MainApp().run()
