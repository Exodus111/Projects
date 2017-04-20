#!/usr/bin/python3
from kivy.uix.relativelayout import RelativeLayout
from kivy.vector import Vector
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics import Line, Color
from kivy.properties import ObjectProperty, ListProperty, StringProperty, NumericProperty, DictProperty, BooleanProperty
from path import Path
import json

from tools import circle_collide

class WorldElement(Image):
    name = StringProperty("")

class World(RelativeLayout):
    home = StringProperty("")
    worldcenter = ListProperty([0,0])
    worldspeed = NumericProperty(5)
    in_world = ListProperty([])
    poi = ListProperty([])
    dots = ListProperty([])
    once = BooleanProperty(True)
    walls = DictProperty({})
    player_line = ListProperty([])
    act_walls = ListProperty([])
    worlddict = DictProperty({
    "church":{"main":{"bg":"images/world/CI Main Back.png",
                      "clutter":"images/world/CI Main Obj.png",
                      "bg_walls":"data/collision/church/main_wall.json",
                      "clutter_collision":"data/collision/church/main_clutter.json",
                      "adjust":1215},

              "basement":{"bg":"images/world/CI Basement Back.png",
                          "clutter":"images/world/CI Basement Obj.png",
                          "bg_walls":"data/collision/church/basement_wall.json",
                          "clutter_collision":"data/collision/church/basement_clutter.json",
                          "adjust":828},

              "thack_room":{"bg":"images/world/CI Player Room Back.png",
                            "clutter":"images/world/CI Player Room Obj.png",
                            "bg_walls":"data/collision/church/thack_room_wall.json",
                            "clutter_collision":"data/collision/church/thack_room_clutter.json",
                            "adjust":510},

              "priest_room":{"bg":"images/world/CI Priest Room Back.png",
                             "clutter":"images/world/CI Priest Room Obj.png",
                             "bg_walls":"data/collision/church/priest_room_wall.json",
                             "clutter_collision":"data/collision/church/priest_room_clutter.json",
                             "adjust":510},

              "tower":{"bg":"images/world/CI Tower Top Back.png",
                       "clutter":"images/world/CI Tower Top Obj.png",
                      "bg_walls":"data/collision/church/tower_wall.json",
                      "clutter_collision":"data/collision/church/tower_clutter.json",
                      "tower":510}}})

    doors = DictProperty({"church":{
                          "main":{
                          "to_basement":(1883, 327),
                          "to_thack_room":(146, 858),
                          "to_priest_room":(1496, 855),
                          "to_tower":(0,0),
                          "out":(830, 72)},

                          "basement":{
                          "from_basement":(1590, 192)},

                          "priest_room":{
                          "from_priest_room":(248, 95)},

                          "tower":{
                          "from_tower":(0,0)},

                          "thack_room":{
                          "from_thack_room":(248, 93)}}})

    def setupworld(self):
        self.load_scene("church", "priest_room", True)
        #self.draw_line([item for sublist in self.act_walls for item in sublist]) #<--- Used to test the walls.

    def draw_line(self, points):
        """For testing collision."""
        with self.canvas:
            Line(points=points, width=1.0)

    def load_scene(self, scene, part, first=False):
        if first:
            self.load_walls(scene)
            self.bg = WorldElement(source=self.worlddict[scene][part]["bg"])
            self.bg_clutter = WorldElement(source=self.worlddict[scene][part]["clutter"])
            self.add_widget(self.bg)
            self.add_widget(self.bg_clutter)
        else:
            self.bg.source = self.worlddict[scene][part]["bg"]
            self.bg_clutter.source = self.worlddict[scene][part]["clutter"]
            self.add_npcs(self.parent.npcs.npcgroup)

        adjust = self.worlddict[scene][part]["adjust"]
        p = self.walls[scene][part]["bg"]["points"]
        w, h = self.walls[scene][part]["bg"]["size"]
        self.size = [w*3, h*3]
        self.act_walls = self.turn_points(p, h, adjust)
        self.linelist = self._make_linelist(self.act_walls)

        for i, v in self.doors[scene][part].items():
            w = Widget(pos=v, size=(64, 64))
            w.name = i
            self.poi.append(w)
        self.home = scene + " " + part

    def _make_linelist(self, pointlist):
        linelist = []
        for n in range(len(pointlist)-1):
            linelist.append([pointlist[n][0], pointlist[n][1] , pointlist[n+1][0], pointlist[n+1][1]])
        return linelist

    def load_walls(self, scene):
        walldict = {}
        for i in self.worlddict[scene]:
            bg = self.worlddict[scene][i]["bg_walls"]
            clutter = self.worlddict[scene][i]["clutter_collision"]
            walldict[i] = {}
            for num, n in enumerate((bg, clutter)):
                with open(n, "r+") as f:
                    wall_info = json.load(f)
                    if num == 0:
                        walldict[i]["bg"] = {"size":wall_info["size"],
                                              "growth":wall_info["growth"],
                                              "points":wall_info[i]}
                    else:
                        walldict[i]["clutter"] = {"rects":wall_info[i]}
        self.walls[scene] = walldict

    def turn_points(self, points, height, adjust):
        """
         main: 1215
         basement: 828
         tower: 510
        """
        newlist = []
        for p in points:
            point = (int(p[0]), int(height - p[1]+adjust))
            newlist.append(point)
        newlist.append(newlist[0])
        return newlist

    def collide_walls(self, pos, direction, mov, dist=50):
        pos2 = Vector(pos) + Vector(direction)*3
        for line in self.linelist:
            pos2 = self.line_collision_projection(pos, pos2, line, direction, mov, dist)
        return Vector(int(round(pos2[0])), int(round(pos2[1])))

    def line_collision_projection(self, pos1, pos2, line, direction, mov, dist):
        collided = False
        p_line = [pos1[0], pos1[1], pos2[0], pos2[1]]
        inter = self.does_it_intersect(p_line, line)
        if inter != None:
            if Vector(pos1).distance(inter) < dist:
                collided = True
        if collided:
            wall = Vector((line[0], line[1])) - Vector((line[2], line[3]))
            wall = Vector(wall)/Vector(wall).length()
            dot = Vector(wall).dot(direction)
            x = (dot/(wall.x*wall.x  + wall.y*wall.y))*wall.x
            y = (dot/(wall.x*wall.x  + wall.y*wall.y))*wall.y
            direction = (x,y)
            pos2 = Vector(pos1) + Vector(direction)
        return pos2

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


    def add_npcs(self, npcs):
        self.in_world = []
        for child in self.children:
            if hasattr(child, "etype"):
                if child.name != "Thack":
                    self.remove_widget(child)
        for npc in npcs:
            if npc.home == self.home:
                self.in_world.append(npc.name)
                self.add_widget(npc)

    def move_world(self, direction):
        if direction == "left":
            self.worldcenter[0] -= self.worldspeed
        if direction == "right":
            self.worldcenter[0] += self.worldspeed
        if direction == "up":
            self.worldcenter[1] -= self.worldspeed
        if direction == "down":
            self.worldcenter[1] += self.worldspeed

    def center_screen(self, dt):
        pos = self.parent.player.pos
        pwin = self.parent.player.to_window(pos[0], pos[1])
        offset = Vector(self.parent.center) - Vector(pwin)
        self.worldcenter = (self.worldcenter[0]+offset[0], self.worldcenter[1]+offset[1])

    def move_player(self, pos):
        self.parent.player.pos = pos
        self.parent.center_screen(0.1)

    def collide_poi(self, w):
        poilist = [poi for poi in self.poi if circle_collide(w, poi)]
        if poilist != []:
            if self.once:
                for p in poilist:
                    if p.name == "to_basement":
                        self.load_scene("church", "basement")
                        self.size = (640*3, 416*3)
                        new_pos = self.doors["church"]["basement"]["from_basement"]
                        self.move_player(new_pos)
                        self.once = False
                        break
                    elif p.name == "to_thack_room":
                        self.load_scene("church", "thack_room")
                        self.size = (192*3, 256*3)
                        new_pos = self.doors["church"]["thack_room"]["from_thack_room"]
                        self.move_player(new_pos)
                        self.once = False
                        break
                    elif p.name == "to_priest_room":
                        self.load_scene("church", "priest_room")
                        self.size = (192*3, 256*3)
                        new_pos = self.doors["church"]["priest_room"]["from_priest_room"]
                        self.move_player(new_pos)
                        self.once = False
                        break
                    elif p.name == "to_tower":
                        self.load_scene("church", "tower")
                        self.size = (192*3, 256*3)
                        break
                    elif p.name == "from_basement":
                        self.load_scene("church", "main")
                        self.size = (768*3, 608*3)
                        new_pos = self.doors["church"]["main"]["to_basement"]
                        self.move_player(new_pos)
                        self.once = False
                        break
                    elif p.name == "from_thack_room":
                        self.load_scene("church", "main")
                        self.size = (768*3, 608*3)
                        new_pos = self.doors["church"]["main"]["to_thack_room"]
                        self.move_player(new_pos)
                        self.once = False
                        break
                    elif p.name == "from_priest_room":
                        self.load_scene("church", "main")
                        self.size = (768*3, 608*3)
                        new_pos = self.doors["church"]["main"]["to_priest_room"]
                        self.move_player(new_pos)
                        self.once = False
                        break
                    elif p.name == "from_tower":
                        self.load_scene("church", "main")
                        self.size = (768*3, 608*3)
                        new_pos = self.doors["church"]["main"]["to_tower"]
                        self.move_player(new_pos)
                        self.once = False
                        break
        else:
            self.once = True
