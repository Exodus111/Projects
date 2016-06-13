import pyglet
import numpy as np

width = 800
height = 600
#pyglet.resource.path = ["./resources"]
#pyglet.resources.reindex()

background_batch = pyglet.graphics.Batch()
character_batch = pyglet.graphics.Batch()

class Tile(object):
    def __init__(self, img, x, y, batch):
        self.sprite = pyglet.sprite.Sprite(img=img, x=x, y=y, batch=batch)

class World(object):
    def __init__(self, size):
        self.block = 6
        self.array = np.zeros(size, size, dtype=np.int16)

    def make_world(self):
        for y in self.array:
            for x in self.array:
                brick = Tile()




