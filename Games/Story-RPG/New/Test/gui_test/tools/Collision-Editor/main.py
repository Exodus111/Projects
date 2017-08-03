#!/usr/bin/python3
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import *

import json

def neg(pos, size):
    x = int(pos[0])
    y = int(pos[1])
    w = int(size[0])
    h = int(size[1])
    if h < 0:
        h *= -1
        y -= h
    return [x, y, w, h]


class EventHandler(Widget):
    calls = DictProperty()
    def setup(self):
        Window.bind(mouse_pos=lambda *x: self.calls["mouseover"](x))
        self.keyboard = Window.request_keyboard(lambda : None, self)
        self.keyboard.bind(on_key_down=lambda *x: self.calls["keydown"](x[1], x[3]))
        self.keyboard.bind(on_key_up=lambda *x: self.calls["keyup"](x[1]))

class Rect(Widget):
    rect_size = ListProperty([0,0])
    rect_pos = ListProperty([0,0])

    def __init__(self, s, p, **kwargs):
        super(Rect, self).__init__(**kwargs)
        self.rect_size = s
        self.rect_pos = p

class Editor(RelativeLayout):
    growth = NumericProperty(3)
    line_points = ListProperty()
    mouse_pos = ListProperty([0,0])
    mouse_pressed = StringProperty("")
    imgpos = ListProperty([0,0])
    images = DictProperty({
        "main":{"BG":"images/CI Main Back.png", "FG":"images/CI Main Obj.png"},
        "basement":{"BG":"images/CI Basement Back.png","FG":"images/CI Basement Obj.png"},
        "tower":{"BG":"images/CI Tower Top Back.png","FG":"images/CI Tower Top Obj.png"},
        "priest_room":{"BG":"images/CI Priest Room Back.png","FG":"images/CI Priest Room Obj.png"},
        "thack_room":{"BG":"images/CI Player Room Back.png","FG":"images/CI Player Room Obj.png"}})
    imgtexture = ObjectProperty(None)
    fgtexture = ObjectProperty(None)
    imgsize = ListProperty([0,0])
    rectlist = ListProperty([])
    speed = NumericProperty(15)
    active_rect = BooleanProperty(False)
    move = DictProperty({"up":False,
                         "down":False,
                         "left":False,
                         "right":False})

    def setup(self):
        events = EventHandler()
        events.calls["keydown"] = self.keydown
        events.calls["keyup"] = self.keyup
        events.calls["mouseover"] = self.mouseover
        events.setup()
        self.bind(on_touch_down=lambda x,y:self.touched(y))

        self.imgtexture = Image(source=self.images[self.parent.scene]["BG"]).texture
        self.fgtexture = Image(source=self.images[self.parent.scene]["FG"]).texture
        self.imgsize = [self.imgtexture.size[0]*self.growth, self.imgtexture.size[1]*self.growth]


    def update(self, dt):
        if self.move["up"]:
            self.pos[1] -= self.speed
        if self.move["down"]:
            self.pos[1] += self.speed
        if self.move["left"]:
            self.pos[0] += self.speed
        if self.move["right"]:
            self.pos[0] -= self.speed
        if self.parent.sav_rects:
            self.save_rects()
            self.parent.sav_rects = False
        if self.parent.sav_lines:
            self.save_lines()
            self.parent.sav_lines = False

    def straighten_line(self, pos1, pos2):
        (x, y) = pos1
        a = x - pos2[0]
        b = y - pos2[1]
        if a > 0 and b > 0 or a < 0 and b < 0:
            diff = a - b
        else:
            diff = a + b
        if abs(diff) < 50:
            if a < 0:
                x = pos2[0] - (abs(a) + abs(b))/2
            else:
                x = pos2[0] + (abs(a) + abs(b))/2
            if b < 0:
                y  = pos2[1] - (abs(a) + abs(b))/2
            else:
                y = pos2[1] + (abs(a) + abs(b))/2
        elif abs(a) > abs(b):
            y = pos2[1]
        else:
            x = pos2[0]
        return (x,y)

    def check_for_endpoint(self, pos):
        p1 = self.line_points[0]
        p2 = pos
        if abs(p1[0] - p2[0]) < 25 and  abs(p1[1] - p2[1]) < 25:
            self.line_points[-1] = p1
            self.line_points[-2] = self.straighten_line(self.line_points[-2], p1)

    def make_line(self, pos):
        pos = (pos[0]-self.pos[0], pos[1]-self.pos[1])
        self.line_points.append(pos)
        if len(self.line_points) > 1:
            self.line_points[-1] = self.straighten_line(pos, self.line_points[-2])
            self.check_for_endpoint(pos)


    def make_rect(self, pos):
        if not self.active_rect:
            pos = (pos[0]-self.pos[0], pos[1]-self.pos[1])
            r = Rect((50,50), pos)
            self.add_widget(r)
            self.rectlist.append(r)
            self.active_rect = True
        else:
            self.active_rect = False

    def save_rects(self):
        if self.rectlist != []:
            savedict = {}
            for num, rect in enumerate(self.rectlist):
                savedict["rect" + str(num)] = neg(rect.rect_pos, rect.rect_size)
            filename = "{}{}".format(self.parent.scene, "_clutter.json")
            with open("./saves/{}".format(filename), "w+") as f:
                json.dump({self.parent.scene:savedict}, f, indent=4, sort_keys=True)
        else:
            print("No rectangles to save.")

    def save_lines(self):
        if self.line_points != []:
            savedict = {self.parent.scene:[int(item) for sublist in self.line_points for item in sublist]}
            savedict["growth"] = self.growth
            savedict["size"] = self.imgsize
            filename = "{}{}".format(self.parent.scene, "_wall.json")
            with open("./saves/{}".format(filename), "w+") as f:
                json.dump(savedict, f, indent=4, sort_keys=True)
        else:
            print("No points to save.")

    def touched(self, e):
        if e.button == "right":
            if self.parent.rect_mode:
                self.make_rect((e.x, e.y))
            else:
                self.make_line((e.x, e.y))

    def mouseover(self, x):
        self.mouse_pos = (x[1][0]-self.pos[0], x[1][1]-self.pos[1])
        if self.parent.rect_mode:
            if self.active_rect:
                rect_pos = self.rectlist[-1].rect_pos
                new_size = [self.mouse_pos[0] - rect_pos[0], self.mouse_pos[1] - rect_pos[1]]
                self.rectlist[-1].rect_size = new_size
        else:
            pass

    def keydown(self, key, mod):
        if key[1] in ("w", "up"):
            self.move["up"] = True
        if key[1] in ("a", "left"):
            self.move["left"] = True
        if key[1] in ("s", "down"):
            self.move["down"] = True
        if key[1] in ("d", "right"):
            self.move["right"] = True

    def keyup(self, key):
        if key[1] in ("w", "up"):
            self.move["up"] = False
        if key[1] in ("a", "left"):
            self.move["left"] = False
        if key[1] in ("s", "down"):
            self.move["down"] = False
        if key[1] in ("d", "right"):
            self.move["right"] = False

class HUD(BoxLayout):
    mode = StringProperty("Rectangle Mode")

    def setup(self):
        pass

    def update(self, dt):
        pass

    def switch_mode(self):
        if self.mode == "Rectangle Mode":
            self.mode = "Line Mode"
        else:
            self.mode = "Rectangle Mode"
        self.parent.rect_mode = not self.parent.rect_mode

    def save_lines(self):
        self.parent.sav_lines = True

    def save_rects(self):
        self.parent.sav_rects = True

class Main(Widget):
    w_size = Window.size
    sav_rects = BooleanProperty(False)
    sav_lines = BooleanProperty(False)
    rect_mode = BooleanProperty(True)
    scene = StringProperty("thack_room")

    def setup(self):
        for child in self.children:
            child.setup()

    def update(self, dt):
        for child in self.children:
            child.update(dt)


class EditorApp(App):
    def build(self):
        main = Main()
        main.setup()
        Clock.schedule_interval(main.update, 1./60.)
        return main

if __name__ == "__main__":
    EditorApp().run()
