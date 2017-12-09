from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.properties import *

from tools.tools import *

class StartMenu(BoxLayout):
    button_new = ObjectProperty()
    button_load = ObjectProperty()
    button_about = ObjectProperty()
    button_options = ObjectProperty()
    button_quit = ObjectProperty()
    gamesize = ListProperty([0,0])
    resolutions = ListProperty([(1024, 960),
    							(1366, 768),
    							(1290, 1080)])

    def setup(self, gamesize):
    	self.gamesize = gamesize
    	for call in ("new", "load", "about", "options", "quit"):
    		eval("self.button_{}.bind(on_release=self._on_{})".format(call, call))

    def disable_buttons(self):
    	for but in self.children:
    		if but.name == "gui_button":
	    		but.disabled = True

    def enable_buttons(self, *_):
    	for but in self.children:
    		if but.name == "gui_button":
    			but.disabled = False

    def _on_new(self, *_):
    	self.parent.start_new_game()
    	self.parent.menu_on_off()

    def _on_load(self, *_):
    	print("Load Pressed")

    def _on_about(self, *_):
    	about = About(size=(self.size[0]+200, self.size[1]+100))
    	about.gamecenter = (self.gamesize[0]/2, self.gamesize[1]/2) 
    	self.parent.add_widget(about)
    	self.disable_buttons()

    def _on_options(self, *_):
    	dsize = self.size
    	dpos = (int((self.gamesize[0]/2)-(dsize[0]/2)), int((self.gamesize[1]/2)-(dsize[1]*.8)))

    	dpdown = DropDown(pos=dpos, size=dsize)
    	for r in self.resolutions:
    		b = ResButton(text="{},{}".format(r[0], r[1]),
    			size_hint=(None,None),
    			size=self.button_new.size)
    		b.bind(on_release=self.change_resolution)
    		dpdown.add_widget(b)
    	dpdown.bind(on_dismiss=self.enable_buttons)
    	self.parent.add_widget(dpdown)
    	self.disable_buttons()

    def _on_quit(self, *_):
    	self.parent.parent.stop()

    def change_resolution(self, e):
    	res = e.text
    	res = [int(i) for i in res.split(",")]
    	self.parent.change_resolution(res)
    	e.parent.parent.dismiss()


class About(BoxLayout):
	textlist = ListProperty(["About the Game", 
							 "About the Author",
							 "About the Artist"])
	gamecenter = ListProperty([0,0])

class ResButton(Button):
	pass
