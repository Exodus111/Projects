#!/usr/bin/python3
import kivy
kivy.require("1.9.0")

from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.label import Label

class Hello(Label):
    text = StringProperty("Hello World")

class HelloApp(App):

    def build(self):
        return Hello()

if __name__ == "__main__":
    app = HelloApp()
    app.run()
