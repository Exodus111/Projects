
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import *

class CommentGUI(RelativeLayout):
    text = StringProperty()
    speechbox = ObjectProperty()
    timeout = NumericProperty(6.)

    def __repr__(self):
        return "Comment GUI Object \n" + self.text

    def setup(self, pos, text):
        self.size = (200, 150)
        self.text = text
        self.center = pos

    def deactivate(self, *args):
        self.speechbox.current = "None"

    def activate(self):
        self.set_text_size()
        self.speechbox.current = "active"
        Clock.schedule_once(self.deactivate, self.timeout)

    def set_text_size(self):
        l = Label(text=self.text, font_size=18, padding_x=15, padding_y=10, shorten=True, shorten_from="right", split_str=",")
        l.texture_update()
        self.size = l.texture_size
