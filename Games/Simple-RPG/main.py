import random, os
import pygame as pg
from pygame.locals import *
from myfuncs import *
from saveload import LoadMap
from load import Template, Tile, Room
from entity import Player, Npc

class Main(Template):
    def __init__(self, size):
        Template.__init__(self, size)
        check_dir("saveload.py")
        self.size = size
        self.background = pg.Surface((40*64, 40*64))
        self.bgpos = (0,0)
        #self.floors, self.walls = self.make_level(32)
        self.walls = pg.sprite.LayeredDirty()
        self.world = self.make_world()
        self.clip = pg.Rect(0,0,size[0],size[1])
        self.player = Player(self.size, self.walls, tuple_div(size, 2))
        self.characters = pg.sprite.LayeredDirty()
        self.characters.add(self.player)
        self.mob = Npc(self.size, 1)
        self.characters.add(self.mob)

    def make_world(self):
        load = LoadMap(os.path.join("save", "savemap1.sav"))
        return load.bg_group


    def move_world(self):
        playercenter = tuple_sub(self.player.rect.center, self.bgpos)
        screencenter = tuple_div(self.size, 2)
        difference = tuple_sub(playercenter, screencenter)
        if difference != 0:
            coords = tuple_sub(playercenter, self.player.rect.center)
            self.bgpos = tuple_sub(coords, difference)
            self.clip.center = self.player.rect.center

    def make_level(self, block):
        bsize = (int(round(self.size[0] / block)), int(round(self.size[1] / block)))
        wall = "./img/wall1_medium.png"
        floor = "./img/floor1_medium.png"
        room = Room(bsize, wall, floor, block)
        room.make_door("north")
        return room.floors_group, room.walls_group

    def update(self, dt):
        self.characters.update(dt)
        self.mob.follow(self.player.pos)
        self.move_world()

    def draw(self):
        self.screen.fill((0,0,0))
        # Background
        #self.floors.draw(self.background)
        #self.walls.draw(self.background)
        self.world.set_clip(self.clip)
        self.world.draw(self.background)

        # Characters
        self.characters.draw(self.background)
        self.screen.blit(self.background, self.bgpos)
        # pg.draw.rect(self.screen, (255, 255, 255), self.player.rect, 1)

        # GUI

        # Mouse pointer

    def key_down(self, key):
        # Escape to quit
        if key == K_ESCAPE:
            self.game_on = False

        # wasd and arrows to move
        if key in (K_w, K_UP): # Up
            self.player.direction["up"] = True
        if key in (K_a, K_LEFT): # Left
            self.player.direction["left"] = True
        if key in (K_s, K_DOWN): # Down
            self.player.direction["down"] = True
        if key in (K_d, K_RIGHT): # Right
            self.player.direction["right"] = True

        # Shift key to run.
        if key == K_LSHIFT:
            self.player.l_shift(True)

    def key_up(self, key):
        if key in (K_w, K_UP): # Up
            self.player.direction["up"] = False
        if key in (K_a, K_LEFT): # Left
            self.player.direction["left"] = False
        if key in (K_s, K_DOWN): # Down
            self.player.direction["down"] = False
        if key in (K_d, K_RIGHT): # Right
            self.player.direction["right"] = False

        if key == K_LSHIFT:
            self.player.l_shift(False)


    def mouse_down(self, button, pos):
        pass

    def mouse_up(self, button, pos):
        pass

    def mouse_motion(self, button, pos, rel):
        pass

if __name__ == "__main__":
    s = Main((1024, 960))
    s.mainloop()
