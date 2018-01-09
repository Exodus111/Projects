from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.properties import *

from tools.tools import *
from tools.fbofloatlayout import FboFloatLayout

class StartMenu(ScreenManager):
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
        self.current = "active"
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
    	self.current = "inactive"
    	Clock.schedule_once(lambda *x: self.parent.start_new_game(), 2)
    	Clock.schedule_once(lambda *x: self.parent.menu_on_off(), 2.1)

    def _on_load(self, *_):
    	print("Load Pressed")

    def _on_about(self, *_):
    	about = About(size_hint=(None, None), size=(self.size[0]+200, self.size[1]+100))
    	about.gamecenter = (self.gamesize[0]/2, self.gamesize[1]/2) 
    	self.parent.add_widget(about)
    	self.disable_buttons()

    def remove_about(self):
    	for child in self.parent.children:
    		if child.name == "about":
    			self.parent.remove_widget(child)
    			self.enable_buttons()

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
    	print("App Stop failed!")

    def change_resolution(self, e):
    	res = e.text
    	res = [int(i) for i in res.split(",")]
    	self.parent.change_resolution(res)
    	e.parent.parent.dismiss()


class About(ButtonBehavior, Widget):
	textlist = ListProperty(["About the Game", 
							 "[Name of Author] Wrote, Coded and Designed the game.",
							 "[Name of Artist] Designed and drew all the art."])
	gamecenter = ListProperty([0,0])

	def on_press(self, *_):
		self.parent.startmenu.remove_about()

	def test_borders_of_widget(self):
		with self.canvas:
			Color(rgba=(1.,1.,1.,.5))
			Rectangle(pos=self.pos, size=self.size)

class ResButton(Button):
	pass

class InGameMenu(FboFloatLayout):
    button_save = ObjectProperty()
    button_load = ObjectProperty()
    button_options = ObjectProperty()
    button_quit = ObjectProperty()
    gamesize = ListProperty([0,0])

    def setup(self, gamesize):
    	self.alpha = 0.
    	self.gamesize = gamesize
    	for call in ("save", "load", "options", "quit"):
    		eval("self.button_{}.bind(on_release=self._on_{})".format(call, call))

    def disable_buttons(self):
    	for but in self.children:
    		if but.name == "gui_button":
	    		but.disabled = True

    def enable_buttons(self, *_):
    	for but in self.children:
    		if but.name == "gui_button":
    			but.disabled = False

    def _on_save(self, *_):
    	print("Save Pressed")

    def _on_load(self, *_):
    	print("Load Pressed")

    def _on_options(self, *_):
    	print("Options Pressed")

    def _on_quit(self, *_):
    	print("App Stop failed!")
