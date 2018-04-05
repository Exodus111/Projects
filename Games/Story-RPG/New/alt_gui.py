#!/usr/bin/python3

from kivy.clock import Clock
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import *

class UnitedGUI(BoxLayout):
	screen_manager = ObjectProperty()
