#!/usr/bin/python3

from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.properties import *

from conversation import Conversation
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

class ButtonLayout(GridLayout):
    pass

class Select(RelativeLayout):
    button_manager = ObjectProperty()
    buttons = ObjectProperty()
    next_button = ObjectProperty()
    prev_button = ObjectProperty()
    array_size = ListProperty([0,0])
    retired_button = ObjectProperty()
    retired_mode = BooleanProperty(False)
    active_cards = ListProperty()
    retired_cards = ListProperty()

    def setup(self, size, titles, retired):
        c, r = size
        self.buttons.cols = c
        self.buttons.rows = r
        self.array_size = size
        self.active_cards = titles
        self.retired_cards = retired
        self.setup_cards(titles)

    def retire_card(self, card):
        print(self.active_cards)
        if card in self.active_cards:
            self.active_cards.remove(card)
            self.retired_cards.append(card)

    def setup_cards(self, titles):
        c,r = self.array_size
        amount = c*r
        amount_left = 0
        pages = []
        if titles == []:
            self.next_button.disabled = True
        else:
            for num, title in enumerate(titles):
                if num % amount == 0:
                    pages.append([])
                pages[-1].append(title)
            if len(pages[-1]) < amount:
                amount_left = amount - len(pages[-1])
            for n, page in enumerate(pages):
                if page == pages[0] and page == pages[-1]: # Only one page.
                    [self.buttons.add_widget(b) for b in self.create_buttons(page, amount_left)]
                    self.next_button.disabled = True
                elif page == pages[0]: # First page of many.
                    [self.buttons.add_widget(b) for b in self.create_buttons(page)]
                    self.next_button.disabled = False
                else:
                    screen = Screen(name="page"+str(n))
                    buttons = ButtonLayout(cols=c, rows=r)
                    screen.add_widget(buttons)
                    if self.button_manager.has_screen("page"+str(n)):
                        delscreen = self.button_manager.get_screen("page"+str(n))
                        self.button_manager.remove_widget(delscreen)
                    self.button_manager.add_widget(screen)
                if page != pages[0] and page == pages[-1]: # Last page.
                    [buttons.add_widget(b) for b in self.create_buttons(page, amount_left)]
                elif page != pages[0] and pages != pages[-1]: # All the other pages.
                    [buttons.add_widget(b) for b in self.create_buttons(page)]
        self.prev_button.disabled = True

    def create_buttons(self, titles, amount_left=0):
        buttons = []
        for i in titles + [None for i in range(amount_left)]:
            if i != None:
                b = Button(text=i, on_release=self.select_card)
            else:
                b = Button(disabled=True, on_release=self.select_card)
            buttons.append(b)
        return buttons

    def select_card(self, *e):
        self.parent.parent.parent.add_text_to_card(e[0].text)
        self.parent.manager.current = "Card1"

    def cycle_inventory(self, direction):
        page = self.button_manager.current
        if direction == "next":
            num = int(page[-1])+1
            page = "page" + str(num)
            self.button_manager.transition.direction = "left"
        else:
            num = int(page[-1])-1
            page = "page" + str(num)
            self.button_manager.transition.direction = "right"
        if num+1 < len(self.button_manager.screen_names) and num > 0:
            self.button_manager.current = page
            if self.next_button.disabled:
                self.next_button.disabled = False
            if self.prev_button.disabled:
                self.prev_button.disabled = False
        elif num < len(self.button_manager.screen_names) and num > 0:
            self.button_manager.current = page
            self.next_button.disabled = True
            if self.prev_button.disabled:
                self.prev_button.disabled = False
        elif num == 0:
            self.button_manager.current = page
            self.prev_button.disabled = True
            if direction != "next":
                self.next_button.disabled = False

    def toggle_retired_cards(self):
        for screen in self.button_manager.screen_names:
            if screen != "page0":
                self.button_manager.remove_widget(self.button_manager.get_screen(screen))
        self.buttons.clear_widgets()
        self.retired_mode = not self.retired_mode
        if self.retired_mode:
            self.setup_cards(self.retired_cards)
            self.retired_button.text = "Active Cards"
        else:
            self.setup_cards(self.active_cards)
            self.retired_button.text = "Retired Cards"
        self.button_manager.current = "page0"
        self.prev_button.disabled = True

class Card(RelativeLayout):
    img_tex = ObjectProperty()
    title_text = StringProperty()
    main_text = StringProperty()
    tags_text = StringProperty()

    def button_one(self):
        self.parent.manager.current = "Selection"

    def button_two(self):
        self.parent.manager.current = "None"

class GUI(FloatLayout):
    w_size = ListProperty([0,0])
    top_bar_texts =  ListProperty(["First Text Area",
                                   "Second Text Area",
                                   "Third Text Area"])
    right_panel_text = StringProperty("Right Bar")
    left_panel_text = StringProperty("Left Bar")
    top_bar = ObjectProperty()
    manager = ObjectProperty()
    info_manager = ObjectProperty()
    info_text = StringProperty()
    notes = ObjectProperty()
    card = ObjectProperty()
    select = ObjectProperty()
    card_text = DictProperty()
    card_db = DictProperty()
    id_counter = NumericProperty(0)
    card_lookup = DictProperty()

    def setup(self):
        self.top_bar.add_text(self.top_bar_texts)
        self.select.setup((4, 4), [], [])
        self.card.img_tex = Image(source="empty_profile.png").texture
        self.conv = Conversation()
        self.conv.setup()
        self.add_widget(self.conv)

    def add_card(self, card):
        self.id_counter += 1
        self.card_db[self.id_counter] = card
        self.card_lookup[card["title"]] = self.id_counter
        self.select.active_cards.append(card["title"])
        self.select.buttons.clear_widgets()
        self.select.setup_cards(self.select.active_cards)

    def retire_card(self, card_title):
        if self.manager.current == "Card1":
            self.manager.current = "Selection"
        self.select.retire_card(card_title)
        self.select.buttons.clear_widgets()
        self.select.setup_cards(self.select.active_cards)

    def add_text_to_card(self, title):
        num = self.card_lookup[title]
        self.card.title_text = self.card_db[num]["title"]
        self.card.main_text = self.card_db[num]["maintext"]
        self.card.tags_text = ", ".join(self.card_db[num]["tags"])

    def toggle_menu(self):
        if self.manager.current_screen.name == "None":
            self.manager.current = "Selection"
        else:
            self.manager.current = "None"

    def show_info(self, text):
        self.info_text = text
        self.info_manager.current = "info"
        Clock.schedule_once(self.hide_info, 2.)

    def hide_info(self, *_):
        self.info_manager.current="None"
        self.info_text = ""

    def update(self, dt):
        pass
