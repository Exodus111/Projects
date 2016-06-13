import random, pygame
from pygame.locals import *

from load import Template, Tile

class Main(Template):
    def __init__(self, size):
        Template.__init__(self, size)
        self.size = size

    def update(self, dt):
        pass

    def draw(self):
        # Background

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
