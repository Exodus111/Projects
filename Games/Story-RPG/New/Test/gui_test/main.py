#!/usr/bin/python3
import kivy
kivy.require("1.9.0")

from kivy.config import Config
xwidth, xheight = 1024, 768
Config.set("graphics", "width", xwidth)
Config.set("graphics", "height", xheight)
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.write()
from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.properties import *

from gui import GUI
from dialogue import Dialogue
from random import choice, randint
import json

def lor():
    return "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque nec lectus sit amet sapien imperdiet lobortis. Nunc congue arcu dictum dui egestas, vel semper ipsum pharetra. Etiam interdum neque malesuada tellus rhoncus bibendum. Aenean lobortis interdum purus vel gravida. Maecenas ut nisi at lacus consequat venenatis. Curabitur nec pulvinar massa, sit amet egestas mauris. Fusce eu sagittis arcu, vel cursus quam. Suspendisse bibendum consequat aliquet. In eu tempor elit, in pulvinar nisl. Nam tincidunt vulputate efficitur. Etiam feugiat lacus id mi tristique ultrices. Nullam eget nulla ante. Morbi eget ultrices neque."

class MyGame(Widget):
    ordinal = lambda c, n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])
    panel_text1 = DictProperty({"top_text":lor(),
                               "question_list":["Question Goes Here ...."]*4})
    panel_text2 = DictProperty({"top_text":"Page 2",
                               "question_list":["Question Goes Here ...."]*6})

    def setup(self):
        Window.bind(size=self.size_changed)
        self.keyboard = Window.request_keyboard(lambda : None, self)
        self.keyboard.bind(on_key_down=self.keydown)

        # Initializing Dialogue
        with open("new_data.json", "r+") as f:
            data = json.load(f)
        self.diag = Dialogue(**data)

        # Initializing GUI elements.
        self.gui = GUI(size=(xwidth, xheight))
        self.gui.setup()
        self.add_widget(self.gui)

        conv = self.diag.current_conv
        self.gui.add_text_to_conv_panels({"top_text":conv.top_text, "question_list":conv.bottom_question_list})

    def question_picked(self, text):
        self.diag.current_conv.question_picked(text)
        conv = self.diag.current_conv
        self.gui.add_text_to_conv_panels({"top_text":conv.top_text, "question_list":conv.bottom_question_list})

    def size_changed(self, _, value):
        self.gui.size_changed(value)

    def speak_comment(self):
        self.gui.comments[0].activate((xwidth/2, xheight/2), "Test text!!")

    def update(self, dt):
        self.gui.update(dt)
        if self.diag.current_conv.end_conversation:
            self.gui.conv_panels_toggle()
            self.diag.current_conv.end_conversation = False

    def keydown(self, *e):
        if e[1][1] == "spacebar":
            self.gui.conv_panels_toggle()
        elif e[1][1] == "e":
            self.gui.add_text_to_conv_panels(next(self.td))
        elif e[1][1] == "r":
            self.speak_comment()

class MainApp(App):

    def build(self):
        game = MyGame(size=(xwidth, xheight))
        game.setup()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game

MainApp().run()
