#!/usr/bin/python3
from kivy.config import Config
Config.set("graphics", "fullscreen", "auto")

from kivy.core.window import Window
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import DictProperty, ListProperty, StringProperty

from entities import *
from dialogue import *
from gui import *
from world import *

from random import choice

class EventHandler(Widget):
    calls = DictProperty()
    def eventsetup(self):
        Window.bind(mouse_pos=lambda *x: self.calls["mouseover"](x[1]))
        self.keyboard = Window.request_keyboard(lambda : None, self)
        self.keyboard.bind(on_key_down=lambda *x: self.calls["keydown"](x[1], x[3]))
        self.keyboard.bind(on_key_up=lambda *x: self.calls["keyup"](x[1]))

class Game(Widget):
    temp_text = StringProperty("")
    temp_textlist = ListProperty(["", "", "", ""])


    def gamesetup(self):
        # Setting up the Event Handler.
        self.events = EventHandler()
        self.events.calls["keydown"] = self.key_down
        self.events.calls["keyup"] = self.key_up
        self.events.calls["mouseover"] = self.mouse_over
        self.events.eventsetup()

        # Setting up the Menu controller.
        self.menus = Menus(size=self.size)
        self.menus.menusetup()

        # Setting up the NPCs.
        self.npcs = NPCController()
        self.npcs.controllersetup()

        # Setting up the Player.
        self.player = Player()
        self.player.playersetup()

        # Adding everything to the Widget stack
        self.add_widget(self.events)
        self.add_widget(self.npcs)
        self.add_widget(self.player)
        self.add_widget(self.menus)

    def update(self, dt):
        self.menus.update(dt)
        self.npcs.update(dt)
        self.player.update(dt)

    def mouse_over(self, pos):
        pass

    def key_down(self, key, mod):
        if key[1] in ("w", "a", "s", "d", "up", "down", "left", "right"):
            self.player.keydown(key[1])
        if key[1] == "spacebar":
            self.menus.menu_on = not self.menus.menu_on


    def change_top_text(self, txt):
        """
          Top text area contains only one ppiece of text at a time.
        """
        self.temp_text = txt
        self.menus.fade_out_top = True

    def change_bottom_text(self, txtlist):
        """
         Bottom Text contains 4 question areas.
        """
        self.menus.bottomtext = txtlist
        self.menus.fade_out_bottom = True

    def key_up(self, key):
        if key[1] in ("w", "a", "s", "d", "up", "down", "left", "right"):
            self.player.keyup(key[1])

class MainApp(App):
    def build(self):
        game = Game(size=Window.size)
        game.gamesetup()
        Clock.schedule_interval(game.update, 1./60.)
        return game

if __name__ == "__main__":
    MainApp().run()
