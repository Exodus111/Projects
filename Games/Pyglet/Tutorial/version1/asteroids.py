import pyglet
import math
from random import randint as rai

import load

def asteroids(num_asteroids, player_position):
    asteroids = []
    for i in xrange(num_asteroids):
        a_x, a_y = player_position
        while distance((a_x, a_y), player_position) < 100:
            a_x = rai(0, 800)
            a_y = rai(0, 600)
        new_asteroid = pyglet.sprite.Sprite(img=load.asteroid_image, x=a_x, y=a_y, batch=load.main_batch)
        new_asteroid.rotation = rai(0, 360)
        asteroids.append(new_asteroid)
    return asteroids

def distance(point_1=(0,0), point_2=(0,0)):
    return math.sqrt((point_1[0] - point_2[0]) ** 2 + 
                     (point_1[1] - point_2[1]) ** 2)


