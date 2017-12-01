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
    	for call in ("new", "load", "credits", "about", "options", "quit"):
    		eval("self.button_{}.bind(on_press=self._on_{})".format(call, call))

    def _on_new(self, *_):
    	self.parent.menu_on_off()
    	print("New Pressed")

    def _on_load(self, *_):
    	print("Load Pressed")

    def _on_credits(self, *_):
    	print("Credits Pressed")

    def _on_about(self, *_):
    	print("About Pressed")

    def _on_options(self, *_):
    	print("Options Pressed")

    def _on_quit(self, *_):
    	print("Quit Pressed")



