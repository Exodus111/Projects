import pyglet
from vec2d import vec2d

def center_images(imgs):
    for img in imgs:
        img.anchor_x = img.width/2
        img.anchor_y = img.height/2

def make_room(size, block, floor, wall):
    global background_batch
    room = []
    y = 0
    for vertical in range(size[1]):
        x = 0
        for brick in range(size[0]):
            if y == 0 or y == size[1]-1 or x == 0 or x == size[0]-1:
                brick = Tile(img=wall, x=x*block, y=y*block, batch=background_batch)
            else:
                brick = Tile(img=floor, x=x*block, y=y*block, batch=background_batch)
            room.append(brick)
            x += 1
        y += 1
    return room

def make_animation(name, frames):
    images = []
    num = 6
    for img in range(frames):
        img = pyglet.resource.image(name + str(num) + ".png")
        images.append(img)
        num -= 1
    return pyglet.image.Animation.from_image_sequence(images, 0.075, True)

class Tile(object):
    def __init__(self, img, x, y, batch):
        self.sprite = pyglet.sprite.Sprite(img=img, x=x, y=y, batch=batch)


class Player(object):
    def __init__(self):
        self.images = self.make_images()
        self.sprite = pyglet.sprite.Sprite(img=self.images["standing"]["down"], x=width/2, y=height/2, batch=character_batch)
        self.sprite.image = self.images["standing"]["down"]
        self.move = {"up":False, "down":False, "left":False, "right":False}
        self.speed = 5

    def aim(self, x, y):
        self.target = vec2d(x, y)


    def moving(self):
        if self.move["up"]:
            self.sprite.y += self.speed 
            if self.sprite.image != self.images["walking"]["up"] and self.sprite.image != self.images["walking"]["left"] and self.sprite.image != self.images["walking"]["right"]:
                self.sprite.image = self.images["walking"]["up"]
        if self.move["down"]:
            self.sprite.y -= self.speed
            if self.sprite.image != self.images["walking"]["down"] and self.sprite.image != self.images["walking"]["left"] and self.sprite.image != self.images["walking"]["right"]:
                self.sprite.image = self.images["walking"]["down"]
        if self.move["left"]:
            self.sprite.x -= self.speed
            if self.sprite.image != self.images["walking"]["left"]:
                self.sprite.image = self.images["walking"]["left"]
        if self.move["right"]:
            self.sprite.x += self.speed
            if self.sprite.image != self.images["walking"]["right"]:
                self.sprite.image = self.images["walking"]["right"]
        
    def make_images(self):
        down_standing = pyglet.resource.image("down_standing.png")
        up_standing = pyglet.resource.image("up_standing.png")
        left_standing = pyglet.resource.image("left_standing.png")
        right_standing = pyglet.resource.image("right_standing.png")

        down_walk = make_animation("down_walk_0", 6)
        up_walk = make_animation("up_walk_0", 6)
        left_walk = make_animation("left_walk_0", 6)
        right_walk = make_animation("right_walk_0", 6)

        imgdict = {"standing":{"down":down_standing, "up":up_standing, "left":left_standing, "right":right_standing}, 
                    "walking":{"down":down_walk, "up":up_walk, "left":left_walk, "right":right_walk}}
        
        return imgdict

width = 800
height = 600
pyglet.resource.path = ["./resources"]
pyglet.resource.reindex()

background_batch = pyglet.graphics.Batch()
character_batch= pyglet.graphics.Batch()

floor_img = pyglet.resource.image("floor.png")
wall_img = pyglet.resource.image("wall.png")


center_images([floor_img, wall_img])
room = make_room((26, 20), 32, floor_img, wall_img)

print "Finished Load."        
