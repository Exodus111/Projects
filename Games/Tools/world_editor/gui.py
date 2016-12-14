import pygame as pg
from collections import OrderedDict
from myfuncs import *

STEEL = (100,118,135)
CONCRETE = (149,165,166)
SUNFLOWER = (241,196,15)
BLACK = (0,0,0)

class Border():
    def __init__(self, size, xy):
        self.size = size
        self.xy = xy
        self.bg_color = BLACK
        self.mn_color = CONCRETE
        self.fg_color = BLACK
        self.border = [{
            "rect": pg.Rect((0,0), self.size),
            "color": (0,0,0)},
                {
            "rect": pg.Rect((0,0), self.size).inflate(-3, -3),
            "color": CONCRETE},
                {
            "rect": pg.Rect((0,0), self.size).inflate(-8, -8),
            "color": (0,0,0)}]

    def draw(self, surf):
        for b in self.border:
            pg.draw.rect(surf, b["color"], b["rect"])

class Panel():
    def __init__(self, size, xy, color=STEEL):
        self.size = size
        self.xy = xy
        self.color = color
        self.display = False
        self.surf = pg.Surface(size)
        self.border = Border(self.size, self.xy)
        self.rect = pg.Rect((0,0), size).inflate(-10, -10)
        self.menus = []
        self.text = []
        self.text_xy = []
        self.setup()

    def setup(self):
        gap = self.size[0]/60
        w, h = (self.size[0]/8, self.size[1]/18)
        x, y = (self.size[0] - w - gap, self.size[1] - h - gap)
        self.add_menu((w,h), (x,y))
        self.menus[0].add_buttons(1, ["OK"])

    def setup_text(self, text_list):
        for num, t in enumerate(text_list):
            font_obj = pg.font.SysFont("arial", 14)
            size_of_text = font_obj.size(t)
            if len(self.text_xy) >= 1:
                for coord in self.text_xy:
                    coord[1] -= (size_of_text[1] +5)
            self.text_xy.append([(self.size[0]/2)-(size_of_text[0]/2), (self.size[1]/2)-(size_of_text[1]/2)])
            self.text.append(font_obj.render(t, True, SUNFLOWER))

    def display_panel(self):
        self.display = (lambda x: False if x else True)(self.display)

    def add_menu(self, size, xy):
        self.menus.append(Menu(size, xy))

    def click(self, pos):
        new_pos = (pos[0] - self.xy[0], pos[1] - self.xy[1])
        if self.menus[0].click(new_pos):
            self.display_panel()

    def draw(self, screen):
        if self.display:
            self.border.draw(self.surf)
            pg.draw.rect(self.surf, self.color, self.rect)
            for menu in self.menus:
                menu.draw(self.surf)
            for num, t in enumerate(self.text):
                self.surf.blit(t, self.text_xy[num])
            screen.blit(self.surf, self.xy)


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

class FloatingText():
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
        self.xy = (self.xy[0], int(self.xy[1]/2))
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
