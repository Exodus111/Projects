#!/usr/bin/python3
# Requires the installation and compilation of KivEnt Core.
# (Which I have not done.) 

import kivy
from kivy.app import App
from kivy.uix.widget import Widget
import kivent_core

class TestGame(Widget):
    pass

class YourAppName(App):
    def build(self):
        pass

if __name__ == "__main__":
    YourAppName().run()
