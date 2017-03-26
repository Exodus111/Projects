#!/usr/bin/python3
# python -m kivy.atlas myatlas 160x256 *.png
from PIL import Image


def divide_image(filename, top, bottom):
    im = Image.open(filename)
    x, y, w, h = (-32, top, 32, 64)
    crops = []
    for i in range(5*4):
        x += 32
        w = x + 32
        h = y + bottom
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
    divide_image("images/stored/Wife.png", 31, 33)
