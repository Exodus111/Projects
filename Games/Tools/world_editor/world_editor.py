#!/usr/bin/python3

import pygame as pg
import json
from collections import OrderedDict, defaultdict
from myfuncs import *
from pygame.locals import *
from load import Template, Tile, SpriteSheet
from path import Path
from gui import Button, Menu, FloatingText, Panel
from saveload import SaveMap, LoadMap
from maps import Map

SUNFLOWER = (241,196,15)
WHITE = (255,255,255)
BLACK = (0,0,0)

MIST  = (142, 175, 196)
STONE = (51, 105, 133)
SHADOW = (41, 49, 50)
AUTUMN = (117, 54, 37)

BG_COLOR = SHADOW
MG_COLOR = AUTUMN
FG_COLOR = STONE
POI_MAP = MIST
POI_MENU = SHADOW
MENU_COLOR = STONE


class Main(Template):
    def __init__(self, size):
        Template.__init__(self, size)
        self.name = "World Editor 1.1"
        self.size = size
        self.block = 64
        self.dt = 0.
        self.empty_tile = pg.image.load("./tiles/Empty_tile_64p.png").convert_alpha()
        self.map_bg = Map("Background", self, self.size, (40,40), self.block, self.empty_tile)
        self.map_mg = Map("Middleground", self, self.size, (40,40), self.block, self.empty_tile)
        self.map_fg = Map("Foreground", self, self.size, (40,40), self.block, self.empty_tile)
        self.poi_map = Map("POI Map", self, self.size, (40,40), self.block, self.empty_tile)
        self.poi_menu = Map("POI Menu", self, self.size, (4,1), self.block, self.empty_tile)
        self.menus = [Map("Menu", self, self.size, (2,14), self.block, self.empty_tile)]
        self.pal_menu = Menu((128, 40), (0,21))
        self.pal_menu.add_buttons(2, ["New", "Pal-1"])
        self.menu = self.menus[0]
        self.menu.xy[1] += 20
        self.men_list = []
        self.sprite_map = self.setup_spritemap()
        self.sprite_map.xy = [250,0]
        self.clip = pg.Rect(0,0, self.size[0],self.size[1])
        self.c_pos = self.clip.topleft
        self.show_full_map = False
        self.show_poi = False
        self.full_map = None
        self.current_tile = None
        self.current_menu = None
        self.ground_state = None
        self.right_m_pos = None
        self.right_m_button = False
        self.m_pos = None
        self.fill = False
        self.m_select_rect = pg.Rect(1,1,1,1)
        self.menu_button = Button((120, 20), (129,1), "Menu")
        self.pal_button = Button((128,20), (0,0), "Palette")
        self.drop_menu = Menu((120, 160), (129, 21))
        self.drop_menu.add_buttons(5, ["Save", "Load", "Sprites", "See Map", "Info"])
        self.drop_menu.set_bg_color(STONE)
        self.load_menu = self.setup_loadmenu()
        self.floating_text = FloatingText("no text", self.size)
        self.info_panel = Panel((self.size[0] - self.size[0]/3, self.size[1] - self.size[1]/3), (self.size[0]/6, self.size[1]/6))
        self.info_panel.setup_text([self.name, "Made by Aurelio Aguirre", "", "Use WASD to move around.", "Use E to toggle the Foreground.", "Use R to toggle the Middleground.", "Use Q to toggle the Point of Interest map."])
        self.setup()
        self.setup_poi()
        self.selected_map = self.map_bg

    def update(self, dt):
        self.dt = dt
        self.map_bg.update(dt)
        self.map_fg.update(dt)
        self.map_mg.update(dt)
        self.menu.update(dt)
        self.sprite_map.update(dt)
        self.poi_map.update(dt)
        self.poi_menu.update(dt)
        self.floating_text.update(dt)
        if self.drop_menu.buttons[0].active:
            self.savemap()
            self.drop_menu.buttons[0].active = False
        if self.drop_menu.buttons[2].active:
            self.selected_map = self.sprite_map
        else:
            self.selected_map = self.map_bg
        if self.pal_button.active:
            if self.pal_menu.clickinfo != None:
                if self.pal_menu.clickinfo == "New":
                    self.new_palette()
                else:
                    self.switch_palette(text=self.pal_menu.clickinfo)
                self.pal_menu.clickinfo = None
        if self.map_bg.clipped:
            self.map_fg.map.set_clip()
            self.map_mg.map.set_clip()
            self.poi_map.map.set_clip()
            self.map_bg.clipped = False
        if self.c_pos != self.clip.topleft:
            self.c_pos = (self.c_pos[0] - self.map_bg.xy[0], self.c_pos[1] - self.map_bg.xy[1])
            self.clip.topleft = self.c_pos
        self.menu_button.update(self.dt)
        self.mouse_select()

    def draw(self):
        self.screen.fill(BLACK)

        # MAPs
        # Background
        self.map_bg.draw(self.screen, self.clip)

        # Middleground
        if self.ground_state == "MG":
            self.map_mg.xy = self.map_bg.xy
            self.map_mg.draw(self.screen, self.clip)

        # Foreground
        if self.ground_state == "FG":
            self.map_fg.xy = self.map_bg.xy
            self.map_fg.draw(self.screen, self.clip)

        # POI Map
        if self.show_poi:
            self.poi_map.xy = self.map_bg.xy
            self.poi_map.draw(self.screen, self.clip)


        # GUI
        self.menu.draw(self.screen)
        if self.show_poi:
            self.poi_menu.draw(self.screen)
        self.menu_button.draw(self.screen)
        self.pal_button.draw(self.screen)
        if self.menu_button.active:
            self.drop_menu.draw(self.screen)
        if self.pal_button.active:
            self.pal_menu.draw(self.screen)
        if self.drop_menu.buttons[1].active:
            self.load_menu.draw(self.screen)
        if self.drop_menu.buttons[2].active:
            self.sprite_map.draw(self.screen)
        if self.right_m_button:
            screen_rect = self.m_select_rect.copy()
            screen_rect.x += self.map_bg.xy[0]
            screen_rect.y += self.map_bg.xy[1]
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
        menu.set_bg_color(STONE)
        return menu

    def setup(self):
        self.map_bg.setup(BG_COLOR)
        self.map_fg.setup(FG_COLOR, 200)
        self.map_mg.setup(MG_COLOR, 200)
        self.menu.setup(MENU_COLOR)
        self.poi_map.setup(POI_MAP, alpha=150)
        self.poi_menu.setup(POI_MENU)

    def setup_poi(self):
        wall = pg.image.load("./tiles/Wall.png").convert_alpha()
        door = pg.image.load("./tiles/Door.png").convert_alpha()
        poi = pg.image.load("./tiles/POI.png").convert_alpha()
        delete = pg.image.load("./tiles/Eliminate.png").convert_alpha()
        self.poi_dict = OrderedDict((("Poi Wall", wall), ("Poi Door", door), ("Poi Symbol", poi), ("Delete", delete)))
        p = [i for i in self.poi_dict.keys()]
        for num, tile in enumerate(self.poi_menu.group):
            tile.image = self.poi_dict[p[num]]
            tile.rect = tile.image.get_rect()
            tile.rect.topleft = ((self.block*num), 1)
            tile.filename = p[num]
            tile.dirty = 1
        xplace = self.size[0] - self.block*4
        self.poi_menu.xy = [xplace, 1]


    def setup_spritemap(self):
        sheet = SpriteSheet("img/magecity_64p.png", 64, (0,0), (8,44))
        self.men_list = sum(sheet.image_list, [])
        length = len(self.men_list)
        size = (10, int(length/10))
        menu = Map("Palette", self, self.size, size, self.block, self.empty_tile)
        menu.setup(MIST)
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
            if self.ground_state == None or self.ground_state == "MG":
                self.ground_state = "FG"
            else:
                self.ground_state = None

        if key == K_r:
            if self.ground_state == None or self.ground_state == "FG":
                self.ground_state = "MG"
            else:
                self.ground_state = None

        if key == K_q:
            self.show_poi = not self.show_poi
            self.current_tile = None

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
            # First we check for the unique states, Info Panel and Full Map.
            if not self.info_panel.display:
                if not self.show_full_map:
                    # Now we check for menu buttons being clicked, and switch our
                    # not_menu switch if they are. From here the rest is handled by update.
                    if self.menu_button.click(pos):
                        not_menu = False
                    elif self.pal_button.click(pos):
                        not_menu = False
                    if self.menu_button.active:
                        if self.drop_menu.click(pos):
                            not_menu = False
                    if self.pal_button.active:
                        if self.pal_menu.click(pos):
                            not_menu = False
                    # Assuming we are in our main menu we check for the the buttons being clicked.
                    # This part is allowed to happen WHILE maps are also being manipulated. (not_menu is not switched)
                    if self.drop_menu.buttons[1].active:
                        if self.load_menu.click(pos):
                            self.loadmap(self.load_menu.clickinfo)
                    elif self.drop_menu.buttons[3].active:
                        self.show_map()
                        self.drop_menu.buttons[3].active = False
                    elif self.drop_menu.buttons[4].active:
                        self.info_panel.display_panel()
                        self.drop_menu.buttons[4].active = False
                    # Here we look for our Maps. Basically we are moving a tile from one map to another.
                    # We just need to pick the right one, and they should all overwrite each other.
                    # In other words, only one map is active at a time.
                    if not_menu:
                        if self.drop_menu.buttons[2].active: # Tiles are showing.
                            self.find_tile(pos, self.sprite_map, self.menu)
                        elif self.show_poi: # POI Map is up.
                            self.find_tile(pos, self.poi_menu, self.poi_map)
                        elif self.ground_state == "FG": # we are on the Foreground map.
                            self.find_tile(pos, self.menu, self.map_fg)
                        elif self.ground_state == "MG": # We are on the middleground map.
                            self.find_tile(pos, self.menu, self.map_mg)
                        else: # We default to the Background map.
                            self.find_tile(pos, self.menu, self.map_bg)
                else:
                    # While the full map is up, any left mouse click will deactivate it.
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
            elif self.ground_state == "FG":
                self.group_select(new_rect, self.map_fg.group)
            elif self.ground_state == "MG":
                self.group_select(new_rect, self.map_mg.group)
            else:
                self.group_select(new_rect, self.map_bg.group)

    def mouse_motion(self, button, pos, rel):
        self.m_pos = pos

    def mouse_select(self):
        if self.right_m_button:
            old_pos = (self.right_m_pos[0] - self.map_bg.xy[0], self.right_m_pos[1] - self.map_bg.xy[1])
            new_pos = (self.m_pos[0] - self.map_bg.xy[0], self.m_pos[1] - self.map_bg.xy[1])
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
                menu.select_rect(tile.rect)
                menu.draw_border = True
                self.current_tile = tile
                self.current_menu = menu.name
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
            if self.current_tile.filename != "Delete":
                tile.filename = self.current_tile.filename
                tile.image = self.current_tile.image
                tile.dirty = 1
            else:
                tile.filename = "Empty_tile"
                tile.image = self.empty_tile
                tile.dirty = 1

    def new_palette(self):
        self.menus.append(Map("Menu", self, self.size, (2,14), self.block, self.empty_tile))
        self.menus[-1].setup(STONE)

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
        for tile in self.map_bg.group:
            full_map.blit(tile.image, tile.rect.topleft)
        for tile in self.map_mg.group:
            if tile.filename != "Empty_tile":
                full_map.blit(tile.image, tile.rect.topleft)
        for tile in self.map_fg.group:
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
        saving.add_map(self.map_bg)
        saving.add_map(self.map_mg)
        saving.add_map(self.map_fg)
        saving.add_map(self.poi_map)
        saving.write_to_file()

    def loadmap(self, filename):
        load = LoadMap(filename)
        maplist = []
        for m in load.maps.values():
            a_map = Map(m["info"]["name"], self, m["info"]["size"], m["info"]["grid"], m["info"]["block"], self.empty_tile)
            if m["info"]["name"] == "Foreground" or m["info"]["name"] == "Middleground":
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
                self.map_bg = j
            if j.name == "Middleground":
                self.map_mg = j
            if j.name == "Foreground":
                self.map_fg = j
            if j.name == "POI Map":
                self.poi_map = j
        print("Loading from file...")

if __name__ == "__main__":
    print("Starting")
    #set_dir(__file__)
    s = Main((800,640))
    s.mainloop()
