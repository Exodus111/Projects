#!/usr/bin/python3

from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.widget import Widget
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
        self.keyboard.bind(on_key_down=lambda *x: self.calls["keydown"](x[2], x[3]))
        self.keyboard.bind(on_key_up=lambda *x: self.calls["keyup"](x[1]))

class Game(Widget):
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

        self.player = Player()
        self.player.playersetup()

        # Adding everything to the Widget stack
        self.add_widget(self.menus)
        self.add_widget(self.events)
        self.add_widget(self.player)

    def update(self, dt):
        self.menus.update(dt)
        self.player.update(dt)

    def mouse_over(self, pos):
        pass

    def key_down(self, text, mod):
        pass

    def key_up(self, keycode):
        pass

class MainApp(App):
    def build(self):
        game = Game()
        game.gamesetup()
        Clock.schedule_interval(game.update, 1./60.)
        return game

if __name__ == "__main__":
    MainApp().run()
