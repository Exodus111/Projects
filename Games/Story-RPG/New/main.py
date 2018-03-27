#!/usr/bin/python3

from screeninfo import get_monitors
_M = [m for m in get_monitors()][0]

SIZE = (_M.width, _M.height)

from kivy.config import Config
Config.set("graphics", "borderless", "1")
Config.set("graphics", "window_state", "maximized")
Config.set("graphics", "width", SIZE[0])
Config.set("graphics", "height", SIZE[1])

from kivy.core.text import LabelBase
LabelBase.register(name="vcrmono", fn_regular="fonts/VCR_OSD_MONO_1.001.ttf")

from kivy.core.window import Window
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import *

from entities import Player, NPCController, TestWidget
from world import World
from gui.gui import GUI
from gui.startmenu import StartMenu
from logic.alt_logic import Dialogue, DialogueSystem

#from logic.dialogue import Dialogue
from logic.events import EventCreator

import json
from random import choice

class InputHandler(Widget):
    calls = DictProperty()
    def eventsetup(self):
        Window.bind(mouse_pos=lambda *x: self.calls["mouseover"](x[1]))
        self.keyboard = Window.request_keyboard(lambda : None, self)
        self.keyboard.bind(on_key_down=lambda *x: self.calls["keydown"](x[1], x[3]))
        self.keyboard.bind(on_key_up=lambda *x: self.calls["keyup"](x[1]))

class Game(Widget):
    temp_text = StringProperty()
    temp_textlist = ListProperty(["", "", "", ""])
    button_cooldown = BooleanProperty(True)
    card_counter = DictProperty({"inv":0, "ret":0})
    menu_on = BooleanProperty(True)
    in_conversation = BooleanProperty(False)
    game_started = BooleanProperty(False)

    def gamesetup(self):
        # Setting up the Input Handler.
        self.input = InputHandler()
        self.input.calls["keydown"] = self.key_down
        self.input.calls["keyup"] = self.key_up
        self.input.calls["mouseover"] = self.mouse_over
        self.input.eventsetup()
        self.events = EventCreator(self)

        # Start Menu
        self.startmenu = StartMenu()
        self.add_widget(self.startmenu)
        self.startmenu.setup(SIZE)

    def start_new_game(self):
        self.game_started = True

        # Setting up the Gui controller.
        self.gui = GUI(size=SIZE)
        self.gui.setup()

        # Setting up the NPCs.
        self.npcs = NPCController()
        self.npcs.controllersetup(SIZE)

        # Setting up the Player.
        self.player = Player(size=(48,110))
        self.player.place(Window.center[0], Window.center[1])
        self.player.pos = [900, 500]
        self.player.playersetup(Window.size)

        # Setting up the world.
        self.world = World()
        self.world.worldcenter = self.center
        self.world.setupworld()

        # Adding everything to the Widget stack
        self.add_widget(self.input)
        self.world.add_npcs(self.npcs.npcgroup)
        self.world.add_widget(self.player, index=2)
        self.add_widget(self.world)
        self.world.set_home_text(self.world.home)

        self.add_widget(self.gui)         # <-- GUI goes last.

        # Setting up the Dialogue controller.
        with open("data/dialogue/dialogue.json", "r+") as f:
            data = json.load(f)
        diag_data = Dialogue(data)
        self.events.setup_dialogue(diag_data)
        self.dialogue = DialogueSystem(self, self.events, diag_data)

        self.gui.hud.add_text_to_top_bar(text2=self.world.home)

        # Centering Screen on the player
        self.center_screen(0.2)

    def key_down(self, key, mod):
        if not self.menu_on:
            if key[1] in ("w", "a", "s", "d", "up", "down", "left", "right"):
                self.player.keydown(key[1])
            elif key[1] == "spacebar":
                if not self.gui.next_comment:
                    self.gui.next_comment = True
                else:
                    print(self.player.pos)

    def key_up(self, key):
        if not self.menu_on:
            if key[1] in ("w", "a", "s", "d", "up", "down", "left", "right"):
                self.player.keyup(key[1])

    def change_resolution(self, new):
        global SIZE
        SIZE = new
        self.startmenu.gamesize = SIZE

    def draw_test_nodes(self):
        for node in self.npcs.npc_paths['djonsiscus_01']["points"]:
            w = TestWidget(pos=node)
            self.world.add_widget(w)

    def center_screen(self, delay=0.1):
        Clock.schedule_once(self.world.center_screen, delay)

    def update(self, dt):
        if self.game_started:
            if not self.in_conversation:
                self.npcs.update(dt)
                self.player.update(dt)
            else:
                self.player.set_frame("idle", 1)
                for direction in self.player.moving: direction = False
                self.player.collide_world(x=(SIZE[0]/2)-50, y=(SIZE[1]/2)-50, speedup=25)
            #self.update_cards(dt)
            if self.dialogue.current_conv != None:
                if self.dialogue.current_conv.end_conversation:
                    self.gui.conv_panels_toggle()
                    self.dialogue.current_conv.end_conversation = False
                    self.in_conversation = False
            self.gui.update(dt)
        self.events.update(dt)

#### GUI Methods

    def insert_menu(self, menu):
        self.add_widget(menu)
        self.menu_on_off()

    def menu_on_off(self):
        self.menu_on = not self.menu_on
        if self.menu_on:
            self.add_widget(self.startmenu)
        else:
            self.remove_widget(self.startmenu)

    def toggle_classmenu(self):
        if self.gui.classmenu.alpha == 0.:
            self.in_conversation = True
        else:
            self.in_conversation = False
        self.gui.toggle_class_menu()

    def size_changed(self, _, value):
        self.gui.size_changed(value)

    def mouse_over(self, pos):
        if self.game_started:
            if self.gui.classmenu.alpha != 0.:
                self.gui.classmenu.check_for_hover(pos)

##### Dialogue Methods

    def question_picked(self, text):
        if self.button_cooldown:      #<-- Needed because Kivy sometimes presses a button multiple times.
            self.dialogue.next_step("question", text)
            self.cooldown_flipper()
            Clock.schedule_once(self.cooldown_flipper, 0.1)

    def begin_conv(self, name):
        if self.events.check_cooldown("Conversation", 2):
            if not self.in_conversation:
                self.dialogue.start_conversation(name)
                if self.dialogue.current_conv.type != "comment":
                    self.events.reset_cooldown("Conversation")
                    self.in_conversation = True

    def update_cards(self, dt):
        if len(self.dialogue.card_inventory) != self.card_counter["inv"]:
            card = self.dialogue.card_inventory[-1]
            self.gui.add_card(card)
            self.card_counter["inv"] += 1

        if len(self.dialogue.retired_cards) != self.card_counter["ret"]:
            card_title = self.dialogue.tag_strip(self.dialogue.retired_cards[-1], "card")
            self.gui.retire_card(card_title)
            self.card_counter["ret"] += 1
            self.card_counter["inv"] -= 1

        if self.dialogue.card_changed != None:
            self.gui.update_card(self.dialogue.card_changed)
            self.dialogue.card_changed = None

    def cooldown_flipper(self, *_):
        self.button_cooldown = not self.button_cooldown

    def cooldown(self, call, time):
        Clock.schedule_once(call, time)

class MainApp(App):
    def build(self):
        game = Game(size=SIZE)
        game.gamesetup()
        Clock.schedule_interval(game.update, 1./30.)
        return game

if __name__ == "__main__":
    MainApp().run()
