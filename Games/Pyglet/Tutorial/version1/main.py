import pyglet

import load, asteroids

game_window = pyglet.window.Window(800, 600)

player_ship = load.player_ship
level_label = load.level_label
score_label = load.score_label

asteroids = asteroids.asteroids(3, player_ship.position)

main_batch = load.main_batch

@game_window.event
def on_draw():
    game_window.clear()
    main_batch.draw()

if __name__ == "__main__":
    pyglet.app.run()