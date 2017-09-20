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
import json

from guipanels import DialoguePanels
from hud import HUD
from comments import Comment
from tools.tools import scale_image

MAIN_COLOR = (0.435, 0.325, 0.239, 1.) # Light Brown.
SECONDARY_COLOR = (.12,.12,.12, 1.) # Dark.
WHITE = (1.,1.,1.,1.)

class GUI(Widget):
    panel_toggle = BooleanProperty(False)
    comment_list = ListProperty()
    up = ListProperty()

    def setup(self):
        self.menus = Menus(size=self.size)
        self.menus.setup()

        self.hud = HUD(size=self.size)

        self.panels = DialoguePanels(size=self.size)

        self.add_widget(self.panels)
        self.add_widget(self.menus)
        self.add_widget(self.hud)

    def size_changed(self, value):
        """
            This method must be linked to size property of the Window Object.
        """
        self.hud.set_size(value)
        self.menus.set_size(value)
        self.panels.set_size(value)

    def add_card(self, card):
        """
            card: Dict.
            Contains the keys 'title', 'maintext' and 'tags'
        """
        self.menus.add_card(card)
        self.hud.show_info(card["title"])

    def toggle_card_menu(self):
        """
            This method is a toggle.
        """
        self.menus.toggle_menu()

    def retire_card(self, card_title):
        self.menus.retire_card(card_title)

    def conv_panels_toggle(self):
        """
            This method is a toggle.
        """
        self.panel_toggle = not self.panel_toggle
        if self.panel_toggle:
            self.panels.drop_panels()
        else:
            self.panels.drop_panels()

    def add_text_to_conv_panels(self, text_dict):
        """
            text_dict: Dict.
             Contains two keys: 'top_text' and 'question_list'.
        """
        self.panels.clear_text()
        self.panels.add_text_to_panels(**text_dict)
        if self.panels.bottom_manager.current == "question_big":
            self.panels.bottom_manager.current = "bottom_panel"

    def add_comment(self, pos, text):
        comment = Comment()
        comment.setup()   # Does nothing atm.
        comment.activate(pos,text)
        self.add_widget(comment)
        self.comment_list.append(comment)

    def update(self, dt):
        if len(self.comment_list) >= 2:
            if self.comment_list[0].speechbox.current == "None":
                del(self.comment_list[0])
        for n1, c1 in enumerate(self.comment_list):
            if c1.pos[0] + c1.size[0] > self.size[0]:
                c1.pos[0] -= 3
            for n2, c2 in enumerate(self.comment_list):
                if n1 > n2:
                    if c1.collide_widget(c2):
                        c1.pos[1] += 3

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

class Menus(FloatLayout):
    manager = ObjectProperty()
    notes = ObjectProperty()
    card = ObjectProperty()
    select = ObjectProperty()
    card_text = DictProperty()
    card_db = DictProperty()
    id_counter = NumericProperty(0)
    card_lookup = DictProperty()

    def setup(self):
        self.select.setup((4, 4), [], [])
        self.card.img_tex = Image(source="images/gui/empty_profile.png").texture

    def set_size(self, size):
        self.size = size

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

    def update(self, dt):
        pass
