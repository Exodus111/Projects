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

from gui_test import GUI
from random import choice, randint

def lor():
    return "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque nec lectus sit amet sapien imperdiet lobortis. Nunc congue arcu dictum dui egestas, vel semper ipsum pharetra. Etiam interdum neque malesuada tellus rhoncus bibendum. Aenean lobortis interdum purus vel gravida. Maecenas ut nisi at lacus consequat venenatis. Curabitur nec pulvinar massa, sit amet egestas mauris. Fusce eu sagittis arcu, vel cursus quam. Suspendisse bibendum consequat aliquet. In eu tempor elit, in pulvinar nisl. Nam tincidunt vulputate efficitur. Etiam feugiat lacus id mi tristique ultrices. Nullam eget nulla ante. Morbi eget ultrices neque."

class MyGame(Widget):
    adder = NumericProperty(0)
    ordinal = lambda c, n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])

    def setup(self):
        self.keyboard = Window.request_keyboard(lambda : None, self)
        self.keyboard.bind(on_key_down=self.keydown)
        self.gui = GUI(size=(xwidth, xheight))
        self.gui.setup()
        self.add_widget(self.gui)

    def add_card(self):
        self.adder += 1
        persons = ["person1", "person2", "person3", "person4", "person5", "person6"]
        card = {"title":self.ordinal(self.adder), "maintext":lor(), "tags":[choice(persons) for i in range(randint(0,10))]}
        self.gui.add_card(card)
        self.gui.show_info(card["title"])

    def update(self, dt):
        self.gui.update(dt)

    def keydown(self, *e):
        if e[1][1] == "spacebar":
            self.gui.toggle_menu()
        elif e[1][1] == "c":
            self.add_card()
        elif e[1][1] == "x":
            self.gui.retire_card(self.gui.card.title_text)
        elif e[1][1] == "e":
            self.gui.conv.drop_panels()

class MainApp(App):
    def build(self):
        game = MyGame()
        game.setup()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game

MainApp().run()
