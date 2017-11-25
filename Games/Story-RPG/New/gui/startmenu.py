from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty, ListProperty, ObjectProperty

class StartMenu(BoxLayout):
    button_new = ObjectProperty()
    button_load = ObjectProperty()
    button_credits = ObjectProperty()
    button_about = ObjectProperty()
    button_options = ObjectProperty()
    button_quit = ObjectProperty()

    def setup(self):
        self.button_new.bind(on_press=lambda *args: self.parent.menu_on_off())
