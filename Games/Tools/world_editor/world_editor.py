#!/usr/bin/python3

import pygame as pg
import json
from myfuncs import *
from pygame.locals import *
from load import Template, Tile, SpriteSheet
from path import Path
from gui import Button, Menu, FloatingText, Panel
from saveload import SaveMap, LoadMap
from maps import Map

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
        self.map1 = Map("Background", self.size, (40,40), self.block, self.empty_tile)
        self.map2 = Map("Foreground", self.size, (40,40), self.block, self.empty_tile)
        self.poi_map = Map("POI Map", self.size, (40,40), self.block, self.empty_tile)
        self.poi_menu = Map("POI Menu", self.size, (3,1), self.block, self.empty_tile)
        self.menus = [Map("Menu", self.size, (2,14), self.block, self.empty_tile)]
        self.menu = self.menus[0]
        self.menu.xy[1] += 20
        self.men_list = []
        self.palette = self.setup_palette()
        self.palette.xy = [250,0]
        self.clip = pg.Rect(0,0, self.size[0],self.size[1])
        self.c_pos = self.clip.topleft
        self.show_full_map = False
        self.show_poi = False
        self.full_map = None
        self.current_tile = None
        self.show_foreground = -1
        self.right_m_button = False
        self.right_m_pos = None
        self.m_pos = None
        self.fill = False
        self.m_select_rect = pg.Rect(1,1,1,1)
        self.button1 = Button((120, 20), (129,1), "Menu")
        self.button2 = Button((128,20), (0,0), "Palette")
        self.pal_menu = Menu((128, 40), (0,21))
        self.pal_menu.add_buttons(2, ["New", "Pal-1"])
        self.drop_menu = Menu((120, 160), (129, 21))
        self.drop_menu.add_buttons(5, ["Save", "Load", "Sprites", "See Map", "Info"])
        self.drop_menu.set_bg_color(CONCRETE)
        self.load_menu = self.setup_loadmenu()
        self.floating_text = FloatingText("no text", self.size)
        self.info_panel = Panel((self.size[0] - self.size[0]/3, self.size[1] - self.size[1]/3), (self.size[0]/6, self.size[1]/6))
        self.setup()
        self.setup_poi()
        self.selected_map = self.map1

    def update(self, dt):
        self.dt = dt
        self.map1.update(dt)
        self.menu.update(dt)
        self.palette.update(dt)
        self.poi_map.update(dt)
        self.poi_menu.update(dt)
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
            self.poi_map.map.set_clip()
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

        # POI Map
        if self.show_poi:
            self.poi_map.xy = self.map1.xy
            self.poi_map.draw(self.screen, self.clip)


        # GUI
        self.menu.draw(self.screen)
        if self.show_poi:
            self.poi_menu.draw(self.screen)
        self.button1.draw(self.screen)
        self.button2.draw(self.screen)
        if self.button1.clicked:
            self.drop_menu.draw(self.screen)
        if self.button2.clicked:
            self.pal_menu.draw(self.screen)
        if self.drop_menu.buttons[1].clicked:
            self.load_menu.draw(self.screen)
        if self.drop_menu.buttons[2].clicked:
            self.palette.draw(self.screen)
        if self.right_m_button:
            screen_rect = self.m_select_rect.copy()
            screen_rect.x += self.map1.xy[0]
            screen_rect.y += self.map1.xy[1]
            pg.draw.rect(self.screen, WHITE, screen_rect, 1)
        if self.show_full_map:
            if self.full_map:
                self.screen.blit(self.full_map, (0,0))
        self.info_panel.draw(self.screen)
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
        self.menu.setup(STEEL)
        self.poi_map.setup((0,0,0), alpha=150)
        self.poi_menu.setup(STEEL)

    def setup_poi(self):
        wall = pg.image.load("./tiles/Wall.png").convert_alpha()
        door = pg.image.load("./tiles/Door.png").convert_alpha()
        poi = pg.image.load("./tiles/POI.png").convert_alpha()
        self.poi_dict = {"Poi Wall":wall, "Poi Door":door, "Poi Symbol":poi}
        p = [i for i in self.poi_dict.keys()]
        for num, tile in enumerate(self.poi_menu.group):
            tile.image = self.poi_dict[p[num]]
            tile.rect = tile.image.get_rect()
            tile.rect.topleft = ((self.block*num), 1)
            tile.filename = p[num]
            tile.dirty = 1
        xplace = self.size[0] - self.block*3
        self.poi_menu.xy = [xplace, 1]

    def setup_palette(self):
        sheet = SpriteSheet("img/magecity_64p.png", 64, (0,0), (8,44))
        self.men_list = sum(sheet.image_list, [])
        length = len(self.men_list)
        size = (10, int(length/10))
        menu = Map("Palette", self.size, size, self.block, self.empty_tile)
        menu.setup(CYAN)
        for i, tile in enumerate(menu.group):
            tile.filename = "{}".format(i)
            tile.image = self.men_list[i]
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

        if key == K_q:
            self.show_poi = not self.show_poi

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
            if not self.info_panel.display:
                if not self.show_full_map:
                    if self.button1.click(pos):
                        not_menu = False
                    elif self.button2.click(pos):
                        not_menu = False
                    if self.button1.clicked:
                        if self.drop_menu.click(pos):
                            not_menu = False
                    if self.button2.clicked:
                        if self.pal_menu.click(pos):
                            not_menu = False
                    if self.drop_menu.buttons[1].clicked:
                        if self.load_menu.click(pos):
                            self.loadmap(self.load_menu.clickinfo)
                    elif self.drop_menu.buttons[3].clicked:
                        self.show_map()
                        self.drop_menu.buttons[3].clicked = False
                    elif self.drop_menu.buttons[4].clicked:
                        self.info_panel.display_panel()
                        self.drop_menu.buttons[4].clicked = False
                    if self.pal_menu.click(pos):
                        if self.pal_menu.clickinfo == "New":
                            self.new_palette()
                        else:
                            self.switch_palette(text=self.pal_menu.clickinfo)
                    if not_menu:
                        if self.drop_menu.buttons[2].clicked:
                            self.find_tile(pos, self.palette, self.menu)
                        elif self.show_poi:
                            self.find_tile(pos, self.poi_menu, self.poi_map)
                        elif self.show_foreground > 0:
                            self.find_tile(pos, self.menu, self.map2)
                        else:
                            self.find_tile(pos, self.menu, self.map1)
                else:
                    self.show_full_map = False
            else:
                self.info_panel.click(pos)

        if button == 3:
            if not self.show_full_map:
                self.right_m_button = True
                self.right_m_pos = pos
            else:
                self.take_image(self.full_map)

    def mouse_up(self, button, pos):
        if button == 3:
            self.right_m_button = False
            self.right_m_pos = pos
            new_rect = self._invert_rect(self.m_select_rect)

            if self.show_poi:
                self.group_select(new_rect, self.poi_map.group)
            elif self.show_foreground < 0:
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
            if found:
                break
        if not found:
            for tile in bg_map.group:
                map_pos = (pos[0] - bg_map.xy[0], pos[1] - bg_map.xy[1])
                if tile.rect.collidepoint(map_pos):
                    self.change_tile(tile)
                    bg_map.clear_map()
        return found

    def change_tile(self, tile):
        if self.current_tile != None:
            tile.filename = self.current_tile.filename
            tile.image = self.current_tile.image
            tile.dirty = 1

    def new_palette(self):
        self.menus.append(Map("Menu", self.size, (2,14), self.block, self.empty_tile))
        self.menus[-1].setup(STEEL)

        size = self.pal_menu.size
        self.pal_menu.change_size((size[0], size[1]+20))
        num = len(self.menus)
        self.pal_menu.add_buttons(1, ["Pal-{}".format(num)])
        self.switch_palette(ind=-1)

    def switch_palette(self, ind=None, text=None):
        if ind:
            self.menu = self.menus[ind]
        elif text:
            self.menu = self.menus[int(text[-1])-1]

    def show_map(self):
        full_map = pg.Surface((40*64, 40*64))
        for tile in self.map1.group:
            full_map.blit(tile.image, tile.rect.topleft)
        for tile in self.map2.group:
            if tile.filename != "Empty_tile":
                full_map.blit(tile.image, tile.rect.topleft)
        self.full_map = pg.transform.smoothscale(full_map, self.size)
        self.show_full_map = True

    def take_image(self, surf):
        folder = Path("./image")
        amount = len(folder.files("*.jpg"))
        filename = "{}{}{}{}".format(folder, "/map", amount, ".jpg")
        pg.image.save(surf, filename)

    def savemap(self):
        saving = SaveMap("Empty_tile")
        saving.add_map(self.map1)
        saving.add_map(self.map2)
        saving.add_map(self.poi_map)
        saving.write_to_file()

    def loadmap(self, filename):
        load = LoadMap(filename)
        maplist = []
        for m in load.maps.values():
            a_map = Map(m["info"]["name"], m["info"]["size"], m["info"]["grid"], m["info"]["block"], self.empty_tile)
            if m["info"]["name"] == "Foreground":
                a_map.setup(m["info"]["color"], 200)
            elif m["info"]["name"] == "POI Map":
                a_map.setup(m["info"]["color"], 150)
            else:
                a_map.setup(m["info"]["color"])
            for t in a_map.group:
                for i in m["tiles"]:
                    if list(t.rect.topleft) in m["tiles"][i]:
                        t.filename = i
                        if i[0] == "P":
                            t.image = self.poi_dict[i]
                            t.dirty = 1
                        else:
                            t.image = self.men_list[int(i)]
                            t.dirty = 1
            maplist.append(a_map)
        for j in maplist:
            if j.name == "Background":
                self.map1 = j
            if j.name == "Foreground":
                self.map2 = j
            if j.name == "POI Map":
                self.poi_map = j
        print("Loading from file...")


if __name__ == "__main__":
    print("Starting")
    set_dir(__file__)
    s = Main((800,640))
    s.mainloop()
