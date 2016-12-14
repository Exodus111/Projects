#!/usr/bin/python3

import pygame as pg
from load import Tile
from myfuncs import *

SUNFLOWER = (241,196,15)

class Map(object):
    def __init__(self, name, parent, screen_size, grid, block, image):
        self.name = name
        self.parent = parent
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
        self.clear_select = False
        self.speed = 1
        self.dt = 0.
        self.once = False
        self.do_once = False
        self.clipped = False
        self.sel_old = None
        self.sel_rect = None
        self.saved_surf = None
        self.draw_border = False
        self.remove_border = False

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

    def select_rect(self, rect):
        self.sel_rect = rect
        if self.sel_old == None:
            self.sel_old = self.sel_rect
        self.do_once = True

    def update(self, dt):
        self.dt = dt
        self.move_map()
        if self.sel_rect != None:
            if self.sel_old != self.sel_rect:
                self.clear_select = True
                self.sel_old = self.sel_rect
        if self.parent.current_menu != self.name and self.do_once:
            self.draw_border = False
            self.clear_select = True
            self.do_once = False
        if self.clear_select:
            self.clear_map()
            self.clear_select = False

    def draw(self, surf, clip=None):
        self.group.draw(self.map)
        if self.draw_border:
            pg.draw.rect(self.map, SUNFLOWER, self.sel_rect, 2)
        if clip != None:
            self.map.set_clip(clip)
        surf.blit(self.map, self.xy)

if __name__ == "__main__":
    pass
