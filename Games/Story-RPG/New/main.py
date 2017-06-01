#!/usr/bin/python3
from kivy.config import Config
Config.set("graphics", "fullscreen", "fake")

from kivy.core.window import Window
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import DictProperty, ListProperty, StringProperty

from entities import Player, NPCController
from dialogue import Dialogue
from gui import Menus
from world import World

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

        # Setting up the world.
        self.world = World()
        self.world.worldcenter = self.center
        self.world.setupworld()

        # Setting up the NPCs.
        self.npcs = NPCController()
        self.npcs.controllersetup()

        # Setting up the Player.
        self.player = Player(size=(48,110))
        self.player.playersetup(Window.size)
        self.player.place(Window.center[0], Window.center[1])
        self.player.pos = [900, 500]

        # Setting up the Dialogue controller.
        self.dialogue = Dialogue()
        self.dialogue.dialoguesetup()

        # Adding everything to the Widget stack
        self.add_widget(self.events)
        self.world.add_npcs(self.npcs.npcgroup)
        self.world.add_widget(self.player)
        self.world.add_fg()
        self.add_widget(self.world)
        self.add_widget(self.menus)
        self.add_widget(self.dialogue)

        # Centering Screen on the player
        self.center_screen(0.2)

    def center_screen(self, delay=0.1):
        Clock.schedule_once(self.world.center_screen, delay)

    def update(self, dt):
        self.menus.update(dt)
        self.npcs.update(dt)
        self.player.update(dt)

    def mouse_over(self, pos):
        pass

    def key_down(self, key, mod):
        if key[1] in ("w", "a", "s", "d", "up", "down", "left", "right"):
            self.player.keydown(key[1])
        elif key[1] == "spacebar":
            print(self.player.pos, self.player.center)

    def key_up(self, key):
        if key[1] in ("w", "a", "s", "d", "up", "down", "left", "right"):
            self.player.keyup(key[1])

    def begin_conv(self, npc):
        self.dialogue.npc = npc
        self.dialogue.start_conv()
        self.menus.menu_on = not self.menus.menu_on

    def change_top_text(self, txt):
        """
          Top text area contains only one piece of text at a time.
        """
        self.temp_text = txt
        self.menus.fade_out_top = True

    def change_bottom_text(self, txtlist):
        """
         Bottom Text contains 4 question areas.
        """
        for num, _ in enumerate(self.menus.bottomtext):
            try:
                self.menus.bottomtext[num] = txtlist[num]
            except IndexError:
                self.menus.bottomtext[num] = ""
        self.menus.fade_out_bottom = True

class MainApp(App):
    def build(self):
        game = Game(size=Window.size)
        game.gamesetup()
        Clock.schedule_interval(game.update, 1./60.)
        return game

if __name__ == "__main__":
    MainApp().run()
