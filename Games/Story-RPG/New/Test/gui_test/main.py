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
from kivy.properties import *

from gui import Menus
from hud import HUD
from conversation import Conversation
from random import choice, randint

def lor():
    return "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque nec lectus sit amet sapien imperdiet lobortis. Nunc congue arcu dictum dui egestas, vel semper ipsum pharetra. Etiam interdum neque malesuada tellus rhoncus bibendum. Aenean lobortis interdum purus vel gravida. Maecenas ut nisi at lacus consequat venenatis. Curabitur nec pulvinar massa, sit amet egestas mauris. Fusce eu sagittis arcu, vel cursus quam. Suspendisse bibendum consequat aliquet. In eu tempor elit, in pulvinar nisl. Nam tincidunt vulputate efficitur. Etiam feugiat lacus id mi tristique ultrices. Nullam eget nulla ante. Morbi eget ultrices neque."

class MyGame(Widget):
    adder = NumericProperty(0)
    ordinal = lambda c, n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])
    panel_toggle = BooleanProperty(False)
    panel_text = DictProperty({"top_text":lor(),
                               "question_list":["Question Goes Here ...."]*4})

    def setup(self):
        Window.bind(size=self.size_changed)
        self.keyboard = Window.request_keyboard(lambda : None, self)
        self.keyboard.bind(on_key_down=self.keydown)

        # Initializing GUI elements.
        self.menus = Menus(size=(xwidth, xheight))
        self.menus.setup()

        self.hud = HUD(size=(xwidth, xheight))

        self.conv = Conversation(size=(xwidth, xheight))

        self.add_widget(self.conv)
        self.add_widget(self.menus)
        self.add_widget(self.hud)

    def size_changed(self, inst, value):
        self.hud.set_size(value)
        self.menus.set_size(value)
        self.conv.set_size(value)


    def add_card(self):
        self.adder += 1
        persons = ["person1", "person2", "person3", "person4", "person5", "person6"]
        card = {"title":self.ordinal(self.adder), "maintext":lor(), "tags":[choice(persons) for i in range(randint(0,10))]}
        self.menus.add_card(card)
        self.hud.show_info(card["title"])

    def update(self, dt):
        self.menus.update(dt)

    def keydown(self, *e):
        if e[1][1] == "spacebar":
            self.menus.toggle_menu()
        elif e[1][1] == "c":
            self.add_card()
        elif e[1][1] == "x":
            self.menus.retire_card(self.menus.card.title_text)
        elif e[1][1] == "e":
            self.panel_toggle = not self.panel_toggle
            if self.panel_toggle:
                self.conv.add_text_to_panels(**self.panel_text)
                self.conv.drop_panels()
            else:
                self.conv.drop_panels()
        elif e[1][1] == "f":
            print("Sizes of all widgets in the stack.")
            print("Main: ", self.size)
            print("Menus", self.menus.size)
            print("Conversation", self.conv.size)
            self.sizes_of_widgets(self.menus)
            self.sizes_of_widgets(self.conv)
            print("Done.")

    def sizes_of_widgets(self, w):
        for child in w.children:
            print(child, child.size)
            if len(child.children) != 0:
                self.sizes_of_widgets(child)


class MainApp(App):

    def build(self):
        game = MyGame(size=(xwidth, xheight))
        game.setup()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game

MainApp().run()
