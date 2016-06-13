import pygame as pg
from myfuncs import *

class Button(object):
    def __init__(self, size, xy, text):
        pg.font.init()
        self.xy = xy
        self.size = size
        self.surf = pg.Surface(size)
        self.rect = pg.Rect((0,0), size)
        self.collide_rect = pg.Rect(xy, size)
        self.color = {"BG":(255,255,255),"FG":(0,0,0)}
        self.font = pg.font.SysFont("arial", 14)
        self.text = text

        size_of_text = self.font.size(text)
        self.text_xy = ((self.size[0]/2)-(size_of_text[0]/2), (self.size[1]/2)-(size_of_text[1]/2))
        self.clicked = False
        self.ren_text = self.font.render(self.text, True, self.color["FG"])

        self.once = 0


    def click(self, point):
        if self.collide_rect.collidepoint(point):
            self.clicked = (lambda x: False if x else True)(self.clicked)
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

class Menu(object):
    """Gui object, self reliant menu object."""
    def __init__(self, size, xy):
        self.size = size
        self.xy = xy
        self.surf = pg.Surface(size)
        self.rect = pg.Rect(xy, size)
        self.buttons = []

    def add_buttons(self, amount, text_list):
        if amount > 0:
            sizex = self.size[0]/amount
            sizey = self.size[1]/amount
            for b in xrange(amount):
                b = Button((self.size[0], sizey),(0, sizey*b), text_list[b])
                self.buttons.append(b)

    def click(self, pos):
        if self.rect.collidepoint(pos):
            point = (pos[0] - self.xy[0], pos[1] - self.xy[1])
            for button in self.buttons:
                if button.click(point):
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

class FloatingText(object):
    def __init__(self, text, size):
        self.size = size
        self.font = pg.font.SysFont("arial", 72)
        self.alpha = 255
        self.set_text(text)

    def set_text(self, text, write=False):
        self.text = self.font.render(text, True, (255,255,255))
        text_size = self.font.size(text)
        self.surf = pg.Surface(text_size)
        pixel = self.surf.get_at((1,1))
        self.surf.set_colorkey(pixel)
        text_size = tuple_div(text_size, 2)
        self.xy = tuple_div(self.size, 2)
        self.xy = tuple_sub(self.xy, text_size)
        self.xy = (lambda (x,y): (x, y/2))(self.xy)
        self.write = write

    def update(self, dt):
        if self.write:
            if mytimer("floating text", 4, dt, False):
                self.write = False
                self.alpha = 255
                remove_timer("floating text")
            if mytimer("alpha timer", .08, dt):
                self.alpha -= 5

    def draw(self, surf):
        if self.write:
            self.surf.blit(self.text, (0,0))
            self.surf.set_alpha(self.alpha)
            surf.blit(self.surf, self.xy)
