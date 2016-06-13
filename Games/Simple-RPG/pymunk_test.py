import pygame as pg
from pygame.locals import *
import pymunk
import pymunk.pygame_util
from load import Template


class Main(Template):
    """Doing a physics test of Pymunk"""
    def __init__(self, size):
        super(Main, self).__init__(size)
        self.size = size
        self.space = pymunk.Space()
        self.space.gravity = (0.0, -500.0)
        self.rad = 14
        self.ball_elasticty = 0.8
        self.friction = 0.8
        self.circles = []
        self.line = self.create_line()
        self.line.color = (0,255,0) # Blue

    def create_circle(self, position):
        mass = 1
        inertia = pymunk.moment_for_circle(mass, 0, self.rad)
        body = pymunk.Body(mass, inertia)
        body.position = position
        shape = pymunk.Circle(body, self.rad)
        shape.elasticty = self.ball_elasticty
        shape.friction = self.friction
        self.space.add(body, shape)
        return shape

    def create_line(self):
        body = pymunk.Body()
        body.position = (400, 600)
        line_shape = pymunk.Segment(body, (-400, -500), (400, -500), 15)
        line_shape.elasticity = 0.5
        self.space.add(line_shape)
        return line_shape
    
    def key_down(self, key):
        # Escape to quit
        if key == K_ESCAPE:
            self.game_on = False

    def mouse_down(self, button, pos):
        if button == 1:
            real_pos = pymunk.pygame_util.from_pygame(pos, self.screen)
            new_circle = self.create_circle(real_pos)
            self.circles.append(new_circle)

    def update(self, dt):
        #self.space.step(1/60)
        pass

    def draw(self):
        self.screen.fill((0,0,0))

        for circle in self.circles:
            pymunk.pygame_util.draw(self.screen, circle)

        pymunk.pygame_util.draw(self.screen, self.line)
        self.space.step(1/60.)

if __name__ == "__main__":
    s = Main((800, 600))
    s.mainloop()


        