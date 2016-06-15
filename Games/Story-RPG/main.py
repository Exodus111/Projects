import sys
from random import randint as ri
import pygame as pg
from pygame.locals import *

from load.load import Template, Tile

if sys.version_info < (3, 0):
    range = xrange

class Main(Template):
    def __init__(self, size):
        Template.__init__(self, size)
        self.size = size
        self.background = []
        self.create_background()

    def create_background(self):
        sizex = int(self.size[0]/32)
        sizey = int(self.size[1]/32)
        for x in range(sizex):
            for y in range(sizey):
                tile = Tile()
                tile.rect = pg.Rect(x*32+1, y*32+1, 32, 32)
                tile.color = (255,255,255)
                self.background.append(tile)

    def update(self, dt):
        pass

    def draw(self):
        # Background
        for tile in self.background:
            pg.draw.rect(self.screen, tile.color, tile.rect, 1)

        # Characters

        # GUI

        # Mouse pointer
        pass


    def key_down(self, key):
        if key == K_ESCAPE:
            self.game_on = False


    def key_up(self, key):
        pass

    def mouse_down(self, button, pos):
        pass

    def mouse_up(self, button, pos):
        pass

    def mouse_motion(self, button, pos, rel):
        pass

if __name__ == "__main__":
    s = Main((800, 600))
    s.mainloop()
