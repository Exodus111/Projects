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
            "dialogue_choice":None,
            "menu_click":None,
            "mouse_over":None
        }
        Window.bind(mouse_pos=self.mouse_over)
        self.keyboard = Window.request_keyboard(self.key_off, self)
        self.keyboard.bind(on_key_down=self.key_down)
        self.keyboard.bind(on_key_up=self.key_up)

    def mouse_over(self, inst, pos):
        #self.calls["mouse_over"](pos)
        pass

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
        elif keycode[1] in [str(i) for i in range(10)] or keycode[1] == "spacebar":
            self.calls["dialogue_choice"](keycode[1])

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
    y_adjust = NumericProperty(0)

    def change_color(self, instance, color):
        self.text_colour = color

class Menus(Widget):
    top_status = BooleanProperty(False)
    bot_status = BooleanProperty(False)
    top_menu = ObjectProperty(None)
    bot_menu = ObjectProperty(None)    # Bot stands for Bottom.
    y1_animate = NumericProperty(0)
    y2_animate = NumericProperty(0)
    text_color = ListProperty([1., 1., 1., 0.])
    current_npc = ObjectProperty(None)
    txtlist = ListProperty(["", ""])

    def setup_menus(self):
        self.top_menu.y_adjust = self.top_menu.height - 20*5
        self.bot_menu.y_adjust = 50
        self.bind(text_color=self.top_menu.change_color)
        self.bind(text_color=self.bot_menu.change_color)
        self.show_anim = Animation(y1_animate=self.height-self.top_menu.height, t='out_bounce')
        self.show_anim &= Animation(y2_animate=0, t='out_bounce')
        self.show_anim += Animation(text_color=[1., 1., 1., 1.])

        self.hide_anim = Animation(text_color=[1., 1., 1., 0.])
        self.hide_anim += Animation(y1_animate=self.height, t='in_out_elastic')
        self.hide_anim &= Animation(y2_animate=-self.bot_menu.height, t='in_out_elastic')

    def text_clicked(self, args):
        self.parent.dialogue.line_clicked(args[1])

    def text_hovered(self, pos):
        for child in self.bot_menu.children:
            for r in child.refs:
                x1, y1, x2, y2 = child.refs[r][0]
                x1, y1 = child.to_window(x1, y1)
                x2, y2 = child.to_window(x2, y2)
                if pos[0] > x1 and pos[0] < x2 and pos[1] > y1 and pos[1] < y2:
                    pass # Doesn't work, Y pos misses by some pixels.
                         # Might need to scrap this approach and redo how Labels handle the text.
                         # Adding Button Widget around every text element might be a better idea.


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
        self.change_text(txt)
        self.show_anim.start(self)

    def change_text(self, txt):
        if txt == []:
            txt = self.ran_text()
        if txt[0] != "":
            self.top_menu.act_text = txt[0]
        if txt[1] != "":
            self.bot_menu.act_text = txt[1]
        self.txtlist = txt

    def hide_top_and_bottom_menu(self):
        self.hide_anim.start(self)

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
        self.add_widget(self.dialogue)
        self.add_widget(self.event)
        self.add_widget(self.world)
        self.add_widget(self.npcs)
        self.add_widget(self.player)
        self.add_widget(self.drop_menus)
        self.drop_menus.setup_menus()
        self.dialogue.setup_nodes()
        self.event.calls["keyup"] = self.player.keyup
        self.event.calls["keydown"] = self.player.keydown
        self.event.calls["dialogue_choice"] = self.dialogue.key_up
        self.event.calls["mouse_over"] = self.drop_menus.text_hovered

    def start_conversaton(self, txt):
        self.player.stopping = True
        self.player.set_idle()
        self.drop_menus.show_top_and_bottom_menu(txt)

    def end_conversation(self):
        self.player.stopping = False
        self.drop_menus.hide_top_and_bottom_menu()

    def change_top_text(self, txt):
        self.drop_menus.change_text([txt, ""])

    def change_bot_text(self, txt):
        self.drop_menus.change_text(["", txt])

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
