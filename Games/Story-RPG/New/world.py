#!/usr/bin/python3
from kivy.uix.relativelayout import RelativeLayout, FloatLayout
from kivy.vector import Vector
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics import Line, Color, Rectangle
from kivy.properties import ObjectProperty, ListProperty, StringProperty, NumericProperty, DictProperty, BooleanProperty
from path import Path
import json

from tools.tools import circle_collide, scale_image, quad_overlap

class WorldElement(Image):
    name = StringProperty("")

class ClutterGroup(Widget):
    pass

class ClutterElement(Widget):
    rect = ListProperty([0,0,0,0])

    def show(self):
        mylabel = Label(pos=(self.rect[0], self.rect[1]), text=str(self.pos), halign="center", valign="middle", font_size=15, color=[0,0,0,1.])
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
    clutter = ObjectProperty(None)
    cluttergroup = ObjectProperty(None)
    poi = ListProperty([])
    dots = ListProperty([])
    once = BooleanProperty(True)
    walls = DictProperty({})
    player_line = ListProperty([])
    act_walls = ListProperty([])
    worlddict = DictProperty({
    "church":{"main":{"bg":"images/world/CI Main Back.png",
                      "fg":"images/world/CI Main FG.png",
                      "clutter":"images/world/CI Main Obj.png",
                      "bg_walls":"data/collision/church/main_wall.json",
                      "clutter_collision":"data/collision/church/main_clutter.json"},

              "basement":{"bg":"images/world/CI Basement Back.png",
                          "clutter":"images/world/CI Basement Obj.png",
                          "fg":"images/world/CI Basement FG.png",
                          "bg_walls":"data/collision/church/basement_wall.json",
                          "clutter_collision":"data/collision/church/basement_clutter.json"},

              "thack_room":{"bg":"images/world/CI Player Room Back.png",
                            "clutter":"images/world/CI Player Room Obj.png",
                            "fg":"images/world/CI Player Room FG.png",
                            "bg_walls":"data/collision/church/thack_room_wall.json",
                            "clutter_collision":"data/collision/church/thack_room_clutter.json"},

              "priest_room":{"bg":"images/world/CI Priest Room Back.png",
                             "clutter":"images/world/CI Priest Room Obj.png",
                             "fg":"images/world/CI Priest Room FG.png",
                             "bg_walls":"data/collision/church/priest_room_wall.json",
                             "clutter_collision":"data/collision/church/priest_room_clutter.json"},

              "tower":{"bg":"images/world/CI Tower Top Back.png",
                       "clutter":"images/world/CI Tower Top Obj.png",
                       "fg":"images/world/CI Tower Top FG.png",
                      "bg_walls":"data/collision/church/tower_wall.json",
                      "clutter_collision":"data/collision/church/tower_clutter.json"}}})

    doors = DictProperty({"church":{
                          "main":{
                          "to_basement":(1883, 327),
                          "to_thack_room":(146, 808),
                          "to_priest_room":(1496, 855),
                          "to_tower":(0,0),
                          "out":(830, 72)},

                          "basement":{
                          "from_basement":(1590, 192)},

                          "priest_room":{
                          "from_priest_room":(248, 115)},

                          "tower":{
                          "from_tower":(0,0)},

                          "thack_room":{
                          "from_thack_room":(248, 115)}}})

    def setupworld(self):
        self.cluttergroup = ClutterGroup()
        self.load_walls("church")
        self.start_scene("church", "main")
        self.add_widget(self.bg, index=1)
        self.add_widget(self.clutter, index=1)
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
                                                  "growth":wall_info["growth"],
                                                  "points":wall_info[i]}
                        else:
                            walldict[i]["clutter"] = {"rects":wall_info[i]}
            self.walls[scene] = walldict

    def start_scene(self, scene, part):
        self.bg = WorldElement(texture=scale_image(self.worlddict[scene][part]["bg"]))
        self.fg = WorldElement(texture=scale_image(self.worlddict[scene][part]["fg"]))
        self.clutter = WorldElement(texture=scale_image(self.worlddict[scene][part]["clutter"]))
        self.load_scene(scene, part, True)

    def load_scene(self, scene, part, first=False):
        # Setting up the scenes textures.
        if not first:
            self.bg.texture = scale_image(self.worlddict[scene][part]["bg"])
            self.fg.texture = scale_image(self.worlddict[scene][part]["fg"])
            self.clutter.texture = scale_image(self.worlddict[scene][part]["clutter"])

        # Setting up the sizes.
        self.bg.size = self.bg.texture.size
        self.fg.size = self.fg.texture.size
        self.clutter.size = self.clutter.texture.size

        # Adding NPCs. (Not on first load.)
        if self.parent != None:
            self.add_npcs(self.parent.npcs.npcgroup)

        # This sets up the collison for the walls.
        self.linelist = self.walls[scene][part]["bg"]["points"]
        #self.draw_line(self.linelist) #<--- Used to test the walls.


        # This sets up the collision for objects in the rooms.
        self.make_clutter_collision(scene, part)

        # This sets up the ability to move between rooms.
        for i, v in self.doors[scene][part].items():
            w = Widget(pos=v, size=(64, 64))
            w.name = i
            self.poi.append(w)
        self.home = scene + " " + part

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
                self.add_widget(npc, index=1)

    def draw_line(self, points):
        """For testing collision."""
        #self.canvas.clear()
        with self.canvas:
            Line(points=points, width=1.0)

    def make_clutter_collision(self, scene, part):
        if len(self.cluttergroup.children) == 0:
            self.add_widget(self.cluttergroup, index=0)
        else:
            self.cluttergroup.clear_widgets()
        rects = self.walls[scene][part]["clutter"]["rects"]
        for r in rects.values():
            clutter = ClutterElement()
            w, h = self.walls[scene][part]["bg"]["size"]
            clutter.rect = r.copy()
            #clutter.show()  #<-- For testing.
            self.cluttergroup.add_widget(clutter)

    def _make_linelist(self, pointlist):
        linelist = []
        for n in range(len(pointlist)-1):
            linelist.append([pointlist[n][0], pointlist[n][1] , pointlist[n+1][0], pointlist[n+1][1]])
        return linelist

## <---------- This part checks for Line collisions. Called from Player()

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

##<------ Movement Methods -------------->

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

## <------------

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
