#!/usr/bin/python3
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import *

class HUD(FloatLayout):

    def setup(self):
        pass

    def update(self, dt):
        pass

    def button_pressed(self, *e):
        print("Testing Button Press")

class Main(Widget):
    def setup(self):
        for child in self.children:
            child.setup()

    def update(self, dt):
        for child in self.children:
            child.update(dt)


class MainApp(App):
    def build(self):
        main = Main()
        main.setup()
        Clock.schedule_interval(main.update, 1./60.)
        return main

if __name__ == "__main__":
    MainApp().run()
