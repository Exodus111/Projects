#!/usr/bin/python3
import kivy
kivy.require("1.9.0")

from kivy.config import Config
xwidth, xheight = 1024, 768
Config.set("graphics", "width", xwidth)
Config.set("graphics", "height", xheight)
Config.set('input', 'mouse', 'mouse, multitouch_on_demand')
Config.write()
from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import *

from gui.gui import GUI
from logic.dialogue import Dialogue
from logic.events import EventCreator
from random import choice, randint
import json

class MyGame(Widget):
    ordinal = lambda c, n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])
    button_cooldown = BooleanProperty(True)

    def cooldown_flipper(self, *_):
        self.button_cooldown = not self.button_cooldown

    def setup(self):
        Window.bind(size=self.size_changed)
        self.keyboard = Window.request_keyboard(lambda : None, self)
        self.keyboard.bind(on_key_down=self.keydown)

        # Initializing Dialogue
        with open("data.json", "r+") as f:
            data = json.load(f)
        self.events = EventCreator()
        self.diag = Dialogue(self.events, **data)
        
        self.button1 = Button(text="Donald", on_release=lambda *_: self.start_conversation("Donald"))
        self.button2 = Button(text="Heidi", on_release=lambda *_: self.start_conversation("Heidi"))
        self.button3 = Button(text="Trigger1", on_release=lambda *_: self.start_conversation("Trigger1"))
        self.buttons = BoxLayout(orientation="vertical")
        self.buttons.add_widget(self.button1)
        self.buttons.add_widget(self.button2)
        self.buttons.add_widget(self.button3)
        self.add_widget(self.buttons)
        self.buttons.pos = (xwidth/2, xheight/2)

        # Initializing GUI elements.
        self.gui = GUI(size=(xwidth, xheight))
        self.gui.setup()
        self.add_widget(self.gui)

    def start_conversation(self, name):
        # Might have had a minor mental breakdown when I wrote this code.
        # But it works so...
        once = False
        while True:
            if self.diag.current_conv != None:
                if self.diag.current_conv.npc.lower() == name.lower():
                    if self.diag.current_conv.type == "comment":
                        self.manage_comments()
                        return
            if once:
                break
            once = True
            self.diag.find_conversation(name)
        conv = self.diag.current_conv
        self.gui.add_text_to_conv_panels({"top_text":conv.top_text, "question_list":conv.bottom_question_list})
        self.gui.conv_panels_toggle()

    def question_picked(self, text):
        if self.button_cooldown:      #<-- Needed because Kivy sometimes presses a button multiple times.
            self.diag.current_conv.question_picked(text)
            conv = self.diag.current_conv
            self.gui.add_text_to_conv_panels({"top_text":conv.top_text, "question_list":conv.bottom_question_list})
            self.cooldown_flipper()
            Clock.schedule_once(self.cooldown_flipper, 0.1)

    def size_changed(self, _, value):
        self.gui.size_changed(value)

    def manage_comments(self, commentlist=None):
        if commentlist == None:
            commentlist = self.diag.current_conv.comments
        for comment in commentlist:
            comment["pos"] = self.get_npc_pos(comment["npc"])
        self.gui.add_comments(commentlist)

    def get_npc_pos(self, npc):
        pos = (0,0)
        if npc == "donald":
            return (xwidth/2-200, xheight/2)
        elif npc == "heidi":
            return (xwidth/2+200, xheight/2)
        elif npc == "player":
            return (xwidth/2, xheight/2+200)

    def update(self, dt):
        self.events.update(dt)
        self.gui.update(dt)
        if self.diag.current_conv != None:
            if self.diag.current_conv.end_conversation:
                self.gui.conv_panels_toggle()
                self.diag.current_conv.end_conversation = False
        if self.diag.card_inventory != []:
            card = self.diag.card_inventory[0]
            self.gui.add_card(card)
            del(self.diag.card_inventory[0])

        if self.events.playerwait_30:
            self.events.playerwait_30 = False
            node_list = []
            for comm in self.diag.comments:
                for node in comm.node_db:
                    if "event_idle_30" in node["tags"]:
                        node_list = comm.comments
                        break
                if node_list != []:
                    break
            if node_list != []:
                self.manage_comments(node_list) #<--- FIX THIS!!!

    def keydown(self, *e):
        if e[1][1] == "spacebar":
            self.gui.conv_panels_toggle()
        elif e[1][1] == "e":
            self.gui.toggle_card_menu()
        elif e[1][1] == "r":
            pass
            #self.speak_comment()

class MainApp(App):

    def build(self):
        game = MyGame(size=(xwidth, xheight))
        game.setup()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game

MainApp().run()
