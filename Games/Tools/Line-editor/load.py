import os, sys, pygame
from pygame.locals import *


class Template(object):
    def __init__(self, size=(640, 480)):
        self.size = size
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()
        pygame.mouse.set_visible(True)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.size)
        self.game_on = True
        self.dt = 0.

    def mainloop(self, fps=0):
        while self.game_on:
            pygame.display.set_caption("FPS: {}".format(int(self.clock.get_fps())))
            self.clock.tick(fps)
            self.dt += float(self.clock.get_rawtime())/1000
            self.events()
            self.update(self.dt)
            self.draw()
            pygame.display.flip()
        self.end_game()

    def events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.game_on = False
            elif event.type == KEYDOWN:
                self.key_down(event.key)
            elif event.type == KEYUP:
                self.key_up(event.key)
            elif event.type == MOUSEBUTTONDOWN:
                self.mouse_down(event.button, event.pos)
            elif event.type == MOUSEBUTTONUP:
                self.mouse_up(event.button, event.pos)
            elif event.type == MOUSEMOTION:
                self.mouse_motion(event.buttons, event.pos, event.rel)

    def update(self, dt):
        pass

    def draw(self):
        pass

    def key_down(self, key):
        pass

    def key_up(self, key):
        pass

    def mouse_down(self, button, pos):
        pass

    def mouse_up(self, button, pos):
        pass

    def mouse_motion(self, button, pos, rel):
        pass

    def end_game(self):
        pygame.quit()
        print("Thank you for playing.")
        print("Time played: {}".format(self.dt))

class Tile(pygame.sprite.DirtySprite):
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.dirty = 1
