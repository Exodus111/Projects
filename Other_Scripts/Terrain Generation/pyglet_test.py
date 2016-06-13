import pyglet
import numpy
from PIL import Image

size = (800, 600)
window = pyglet.window.Window(size[0], size[1])
mapbatch = pyglet.graphics.Batch()
maparray = numpy.zeros((5, 5), dtype=numpy.int)
print maparray

def on_draw():
    window.clear()
    mapbatch.draw()

if __name__ == "__main__":
    pyglet.app.run()
