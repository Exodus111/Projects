#!/usr/bin/python3
import pygame as pg
from pygame.locals import *

BUTTON_COLOR = (255, 255, 255)
BLACK = (0,0,0)

class Menu():
    """Gui object, self reliant menu object."""
    def __init__(self, size, xy):
        self.size = size
        self.xy = xy
        self.surf = pg.Surface(size)
        self.rect = pg.Rect(xy, size)
        self.buttons = []
        self.clickinfo = None

    def change_size(self, size):
        self.size = size
        self.surf = pg.Surface(size)
        self.rect = pg.Rect(self.xy, size)

    def add_buttons(self, amount, text_list):
        if amount > 0:
            adj = len(self.buttons)
            sizex = self.size[0]
            sizey = self.size[1]/(amount + adj)
            for b in range(amount):
                b = Button((sizex, sizey),(0, sizey*(b + adj)), text_list[b])
                self.buttons.append(b)

    def click(self, pos):
        if self.rect.collidepoint(pos):
            point = (pos[0] - self.xy[0], pos[1] - self.xy[1])
            for button in self.buttons:
                if button.click(point):
                    self.clickinfo = button.text
                    break
            return True
        else:
            return False

    def set_bg_color(self, color):
        for button in self.buttons:
            button.color["BG"] = color

    def draw(self, screen):
        for button in self.buttons:
            button.draw(self.surf)
        screen.blit(self.surf, self.xy)

class Button():
    def __init__(self, size, xy, text):
        pg.font.init()
        self.xy = xy
        self.size = size
        self.surf = pg.Surface(size)
        self.rect = pg.Rect((0,0), size)
        self.collide_rect = pg.Rect(xy, size)
        self.color = {"BG":BUTTON_COLOR,"FG":BLACK}
        self.font = pg.font.SysFont("arial", 14)
        self.text = text

        size_of_text = self.font.size(text)
        self.text_xy = ((self.size[0]/2)-(size_of_text[0]/2), (self.size[1]/2)-(size_of_text[1]/2))
        self.active = False
        self.ren_text = self.font.render(self.text, True, self.color["FG"])
        self.once = 0

    def click(self, point):
        if self.collide_rect.collidepoint(point):
            self.active = not self.active
            return True
        else:
            return False

    def update(self, dt):
        pass

    def draw(self, screen):
        pg.draw.rect(self.surf, self.color["BG"], self.rect)
        pg.draw.rect(self.surf, self.color["FG"], self.rect, 1)
        self.surf.blit(self.ren_text, self.text_xy)
        screen.blit(self.surf, self.xy)
