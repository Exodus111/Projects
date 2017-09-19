
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import *

class Comment(RelativeLayout):
    text = StringProperty()
    speechbox = ObjectProperty()

    def setup(self):
        self.size = (200, 150)

    def deactivate(self, *args):
        self.speechbox.current = "None"

    def activate(self, pos, text):
        self.center = pos
        self.text = text
        self.set_text_size()
        self.speechbox.current = "active"
        Clock.schedule_once(self.deactivate, 30.)

    def set_text_size(self):
        l = Label(text=self.text, font_size=18, padding_x=15, padding_y=10, shorten=True, shorten_from="right", split_str=",")
        l.texture_update()
        self.size = l.texture_size
