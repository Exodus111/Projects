#!/usr/bin/python3
import kivy
kivy.require("1.9.0")

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.properties import ListProperty, DictProperty, ObjectProperty
from kivy.graphics import Line

from path import Path
import json
from random import randint

# Line collison Projection ALMOST works.
# Corners and some lines no not work.

DIAGONAL_LINE = [[100, 100], [110, 100], [400, 800]]
HOUSE = [[100, 100], [100, 600], [500, 600], [500, 100], [900, 800]]


class Main(Widget):
    line1 = ListProperty(HOUSE)
    linelist = ListProperty([])
    pos1 = ListProperty([200, 400])
    move = DictProperty({"up":False, "down":False, "right":False, "left":False})
    direction = DictProperty({"up":[0,1], "down":[0,-1], "right":[1,0], "left":[-1,0]})

    def setup(self):
        self.keyboard = Window.request_keyboard(self.key_off, self)
        self.keyboard.bind(on_key_down=self.key_down)
        self.keyboard.bind(on_key_up=self.key_up)
        #self.import_json("main_wall.json")
        #self.random_points()
        self.make_linelist()
        self.draw_poly()

    def random_points(self):
        x, y = (100, 100)
        self.line1 = []
        for line in range(12):
            x += randint(0, 100)
            y += randint(0, 100)
            line = [x, y]
            self.line1.append(line)

    def make_linelist(self):
        for n in range(len(self.line1)-1):
            self.linelist.append([self.line1[n][0], self.line1[n][1] , self.line1[n+1][0], self.line1[n+1][1]])


    def key_off(self):
        pass

    def key_down(self, keyboard, keycode, text, mod):
        if keycode[1] == "w":
            self.move["up"] = True
        if keycode[1] == "s":
            self.move["down"] = True
        if keycode[1] == "d":
            self.move["right"] = True
        if keycode[1] == "a":
            self.move["left"] = True

    def key_up(self, k, keycode):
        if keycode[1] == "w":
            self.move["up"] = False
        if keycode[1] == "s":
            self.move["down"] = False
        if keycode[1] == "d":
            self.move["right"] = False
        if keycode[1] == "a":
            self.move["left"] = False

    def on_touch_down(self, touch):
        pass

    def import_json(self, filename, height=608):
        js_file = Path("./data/collision/church/{}".format(filename))
        with open(js_file, "r+") as f:
            js_dict = json.load(f)
        self.line1 = [[int(i[0]), int((height-i[1]+500))] for i in js_dict["main"]]

    def draw_poly(self):
        with self.canvas:
            Line(points=[i for sub in self.line1 for i in sub], width=1.0)

    def h_l(self, n1, n2):
        """
        higher_lower. Returns the higher number first.
        """
        if n1 > n2:
            return n1, n2
        else:
            return n2, n1

    def does_it_intersect(self, line1, line2):
        a1 = (line1[0], line1[1])
        a2 = (line1[2], line1[3])
        b1 = (line2[0], line2[1])
        b2 = (line2[2], line2[3])
        inter = Vector.line_intersection(a1, a2, b1, b2)
        if inter != None:
            inter = (int(round(inter[0])), int(round(inter[1])))
            x,y = inter
            a_xh, a_xl = self.h_l(a1[0], a2[0])
            a_yh, a_yl = self.h_l(a1[1], a2[1])
            b_xh, b_xl = self.h_l(b1[0], b2[0])
            b_yh, b_yl = self.h_l(b1[1], b2[1])
            if x <= b_xh and x >= b_xl and y <= b_yh and y >= b_yl:
                if x <= a_xh and x >= a_xl and y >= a_yl and y <= a_yh:
                    return (x,y)
        return None

    def placeholder(self):
        return True

    def moving(self):
        move_str = ""
        moving = False
        for mov in self.move:
            if self.move[mov]:
                moving = True
                self.move[mov] = self.placeholder()
                if self.move[mov]:
                    move_str += mov
        if move_str in ("up", "down", "left", "right"):
            direction = self.direction[move_str]
        elif move_str in ("upleft", "leftup"):
            direction = [-1,1]
        elif move_str in ("upright", "rightup"):
            direction = [1,1]
        elif move_str in ("downleft", "leftdown"):
            direction = [-1,-1]
        elif move_str in ("downright", "rightdown"):
            direction = [1,-1]
        else:
            direction = [0,0]
        if moving:
            for line in self.linelist:
                    direction = self.line_collision_projection(direction, line)
            self.pos1 = Vector(self.pos1) + Vector(direction)*5

    def line_collision_projection(self, direction, line):
        collided = False
        pos2 = Vector(self.pos1) + Vector(direction)*6
        inter = Vector.segment_intersection(self.pos1, pos2, (line[0], line[1]), (line[2], line[3]))
        if inter != None:
            if Vector(self.pos1).distance(inter) < 15:
                collided = True
        if collided:
            wall = Vector((line[0], line[1])) - Vector((line[2], line[3]))
            dot = Vector(wall).dot(direction)
            x = (dot/(wall.x*wall.x  + wall.y*wall.y))*wall.x
            y = (dot/(wall.x*wall.x  + wall.y*wall.y))*wall.y
            direction = (int(x),int(y))
        return direction

    def update(self, dt):
        self.moving()

class LineApp(App):

    def build(self):
        game = Main()
        game.setup()
        Clock.schedule_interval(game.update, 1/60)
        return game

if __name__ == "__main__":
    app = LineApp()
    app.run()
