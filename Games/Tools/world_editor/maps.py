#!/usr/bin/python3

import pygame as pg
from load import Tile
from myfuncs import *

SUNFLOWER = (241,196,15)

class Map(object):
    def __init__(self, name, screen_size, grid, block, image):
        self.name = name
        self.screen_size = screen_size
        self.grid = grid
        self.block = block
        self.image = image
        self.image_string = "Empty_tile"
        self.size = (self.grid[0]*self.block, self.grid[1]*self.block)
        self.rect = pg.Rect(0,0,screen_size[0]/2, screen_size[1]/2)
        self.map = pg.Surface(self.size)
        self.alpha = 150
        self.xy = [0,0]
        self.move = {"up":False,"left":False,"down":False,"right":False}
        self.speed = 1
        self.dt = 0.
        self.once = False
        self.clipped = False
        self.selected = None
        self.sel_old = None
        self.saved_surf = None

    def setup(self, color, alpha=255):
        self.alpha = alpha
        self.color = color
        self.map.fill(color)
        self.group = self.make_grid()
        self.map.set_alpha(self.alpha)

    def make_grid(self):
        group = pg.sprite.LayeredDirty()
        for y in range(self.grid[1]):
            for x in range(self.grid[0]):
                tile = Tile(self.image, self.image_string, xy=(x*self.block, y*self.block))
                tile.dirty = 1
                group.add(tile)
        return group

    def move_map(self):
        if self.move["up"]:
            if not self.xy[1] > self.screen_size[1] - (self.screen_size[1]*0.2):
                self.xy[1] += self.speed
        if self.move["left"]:
            if not self.xy[0] > self.screen_size[0] - (self.screen_size[0]*.2):
                self.xy[0] += self.speed
        if self.move["down"]:
            if not self.xy[1]+(self.size[1]-(self.block*4)) < 0:
                self.xy[1] -= self.speed
        if self.move["right"]:
            if not self.xy[0]+(self.size[0]-(self.block*4)) < 0:
                self.xy[0] -= self.speed
        if True in self.move.values():
            self.once = True
            if mytimer("map_speed", .05, self.dt):
                if self.speed < 100:
                    self.speed *= 1.8
        else:
            self.speed = 1
            if self.once:
                self.clipped = True
                self.map.set_clip()

    def clear_map(self):
        self.map.fill(self.color)
        for tile in self.group:
            tile.dirty = 1

    def update(self, dt):
        self.dt = dt
        self.move_map()
        if self.selected != self.sel_old:
            if self.sel_old != None:
                self.clear_map()
            self.sel_old = self.selected

    def draw(self, surf, clip=None):
        self.group.draw(self.map)
        if self.selected != None:
            myrect = self.selected.rect.copy()
            myrect.inflate_ip(-1, -1)
            pg.draw.rect(self.map, SUNFLOWER, myrect, 2)
        if clip != None:
            self.map.set_clip(clip)
        surf.blit(self.map, self.xy)

if __name__ == "__main__":
    pass
