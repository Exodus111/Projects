#!/usr/bin/python3

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.properties import *

from tools.tools import scale_image

MAIN_COLOR = (0.435, 0.325, 0.239, 1.) # Light Brown.
SECONDARY_COLOR = (.12,.12,.12, 1.) # Dark.
WHITE = (1.,1.,1.,1.)

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

class Menu(Screen):
    pass

class Select(RelativeLayout):
    buttons = ObjectProperty()
    rows = NumericProperty(0)
    cols = NumericProperty(0)

    def setup(self, c, r):
        self.cols = c
        self.rows = r
        for i in range(c*r):
            b = Button(text=str(i), on_release=self.select_card)
            self.buttons.add_widget(b)

    def select_card(self, *e):
        self.parent.parent.parent.add_text_to_card(e[0].text)
        self.parent.manager.current = "Card1"

class Card(RelativeLayout):
    img_tex = ObjectProperty()
    title_text = StringProperty()
    main_text = StringProperty()

class GUI(FloatLayout):
    w_size = ListProperty([0,0])
    top_bar_texts =  ListProperty(["First Text Area",
                                   "Second Text Area",
                                   "Third Text Area"])
    right_panel_text = StringProperty("Right Bar")
    left_panel_text = StringProperty("Left Bar")
    top_bar = ObjectProperty()
    manager = ObjectProperty()
    notes = ObjectProperty()
    card = ObjectProperty()
    select = ObjectProperty()
    card_text = DictProperty()

    def setup(self):
        # Setting up the Top Bar.
        self.top_bar.add_text(self.top_bar_texts)

        # Setting up the Selection and Cards.
        self.select.setup(3, 2)
        self.card.img_tex = Image(source="empty_profile.png").texture

    def add_text_to_card(self, card):
        self.card.title_text = "Title for card " + card
        self.card.main_text = "Main Text for card " + card

    def toggle_menu(self):
        if self.manager.current_screen.name == "None":
            self.manager.current = "Selection"
        else:
            self.manager.current = "None"

    def update(self, dt):
        pass
