
import pygame as pg
import numpy as np
import json
from myfuncs import *
from pygame.locals import *
from load import Template, Tile, SpriteSheet
from path import Path
from gui import Button, Menu, FloatingText
from saveload import SaveMap, LoadMap

TEAL = (0,171,169)
STEEL = (100,118,135)
BROWN = (138,90,44)
CYAN = (27,161,226)
CONCRETE = (149,165,166)
SUNFLOWER = (241,196,15)
WHITE = (255,255,255)
BLACK = (0,0,0)

class Main(Template):
    def __init__(self, size):
        Template.__init__(self, size)
        self.name = "Under Construction"
        self.size = size
        self.block = 64
        self.dt = 0.
        self.empty_tile = pg.image.load("./tiles/Empty_tile_64p.png").convert_alpha()
        self.map1 = Map(self.size, (40,40), self.block, self.empty_tile)
        self.map2 = Map(self.size, (40,40), self.block, self.empty_tile)
        self.menu = Map(self.size, (2,14), self.block, self.empty_tile)
        self.menu_list = []
        self.palette = self.setup_menu()
        self.palette.xy = [250,0]
        self.clip = pg.Rect(0,0, self.size[0],self.size[1])
        self.c_pos = self.clip.topleft
        self.current_tile = None
        self.show_foreground = -1
        self.right_m_button = False
        self.right_m_pos = None
        self.m_pos = None
        self.fill = False
        self.m_select_rect = pg.Rect(1,1,1,1)
        self.button1 = Button((120, 20), (129,1), "Menu")
        self.drop_menu = Menu((120, 160), (129, 21))
        self.drop_menu.add_buttons(4, ["Save", "Load", "Palette", "Info"])
        self.drop_menu.set_bg_color(CONCRETE)
        self.load_menu = self.setup_loadmenu()
        self.floating_text = FloatingText("no text", self.size)
        self.setup()

        self.selected_map = self.map1

    def update(self, dt):
        self.dt = dt
        self.map1.update(dt)
        self.menu.update(dt)
        self.palette.update(dt)
        self.floating_text.update(dt)
        if self.drop_menu.buttons[0].clicked:
            self.savemap()
            self.drop_menu.buttons[0].clicked = False
        if self.drop_menu.buttons[2].clicked:
            self.selected_map = self.palette
        else:
            self.selected_map = self.map1
        if self.map1.clipped:
            self.map2.map.set_clip()
            self.map1.clipped = False
        if self.c_pos != self.clip.topleft:
            self.c_pos = (self.c_pos[0] - self.map1.xy[0], self.c_pos[1] - self.map1.xy[1])
            self.clip.topleft = self.c_pos
        self.button1.update(self.dt)
        self.mouse_select()

    def draw(self):
        self.screen.fill(BLACK)

        # MAP
        # Background
        self.map1.draw(self.screen, self.clip)

        # Foreground
        if self.show_foreground > 0:
            self.map2.xy = self.map1.xy
            self.map2.draw(self.screen, self.clip)

        # GUI
        self.menu.draw(self.screen, None)
        self.button1.draw(self.screen)
        if self.button1.clicked:
            self.drop_menu.draw(self.screen)
        if self.drop_menu.buttons[1].clicked:
            self.load_menu.draw(self.screen)
        if self.drop_menu.buttons[2].clicked:
            self.palette.draw(self.screen)
        if self.right_m_button:
            screen_rect = self.m_select_rect.copy()
            screen_rect.x += self.map1.xy[0]
            screen_rect.y += self.map1.xy[1]
            pg.draw.rect(self.screen, WHITE, screen_rect, 1)

        self.floating_text.draw(self.screen)

########################## Setup methods #######################################

    def setup_loadmenu(self):
        folder = Path("./save")
        filelist = [f.basename() for f in folder.files("*.sav")]
        amount = len(filelist)
        menu = Menu((240, amount*21), (250, 21))
        menu.add_buttons(amount, filelist)
        menu.set_bg_color(CONCRETE)
        return menu

    def setup(self):
        self.map1.setup(TEAL)
        self.map2.setup(CONCRETE, 200)
        self.menu.setup(CYAN)

    def setup_menu(self):
        sheet = SpriteSheet("img/magecity_64p.png", 64, (0,0), (8,44))
        self.menu_list = sum(sheet.image_list, [])
        length = len(self.menu_list)
        size = (10, int(length/10))
        menu = Map(self.size, size, self.block, self.empty_tile)
        menu.setup(CYAN)
        for i, tile in enumerate(menu.group):
            tile.filename = "{}".format(i)
            tile.image = self.menu_list[i]
            if i+1 >= length:
                break
        return menu

#################### Key and Mouse Methods #####################################

    def key_down(self, key):
        if key == K_ESCAPE:
            print("Quitting...")
            self.game_on == False
            self.end_game()

        if key == K_e:
            self.show_foreground *= -1

        if key in (K_w, K_UP):
            self.selected_map.move["up"] = True
        if key in (K_a, K_LEFT):
            self.selected_map.move["left"] = True
        if key in (K_s, K_DOWN):
            self.selected_map.move["down"] = True
        if key in (K_d, K_RIGHT):
            self.selected_map.move["right"] = True

    def key_up(self, key):
        if key in (K_w, K_UP):
            self.selected_map.move["up"] = False
        if key in (K_a, K_LEFT):
            self.selected_map.move["left"] = False
        if key in (K_s, K_DOWN):
            self.selected_map.move["down"] = False
        if key in (K_d, K_RIGHT):
            self.selected_map.move["right"] = False

    def mouse_down(self, button, pos):
        not_menu = True
        if button == 1:
            if self.button1.click(pos):
                not_menu = False
            if self.button1.clicked:
                if self.drop_menu.click(pos):
                    not_menu = False
            if self.drop_menu.buttons[1].clicked:
                if self.load_menu.click(pos):
                    self.loadmap()
            if not_menu:
                if self.drop_menu.buttons[2].clicked:
                    self.find_tile(pos, self.palette, self.menu)
                elif self.show_foreground > 0:
                    self.find_tile(pos, self.menu, self.map2)
                else:
                    self.find_tile(pos, self.menu, self.map1)
        if button == 3:
            self.right_m_button = True
            self.right_m_pos = pos

    def mouse_up(self, button, pos):
        if button == 3:
            self.right_m_button = False
            self.right_m_pos = pos
            new_rect = self._invert_rect(self.m_select_rect)

            if self.show_foreground < 0:
                self.group_select(new_rect, self.map1.group)
            else:
                self.group_select(new_rect, self.map2.group)

    def mouse_motion(self, button, pos, rel):
        self.m_pos = pos

    def mouse_select(self):
        if self.right_m_button:
            old_pos = (self.right_m_pos[0] - self.map1.xy[0], self.right_m_pos[1] - self.map1.xy[1])
            new_pos = (self.m_pos[0] - self.map1.xy[0], self.m_pos[1] - self.map1.xy[1])
            self.m_select_rect = pg.Rect(1,1,1,1)
            xoff, yoff = new_pos[0] - old_pos[0], new_pos[1] - old_pos[1]
            self.m_select_rect.inflate_ip(xoff, yoff)
            self.m_select_rect.topleft = old_pos

    def _invert_rect(self, rect):
            new_rect = pg.Rect(1,1,1,1)
            new_rect.size = rect.size
            if rect.width < 0:
                new_rect.width *= -1
            if rect.height < 0:
                new_rect.height *= -1
            if rect.left > rect.right:
                new_rect.left = rect.right
            else:
                new_rect.left = rect.left
            if rect.top > rect.bottom:
                new_rect.top = rect.bottom
            else:
                new_rect.top = rect.top
            return new_rect

###################### Button Activated Methods ################################

    def group_select(self, rect, group):
        for sprite in group:
            if sprite.rect.colliderect(rect):
                self.change_tile(sprite)

    def find_tile(self, pos, menu, bg_map):
        found = False
        for tile in menu.group:
            map_pos = (pos[0] - menu.xy[0], pos[1] - menu.xy[1])
            if tile.rect.collidepoint(map_pos):
                found = True
                menu.fill = True
                menu.selected = tile
                self.current_tile = tile
        if not found:
            for tile in bg_map.group:
                map_pos = (pos[0] - bg_map.xy[0], pos[1] - bg_map.xy[1])
                if tile.rect.collidepoint(map_pos):
                    self.change_tile(tile)
                    bg_map.clear_map()

    def change_tile(self, tile):
        if self.current_tile != None:
            tile.filename = self.current_tile.filename
            tile.image = self.current_tile.image
            tile.dirty = 1

    def savemap(self):
        data = {
        "Name":self.name,
        "Background":self.map1,
        "Foreground":self.map2,
        "Menu":self.menu
        }
        save = SaveMap(data)
        save.write_to_file("./save/savefile.sav")

    def loadmap(self):
        loadmap = LoadMap()
        data = loadmap.load_from_file("./save/savefile.sav", self.menu_list)
        self.name = data["Name"]
        self.map1 = data["Background"]
        self.map2 = data["Foreground"]
        self.menu = data["Menu"]
        print("map loaded")


    def old_savemap(self):
        size = tuple_mult((40,40), self.block)
        save = SaveMap("savemap", size, self.block, "img/magecity_64p.png",
                        self.map1.group, self.map2.group)
        save.write_to_file()
        self.floating_text.set_text("Map Saved", True)

    def old_loadmap(self):
        select = None
        for button in self.load_menu.buttons:
            if button.clicked:
                select = button.text
        if select != None:
            load = LoadMap(select)
            self.map1.group = load.bg_group
            self.map2.group = load.fg_group
            self.floating_text.set_text("Map Loaded", True)


class Map(object):
    def __init__(self, screen_size, grid, block, image):
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
        self.speed = 1
        self.dt = 0.
        self.once = False
        self.clipped = False
        self.selected = None
        self.sel_old = None
        self.saved_surf = None

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
                tile = Tile(None, xy=(x*self.block, y*self.block))
                tile.image = self.image
                tile.filename = self.image_string
                tile.rect = tile.image.get_rect()
                tile.rect.topleft = tile.xy
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

    def update(self, dt):
        self.dt = dt
        self.move_map()
        if self.selected != self.sel_old:
            if self.sel_old != None:
                self.clear_map()
            self.sel_old = self.selected

    def draw(self, surf, clip=None):
        self.group.draw(self.map)
        if self.selected != None:
            myrect = self.selected.rect.copy()
            myrect.inflate_ip(-1, -1)
            pg.draw.rect(self.map, SUNFLOWER, myrect, 2)

        if clip != None:
            self.map.set_clip(clip)

        surf.blit(self.map, self.xy)

if __name__ == "__main__":
    print("Starting")
    set_dir(__file__)
    s = Main((800,640))
    s.mainloop()
