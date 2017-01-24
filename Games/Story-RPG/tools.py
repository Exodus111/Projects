#!/usr/bin/python3
from collections import OrderedDict
import json
from PIL import Image


def make_atlas(filename, amount, gaps):
    my_atlas = OrderedDict()
    my_atlas[filename] = OrderedDict()
    moves = ["idle", "walkdown", "walkleft", "walkright", "walkup"]
    indx = 0
    _id = 1
    for i in range(amount):
        if i >= len(moves)*_id:
            _id += 1
            indx = 0
        my_atlas[filename][moves[indx]+str(_id)] = [(indx*(128+gaps[0]+gaps[0])), 0+((_id-1)*(128+gaps[1]))+gaps[1], 128, 128]
        indx += 1
    # Deleting idle3 and above (some files needs to delete idle2 as well).
    for j in range(3, 5):
        del my_atlas[filename]["idle"+str(j)]
    with open("./images/player_sheet128.atlas", "+w") as f:
        f.write(json.dumps(my_atlas))

def divide_image():
    im = Image.open("images/player_sheet32.png")
    x, y, w, h = (-32, 32, 32, 64)
    crops = []
    for i in range(5*4):
        x += 32
        w = x + 32
        h = y + 32
        crops.append(im.crop((x, y, w, h)))
        if i != 0 and i % 5 == 0:
            print(y)
            y += 64
            x = 0
    poses = ["idle", "walkdown", "walkleft", "walkright", "walkup"]
    j = 0
    h = 0
    for num, c in enumerate(crops):
        if num % 5 == 0:
            j += 1
            h = 0
        c.save("./images/crops/{}{}.png".format(poses[h], j))
        h += 1

if __name__ == "__main__":
    #make_atlas("player_sheet128.png", 5*4, (0, 128))
    divide_image()
