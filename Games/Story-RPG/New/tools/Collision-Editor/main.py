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
from kivy.uix.popup import Popup
from kivy.properties import *

from path import Path
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

def get_json(filename):
    with open(filename, "r+") as f:
        out = json.load(f)
    return out


class EventHandler(Widget):
    calls = DictProperty()
    def setup(self):
        Window.bind(mouse_pos=lambda *x: self.calls["mouseover"](x))
        self.keyboard = Window.request_keyboard(lambda : None, self)
        self.keyboard.bind(on_key_down=lambda *x: self.calls["keydown"](x[1], x[3]))
        self.keyboard.bind(on_key_up=lambda *x: self.calls["keyup"](x[1]))

class PathPoint(Widget):
    pass

class FileMenu(Popup):
    path = StringProperty("./")
    filepattern = StringProperty("*.*")

    def file_name(self, selection):
        self.path = selection and Path(selection[0]).dirname() or self.path
        return selection and Path(selection[0]).basename() or ""

class Rect(Widget):
    rect_size = ListProperty([0,0])
    rect_pos = ListProperty([0,0])

    def __init__(self, s, p, **kwargs):
        super(Rect, self).__init__(**kwargs)
        self.rect_size = s
        self.rect_pos = p

class Editor(RelativeLayout):
    name = StringProperty("Editor")
    pause = BooleanProperty(False)
    growth = NumericProperty(4)
    line_points = ListProperty()
    path_list = ListProperty()
    paths = ListProperty()
    rectlist = ListProperty([])
    mouse_pos = ListProperty([0,0])
    mouse_pressed = StringProperty("")
    imgpos = ListProperty([0,0])
    images = DictProperty(get_json("images.json"))
    imgtexture = ObjectProperty(None)
    fgtexture = ObjectProperty(None)
    imgsize = ListProperty([0,0])
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
        
        self.savescreen = FileMenu()
        self.savescreen.ok_pressed = self.save_to_file
        self.savescreen.filepattern = "*.json"
        self.savescreen.bind(on_open=self.toggle_pause)
        self.savescreen.bind(on_dismiss=self.toggle_pause)

        self.loadbg = FileMenu()
        self.loadbg.ok_pressed = self.load_bg_image
        self.loadbg.path = "./images"
        self.loadbg.filepattern = "*.png"
        self.loadbg.bind(on_open=self.toggle_pause)
        self.loadbg.bind(on_dismiss=self.toggle_pause)

        self.loadfg = FileMenu()
        self.loadfg.ok_pressed = self.load_fg_image
        self.loadfg.path = "./images"
        self.loadfg.filepattern = "*.png"
        self.loadfg.bind(on_open=self.toggle_pause)
        self.loadfg.bind(on_dismiss=self.toggle_pause)

    def clear_all(self):
        if self.parent.mode == "Rectangle Mode":
            for rect in self.rectlist:
                self.remove_widget(rect)
            self.rectlist = []
        elif self.parent.mode == "Line Mode":
            self.line_points = []
        elif self.parent.mode == "Path Mode":
            for path in self.paths:
                self.remove_widget(path)
            self.path_list = []
            self.paths = []

    def load_bg_image(self, filename):
        self.imgtexture = Image(source=filename).texture
        self.imgsize = [self.imgtexture.size[0]*self.growth, self.imgtexture.size[1]*self.growth]
        self.loadbg.dismiss()

    def load_fg_image(self, filename):
        self.fgtexture = Image(source=filename).texture
        self.loadfg.dismiss()

    def toggle_pause(self, *args):
        self.pause = not self.pause

    def update(self, dt):
        if not self.pause:
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
            elif self.parent.sav_lines:
                self.save_lines()
                self.parent.sav_lines = False
            elif self.parent.sav_path:
                self.save_path()
                self.parent.sav_path = False


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

    def make_path(self, pos):
        pos = (pos[0]-self.pos[0], pos[1]-self.pos[1])
        pos = (pos[0]-15, pos[1]-15)
        center = (int(pos[0]+15), int(pos[1]+15))
        path = PathPoint(pos=pos)
        self.add_widget(path)
        self.paths.append(path)
        self.path_list.append(center)

    def savemenu(self, mode):
        self.savescreen.open()

    def save_to_file(self, filename):
        modes = ["Rectangle Mode", "Line Mode",  "Path Mode"]
        if self.parent.mode == modes[0]:
            self.save_rects(filename)
        elif self.parent.mode == modes[1]:
            self.save_lines(filename)
        elif self.parent.mode == modes[2]:
            self.save_path(filename)
        self.savescreen.dismiss()

    def save_path(self, filename):
        if self.path_list != []:
            new_path = []
            for cent in self.path_list: # Doing an adjustment in the Y axis.
                new_cent = (cent[0]-300, cent[1]-300)
                new_path.append(new_cent)
            savedict = {"points":new_path,
                        "npc":self.parent.npc,
                        "room": self.parent.scene,
                        "id":self.parent.path_id}
            with open(filename, "w+") as f:
                json.dump(savedict, f, indent=4, sort_keys=True)
            self.path_list = []
        else:
            print("No Path to Save.")

    def save_rects(self, filename):
        if self.rectlist != []:
            savedict = {}
            for num, rect in enumerate(self.rectlist):
                savedict["rect" + str(num)] = neg(rect.rect_pos, rect.rect_size)
            with open(filename, "w+") as f:
                json.dump({self.parent.scene:savedict}, f, indent=4, sort_keys=True)
        else:
            print("No rectangles to save.")

    def save_lines(self, filename):
        if self.line_points != []:
            savedict = {self.parent.scene:[int(item) for sublist in self.line_points for item in sublist]}
            savedict["growth"] = self.growth
            savedict["size"] = self.imgsize
            with open(filename, "w+") as f:
                json.dump(savedict, f, indent=4, sort_keys=True)
        else:
            print("No points to save.")

    def touched(self, e):
        if e.button == "right":
            if self.parent.mode == "Rectangle Mode":
                self.make_rect((e.x, e.y))
            elif self.parent.mode == "Line Mode":
                self.make_line((e.x, e.y))
            elif self.parent.mode == "Path Mode":
                self.make_path((e.x, e.y))

    def mouseover(self, x):
        self.mouse_pos = (x[1][0]-self.pos[0], x[1][1]-self.pos[1])
        if self.parent.mode == "Rectangle Mode":
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
        if key[1] == "backspace":  ## <-- Clears Rects/Lines/Paths, mode dependent.
            if not self.pause:
                self.clear_all()

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
    modes = ListProperty(["Rectangle Mode", "Line Mode",  "Path Mode"])
    mode = StringProperty("Rectangle Mode")
    name = StringProperty("HUD")

    def setup(self):
        pass

    def update(self, dt):
        pass

    def switch_mode(self):
        index = self.modes.index(self.mode)
        index += 1
        if index > 2: index = 0
        self.mode = self.modes[index]
        self.parent.mode = self.mode

    def save(self):
        self.parent.editor.savemenu(self.mode)

    def load_bg(self):
        self.parent.editor.loadbg.open()

    def load_fg(self):
        self.parent.editor.loadfg.open()

class Main(Widget):
    w_size = Window.size
    editor = ObjectProperty()
    hud = ObjectProperty()
    sav_rects = BooleanProperty(False)
    sav_lines = BooleanProperty(False)
    sav_path = BooleanProperty(False)
    mode = StringProperty("Rectangle Mode")
    scene = StringProperty("main")
    npc = StringProperty("Djonsiscus")
    path_id = StringProperty("01")

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
