import pyglet
from pyglet.window import key, mouse

import load

width, height = load.width, load.height
window = pyglet.window.Window(width, height)

background_batch = load.background_batch
character_batch = load.character_batch
player = load.Player()

def update(dt):
    player.moving()

@window.event
def on_key_press(k, m):
    if k == key.W:
        player.move["up"] = True
    if k == key.S:
        player.move["down"] = True
    if k == key.A:
        player.move["left"] = True
    if k == key.D:
        player.move["right"] = True

@window.event
def on_key_release(k, m):
    if k == key.W:
        player.move["up"] = False
        player.sprite.image = player.images["standing"]["up"]
    if k == key.S:
        player.move["down"] = False
        player.sprite.image = player.images["standing"]["down"]
    if k == key.A:
        player.move["left"] = False
        player.sprite.image = player.images["standing"]["left"]
    if k == key.D:
        player.move["right"] = False
        player.sprite.image = player.images["standing"]["right"]

@window.event
def on_mouse_motion(x, y, dx, dy):
    player.aim(x, y)

@window.event
def on_mouse_press(x, y, button, mods):
    if button == mouse.LEFT:
        pass
    if button == mouse.RIGHT:
        pass

@window.event
def on_draw():
    window.clear()
    background_batch.draw()
    character_batch.draw()

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1/60.0) # update at 60Hz
    pyglet.app.run()
