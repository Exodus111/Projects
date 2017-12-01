#!/usr/bin/python3
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.vector import Vector
from kivy.atlas import Atlas
from kivy.graphics import Color, Rectangle

from kivy.properties import *

from tools.tools import *
from random import choice
from path import Path
import json

class CWidget(Widget):
    rect_color = ListProperty([1., 1., 1., .5])

    def show_rect(self):
        pass

    def turn_red(self):
        self.rect_color = [1., 0., 0., .5]

    def turn_white(self, *_):
        self.rect_color = [1., 1., 1., .5]

    def on_rect_color(self, *_):
        pass

class Entity(Widget):
    etype = StringProperty("entity")
    home = StringProperty("")
    frame = ObjectProperty(None)
    collider_size = ListProperty([48,110])
    frames = DictProperty()
    dirs = DictProperty({"up":[0,1],
            "down":[0,-1],
            "left":[-1,0],
            "right":[1,0]})
    moving = DictProperty({"up":False,
                           "down":False,
                           "left":False,
                           "right":False})
    last_known_good = ListProperty([0,0])
    current = StringProperty("idle")
    framenum = NumericProperty(1)
    counter = NumericProperty(0)
    name = StringProperty("")
    collided_with = StringProperty("")
    entsize = ListProperty([0,0])
    frame_pos = ListProperty([0,0])
    multiplier = NumericProperty(3)
    timer = NumericProperty(0.)

    def place(self, x, y):
        self.pos = self.to_widget(x, y)

    def entitysetup(self, atlasfile, screen_size):
        self.atlas = Atlas(atlasfile)
        self.frame_pos = self.pos_to_frame()
        if len(self.atlas.textures.keys()) > 1:
            for pose in self.atlas.textures.keys(): self.frames[pose] = scale_and_convert(self.atlas[pose], self.multiplier, True, False) # <-- The False stops the image from being flipped. No idea why it happens.
        self.set_frame("idle", 1)
        self.gen = self._num()
        self.collider.pos = self.pos

    def pos_to_frame(self):
        return (self.pos[0]-(self.size[0]/2), self.pos[1])

    def update(self, dt):
        self.timer += dt
        if self.counter > 4: # <--Animation speed.
            self.framenum = next(self.gen)
            self.counter = 0
        self.counter += 1
        self.move()
        self.collide_world()
        self.frame_pos = self.pos_to_frame()

    def move(self):
        pass

    def set_frame(self, pose, num):
        if pose == "idle":
            num = 1
        self.frame = self.frames["{}{}".format(pose, num)]
        self.entsize = self.frame.size

    def _num(self):
        while True:
            for i in range(1, 5):
                yield i

    def collide_world(self):
        pass

    def comment_pos(self):
        return self.pos[0]+40, self.pos[1]+200

    def collide_npcs(self, mov):
        if self.name != "Thack":
            collidelist = self.parent.parent.coll_childs(self)
        else:
            collidelist = self.parent.parent.npcs.coll_childs(self)
        if collidelist != []:
            if collidelist[0].name in self.parent.in_world:
                return True
        return False

    def reverse_movement(self, mov, w=None):
        if w == None:
            w = self
        if mov == "up":
            return Vector(w.pos) + Vector(self.dirs["down"])*3
        elif mov == "down":
            return Vector(w.pos) + Vector(self.dirs["up"])*3
        elif mov == "left":
            return Vector(w.pos) + Vector(self.dirs["right"])*3
        elif mov == "right":
            return Vector(w.pos) + Vector(self.dirs["left"])*3

class Player(Entity):
    screen_size = ListProperty([0,0])
    collider_size = ListProperty([48, 48])
    walk_speed = NumericProperty(6)

    def playersetup(self, screen_size):
        self.screen_size = screen_size
        self.entitysetup("images/player_sheet.atlas", screen_size)
        self.name = "Thack"

    def collide_world(self, x=500, y=500, speedup=0):
        window_pos = self.to_window(self.pos[0], self.pos[1])
        if window_pos[0] < x:
            self.parent.move_world("right", speedup)
        if window_pos[0] > self.screen_size[0]-x:
            self.parent.move_world("left", speedup)
        if window_pos[1] < y:
            self.parent.move_world("down", speedup)
        if window_pos[1] > self.screen_size[1]-y:
            self.parent.move_world("up", speedup)

    def keydown(self, key):
        if key in ("up", "w"):
            self.moving["up"] = True
        if key in ("down", "s"):
            self.moving["down"] = True
        if key in ("left", "a"):
            self.moving["left"] = True
        if key in ("right", "d"):
            self.moving["right"] = True

    def keyup(self, key):
        if key in ("up", "w"):
            self.moving["up"] = False
        if key in ("down", "s"):
            self.moving["down"] = False
        if key in ("left", "a"):
            self.moving["left"] = False
        if key in ("right", "d"):
            self.moving["right"] = False

    def move(self):
        move_str = ""
        moving = False
        self.current = "idle"

        # Movement Code.
        for mov in self.moving:
            if self.moving[mov]:
                moving = True

                # Clutter Collision Code.
                old_pos = self.collider.pos.copy()
                self.collider.pos = Vector(self.collider.pos) + Vector(self.dirs[mov])*self.walk_speed
                for w in self.parent.cluttergroup.children:
                    if self.parent.collide_npcs(self) or self.collider.collide_widget(w):
                            moving = False
                            self.collider.pos = old_pos
                if moving:
                    move_str += mov

                # Animation Code.
                if self.moving["right"] or self.moving["left"]:
                    if mov == "up" or mov == "down":
                        pass
                    else:
                        self.current = "walk{}".format(mov)
                else:
                    self.current = "walk{}".format(mov)

        # Wall Collision Code.
        if move_str in ("up", "down", "left", "right"):
            direction = self.dirs[move_str]
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

        if move_str != "":
            direction = self.parent.collide_walls(self.collider.center, direction)
            self.pos = Vector(self.pos) + Vector(direction)*self.walk_speed
            self.collider.pos = (self.pos[0], self.pos[1])

        # Collide with POI (Doors).
        self.parent.collide_poi(self.collider)

        # Set Animation Frame.
        self.set_frame(self.current, self.framenum)

class NPC(Entity):
    current_direction = StringProperty("idle")
    last_direction = StringProperty("idle")
    move_list = ListProperty()
    npc_speed = NumericProperty(8)
    cooldowns = DictProperty()

    def npcsetup(self, atlasfile, size):
        self.entitysetup(atlasfile, size)

    def move(self):
        if self.move_list != []:
            self.calc_direction()
        self._move()
        if self.current_direction != self.last_direction and self.current_direction != "idle":
            if self.cooldown("animation_switch", .1): # Cooldown to avoid stuttering.
                self._move_animate()
                self.last_direction = self.current_direction
        else:
            self._move_animate()

        self.collider.pos = (self.pos[0], self.pos[1])

    def calc_direction(self):
        if circle_collide(Widget(pos=self.move_list[0]), self, dist=20):
            self.move_list.pop(0)
        if self.move_list != []:
            x1, y1 = self.pos
            x2, y2 = self.move_list[0]
            dist_x = abs(x1 - x2)
            dist_y = abs(y1 - y2)

            left = x1 > x2
            down = y1 > y2
            x_axis = dist_x > dist_y
            diag_x = (dist_y*2) > dist_x
            diag_y = (dist_x*2) > dist_y

            if x_axis:
                if left:
                    if diag_x:
                        if down:
                            self.current_direction = "leftdown"
                        else:
                            self.current_direction = "leftup"
                    else:
                        self.current_direction = "left"
                elif diag_x:
                    if down:
                        self.current_direction = "rightdown"
                    else:
                        self.current_direction = "rightup"
                else:
                    self.current_direction = "right"
            else:
                if down:
                    if diag_y:
                        if left:
                            self.current_direction = "leftdown"
                        else:
                            self.current_direction = "rightdown"
                    else:
                        self.current_direction = "down"
                elif diag_y:
                    if left:
                        self.current_direction = "leftup"
                    else:
                        self.current_direction = "rightup"
        else:
            self.current_direction = "idle"

    def _move_animate(self):
        if self.current_direction == "idle":
            self.set_frame("idle", self.framenum)
        if self.current_direction == "up":
            self.set_frame("walkup", self.framenum)
        elif self.current_direction == "down":
            self.set_frame("walkdown", self.framenum)
        elif self.current_direction == "left":
            self.set_frame("walkleft", self.framenum)
        elif self.current_direction == "right":
            self.set_frame("walkright", self.framenum)
        elif self.current_direction == "leftup":
            self.set_frame("walkleft", self.framenum)
        elif self.current_direction == "rightup":
            self.set_frame("walkright", self.framenum)
        elif self.current_direction == "leftdown":
            self.set_frame("walkleft", self.framenum)
        elif self.current_direction == "rightdown":
            self.set_frame("walkright", self.framenum)

    def _move(self):
        if self.current_direction == "up":
            self.pos = self.pos[0], self.pos[1]+self.npc_speed
        elif self.current_direction == "down":
            self.pos = self.pos[0], self.pos[1]-self.npc_speed
        elif self.current_direction == "left":
            self.pos = self.pos[0]-self.npc_speed, self.pos[1]
        elif self.current_direction == "right":
            self.pos = self.pos[0]+self.npc_speed, self.pos[1]
        elif self.current_direction == "leftup":
            self.pos = self.pos[0]-(self.npc_speed/2), self.pos[1]+(self.npc_speed/2)
        elif self.current_direction == "rightup":
            self.pos = self.pos[0]+(self.npc_speed/2), self.pos[1]+(self.npc_speed/2)
        elif self.current_direction == "leftdown":
            self.pos = self.pos[0]-(self.npc_speed/2), self.pos[1]-(self.npc_speed/2)
        elif self.current_direction == "rightdown":
            self.pos = self.pos[0]+(self.npc_speed/2), self.pos[1]-(self.npc_speed/2)


    def cooldown(self, name, num):
        if name not in self.cooldowns.keys():
            self.cooldowns[name] = self.timer
            return False
        else:
            if self.cooldowns[name] + num < self.timer:
                del(self.cooldowns[name])
                return True
            else:
                return False

class NPCController(Widget):
    npcs = DictProperty({"Djonsiscus":{"home":"church main", "place":(1955, 733)},
                         "Jarod":{"home":"church basement", "place":(1602, 694)},
                         "Tylda Travisteene":{"home":"outside", "place":(1955, 733)},
                         "Sheila Travisteene":{"home":"outside", "place":(278, 317)},
                         "Mr Johes":{"home":"outside", "place":(1955, 733)},
                         "Riff Danner":{"home":"outside", "place":(1955, 733)}})
    npc_paths = DictProperty()
    npcgroup = ListProperty([])

    def controllersetup(self, size):
        self.get_paths()
        for name in self.npcs.keys():
            npc = NPC(size=(48, 110))
            npc.name = name
            npc.home = self.npcs[name]["home"]
            npc.pos = self.npcs[name]["place"]
            npc.npcsetup("images/{}.atlas".format(name), size)
            self.npcgroup.append(npc)

    @staticmethod
    def _get_json(filename):
        with open(filename) as f:
            out = json.load(f)
        return out

    def get_paths(self):
        for f in Path("./data").files():
            if "path" in f.name:
                key = f.name.replace("path_", "")
                key = key.replace(".json", "")
                self.npc_paths[key] = self._get_json(f)

    def update(self, dt):
        for npc in self.npcgroup:
            npc.update(dt)

    def npc_walk_path(self, name, path_id):
        nameid = "{}{}{}".format(name.lower(), "_", path_id)
        for key in self.npc_paths.keys():
            if nameid == key:
                 self.move_npc(name, self.npc_paths[key]["points"])

    def move_npc(self, name, poslist):
        for npc in self.npcgroup:
            if npc.name == name:
                for pos in poslist:
                    npc.move_list.append(pos)

    def coll_childs(self, w):
        return [child for child in self.npcgroup if circle_collide(child, w)]

class TestWidget(Widget):
    pass