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

from gui.guipanels import DialoguePanels
from gui.hud import HUD
from gui.comment_gui import CommentGUI
from gui.startmenu import InGameMenu
from tools.tools import scale_image
from tools.fbofloatlayout import FboFloatLayout

MAIN_COLOR = (0.435, 0.325, 0.239, 1.) # Light Brown.
SECONDARY_COLOR = (.12,.12,.12, 1.) # Dark.
WHITE = (1.,1.,1.,1.)

class GUI(Widget):
    panel_toggle = BooleanProperty(False)
    comment_list = ListProperty()
    textpos_list = ListProperty()
    up = ListProperty()
    timer = NumericProperty()
    active_card_amount = NumericProperty()

    def __repr__(self):
        return "Main GUI Object \n"

    def setup(self):
        self.menus = Menus(size=self.size)
        self.menus.setup()

        self.hud = HUD(size=self.size)

        self.ingame = InGameMenu()
        self.ingame.setup(self.size)

        self.panels = DialoguePanels(size=self.size)

        self.add_widget(self.panels)
        self.add_widget(self.menus)
        self.add_widget(self.ingame)
        self.add_widget(self.hud)

        self.update_card_top_list()

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
        if card not in self.menus.card_db.values(): 
            self.menus.add_card(card)
            self.hud.show_info(card["title"])

    def update_card(self, card):
        """
            card: Dict.
            Contains the keys 'title', 'maintext' and 'tags'
        """
        num = self.menus.card_lookup[card["title"]]
        self.menus.card_db[num]["tags"] = card["tags"]
        if not any(self.menus.card_db[num]["tags"].values()):
            self.retire_card(card["title"])
        self.update_card_top_list()

    def update_card_top_list(self):
        self.active_card_amount = self.menus.check_for_amount_of_active_cards()
        if self.active_card_amount == 0:            
            self.hud.add_text_to_top_bar(text3="Active Cards: None")
        else:
            self.hud.add_text_to_top_bar(text3="Active Cards: {}".format(self.active_card_amount))

    def toggle_card_menu(self):
        """
            This method is a toggle.
        """
        self.menus.toggle_menu()

    def toggle_ingame_menu(self):
        if self.ingame.alpha == 0.:
            Animation(alpha=1.0, duration=.5).start(self.ingame)
        elif self.ingame.alpha == 1.0:
            Animation(alpha=0.0, duration=.5).start(self.ingame)


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

    def add_comments(self, textdicts):
        """
            Activates a comment thread.
          textdicts: List containing Dicts.
           Dict keys are: pos, text
        """
        neg = 0
        for n, i in enumerate(textdicts):
            if i["text"] == "":
                neg += 1
            else:
                self.textpos_list.append((i, abs(n-neg)*4))

    def run_comments(self, dt):
        if self.textpos_list != []:
            self.timer += dt
            dct, tm = self.textpos_list[0]
            if tm <= self.timer:
                self.activate_comment(dct)
                del(self.textpos_list[0])
        else:
            if self.timer != 0.:
                self.timer = 0.

    def collide_comments(self):
        if self.comment_list != []:
            if self.comment_list[0].speechbox.current == "None":
                self.parent.world.remove_widget(self.comment_list[0])
                del(self.comment_list[0])

        for n1, c1 in enumerate(self.comment_list):
            pos = c1.to_window(c1.pos[0], c1.pos[1])
            if pos[0] + c1.size[0] > self.size[0]:
                c1.pos[0] -= 3
            if pos[1] + c1.size[1] > self.size[1]:
                c1.pos[1] -= 3
            for n2, c2 in enumerate(self.comment_list):
                if n1 > n2:
                    if c1.collide_widget(c2):
                        c1.pos[1] += 3

    def activate_comment(self, txt_dict):
        comment = CommentGUI(size_hint=(None, None))
        comment.setup(txt_dict["pos"], txt_dict["text"])
        self.parent.world.add_widget(comment)
        comment.activate()
        self.comment_list.append(comment)

    def update(self, dt):
        self.run_comments(dt)
        self.collide_comments()

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

class Menus(FboFloatLayout):
    manager = ObjectProperty()
    notes = ObjectProperty()
    card = ObjectProperty()
    select = ObjectProperty()
    card_text = DictProperty()
    card_db = DictProperty()
    id_counter = NumericProperty(0)
    card_lookup = DictProperty()

    def setup(self):
        self.alpha = 0.0
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
        namelist = []
        for name, b in self.card_db[num]["tags"].items():
            if b:
                name = "[color=#4666ff]{}[/color]".format(name)
            else:
                name = "[color=#c0c0c0]{}[/color]".format(name)
            namelist.append(name)
        self.card.tags_text = ", ".join(namelist)

    def toggle_menu(self):
        if self.alpha == 0.0:
            Animation(alpha=1.0, duration=.5).start(self)
        elif self.alpha == 1.0:
            Animation(alpha=0.0, duration=.5).start(self)

    def check_for_amount_of_active_cards(self):
        return len(self.select.active_cards)

    def update(self, dt):
        pass
