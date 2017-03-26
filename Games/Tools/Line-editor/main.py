import pygame as pg
from pygame.locals import *
import json

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
        self.surface = pg.Surface((self.size[0]*2, self.size[1]*2))
        self.pointlist = []
        self.groups = {}
        for key in self.filenames:
            back = self.create_map(key, "bg")
            obj = self.create_map(key, "obj")
            self.groups[key] = []
            self.groups[key].append(back)
            self.groups[key].append(obj)
        self.bg = self.add_map()
        self.rect_started = False
        self.new_rect = None
        self.rect_list = []

    def create_map(self, key, name):
        layer = self.filenames[key][name]
        filename = "./images/" + layer +".png"
        img = pg.image.load(filename).convert_alpha()
        tile = Tile(img)
        tile.name = layer
        tile.filename = filename
        return tile

    def add_map(self):
        surf = pg.Surface(self.size)
        for t in self.groups[self.current_map]:
            surf.blit(t.image, t.rect)
        w, h = surf.get_size()
        w *= 2
        h *= 2
        return pg.transform.smoothscale(surf, (w, h))

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
        self.save_lines()
        self.pointlist = []

    def save_lines(self):
        walls = {self.current_map:[(point.x, point.y) for point in self.pointlist]}
        with open("./saves/{}_wall.json".format(self.current_map), "w+") as f:
            json.dump(walls, f, indent=4, sort_keys=True)

    def start_rect(self, pos):
        self.rect_started = True
        self.new_rect = pg.Rect(pos[0]-self.xy[0], pos[1]-self.xy[1], 2, 2)

    def expand_rect(self, pos):
        x,y = self.new_rect.topleft
        pos = (pos[0]-self.xy[0], pos[1]-self.xy[1])
        w,h = (abs(x - pos[0]), abs(y - pos[1]))
        self.new_rect.w = w
        self.new_rect.h = h

    def finish_rect(self, pos):
        self.rect_list.append(self.new_rect)
        self.new_rect = None
        self.rect_started = False

    def save_rects(self):
        rects = {self.current_map:{}}
        for num, rect in enumerate(self.rect_list):
            rects[self.current_map]["rect{}".format(num)] = [rect.x, rect.y, rect.w, rect.h]
        with open("./saves/{}_clutter.json".format(self.current_map), "w+") as f:
            json.dump(rects, f, indent=4, sort_keys=True)



    def update(self, dt):
        if self.move["up"]:
            self.xy[1] += 5
        if self.move["down"]:
            self.xy[1] -= 5
        if self.move["left"]:
            self.xy[0] += 5
        if self.move["right"]:
            self.xy[0] -= 5

    def draw(self):
        #self.screen.fill(BLACK)
        # Background.
        self.surface.blit(self.bg, (0,0))

        # Drawing Rects
        if self.new_rect != None:
            pg.draw.rect(self.surface, WHITE, self.new_rect, 1)
        for rect in self.rect_list:
            pg.draw.rect(self.surface, WHITE, rect, 1)

        # Blitting to Screen.
        self.screen.blit(self.surface, self.xy)

    def key_down(self, key):
        if key == K_ESCAPE:
            self.game_on = False
        if key == K_SPACE:
            self.save_rects()
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
        elif button == 3:
            self.start_rect(pos)

    def mouse_up(self, button, pos):
        if button == 3:
            self.finish_rect(pos)

    def mouse_motion(self, button, pos, rel):
        if self.rect_started:
            self.expand_rect(pos)


if __name__ == "__main__":
    s = Main((1024,960))
    s.mainloop()
