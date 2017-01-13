#!/usr/bin/python3
import kivy
kivy.require("1.9.0")

from kivy.app import App
from kivy.uix.widget import Widget

class CustomWidget(Widget):
    pass

class AbsoluteLayoutApp(App):

    def build(self):
        return CustomWidget()

customWidget = AbsoluteLayoutApp()
customWidget.run()
