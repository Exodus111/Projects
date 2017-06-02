#!/usr/bin/python3
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.atlas import Atlas
from kivy.properties import ListProperty, BooleanProperty, ObjectProperty, DictProperty, StringProperty, NumericProperty

from tools import *

class CollisionWidget(Widget): pass

class Entity(Widget):
    etype = StringProperty("entity")
    home = StringProperty("")
    frame = ObjectProperty(None)
    dirs = DictProperty({"up":[0,1],
            "down":[0,-1],
            "left":[-1,0],
            "right":[1,0]})
    moving = DictProperty({"up":False,
                           "down":False,
                           "left":False,
                           "right":False})
    last_known_good =  ListProperty([0,0])
    current = StringProperty("idle")
    framenum = NumericProperty(1)
    counter = NumericProperty(0)
    name = StringProperty("")
    collided_with = StringProperty("")
    movement_reversed = BooleanProperty(False)
    collide_widget = ObjectProperty(None)

    def place(self, x, y):
        self.pos = self.to_widget(x, y)

    def entitysetup(self, atlasfile):
        self.atlas = Atlas(atlasfile)
        self.set_frame("idle", 1)
        self.gen = self._num()

    def update(self, dt):
        if self.counter > 8: # <--Animation speed.
            self.framenum = next(self.gen)
            self.counter = 0
        self.counter += 1
        self.move()
        self.collide_world()

    def move(self):
        pass

    def set_frame(self, pose, num):
        if pose == "idle":
            num = 1
        self.frame = self.atlas["{}{}".format(pose, num)]

    def _num(self):
        while True:
            for i in range(1, 5):
                yield i

    def collide_world(self):
        pass

    def collide_npcs(self, mov):
        if self.name != "Thack":
            collidelist = self.parent.parent.coll_childs(self)
        else:
            collidelist = self.parent.parent.npcs.coll_childs(self)
        if collidelist != []:
            if collidelist[0].name in self.parent.in_world:
                self.collided_with = collidelist[0].name
                self.reverse_movement(mov)

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
    right_pos = ListProperty([0,0])
    left_pos = ListProperty([0,0])
    top_pos = ListProperty([0,0])
    bot_pos = ListProperty([0,0])

    def playersetup(self, screen_size):
        self.screen_size = screen_size
        self.entitysetup("images/player_sheet.atlas")
        self.name = "Thack"
        self.bind(collided_with=lambda x, y: self.parent.parent.begin_conv(y))
        #self.collide_widget.pos = [self.pos[0]+25, self.pos[1]]


    def collide_world(self):
        ws = 500
        window_pos = self.to_window(self.pos[0], self.pos[1])
        if window_pos[0] < ws:
            self.parent.move_world("right")
        if window_pos[0] > self.screen_size[0]-ws:
            self.parent.move_world("left")
        if window_pos[1] < ws:
            self.parent.move_world("down")
        if window_pos[1] > self.screen_size[1]-ws:
            self.parent.move_world("up")
        self.parent.collide_poi(self)

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
                self.collide_widget.pos = Vector(self.collide_widget.pos) + Vector(self.dirs[mov])
                for w in self.parent.cluttergroup.children:
                    if self.collide_widget.collide_widget(w):
                        self.moving[mov] = False
                        self.collide_widget.pos = [self.pos[0]+25, self.pos[1]]
                if self.moving[mov]:
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
        if moving:
            direction = self.parent.collide_walls(self.pos, direction)
            self.pos = Vector(self.pos) + Vector(direction)*3

        # Set Animation Frame.
        self.set_frame(self.current, self.framenum)

    def move_old(self):
        self.current = "idle"
        for mov in self.moving:
            if self.moving[mov]:
            # Movement Code.
                # Collision Code.
                # NPCs
                self.collide_npcs(mov)

                # Walls
                if mov == "right":
                    pos1 = self.right_pos
                elif mov == "left":
                    pos1 = self.left_pos
                elif mov == "up":
                    pos1 = self.top_pos
                elif mov == "down":
                    pos1 = self.bot_pos
                pos2 = self.parent.collide_walls(pos1, self.dirs[mov], mov)
                if pos2 != False:
                    self.pos = Vector(self.pos) + Vector(pos2)
                else:
                    self.last_known_good = self.pos.copy()
                    self.pos = Vector(self.pos) + Vector(self.dirs[mov])*3

                # Clutter
                for w in self.parent.cluttergroup.children:
                    if self.collide_widget.collide_widget(w):
                        self.pos = self.last_known_good
                        break


                # Animation Code.
                if self.moving["right"] or self.moving["left"]:
                    if mov == "up" or mov == "down":
                        pass
                    else:
                        self.current = "walk{}".format(mov)
                else:
                    self.current = "walk{}".format(mov)
        self.set_frame(self.current, self.framenum)

class NPC(Entity):
    def npcsetup(self, atlasfile):
        self.entitysetup(atlasfile)

class NPCController(Widget):
    npcs = DictProperty({"Djonsiscus":{"home":"church main", "place":(1955, 733)},
                         "Jarod":{"home":"church basement", "place":(1955, 733)},
                         "Tylda Travisteene":{"home":"outside", "place":(1955, 733)},
                         "Sheila Travisteene":{"home":"outside", "place":(1955, 733)},
                         "Mr Johes":{"home":"outside", "place":(1955, 733)},
                         "Riff Danner":{"home":"outside", "place":(1955, 733)}})
    npcgroup = ListProperty([])

    def controllersetup(self):
        for name in self.npcs:
            npc = NPC(size=(48,110))
            npc.name = name
            npc.home = self.npcs[name]["home"]
            npc.npcsetup("images/{}.atlas".format(name))
            npc.pos = self.npcs[name]["place"]
            self.npcgroup.append(npc)

    def update(self, dt):
        for npc in self.npcgroup:
            npc.update(dt)

    def coll_childs(self, w):
        return [child for child in self.npcgroup if circle_collide(child, w)]
