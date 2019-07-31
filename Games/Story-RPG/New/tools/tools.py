#!/usr/bin/python3
# python -m kivy.atlas myatlas 160x256 *.png
from PIL import Image as Img
from path import Path
from kivy.atlas import Atlas
from kivy.vector import Vector
from kivy.graphics.texture import Texture

NUMBER = iter(i for i in range(10000))

def console(game):
    while True:
        inp = input(">>> ")
        if inp.lower() in ("quit", "exit", "q"):
            print("Closing console.")
            break
        else:
            try:
                print(eval(inp))
            except Exception as e:
                print(e)

def log_to_textfile(filename, text):
    with open(filename, "a") as outfile:
        outfile.write("\n")
        outfile.write(str(text))

def mult_tuple(tup, num):
    return (int(tup[0]*num), int(tup[1]*num))

def add_tuple(tup, num):
    return (tup[0]+num[0], tup[1]+num[1])

def pairwise(iterable):
    a = iter(iterable)
    return zip(a, a)

def quadwise(iterable):
    a = iter(iterable)
    return zip(a, a, a, a)

def quad_overlap(iterable):
    """
        Take a list of ints, and gives back overlapping pairs.
        Imagine a sequence of lines, the ints are x,y points. 
    """
    count = 0
    for n in range(int(len(iterable)/4)):
        yield iterable[count:count+4]
        count += 2

def circle_collide(w1, w2, dist=50):
    return Vector(w1.pos).distance(w2.pos) < dist

def load_json(filename):
    import json
    with open(filename, "+r") as f:
        myfile = json.load(f)
    return myfile


def divide_image(filename, top, bottom, name):
    im = Img.open(filename)
    x, y = (-(32*3), top)
    crops = []
    for i in range(5*4):
        x += (32*3)
        w = x + (32*3)
        h = y + bottom
        crops.append(im.crop((x, y, w, h)))
        if i != 0 and i % 5 == 0:
            print(name, y)
            y += (64*3)
            x = 0
    poses = ["idle", "walkdown", "walkleft", "walkright", "walkup"]
    j = 0
    h = 0
    for num, c in enumerate(crops):
        if num % 5 == 0:
            j += 1
            h = 0
        dest = Path("./{}".format(name))
        dest.mkdir_p()
        c.save("./{}/{}{}.png".format(name, poses[h], j))
        h += 1

def divide_all(folder):
    myfolder = Path(folder)
    d = {
         "Priest":{"name":"Djonsiscus", "size":(27*3, 37*3)},
         "Bracksmith":{"name":"Jarold", "size":(27*3, 37*3)}, # Worked
         "Wife":{"name":"Tylda Travisteene", "size":(31*3, 33*3)}, # Worked
         "Girl":{"name":"Sheila Travisteene", "size":(30*3, 34*3)},
         "Apothecary":{"name":"Mr Johes", "size":(28*3, 36*3)}, # Worked
         "Guy":{"name":"Riff Danner", "size":(31*3, 33*3)},
         "Player":{"name":"Player", "size":(27*3, 37*3)}
    }
    for img in myfolder.files("*.png"):
        n = img.basename()
        n = n.rstrip(".png")
        divide_image(img, d[n]["size"][0], d[n]["size"][1], d[n]["name"])

def make_atlas(folder, size):
    fold = Path(folder)
    subdirs = fold.dirs()
    for dirc in subdirs:
        Atlas.create("./images/{}".format(dirc.basename()), dirc.files("*.png"), size)

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
    #divide_image("orig_images/Player.png", 27, 37, "Player")
    make_atlas("./crops/big_crops", (160*3, 256*3))




    