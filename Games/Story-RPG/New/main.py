#!/usr/bin/python3

from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import DictProperty

from entities import *
from dialogue import *
from gui import *
from world import *

class EventHandler(Widget):
    calls = DictProperty()
    def eventsetup(self):
        Window.bind(mouse_pos=lambda *x: self.calls["mouseover"](x[1]))
        self.keyboard = Window.request_keyboard(lambda : None, self)
        self.keyboard.bind(on_key_down=lambda *x: self.calls["keydown"](x[1], x[3]))
        self.keyboard.bind(on_key_up=lambda *x: self.calls["keyup"](x[1]))

class Game(FloatLayout):
    def gamesetup(self):
        # Setting up the Event Handler.
        self.events = EventHandler()
        self.events.calls["keydown"] = self.key_down
        self.events.calls["keyup"] = self.key_up
        self.events.calls["mouseover"] = self.mouse_over
        self.events.eventsetup()

        # Setting up the Menu controller.
        self.menus = Menus()
        self.menus.menusetup()

        # Setting up the NPCs.
        self.npcs = NPCController()
        self.npcs.controllersetup()

        # Setting up the Player.
        self.player = Player()
        self.player.playersetup()

        # Adding everything to the Widget stack
        self.add_widget(self.menus)
        self.add_widget(self.events)
        self.add_widget(self.npcs)
        self.add_widget(self.player)

    def update(self, dt):
        self.menus.update(dt)
        self.npcs.update(dt)
        self.player.update(dt)

    def mouse_over(self, pos):
        pass

    def key_down(self, key, mod):
        if key[1] in ("w", "a", "s", "d", "up", "down", "left", "right"):
            self.player.keydown(key[1])

    def key_up(self, key):
        if key[1] in ("w", "a", "s", "d", "up", "down", "left", "right"):
            self.player.keyup(key[1])

class MainApp(App):
    def build(self):
        game = Game()
        game.gamesetup()
        Clock.schedule_interval(game.update, 1./60.)
        return game

if __name__ == "__main__":
    MainApp().run()
