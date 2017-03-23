import pygame as pg
from pygame.locals import *
from path import Path

from load import Template, Tile

BLACK = (0,0,0)
WHITE = (255,255,255)

class Main(Template):
    def __init__(self, size):
        Template.__init__(self, size)
        self.size = size
        self.xy = [0,0]
        self.clip = pg.Rect(0,0, self.size[0],self.size[1])
        self.move = {"up":False,"down":False,"right":False,"left":False}
        self.filenames = {
            "Main":{"bg":"CI Main Back","obj":"CI Main Obj"},
            "Basement":{"bg":"CI Basement Back","obj":"CI Basement Obj"},
            "Player Room":{"bg":"CI Player Room Back","obj":"CI Player Room Obj"},
            "Priest Room":{"bg":"CI Priest Room Back","obj":"CI Priest Room Obj"},
            "Tower":{"bg":"CI Tower Top Back","obj":"CI Tower Top Obj"}
        }
        self.current_map = "Main"
        self.surface = pg.Surface(self.size)
        self.pointlist = []
        self.groups = {}
        for key in self.filenames:
            bg_name = self.filenames[key]["bg"]
            bg_filename = "./images/" + bg_name +".png"
            obj_name = self.filenames[key]["obj"]
            obj_filename = "./images/" + obj_name +".png"
            backimg = pg.image.load(bg_filename).convert_alpha()
            objimg = pg.image.load(obj_filename).convert_alpha()
            back = Tile(backimg)
            obj = Tile(objimg)
            back.name = bg_name
            obj.name =  obj_name
            back.filename = bg_filename
            obj.filename = obj_filename
            self.groups[key] = []
            self.groups[key].append(back)
            self.groups[key].append(obj)
        self.add_map(self.current_map)

    def add_map(self, level):
        for t in self.groups[level]:
            self.surface.blit(t.image, t.rect)
        w, h = self.surface.get_size()
        w *= 2
        h *= 2
        self.surface = pg.transform.smoothscale(self.surface, (w, h))

    def draw_points(self, pos):
        pos = (pos[0]-self.xy[0], pos[1]-self.xy[1])
        rect = pg.draw.circle(self.surface, WHITE, pos, 2)
        if self.pointlist != []:
            for p in self.pointlist:
                xdiff = p.x - rect.x
                ydiff = p.y - rect.y
                if abs(xdiff) < 10 and abs(ydiff) < 10:
                    rect = p
                    if len(self.pointlist) > 1:
                        self.draw_lines()
                    return
        self.pointlist.append(rect)

    def draw_lines(self):
        pg.draw.lines(self.surface, WHITE, True, [(point.x, point.y) for point in self.pointlist])
        self.pointlist = []


    def update(self, dt):
        if self.move["up"]:
            self.xy[1] += 3
        if self.move["down"]:
            self.xy[1] -= 3
        if self.move["left"]:
            self.xy[0] += 3
        if self.move["right"]:
            self.xy[0] -= 3

    def draw(self):
        self.screen.fill(BLACK)
        # Background
        self.screen.blit(self.surface, self.xy)

    def key_down(self, key):
        if key == K_ESCAPE:
            self.game_on = False
        if key in (K_UP, K_w):
            self.move["up"] = True
        if key in (K_DOWN, K_s):
            self.move["down"] = True
        if key in (K_RIGHT, K_d):
            self.move["right"] = True
        if key in (K_LEFT, K_a):
            self.move["left"] = True

    def key_up(self, key):
        if key in (K_UP, K_w):
            self.move["up"] = False
        if key in (K_DOWN, K_s):
            self.move["down"] = False
        if key in (K_RIGHT, K_d):
            self.move["right"] = False
        if key in (K_LEFT, K_a):
            self.move["left"] = False

    def mouse_down(self, button, pos):
        if button == 1:
            self.draw_points(pos)

    def mouse_up(self, button, pos):
        pass

    def mouse_motion(self, button, pos, rel):
        pass

if __name__ == "__main__":
    s = Main((1024,960))
    s.mainloop()
