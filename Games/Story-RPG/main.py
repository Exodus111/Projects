#!/usr/bin/python3
from kivy.app import App
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.properties import StringProperty, ListProperty, BooleanProperty, ObjectProperty, NumericProperty

from entities import *
from dialogue import *

class EventHandler(Widget):
    def __init__(self):
        super(EventHandler, self).__init__()
        self.calls = {
            "keydown":None,
            "keyup":None,
            "dropmenus":None,
            "speechbubble":None,
            "npc_speech":None
        }
        self.keyboard = Window.request_keyboard(self.key_off, self)
        self.keyboard.bind(on_key_down=self.key_down)
        self.keyboard.bind(on_key_up=self.key_up)

    def key_up(self, k, keycode):
        if keycode[1] in ("up", "down", "left", "right", "w", "a", "s", "d"):
            self.calls["keyup"](keycode)


    def key_down(self, keyboard, keycode, text, mod):
        if keycode[1] in ("up", "down", "left", "right", "w", "a", "s", "d"):
            self.calls["keydown"](keycode, mod)
        elif keycode[1] in ("t", "b"):
            self.calls["dropmenus"](keycode[1])
        elif keycode[1] == "h":
            self.calls["speechbubble"]()
        elif keycode[1] in [str(i) for i in range(10)]:
            self.calls["npc_speech"](keycode[1])

    def key_off(self):
        pass

class QuestionButton(Button): pass

class GameWorld(Widget):
    def __init__(self, **kwargs):
        super(GameWorld, self).__init__(**kwargs)
        self.background = Image(source='images/game_borders.png', size=(2048/2,1080/2))
        self.size = self.background.size
        self.add_widget(self.background)
        self.foreground = ForeGround(size=self.size)
        #self.foreground.add_widget(Clutter(img='images/obj_32px.png', pos=(200, 200)))
        #self.foreground.add_widget(Clutter(img='images/obj_128x32px.png', pos=(600, 200)))
        #self.foreground.add_widget(Clutter(img='images/obj_64px.png', pos=(500, 300)))
        self.add_widget(self.foreground)

    def update(self, dt):
        self.foreground.update(dt)

class ForeGround(Widget):
    def coll_childs(self, w):
        return [child for child in self.children if child.collide_widget(w)]

    def update(self, dt):
        for child in self.children:
            child.update(dt)

class Clutter(Widget):
    def __init__(self, img, pos):
        super(Clutter, self).__init__()
        self.image = Image(source=img)
        self.size = self.image.size = self.image.texture_size
        self.pos = pos
        self.image.center = self.center
        self.add_widget(self.image)

    def update(self, dt):
        pass

class DropMenu(Widget):
    act_text = StringProperty("")
    text_colour = ListProperty([1., 1., 1., 0.])


class Menus(Widget):
    top_status = BooleanProperty(False)
    bot_status = BooleanProperty(False)
    top_menu = ObjectProperty(None)
    bot_menu = ObjectProperty(None)    # Bot stands for Bottom.
    y1_animate = NumericProperty(0)
    y2_animate = NumericProperty(0)
    text_colour = ListProperty([1., 1., 1., 0.])
    current_npc = ObjectProperty(None)

    def menu_press(self, k):
        if k == "t":
            self.top_status = not self.top_status
            if self.top_status:
                self.show_top_menu()
            else:
                self.hide_top_menu()
        elif k == "b":
            self.bot_status = not self.bot_status
            if self.bot_status:
                self.show_bottom_menu()
            else:
                self.hide_bottom_menu()

    def ran_text(self):
        return ran.choice([("Oops, something went wrong here.", "I shouldn't be seeing this."),
                           ("Dialogue not found for some reason.", "I need to send an error message about this."),
                           ("No dialogue here, sorry.", "Dammit, another bug!")])

    def show_top_and_bottom_menu(self, txt=[]):
        anim = Animation(y1_animate=self.height-self.top_menu.height, t='out_bounce')
        anim &= Animation(y2_animate=0, t='out_bounce')
        anim.bind(on_complete=lambda x,y: self.add_text(txt))
        anim.start(self)

    def add_text(self, txt):
        if txt == []:
            txt = self.ran_text()
        if txt[0] != "":
            self.top_menu.act_text = txt[0]
        if txt[1] != "":
            self.bot_menu.act_text = txt[1]
        anim2 = Animation(text_colour=[1., 1., 1., 1.])
        anim2.start(self.top_menu)
        anim2.start(self.bot_menu)

    def hide_top_and_bottom_menu(self):
        anim = Animation(y1_animate=self.height, t='in_out_elastic')
        anim &= Animation(y2_animate=-self.bot_menu.height, t='in_out_elastic')
        animtext = Animation(text_colour=[1., 1., 1., 0.])
        anim.start(self)
        animtext.start(self.top_menu)
        animtext.start(self.bot_menu)
        self.top_menu.act_text = ""
        self.bot_menu.act_text = ""

    def show_top_menu(self):
        anim = Animation(x=0, y=self.height-self.top_menu.height, t='out_bounce')
        anim.start(self.top_menu)

    def hide_top_menu(self):
        anim = Animation(x=0, y=self.height, t='in_out_elastic')
        anim.start(self.top_menu)

    def show_bottom_menu(self):
        anim = Animation(x=0, y=0, t='out_bounce')
        anim.start(self.bot_menu)

    def hide_bottom_menu(self):
        anim = Animation(x=0, y=-self.bot_menu.height, t='in_out_elastic')
        anim.start(self.bot_menu)

class Game(Widget):
    def __init__(self):
        super(Game, self).__init__()
        self.event = EventHandler()
        self.world = GameWorld()
        self.npcs = NPCController()
        self.player = Player()
        self.drop_menus = Menus()
        self.dialogue = Dialogue()
        Window.size = self.world.size
        self.player.world = self.world.size
        self.drop_menus.size = self.world.size
        self.drop_menus.y1_animate = self.drop_menus.height
        self.drop_menus.y2_animate = -(self.drop_menus.height/3)
        self.event.calls["keyup"] = self.player.keyup
        self.event.calls["keydown"] = self.player.keydown
        self.event.calls["speechbubble"] = self.player.animate_speech
        self.event.calls["npc_speech"] = self.npcs.activate
        self.add_widget(self.dialogue)
        self.add_widget(self.event)
        self.add_widget(self.world)
        self.add_widget(self.npcs)
        self.add_widget(self.player)
        self.add_widget(self.drop_menus)

    def start_conversaton(self, txt):
        self.drop_menus.show_top_and_bottom_menu(txt)

    def end_conversation():
        self.drop_menus.hide_top_and_bottom_menu()

    def change_text(self, top="", bot=""):
        self.drop_menus.add_text([top, bot])

    def update(self, dt):
        self.world.update(dt)
        self.player.update(dt)
        self.npcs.update(dt)
        self.dialogue.update(dt)

class MainApp(App):
    def build(self):
        game = Game()
        Clock.schedule_interval(game.update, 1./60.)
        return game

if __name__ == "__main__":
    my_app = MainApp()
    my_app.run()
