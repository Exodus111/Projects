#!/usr/bin/python3

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.properties import *

MAIN_COLOR = (0.435, 0.325, 0.239, 1.) # Light Brown.
SECONDARY_COLOR = (.12,.12,.12, 1.) # Dark.
WHITE = (1.,1.,1.,1.)

class Element(Widget):
    name = StringProperty()
    e_color = ListProperty([0,0,0,0])
    bordersize = NumericProperty(10)
    text_area = ListProperty()

    def move(self, pos):
        if pos[0] == None:
            pos[0] = self.e_pos[0]
        if pos[1] == None:
            pos[1] = self.e_pos[1]
        anim = Animation(e_pos=pos, t="out_cubic", duration=.5)
        anim.start(self)

    def create_labels(self, labels):
        self.area = RelativeLayout(size=self.size, pos=self.pos)
        self.add_widget(self.area)
        for l in labels:
            text = Text(**l) # Fix this order. pos_hint must come after add_widget.
            self.area.add_widget(text)

class Text(Label):
    e_pos = DictProperty()


class GUI(FloatLayout):
    w_size = ListProperty([0,0])
    top_bar_texts =  ListProperty(["First Text Area",
                                   "Second Text Area",
                                   "Third Text Area"])
    right_panel_text = StringProperty("Right Bar")
    left_panel_text = StringProperty("Left Bar")

    def setup(self):

        # Create the Top Bar.
        tb_size, tb_pos = self.placement_and_size("top bar")
        bar_text = [{"text":self.top_bar_texts[0], "color":WHITE, "e_pos":{"x":.1, "y":1.}},
                    {"text":self.top_bar_texts[1], "color":WHITE, "e_pos":{"x":.5, "y":1.}},
                    {"text":self.top_bar_texts[2], "color":WHITE, "e_pos":{"x":.8, "y":1.}}]
        self.top_bar = self.add_element("Top Bar", tb_size, tb_pos, MAIN_COLOR, bar_text)

        # Create the Top Panel.
        tp_size, tp_pos = self.placement_and_size("top panel")
        self.top_panel = self.add_element("Top Panel", tp_size, tp_pos, MAIN_COLOR)


        # Adding widgets to widget stack.
        #self.add_widget(self.top_panel)
        self.add_widget(self.top_bar)

    def placement_and_size(self, location):
        if location == "top panel":
            s = (.8, .5)
            p = {"x":.2, "top":1.}
            return s, p
        elif location == "bottom panel":
            pass
        elif location == "top bar":
            s = (1., .025)
            p = {"x":0., "top":1.}
            return s, p


    def add_element(self, name, size, pos, color=(WHITE), texts=[]):
        el = Element(size_hint=size, pos_hint=pos)
        el.name = name
        el.e_color = color
        el.create_labels(texts)
        return el

    def update(self, dt):
        pass
