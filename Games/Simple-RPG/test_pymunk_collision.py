import pygame as pg
import pymunk as pk

from pygame.locals import *
from load import Template, Tile

class Main(Template):
    """Testing movement with Pymunk"""
    def __init__(self, size):
        super(Main, self).__init__(size)
        self.size = size
        self.player = Player()
        self.char = pg.sprite.LayeredDirty()
        self.char.add(self.player)
        self.bg = pg.Surface(self.size)
        self.space = pk.Space()
        self.space.gravity = (.0,.0)
        self.space.add(self.player.body, self.player.shape)
        self.walls = self.walls()

    def walls(self):
        walls = pg.sprite.LayeredDirty()
        w, h = (25, 19)
        l1, l2, l3, l4 = self.translate_num((w,h), 32)
        for y in xrange(h):
            for x in xrange(w):
                if x == 0 or x == w-1 or y == 0 or y == h-1: 
                    tile = Tile("./img/wall1_medium.png", (x*32, y*32))
                    walls.add(tile)
        static_lines = [pk.Segment(self.space.static_body, l1[0], l1[1], 16),
                        pk.Segment(self.space.static_body, l2[0], l2[1], 16),
                        pk.Segment(self.space.static_body, l3[0], l3[1], 16),
                        pk.Segment(self.space.static_body, l4[0], l4[1], 16)]
        self.space.add(static_lines)
        return walls

    def translate_num(self, numbers, block):
        w, h = numbers
        c1 = (0+block/2, 0+block/2)
        c2 = (0+block/2, h*block-(block/2))
        c3 = (w*block-(block/2), h*block-(block/2))
        c4 = (w*block-(block/2), 0+block/2)

        l1 = (c1, c2)
        l2 = ((c2[0]-(block/2), c2[1]), c3)
        l3 = ((c3[0], c3[1]-(block/2)), c4)
        l4 = (c1[0]+(block/2), c1[1]),(c4[0]-(block/2), c4[1])

        return l1, l2, l3, l4

    def key_down(self, key):
        if key == K_ESCAPE:
            self.game_on = False

        if key in (K_w, K_UP):
            self.player.moving["up"] = True
        if key in (K_a, K_LEFT):
            self.player.moving["left"] = True
        if key in (K_s, K_DOWN):
            self.player.moving["down"] = True
        if key in (K_d, K_RIGHT):
            self.player.moving["right"] = True

    def key_up(self, key):
        if key in (K_w, K_UP):
            self.player.moving["up"] = False
        if key in (K_a, K_LEFT):
            self.player.moving["left"] = False
        if key in (K_s, K_DOWN):
            self.player.moving["down"] = False
        if key in (K_d, K_RIGHT):
            self.player.moving["right"] = False

    def update(self, dt):
        self.player.update(dt)
        self.space.step(1/3.)

    def draw(self):
        self.bg.fill((0,0,0))
        self.walls.draw(self.bg)
        self.char.draw(self.bg)

        self.screen.blit(self.bg, (0,0))

class Player(pg.sprite.DirtySprite):
    """Quick player class"""
    def __init__(self):
        super(Player, self).__init__()
        self.dirty = 2
        self.image = pg.image.load("./img/blob.png")
        self.rect = self.image.get_rect()
        self.rect.center = (200, 200)
        moment = pk.moment_for_circle(1, 0, 16)
        self.body = pk.Body(1, moment)
        self.shape = pk.Circle(self.body, 16)
        self.shape.elasticity = 1.
        self.shape.friction = .8
        self.body.position = self.rect.center

        self.moving = {"up":False,"left":False,"down":False,"right":False,}
        self.speed = 5

    def update(self, dt):
        self.move()
        self.rect.center = self.body.position

    def move(self):
        if self.moving["up"]:
            self.body.velocity[1] = -10
        elif not self.moving["down"]:
            self.body.velocity[1] = 0

        if self.moving["left"]:
            self.body.velocity[0] = -10
        elif not self.moving["right"]:
            self.body.velocity[0] = 0

        if self.moving["down"]:
            self.body.velocity[1] = 10
        elif not self.moving["up"]:
            self.body.velocity[1] = 0

        if self.moving["right"]:
            self.body.velocity[0] = 10
        elif not self.moving["left"]:
            self.body.velocity[0] = 0

        

if __name__ == "__main__":
    s = Main((1024, 960))
    s.mainloop()
        