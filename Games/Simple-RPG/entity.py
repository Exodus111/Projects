import pygame
from vec2d import vec2d
from pygame.locals import *
from load import *
import random, math

class Entity(pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 2

class Npc(Entity):
    """The General purpose NPC class"""
    def __init__(self, size, number):
        Entity.__init__(self)
        self.size = size
        self.number = number
        self.walk_sheet = SpriteSheet("./img/sprite_male.png", block=64, start=(0,512), size=(9,4))
        self.idle_sheet = SpriteSheet("./img/sprite_male.png", block=64, start=(0,0), size=(1,4))
        self.animate = Animate("mob {}".format(self.number))
        self.animate.load_animations("walk", ["up", "left", "down", "right"], self.walk_sheet.image_list)
        self.animate.load_animations("idle", ["up", "left", "down", "right"], self.idle_sheet.image_list)
        self.image = self.animate.update(0)
        self.rect = pygame.Rect(random.randint(0, 400), random.randint(0, 400), 64, 64)
        self.pos = vec2d(self.rect.center)
        self.direction = [0,0,0,0]
        self.dir = vec2d(0,0)
        self.target = vec2d(0,0)
        self.straight = vec2d(1,0)
        direction = random.randint(-0, 3)
        self.direction[direction] = 1
        self.speed = 2


    def update(self, dt):
        self.check_walls()
        self.move(dt)

    def follow(self, target):
        between = target - self.pos
        ab = int(self.straight.get_angle_between(between))
        self.direction = [0,0,0,0]
        distance = int(self.pos.get_distance(target))
        if distance < 50:
            pass
        elif ab < -45 and ab > -135: #up
            self.direction[0] = 1
        elif ab <= -135 or ab >= 135: #left
            self.direction[1] = 1
        elif ab < 135 and ab > 45: #down
            self.direction[2] = 1
        elif ab <= 45 and ab >= -45: #right
            self.direction[3] = 1

    def move(self, dt):
        moving = True
        if self.direction[0]: #up
            self.dir = vec2d(0,-5)
            self.dir.length = self.speed
            self.animate.switch("walk", "up")
            self.image = self.animate.update(dt)
        elif self.direction[1]: #left
            self.dir = vec2d(-5,0)
            self.dir.length = self.speed
            self.animate.switch("walk", "left")
            self.image = self.animate.update(dt)
        elif self.direction[2]: #down
            self.dir = vec2d(0,5)
            self.dir.length = self.speed
            self.animate.switch("walk", "down")
            self.image = self.animate.update(dt)
        elif self.direction[3]: #right
            self.dir = vec2d(5,0)
            self.dir.length = self.speed
            self.animate.switch("walk", "right")
            self.image = self.animate.update(dt)
        else:
            moving = False
            self.animate.switch("idle")
            self.animate.new = True
            self.image = self.animate.update(dt)
        if moving:
            self.pos += self.dir
            self.rect.center = self.pos.inttup()

    def check_walls(self):
        center = self.rect.center
        size = self.size
        if center[0] >= size[0]:
            self.direction[3] = 0
            self.direction[1] = 1
        if center[0] <= 0:
            self.direction[1] = 0
            self.direction[3] = 1
        if center[1] >= size[0]:
            self.direction[2] = 0
            self.direction[0] = 1
        if center[1] <= 0:
            self.direction[0] = 0
            self.direction[2] = 1

class Player(Entity):
    """The class for the player."""
    def __init__(self, size, walls, center=(150, 150)):
        Entity.__init__(self)
        self.walk_sheet = SpriteSheet("./img/sprite_male.png", block=64, start=(0,512), size=(9,4))
        self.idle_sheet = SpriteSheet("./img/sprite_male.png", block=64, start=(0,0), size=(1,4))
        self.animate = Animate("Player")
        self.animate.load_animations("walk", ["up", "left", "down", "right"], self.walk_sheet.image_list)
        self.animate.load_animations("idle", ["up", "left", "down", "right"], self.idle_sheet.image_list)
        self.image = self.animate.update(0)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.direction = {"up":False,"left":False,"down":False,"right":False}
        self.speed = 2
        self.dt = 0
        self.pos = vec2d(self.rect.center)
        self.dir = vec2d(0,0)
        self.dir_vecs = [vec2d(0,-1), vec2d(-1,0), vec2d(0,1), vec2d(1,0)]
        self.once = True
        self.collide = Collide(walls)

    def l_shift(self, lskey):
        if lskey:
            self.speed = 4
            self.animate.speed = .025
        else:
            self.speed = 2
            self.animate.speed = .05

    def move(self, key, up_or_down):
        if key in (K_w, K_UP):
            self.direction["up"] = up_or_down
        if key in (K_a, K_LEFT):
            self.direction["left"] = up_or_down
        if key in (K_s, K_DOWN):
            self.direction["down"] = up_or_down
        if key in (K_d, K_RIGHT):
            self.direction["right"] = up_or_down
        if up_or_down:
            self.animate.new = True
        self.once = True

    def _move(self, dt):
        if self.direction["up"]:
            self.dir[1] = -5
            self.animate.switch("walk", "up")
            if not self.direction["left"]:
                if not self.direction["right"]:
                    self.image = self.animate.update(dt)
        elif not self.direction["down"]:
            self.dir[1] = 0

        if self.direction["left"]:
            self.dir[0] = -5
            self.animate.switch("walk", "left")
            self.image = self.animate.update(dt)
        elif not self.direction["right"]:
            self.dir[0] = 0

        if self.direction["down"]:
            self.dir[1] = 5
            self.animate.switch("walk", "down")
            if not self.direction["left"]:
                if not self.direction["right"]:
                    self.image = self.animate.update(dt)
        elif not self.direction["up"]:
            self.dir[1] = 0

        if self.direction["right"]:
            self.dir[0] = 5
            self.animate.switch("walk", "right")
            self.image = self.animate.update(dt)
        elif not self.direction["left"]:
            self.dir[0] = 0


        if True not in self.direction.values():
            if self.once:
                self.animate.switch("idle")
                self.animate.new = True
                self.image = self.animate.update(self.dt)
                self.once = False

    def update(self, dt):
        self._move(dt)
        if self.dir.length != 0:
            self.dir.length = self.speed
        self.collide.check(self)
        self.pos += self.dir
        self.rect.center = self.pos.inttup()
