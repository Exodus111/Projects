#!/usr/bin/python3

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.properties import *

from tools.tools import scale_image

MAIN_COLOR = (0.435, 0.325, 0.239, 1.) # Light Brown.
SECONDARY_COLOR = (.12,.12,.12, 1.) # Dark.
WHITE = (1.,1.,1.,1.)

class Notes(Widget):
    name = StringProperty()
    main_color = ListProperty(MAIN_COLOR)
    second_color = ListProperty(SECONDARY_COLOR)
    bordersize = NumericProperty(10)
    text_area = StringProperty("Test")
    text_storage = StringProperty()
    original_pos = ListProperty()
    visible = BooleanProperty(False)
    fade_float = NumericProperty(1.)
    mid_label = ObjectProperty()
    img_pos = ListProperty([0,0])

    def setup(self, text=""):
        self.bind(fade_float=self._fader)
        self.fade_float = 0.
        self.text_area = ""
        self.text_storage = text

    def _fader(self, *_):
        self.main_color[-1] = self.fade_float
        self.second_color[-1] = self.fade_float

    def toggle_label(self):
        if self.visible:
            self.text_area = self.text_storage
        else:
            self.text_area = ""

    def fade_in_out(self):
        if self.visible:
            anim = Animation(fade_float=0., t="in_circ", duration=.5)
            anim.bind(on_complete=lambda *x: self.toggle_label())
            anim.start(self)
        else:
            anim = Animation(fade_float=1., t="in_circ", duration=.5)
            anim.bind(on_complete=lambda *x: self.toggle_label())
            anim.start(self)
        self.toggle_label()
        self.visible = not self.visible

class TopBar(Widget):
    text_one = StringProperty()
    text_two = StringProperty()
    text_three = StringProperty()
    main_color = ListProperty(MAIN_COLOR)
    rela = ObjectProperty()
    text1 = ObjectProperty()

    def add_text(self, text):
        self.text_one, self.text_two, self.text_three = text

class GUI(FloatLayout):
    w_size = ListProperty([0,0])
    top_bar_texts =  ListProperty(["First Text Area",
                                   "Second Text Area",
                                   "Third Text Area"])
    right_panel_text = StringProperty("Right Bar")
    left_panel_text = StringProperty("Left Bar")
    top_bar = ObjectProperty()
    notes = ObjectProperty()

    def setup(self):

        # Setting up the Top Bar.
        self.top_bar.add_text(self.top_bar_texts)

        # Setting up Notes Menu.
        self.notes.setup("Testing the Text Area!")


    def update(self, dt):
        pass
