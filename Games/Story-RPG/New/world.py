#!/usr/bin/python3
from kivy.clock import Clock
from kivy.uix.relativelayout import RelativeLayout, FloatLayout
from kivy.vector import Vector
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics import Line, Color, Rectangle
from kivy.properties import *
from random import choice
from path import Path
import json

from tools.tools import *

class WorldElement(Image):
    name = StringProperty("")

class ClutterGroup(Widget):
    name = StringProperty("Nothing.")

    def __repr__(self):
        return "<Clutter Group Widget, {}>".format(self.name)

    def show_all(self):
        for child in self.children:
            child.show()

class DoorWidget(Widget):
    name = StringProperty("")

    def __repr__(self):
        return "<Door Widget, {}>".format(self.name)

class ClutterElement(Widget):
    rect = ListProperty([0,0,0,0])

    def show(self):
        mylabel = Label(pos=(self.rect[0], self.rect[1]),
          text=str(self.pos), halign="center", valign="middle",
          font_size=15, color=[0,0,0,1.])

        self.add_widget(mylabel)
        with mylabel.canvas:
            Color(rgba=[1.,1.,1.,.5])
            Rectangle(pos=self.pos, size=self.size)

class World(RelativeLayout):
    home = StringProperty("")
    worldcenter = ListProperty([0,0])
    worldspeed = NumericProperty(5)
    in_world = ListProperty([])
    bg = ObjectProperty(None)
    fg = ObjectProperty(None)
    cluttergroup = ObjectProperty(None)
    poi = ListProperty([])
    dots = ListProperty([])
    once = BooleanProperty(True)
    _once = BooleanProperty(True)
    colliding_with = ListProperty()
    walls = DictProperty({})
    player_line = ListProperty([])
    act_walls = ListProperty([])
    worlddict = DictProperty()

    doors = DictProperty(load_json("./data/doors.json"))

    def setupworld(self):
        with open("world.json", "r+") as f:
            self.worlddict = json.load(f)
        self.cluttergroup = ClutterGroup()
        self.load_walls("church")
        self.start_scene("church", "main")
        self.add_widget(self.bg, index=1)
        self.add_widget(self.fg, index=1)

    def load_walls(self, scene):
        if scene not in self.walls.keys():
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
                                                 "points":wall_info[i]}
                        else:
                            walldict[i]["clutter"] = {"rects":wall_info[i]}
            self.walls[scene] = walldict

    def start_scene(self, scene, part):
        self.bg = WorldElement(texture=scale_and_convert(self.worlddict[scene][part]["bg"]))
        self.fg = WorldElement(texture=scale_and_convert(self.worlddict[scene][part]["fg"]))
        self.load_scene(scene, part, True)

    def load_scene(self, scene, part, first=False):
        # Setting up the scenes textures.
        if not first:
            if scene == "outside":
                growth = 4
            else:
                growth = 3
            self.bg.texture = scale_and_convert(self.worlddict[scene][part]["bg"], growth)
            self.fg.texture = scale_and_convert(self.worlddict[scene][part]["fg"], growth)

        # Setting up the sizes.
        self.bg.size = self.bg.texture.size
        self.fg.size = self.fg.texture.size

        # Adding NPCs. (Not on first load.)
        self.home = scene + " " + part
        if self.parent != None:
            self.add_npcs(self.parent.npcs.npcgroup)

        # This sets up the collison for the walls.
        if scene not in self.walls.keys():
            self.load_walls(scene)
        self.linelist = self.walls[scene][part]["bg"]["points"]
        #self.draw_line(self.linelist) #<--- Used to test the walls.


        # This sets up the collision for objects in the rooms.
        self.make_clutter_collision(scene, part)
        #self.cluttergroup.show_all() # for Testing clutter collisions.

        # This sets up the ability to move between rooms.
        [self.remove_widget(j) for j in self.poi]
        self.poi = []
        for i, v in self.doors[scene][part].items():
            if "to_" in i or "from_" in i:
                w = DoorWidget()
                w.pos = v
                w.name = i
                self.poi.append(w)
                self.add_widget(w)

## <-------- Loading Methods, loaded from load_scene. ---------->

    def add_npcs(self, npcs):
        self.in_world = []
        for child in self.children:
            if hasattr(child, "etype"):
                if child.name != "Thack":
                    self.remove_widget(child)
        for npc in npcs:
            if npc.home == self.home:
                self.in_world.append(npc.name)
                self.add_widget(npc, index=2)

    def draw_line(self, points):
        """For testing collision."""
        #self.canvas.clear()
        with self.canvas:
            Line(points=points, width=1.0)

    def make_clutter_collision(self, scene, part):
        if self.cluttergroup not in self.children:
            self.add_widget(self.cluttergroup, index=0)
        else:
            self.cluttergroup.clear_widgets()
        rects = self.walls[scene][part]["clutter"]["rects"]
        for r in rects.values():
            clutter = ClutterElement()
            clutter.rect = r.copy()
            #clutter.show()  #<-- For testing.
            self.cluttergroup.add_widget(clutter)
        self.cluttergroup.name = scene + " " + part

    def _make_linelist(self, pointlist):
        linelist = []
        for n in range(len(pointlist)-1):
            linelist.append([pointlist[n][0], pointlist[n][1] , pointlist[n+1][0], pointlist[n+1][1]])
        return linelist

## <-------- Collision Methods. -------------------->

    def collide_walls(self, pos, direction, dist=20):
        for line in quad_overlap(self.linelist):
            direction = self.line_collision_projection(pos, line, direction, dist)
        return direction

    def line_collision_projection(self, pos, line, direction, dist):
        collided = False
        pos2 = Vector(pos) + Vector(direction)*20
        inter = Vector.segment_intersection(pos, pos2, (line[0], line[1]), (line[2], line[3]))
        if inter != None:
            if Vector(pos).distance(inter) < dist:
                collided = True
        if collided:
            wall = Vector((line[0], line[1])) - Vector((line[2], line[3]))
            dot = Vector(wall).dot(direction)
            x = (dot/(wall.x*wall.x  + wall.y*wall.y))*wall.x
            y = (dot/(wall.x*wall.x  + wall.y*wall.y))*wall.y
            direction = (int(x),int(y))
        return direction

    def collide_npcs(self, wid):
        for child in self.children:
            if hasattr(child, "etype"):
                if child.name != "Thack":
                    if child.collider.collide_widget(wid.collider):
                        self.parent.begin_conv(child.name)
                        return True
        else:
            return False

##<------ Movement Methods -------------->
    
    def center_world(self, pos):
        pass

    def move_world(self, direction, speedup=0):
        if direction == "left":
            self.worldcenter[0] -= (self.worldspeed+speedup)
        if direction == "right":
            self.worldcenter[0] += (self.worldspeed+speedup)
        if direction == "up":
            self.worldcenter[1] -= (self.worldspeed+speedup)
        if direction == "down":
            self.worldcenter[1] += (self.worldspeed+speedup)

    def center_screen(self, dt):
        pos = self.parent.player.pos
        pwin = self.parent.player.to_window(pos[0], pos[1])
        offset = Vector(self.parent.center) - Vector(pwin)
        self.worldcenter = (self.worldcenter[0]+offset[0], self.worldcenter[1]+offset[1])

    def move_player(self, pos):
        self.parent.player.pos = pos
        self.parent.center_screen(0.1)

## <------------
    
    @staticmethod
    def _switch_to_from(name):
        if "to_" in name:
            return name.replace("to_",  "from_")
        elif "from_" in name:
            return name.replace("from_", "to_")

    def _get_opposing_door_pos(self, name):
        for key in self.doors.keys():
            for k in self.doors[key]:
                if name in self.doors[key][k]:
                    return self.doors[key][k][name]

    def check_door(self, name):
        name = self._switch_to_from(name)
        for key in self.doors.keys():
            for k in self.doors[key]:
                if name in self.doors[key][k].keys():
                    self.load_scene(key, k)
                    self.size = mult_tuple(self.doors[key][k]["size"], 3)
                    new_pos = self._get_opposing_door_pos(name)
                    shunt = self.get_shunt(key, k, name)
                    new_pos = add_tuple(new_pos, shunt)
                    self.move_player(new_pos)
                    self.once = False
                    if "outside" in self.home and not self.parent.events.player_outside:
                        self.parent.events.player_outside = True
                        self.parent.player.resize_entity("small")
                    elif "outside" not in self.home and self.parent.events.player_outside:
                        self.parent.events.player_outside = False
                        self.parent.player.resize_entity("big")
                    self.parent.gui.hud.add_text_to_top_bar(text2=self.home)
                    return

    def get_shunt(self, key, k, name):
        if name in self.doors[key][k]["shunts"].keys():
            return (self.doors[key][k]["shunts"][name][0], self.doors[key][k]["shunts"][name][1])
        else:
            return (0,0)

    def collide_poi(self, w):
        for poi in self.poi:
            if w.collide_widget(poi):
                if self.once:
                    self.check_door(poi.name)
                    self.once = False
                    self.colliding_with.append(poi)
                    return
        if self.colliding_with != []:
            if not w.collide_widget(self.colliding_with[0]):
                Clock.schedule_once(lambda *x: self._set_once(True), 2)
                self.colliding_with = []

    def _set_once(self, truefalse):
        self.once = truefalse