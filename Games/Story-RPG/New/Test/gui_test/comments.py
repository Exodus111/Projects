
from kivy.clock import Clock
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import *

class Comment(RelativeLayout):
    text = StringProperty()
    speechbox = ObjectProperty()

    def setup(self):
        self.size = (200, 75)

    def activate(self, pos, text):
        self.pos = pos
        self.text = text
        self.speechbox.current = "active"
        Clock.schedule_once(self.deactivate, 3.)

    def deactivate(self, *args):
        self.speechbox.current = "None"
