#!/usr/bin/python3

from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.properties import *

class Element(Widget):
    name = StringProperty()
    e_size = ListProperty([0,0])
    e_pos = ListProperty([0,0])
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


class GUI(Widget):
    w_size = ListProperty([0,0])
    top_bar_texts =  ListProperty(["First Text Area",
                                   "Second Text Area",
                                   "Third Text Area"])
    right_panel_text = StringProperty("Right Bar")
    left_panel_text = StringProperty("Left Bar")

    def setup(self, size):
        self.w_size = size
        gcolor = (0.435, 0.325, 0.239, 1.)

        # Create Right Panel.
        rp_size, rp_pos = self.placement_and_size("right panel")
        rp_text = [{"text":self.right_panel_text, "color":(.12,.12,.12, 1.), "pos":(rp_pos[0]+20, rp_pos[1]+20)}]
        self.right_panel = self.add_element("Right Panel", rp_size, rp_pos, gcolor, rp_text)

        # Create Left Panel.
        lp_size, lp_pos = self.placement_and_size("left panel")
        self.left_panel = self.add_element("Left Panel", lp_size, lp_pos, gcolor)

        # Create the Top Bar.
        tb_size, tb_pos = self.placement_and_size("top bar")
        bar_text = [{"text":self.top_bar_texts[0], "color":(.12,.12,.12, 1.), "pos":(tb_pos[0]+20, tb_pos[1]-40)},
                    {"text":self.top_bar_texts[1], "color":(.12,.12,.12, 1.), "pos":(tb_pos[0]+400, tb_pos[1]-40)},
                    {"text":self.top_bar_texts[2], "color":(.12,.12,.12, 1.), "pos":(tb_pos[0]+850, tb_pos[1]-40)}]
        self.top_bar = self.add_element("Top Bar", tb_size, tb_pos, gcolor, bar_text)

        # Adding widgets to widget stack.
        self.add_widget(self.right_panel)
        self.add_widget(self.left_panel)
        self.add_widget(self.top_bar)

    def placement_and_size(self, location):
        if location == "right panel":
            s = ((self.w_size[0]/8)*3.2, (self.w_size[1]/8)*6)
            p = (self.w_size[0], (self.w_size[1]/8)*1.5)
            return s, p
        elif location == "left panel":
            s = ((self.w_size[0]/8)*3.2, (self.w_size[1]/8)*6)
            p = (-s[0], (self.w_size[1]/8)*1.5)
            return s, p
        elif location == "top panel":
            pass
        elif location == "bottom panel":
            pass
        elif location == "top bar":
            s = (self.w_size[0], 20)
            p = (0, self.w_size[1]-20)
            return s, p


    def add_element(self, name, size, pos, color=(1.,1.,1.,1.), texts=[]):
        el = Element()
        el.e_size = size
        el.e_pos = pos
        el.e_color = color
        for t in texts:
            l = Label(**t)
            el.add_widget(l)
        return el

    def update(self, dt):
        pass
