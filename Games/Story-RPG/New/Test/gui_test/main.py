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
    wsize = (xwidth, xheight)

    def setup(self):
        self.keyboard = Window.request_keyboard(lambda : None, self)
        self.keyboard.bind(on_key_down=self.keydown)
        self.gui = GUI()
        self.gui.setup(self.wsize)
        self.add_widget(self.gui)

    def update(self, dt):
        self.gui.update(dt)

    def keydown(self, *e):
        if e[1][1] == "spacebar":
            if self.gui.right_panel.e_pos[0] == self.wsize[0]:
                self.gui.right_panel.move([self.wsize[0]-self.gui.right_panel.e_size[0], None])
            else:
                self.gui.right_panel.move([self.wsize[0], None])
        if e[1][1] == "c":
            if self.gui.left_panel.e_pos[0] != 0:
                self.gui.left_panel.move([0, None])
            else:
                self.gui.left_panel.move([-self.gui.left_panel.e_size[0], None])

class MainApp(App):
    def build(self):
        game = MyGame()
        game.setup()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game

MainApp().run()
