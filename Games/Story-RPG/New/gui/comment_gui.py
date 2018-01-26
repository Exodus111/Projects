
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import *

class CommentGUI(RelativeLayout):
    text = StringProperty()
    speechbox = ObjectProperty()
    timeout = NumericProperty(6.)
    entity = ObjectProperty()
    moveup = NumericProperty(0) 
    moveside = NumericProperty(0) 

    def __repr__(self):
        return "Comment GUI Object: \n" + self.text

    def setup(self, entity, text):
        self.size = (200, 150)
        self.text = text
        self.timeout = float((len(text)/15)+5)
        self.entity = entity
        self.set_center()

    def set_center(self, *_):
        self.center[0] = self.entity.comment_pos[0] + self.moveside
        self.center[1] = self.entity.comment_pos[1] + self.moveup

    def timeout_comment(self, tmr):
        Clock.schedule_once(self.deactivate, tmr)

    def deactivate(self, *args):
        self.speechbox.current = "None"

    def activate(self):
        self.set_text_size()
        self.speechbox.current = "active"

    def set_text_size(self):
        l = Label(text=self.text, font_size=18, padding_x=15, padding_y=10, shorten=True, shorten_from="right", split_str=",")
        l.texture_update()
        self.size = l.texture_size
