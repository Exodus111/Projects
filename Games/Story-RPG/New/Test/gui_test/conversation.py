from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import *

class Conversation(FloatLayout):
    top_manager = ObjectProperty()
    bottom_manager = ObjectProperty()
    top_panel = ObjectProperty()
    bottom_panel = ObjectProperty()
    top_text = StringProperty()
    bottom_buttons = ListProperty()
    open_close = BooleanProperty(False)

    def setup(self):
        self.top_panel.add_widget(Label(text="Text Area"))
        self.bottom_panel.add_widget(Label(text="Text Area"))

    def drop_panels(self):
        self.open_close = not self.open_close
        if self.open_close:
            self.top_manager.current = "top_panel"
            self.bottom_manager.current = "bottom_panel"
        else:
            self.top_manager.current = "None"
            self.bottom_manager.current = "None"
