
import pyglet, load
from pyglet.window import key, mouse

width, height = load.width, load.height
background_batch = load.background_batch
character_batch = load.background_batch

window = pyglet.window.Window(width, height)

def update(dt):
    pass

@window.event
def on_key_press(k, m_key):
    pass

@window.event
def on_key_release(k, m_key):
    pass

@window.event
def on_mouse_motion(x, y, dx, dy):
    pass

@window.event
def on_mouse_press(x, y, button, mods):
    pass

@window.event
def on_draw():
    window.clear()
    background_batch.draw()
    character_batch.draw()

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1/60.0) # update at 60Hz
    pyglet.app.run()