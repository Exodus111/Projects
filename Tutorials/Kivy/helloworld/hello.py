#!/usr/bin/python3
import kivy
kivy.require("1.9.0")

from kivy.app import App
from kivy.uix.label import Label

class Hello(Label):
    text = "Hello World"

class HelloApp(App):

    def build(self):
        return Hello()

if __name__ == "__main__":
    app = HelloApp()
    app.run()
