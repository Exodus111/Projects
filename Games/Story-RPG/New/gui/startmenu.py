from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import *

class StartMenu(BoxLayout):
    button_new = ObjectProperty()
    button_load = ObjectProperty()
    button_credits = ObjectProperty()
    button_about = ObjectProperty()
    button_options = ObjectProperty()
    button_quit = ObjectProperty()
    gamesize = ListProperty([0,0])

    def setup(self, gamesize):
    	self.gamesize = gamesize
    	for call in ("new", "load", "credits", "about", "options", "quit"):
    		eval("self.button_{}.bind(on_press=self._on_{})".format(call, call))

    def _on_new(self, *_):
    	self.parent.start_new_game()
    	self.parent.menu_on_off()

    def _on_load(self, *_):
    	print("Load Pressed")

    def _on_credits(self, *_):
    	print("Credits Pressed")

    def _on_about(self, *_):
    	print("About Pressed")

    def _on_options(self, *_):
    	options = Options(size=(int(self.size[0]*2), int(self.size[1]*1.2)))
    	options.setup(self.gamesize)
    	self.parent.insert_menu(options)
    	self.parent.menu_on_off()

    def _on_quit(self, *_):
    	print("Quit Pressed")

class Credits(Screen): ## Need to  make transition to Credits
	text = StringProperty("") ## Or redo  how Options/Credits work.

class Options(BoxLayout): 
	manager = ObjectProperty()
	credits = ObjectProperty()
	textdict = DictProperty({"Title":""})
	gamesize = ListProperty([0,0])

	def setup(self, gamesize):
		self.gamesize = gamesize
		self.credits.text = "Credits Go here."
		self.textdict["Title"] = "Options Menu"
