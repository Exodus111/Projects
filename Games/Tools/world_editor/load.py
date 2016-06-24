import os, sys, pygame
from pygame.locals import *
from vec2d import vec2d

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

    def mainloop(self, fps=100):
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
        #pygame.quit()
        print("Thank you for playing.")
        print("Time played: {} seconds.".format(self.dt))
        sys.exit()

class Tile(pygame.sprite.DirtySprite):
    def __init__(self, image, xy):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 2
        self.xy = xy
        self.filename = image
        if image != None:
            self.image = pygame.image.load(image).convert_alpha()
            self.reload()

    def reload(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = self.xy

class Room(object):
    """Room class that uses the Tile Class"""
    def __init__(self, size, wall, floor, block):
        self.floors_group = pygame.sprite.LayeredDirty()
        self.walls_group = pygame.sprite.LayeredDirty()
        self.size = size
        self.block = block
        self.wall = wall
        self.floor = floor
        self.centerx = size[0]/2
        self.centery = size[1]/2
        self.make_room(block)

    def make_room(self, block):
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if y == 0 or x == 0 or y == self.size[1]-1 or x == self.size[0]-1:
                    tile = Tile(self.wall, (x*block, y*block))
                    self.walls_group.add(tile)
                elif x > self.centerx-4 and x < self.centerx+4 and y > self.centery-2 and y < self.centery+2:
                    tile = Tile(self.wall, (x*block, y*block))
                    self.walls_group.add(tile)
                else:
                    tile = Tile(self.floor, (x*block, y*block))
                    self.floors_group.add(tile)

    def make_door(self, placement, image=None):
        if image == None:
            if placement == "north":
                collider = pygame.sprite.Sprite()
                collider.rect = pygame.Rect(32,32, self.centerx,0)
                collided = pygame.sprite.spritecollide(collider, self.walls_group, True)
                for wall in collided:
                    tile = Tile(self.floor, wall.rect.topleft)
                    self.floors_group.add(tile)
                    #self.walls_group.remove(tile)

            if placement == "west":
                pass
            if placement == "south":
                pass
            if placement == "east":
                pass


class Collide(object):
    def __init__(self, walls):
        self.walls = walls

    def check(self, player):
        mtop = mleft = mbottom = mright = False
        collided = pygame.sprite.spritecollide(player, self.walls, False)
        if collided != []:
            for brick in collided:
                if not mtop: mtop = brick.rect.collidepoint(player.rect.midtop)
                if not mleft: mleft = brick.rect.collidepoint(player.rect.midleft)
                if not mbottom: mbottom = brick.rect.collidepoint(player.rect.midbottom)
                if not mright: mright = brick.rect.collidepoint(player.rect.midright)
            if mtop:
                if player.direction["up"]:
                    wall_vector = vec2d(10,0)
                    player.dir = player.dir.projection(wall_vector)
            if mleft:
                if player.direction["left"]:
                    wall_vector = vec2d(0,10)
                    player.dir = player.dir.projection(wall_vector)
            if mbottom:
                if player.direction["down"]:
                    wall_vector = vec2d(10,0)
                    player.dir = player.dir.projection(wall_vector)
            if mright:
                if player.direction["right"]:
                    wall_vector = vec2d(0,10)
                    player.dir = player.dir.projection(wall_vector)


class Animate(object):
    def __init__(self, name):
        self.new = True
        self.name = name
        self.anim_type = "walk"
        self.direction = "down"
        self.mytimers = {}
        self.speed = .05
        self.frame = None
        self.poses = {
            "idle":{"up":[],"left":[],"down":[],"right":[]},
            "walk":{"up":[],"left":[],"down":[],"right":[]},
            "attack":{"up":[],"left":[],"down":[],"right":[]},
            "cast":{"up":[],"left":[],"down":[],"right":[]},
            "death":{"up":[],"left":[],"down":[],"right":[]}
        }

    def mytimer(self, name, seconds, dt):
        if name in self.mytimers.keys():
            if self.mytimers[name] < dt:
                self.mytimers[name] = dt + seconds
                return True
            else:
                return False
        else:
            self.mytimers[name] = dt + seconds
            return True

    def load_animations(self, atype, order, images):
        for i, direction in enumerate(order):
            self.poses[atype][direction] = images[i]

    def switch(self, atype, direction=None):
        self.anim_type = atype
        if direction != None:
            self.direction = direction

    def new_pose(self, name, images):
        self.poses[name] = {"up":images[0],"left":images[1],"down":images[2],"right":images[3]}

    def _draw_frame(self):
        while True:
            for frame in self.poses[self.anim_type][self.direction]:
                yield frame

    def update(self, dt):
        if self.new:
            self.draw = self._draw_frame()
            self.new = False
        if self.mytimer(self.name, self.speed, dt):
            self.frame = self.draw.next()
        return self.frame


class SpriteSheet(object):
    def __init__(self, filename, block, start, size):
        self.sheet = pygame.image.load(filename).convert_alpha()
        x_b, y_b = size
        rects = []
        for y in range(y_b):
            line_rects = []
            for x in range(x_b):
                rect = pygame.Rect(start[0]+(x*block), start[1]+(y*block), block, block)
                line_rects.append(rect)
            rects.append(line_rects)
        self.image_list = [self.load_images(rectlist) for rectlist in rects]

    def image_at(self, rect):
        image = pygame.Surface(rect.size)
        trans = image.get_at((1,1))
        image.set_colorkey(trans)
        image.blit(self.sheet, (0,0), rect)
        return image


    def load_images(self, rects):
        return [self.image_at(rect) for rect in rects]
