#!/usr/bin/python3
# python -m kivy.atlas myatlas 160x256 *.png
from PIL import Image as Img
from path import Path
from kivy.atlas import Atlas
from kivy.vector import Vector
from kivy.graphics.texture import Texture


def circle_collide(w1, w2):
    if Vector(w1.pos).distance(w2.pos) < 50:
        return True
    else:
        return False

def divide_image(filename, top, bottom, name):
    im = Image.open(filename)
    x, y = (-32, top)
    crops = []
    for i in range(5*4):
        x += 32
        w = x + 32
        h = y + bottom
        crops.append(im.crop((x, y, w, h)))
        if i != 0 and i % 5 == 0:
            print(name, y)
            y += 64
            x = 0
    poses = ["idle", "walkdown", "walkleft", "walkright", "walkup"]
    j = 0
    h = 0
    for num, c in enumerate(crops):
        if num % 5 == 0:
            j += 1
            h = 0
        dest = Path("./images/crops/{}".format(name))
        dest.mkdir_p()
        c.save("./images/crops/{}/{}{}.png".format(name, poses[h], j))
        h += 1

def divide_all(folder):
    myfolder = Path(folder)
    d = {
         "Priest":{"name":"Djonsiscus", "size":(27, 37)},
         "Bracksmith":{"name":"Jarod", "size":(27, 37)}, # Worked
         "Wife":{"name":"Tylda Travisteene", "size":(31, 33)}, # Worked
         "Girl":{"name":"Sheila Travisteene", "size":(30, 34)},
         "Apothecary":{"name":"Mr Johes", "size":(28, 36)}, # Worked
         "Guy":{"name":"Riff Danner", "size":(31, 33)},
    }
    for img in myfolder.files("*.png"):
        n = img.basename()
        n = n.rstrip(".png")
        divide_image(img, d[n]["size"][0], d[n]["size"][1], d[n]["name"])

def make_atlas(folder):
    fold = Path(folder)
    subdirs = fold.dirs()
    for dirc in subdirs:
        Atlas.create("images/{}".format(dirc.basename()), dirc.files("*.png"), [160,256])


def scale_image(filename, multiplier=3):
    img = Img.open(filename)
    img = img.transpose(Img.FLIP_TOP_BOTTOM)
    size = img.size
    new_size = (size[0]*multiplier, size[1]*multiplier)
    img = img.resize(new_size)
    image = Texture.create(size=new_size)
    image.blit_buffer(img.tobytes(), colorfmt="rgba", bufferfmt="ubyte")
    return image

if __name__ == "__main__":
    #divide_all("images/stored")
    #make_atlas("images/crops")
    #clear_temp()
    pass
