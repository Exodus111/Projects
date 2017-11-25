#!/usr/bin/python3
# python -m kivy.atlas myatlas 160x256 *.png
from PIL import Image as Img
from path import Path
from kivy.atlas import Atlas
from kivy.vector import Vector
from kivy.graphics.texture import Texture

def mult_tuple(tup, num):
    return (tup[0]*num, tup[1]*num)

def add_tuple(tup, num):
    return (tup[0]+num[0], tup[1]+num[1])

def pairwise(iterable):
    a = iter(iterable)
    return zip(a, a)

def quadwise(iterable):
    a = iter(iterable)
    return zip(a, a, a, a)

def quad_overlap(iterable):
    itr1 = iter(iterable[::2])
    itr2 = iter(iterable[1::2])
    a,b,c,d = next(itr1), next(itr2), next(itr1), next(itr2)
    yield a,b,c,d
    for _ in iterable:
        a,b = next(itr1), next(itr2)
        yield c,d,a,b
        c,d = next(itr1), next(itr2)
        yield  a,b,c,d

def circle_collide(w1, w2, dist=50):
    return Vector(w1.pos).distance(w2.pos) < dist


def load_json(filename):
    import json
    with open(filename, "+r") as f:
        myfile = json.load(f)
    return myfile


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

def make_atlas(folder, size):
    fold = Path(folder)
    subdirs = fold.dirs()
    for dirc in subdirs:
        Atlas.create("images/{}".format(dirc.basename()), dirc.files("*.png"), size)

def scale_and_convert(filename, multiplier=3, fil=False, flip=True):
    img = scale_image(filename, multiplier, fil, flip)
    return convert_pil_to_kivy_image(img)

def scale_image(filename, multiplier=3, fil=False, flip=True):
    """ Returns Pil Image Object"""
    if fil:
        filename.save("temp_")
        filename = "temp_"
    img = Img.open(filename)
    if flip:
        img = img.transpose(Img.FLIP_TOP_BOTTOM)
    size = img.size
    new_size = (size[0]*multiplier, size[1]*multiplier)
    img = img.resize(new_size)
    return img

def convert_pil_to_kivy_image(img):
    """Returns Kivy Texture Object"""
    image = Texture.create(size=img.size)
    image.blit_buffer(img.tobytes(), colorfmt="rgba", bufferfmt="ubyte")
    return image


def scale_images(folders, multiplier=3):
    """Returns Atlas Object"""
    for folder in folders.dirs():
        for f in folder.files():
            img = scale_image(f, multiplier)
            img.save("./temp/{}{}".format(folder.basename(), f.basename()), "PNG")
    make_atlas("./temp", (160,256))
    for t in Path("./temp").dirs():
        t.rmdir()

def multiply(nums):
    factor = 1
    for i in nums:
        factor *= i
    return factor

if __name__ == "__main__":
    #divide_all("images/stored")
    #make_atlas("images/crops")
    #clear_temp()
    pass