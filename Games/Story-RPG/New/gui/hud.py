from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.properties import *

MAIN_COLOR = (0.435, 0.325, 0.239, 1.) # Light Brown.
SECONDARY_COLOR = (.12,.12,.12, 1.) # Dark.

class HUD(FloatLayout):
    top_bar = ObjectProperty()
    info_manager = ObjectProperty()
    floatmenu = ObjectProperty()
    info_text = StringProperty()

    def set_size(self, size):
        self.size = size

    def add_text_to_top_bar(self, text1=None, text2=None, text3=None):
        if text1: self.top_bar.text_one = text1
        if text2: self.top_bar.text_two = text2
        if text3: self.top_bar.text_three = text3

    def show_info(self, text):
        self.info_text = text
        self.info_manager.current = "info"
        Clock.schedule_once(self.hide_info, 2.)

    def hide_info(self, *_):
        self.info_manager.current="None"
        self.info_text = ""

    def on_press_inv(self):
        self.parent.toggle_card_menu()

    def on_press_opt(self, *_):
        self.parent.toggle_ingame_menu()

class TopBar(Widget):
    text_one = StringProperty()
    text_two = StringProperty()
    text_three = StringProperty()
    main_color = ListProperty(MAIN_COLOR)
    second_color = ListProperty(SECONDARY_COLOR)
    rela = ObjectProperty()
    text1 = ObjectProperty()

    def add_text(self, text):
        self.text_one, self.text_two, self.text_three = text

class FloatMenu(FloatLayout):
    inventory = ObjectProperty()
    options = ObjectProperty()

