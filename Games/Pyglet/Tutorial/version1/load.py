import pyglet

pyglet.resource.path = ["../resources"]
pyglet.resource.reindex()

main_batch = pyglet.graphics.Batch()

asteroid_image = pyglet.resource.image("asteroid.png")
player_image = pyglet.resource.image("player.png")
bullet_image = pyglet.resource.image("bullet.png")

player_ship = pyglet.sprite.Sprite(img=player_image, x=400, y=300, batch=main_batch)

score_label = pyglet.text.Label(text="Score: 0", x=10, y=575, batch=main_batch)
level_label = pyglet.text.Label(text="My Amazing Game", x=400, y=575, anchor_x="center", batch=main_batch)


def center_image(image):
    image.anchor_x = image.width/2
    image.anchor_y = image.height/2

center_image(asteroid_image)
center_image(bullet_image)
center_image(player_image)