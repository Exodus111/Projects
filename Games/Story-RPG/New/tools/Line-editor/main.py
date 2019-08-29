import pygame as pg
from pygame.locals import *
import json

from load import Template, Tile
from gui import Menu

BLACK = (0,0,0)
WHITE = (255,255,255)
MAP = "main"

class Main(Template):
    def __init__(self, size):
        Template.__init__(self, size)
        self.size = size
        self.xy = [0,0]
        self.clip = pg.Rect(0,0, self.size[0],self.size[1])
        self.move = {"up":False,"down":False,"right":False,"left":False}
        self.filenames = {
            "main":{"bg":"CI Main Back","obj":"CI Main Obj", "size":(768,608)},
            "basement":{"bg":"CI Basement Back","obj":"CI Basement Obj", "size":(640,416)},
            "thack_room":{"bg":"CI Player Room Back","obj":"CI Player Room Obj", "size":(192,256)},
            "priest_room":{"bg":"CI Priest Room Back","obj":"CI Priest Room Obj", "size":(192,256)},
            "tower":{"bg":"CI Tower Top Back","obj":"CI Tower Top Obj", "size":(192,256)}
        }
        self.current_map = MAP
        self.growth = 3
        self.surface = pg.Surface((self.size[0]*4, self.size[1]*4))
        self.pointlist = []
        self.linelist = []
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
        self.create_menu()

    def create_menu(self):
        size = (self.size[0]/8, self.size[1]/8)
        xy = (0,0)
        self.menu = Menu(size, xy)
        textlist = ["Save Lines", "Save Rects"]
        self.menu.add_buttons(2, textlist)

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
        w *= self.growth
        h *= self.growth
        return pg.transform.smoothscale(surf, (w, h))

    def draw_points(self, pos):
        pos = (pos[0]-self.xy[0], pos[1]-self.xy[1])
        rect = pg.draw.circle(self.surface, WHITE, pos, 2)
        if self.pointlist != []:
            rect = self._enforce_straight_lines(pos, rect)
            rect = self.check_for_end(rect)
        if rect != None:
            self.pointlist.append(rect)


    def check_for_end(self, rect):
        a = (rect.x, rect.y)
        b = (self.pointlist[0].x, self.pointlist[0].y)
        if abs(a[0] - b[0]) < 15 and abs(a[1] - b[1]) < 15:
            c = (self.pointlist[-1].x, self.pointlist[-1].y)
            if abs(b[0] - c[0]) > abs(b[1] - c[1]):
                self.pointlist[-1].y = b[1]
            else:
                self.pointlist[-1].x = b[0]
            self.linelist.append(self.pointlist.copy())
            self.pointlist = []
            return None
        else:
            return rect

    def _enforce_straight_lines(self, pos, rect=None):
        if rect == None:
            rect = pg.draw.circle(self.surface, WHITE, pos, 2)
        op = self.pointlist[-1]
        op = (op.x, op.y)
        a = pos[0] - op[0]
        b = pos[1] - op[1]
        if a > 0 and b > 0 or a < 0 and b < 0:
            diff = a - b
        else:
            diff = a + b
        if abs(diff) < 50:
            if a < 0:
                rect.x = op[0] - (abs(a) + abs(b))/2
            else:
                rect.x = op[0] + (abs(a) + abs(b))/2
            if b < 0:
                rect.y = op[1] - (abs(a) + abs(b))/2
            else:
                rect.y = op[1] + (abs(a) + abs(b))/2
        elif abs(a) > abs(b):
            rect.y = op[1]
        else:
            rect.x = op[0]
        return rect

    def save_lines(self):
        print("Saving Lines to ", "./saves/{}_wall.json".format(self.current_map))
        mydict = {}
        list_of_lines = [(point.x, self.flip_y(point.y)) for point in self.linelist[0]]
        list_of_lines.append(list_of_lines[0])
        mydict[self.current_map] = list_of_lines
        mydict["size"] = self.filenames[self.current_map]["size"]
        mydict["growth"] = self.growth
        with open("./saves/{}_wall.json".format(self.current_map), "w+") as f:
            json.dump(mydict, f, indent=4, sort_keys=True)

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

    def erase_rects(self, arg):
        if arg == "last":
            self.rect_list.pop()
        elif arg == "all":
            self.rect_list = []

    def save_rects(self):
        print("Saving rects to ", "./saves/{}_clutter.json".format(self.current_map))
        rects = {self.current_map:{}}
        for num, rect in enumerate(self.rect_list):
            rects[self.current_map]["rect{}".format(num)] = [rect.x, self.flip_y(rect.y), rect.w, rect.h]
        with open("./saves/{}_clutter.json".format(self.current_map), "w+") as f:
            json.dump(rects, f, indent=4, sort_keys=True)

    def flip_y(self, y):
        print("y is: ", y)
        h = self.filenames[self.current_map]["size"][1]
        print("h is: ", h)
        return (h*self.growth) - y

    def update(self, dt):
        if self.move["up"]:
            self.xy[1] += 15
        if self.move["down"]:
            self.xy[1] -= 15
        if self.move["left"]:
            self.xy[0] += 15
        if self.move["right"]:
            self.xy[0] -= 15

    def draw(self):
        #self.screen.fill(BLACK)
        # Background.
        self.surface.blit(self.bg, (0,0))

        # Drawing Rects
        if self.new_rect != None:
            pg.draw.rect(self.surface, WHITE, self.new_rect, 1)
        for rect in self.rect_list:
            pg.draw.rect(self.surface, WHITE, rect, 1)

        # Drawing lines
        if len(self.pointlist) > 1:
            p_list = self.pointlist.copy()
            p_list.append(self.mousepoint)
            pg.draw.lines(self.surface, WHITE, False, [(point.x, point.y) for point in p_list])

        for lines in self.linelist:
            pg.draw.lines(self.surface, WHITE, True, [(point.x, point.y) for point in lines])

        # Blitting to Screen.
        self.screen.blit(self.surface, self.xy)

        # Drawing the menu
        self.menu.draw(self.screen)

    def key_down(self, key):
        if key == K_ESCAPE:
            self.game_on = False
        if key == K_SPACE:
            pass
        if key in (K_UP, K_w):
            self.move["up"] = True
        if key in (K_DOWN, K_s):
            self.move["down"] = True
        if key in (K_RIGHT, K_d):
            self.move["right"] = True
        if key in (K_LEFT, K_a):
            self.move["left"] = True
        if key == K_BACKSPACE:
            self.erase_rects("last")
        if key == K_RETURN:
            self.erase_rects("all")


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
            if self.menu.click(pos):
                if self.menu.clickinfo == "Save Lines":
                    self.save_lines()
                elif self.menu.clickinfo == "Save Rects":
                    self.save_rects()
            else:
                self.draw_points(pos)
        elif button == 3:
            self.start_rect(pos)

    def mouse_up(self, button, pos):
        if button == 3:
            self.finish_rect(pos)

    def mouse_motion(self, button, pos, rel):
        if self.rect_started:
            self.expand_rect(pos)
        elif self.pointlist != []:
            pos = (pos[0]-self.xy[0], pos[1]-self.xy[1])
            rect = self._enforce_straight_lines(pos)
            self.mousepoint = rect

if __name__ == "__main__":
    s = Main((1024,960))
    s.mainloop()
