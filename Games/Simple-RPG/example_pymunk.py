import pygame
from pygame.locals import *
from pygame.color import *
import pymunk as pm
import random
import math

to_pygame = lambda p: (int(p.x), int(-p.y+600))

def end_game(e):
    global running
    running = False

def add_ball(x, y, mass=10, radius=25, elasticity=0.6 ):
    if random.random() < 0.3:
        inertia = pm.moment_for_circle(100, 0, 50, (0,0))
        body = pm.Body(mass, inertia)
        shape = pm.Circle(body, 50, (0,0))
        shape.elasticity = elasticity
        shape.collision_type = 2
        shape.color = "red"
    else:
        inertia = pm.moment_for_circle(mass, 0, radius, (0,0))
        body = pm.Body(mass, inertia)
        shape = pm.Circle(body, radius, (0,0))
        shape.elasticity = elasticity
        shape.collision_type = 1
        shape.color = "blue"
    body.position = x, y
    space.add(body, shape)
    balls.append(shape)

def toggle_gravity(e):
    global space
    space.gravity[1] = 0.0 if space.gravity[1] != 0.0 else -900.0
    print space.gravity[1]

def smack(space, arbiter):
    if arbiter.is_first_contact: # is this the first frame contact was made?
        for shape in arbiter.shapes:
            shape.color = random.choice(["blue","green","yellow","purple","orange","red"])
        for contact in arbiter.contacts: # go through all contacts
            hit_marks.append([2+int(math.sqrt(arbiter.total_ke/2000)), contact.position, "blue"])

space = pm.Space()
space.add_collision_handler(1, 1, post_solve=smack) # calls the ball

static_body = pm.Body()
static_lines = [pm.Segment(static_body, (111.0, 180.0), (407.0, 146.0), 0.0)
                ,pm.Segment(static_body, (407.0, 146.0), (407.0, 343.0), 0.0)
                    ]

key_down_actions = {
    K_ESCAPE: end_game,
    K_SPACE: lambda e: add_ball(random.randint(115,350), 400),
    K_g: toggle_gravity
}

for line in static_lines:
    line.elasticity = 0.95
space.add(static_lines)

pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
running = True

balls = []
hit_marks=[]

add_ball(random.randint(115,350), 400)

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            end_game(event)
        elif event.type == KEYDOWN:
            if event.key in key_down_actions:
                key_down_actions[event.key](event)

    for ball in [b for b in balls if b.body.position.y < 100]:
        space.remove(ball, ball.body)
        balls.remove(ball)

    for mark in [m for m in hit_marks if m[0] <= 0]:
        hit_marks.remove(mark)

    screen.fill(THECOLORS["white"])

    for ball in balls:
        p = to_pygame(ball.body.position)
        pygame.draw.circle(screen, THECOLORS[ball.color], p, int(ball.radius), 2)

    for line in static_lines:
        pv = [to_pygame(line.body.position + v.rotated(line.body.angle)) for v in [line.a, line.b]]
        pygame.draw.lines(screen, THECOLORS["lightgray"], False, pv)

    for mark in hit_marks:
        pygame.draw.circle(screen, THECOLORS[mark[2]], to_pygame(mark[1]), mark[0], 0)
        mark[0] -= 1

    for x in range(10):
        space.step(1/600)

    pygame.display.flip()
    clock.tick(60)    