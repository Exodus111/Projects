#!/usr/bin/python3
import kivy
kivy.require('1.9.1')

from kivy.core.window import Window
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.core.text import Label
from kivy.properties import StringProperty, BooleanProperty

class Console(Widget):
	runonce = BooleanProperty(True)
	mytext = StringProperty("Testing Testing!")

	def setup(self):
		pass

	def update(self, dt):
		pass

class ConsoleApp(App):
	def build(self):
		console = Console()
		console.setup()
		Clock.schedule_interval(console.update, 1./30.)
		return console

if __name__ == "__main__":
	ConsoleApp().run()
