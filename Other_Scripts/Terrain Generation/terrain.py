from noise import snoise2
from PIL import Image, ImageDraw
from poly import Poly
from vec2d import vec2d
import random
from random import randint as rai
import numpy as np
import math



def make_img(array, name):
    img = Image.new("I", (size, size))
    draw = ImageDraw.Draw(img)
    x = y = 0
    for x in xrange(size):
        for y in xrange(size):
            va = array[x,y]
            va = (va + 1)/2 * 0xFFFF
            va = int(round(va))
            draw.point((x, y), va)
    img.save(name, "PNG")

def make_simple_img(array, name):
    img = Image.new("RGB", (size, size))
    draw = ImageDraw.Draw(img)
    x = y = 0
    for x in xrange(size):
        for y in xrange(size):
            va = array[x,y]
            va = (va + 1)/2 * 255
            va = int(round(va))
            draw.point((x, y), va)
    img.save(name, "PNG")

def add_waterlevel(x, lvl):
    if x < lvl: x = lvl
    return x


def make_array(oct, scale, wlevel=False, lac=2.0):
    array = np.zeros((size, size), np.float32)
    val = random.randint(0, 256)
    for y in xrange(size):
        for x in xrange(size):
            v = snoise2(x * scale, y * scale, oct, persistence=.5, lacunarity=lac, base = val)
            if wlevel != False:
                v = add_waterlevel(v, wlevel)
            array[x, y] += v
    return array

def _linear_ip(a, b, x):
    return a*(1-x) + b*x

def _cos_ip(a, b, x):
    ft = x * 3.1415927
    f = (1 - math.cos(ft)) * .5
    return a*(1-f) + b*f


def smooth_array(array, num=1):
    while num:
        num -= 1
        print num, " iterrations left"
        for y in xrange(size):
            for x in xrange(size):
                x,y = _bounds(x,y)
                corners = (array[x-1, y-1] + array[x+1, y-1] + array[x-1, y+1] + array[x+1, y+1])/16
                sides = (array[x-1, y] + array[x+1, y] + array[x, y-1] + array[x, y+1])/8
                center = array[x, y] / 4
                array[x,y] = corners + sides + center
    return array        

def _bounds(x, y):
    if x <= 0: 
        x = 1
    elif x >= size-1: 
        x = size-2
    if y <= 0: y = 1
    elif y >= size-1: 
        y = size-2
    return x,y

def make_bw(array, height=0):
    for y in xrange(size):
        for x in xrange(size):
            a = array[x,y]
            if a <= height:
                a = -1
            if a > height:
                a = 1
            array[x,y] = a
    return array 

def make_square(array, dist):
    loc1 = (random.randint(0, size), random.randint(0, size))
    mysq = np.zeros((dist, dist), dtype=np.float32)
    x = loc1[0] - mysq.shape[0]
    y = loc1[1] - mysq.shape[1]
    if x < 0: x = 1
    if y < 0: y = 1
    cursq = array[x:x+mysq.shape[0], y:y+mysq.shape[1]]
    mean = np.mean(cursq)
    array[x:x+mysq.shape[0], y:y+mysq.shape[1]] = mean

    return array, loc1

def interpolate(array1, array2, exx=.5, img=None):
    array = np.zeros((size, size), np.float32)
    for x in xrange(size):
        for y in xrange(size):
            if img != None:
                ip = img[x,y]
                ip *= 1.5
                exx = (ip+1)/2
            a = array1[x,y]
            b = array2[x,y]
            num = _cos_ip(a, b, exx)
            array[x,y] += num
    return array

def make_lines(array):
    for y in xrange(size):
        for x in xrange(size):
            a = array[x,y]
            if a < 0: a *= -1
            if a < .02: a = -1
            else: a = 1
            array[x,y] = a
    return array

def exclude_region(array, region):
    for y in xrange(size):
        for x in xrange(size):
            a = array[x,y]
            b = region[x,y]
            if b < 0:
                a = -1
                array[x,y] = a
    return array

def circular_gradient(center, radius, reverse=False):
    a = center
    maxdist = math.sqrt((0 - radius)**2 + (0 - radius)**2) 
    grray = np.ones((size, size), dtype=np.float32)
    for y in xrange(size):
        for x in xrange(size):
            b = (x,y)
            dist = math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
            dist = dist/maxdist
            if dist >= 1:
                dist = 1
            if reverse:
                grray[x,y] = dist
            else:
                if dist == 1 or dist == 0:
                    grray[x,y] = -1
                else:
                    grray[x,y] = 1 - dist
            

    return grray

def make_ridge(a, b, amount):
    ax = float(a[0])
    ay = float(a[1])

    bx = float(b[0])
    by = float(b[1])

    abx = math.sqrt((ax - bx)**2)
    aby = math.sqrt((ay - by)**2)

    stepx = abx / amount
    stepy = aby / amount

    points = []
    for i in xrange(amount):
        px = ax + (stepx*i)
        py = ay + (stepy*i)
        points.append((int(px), int(py)))
    return points

def expo(array, ran1, ran2):
    for y in xrange(size):
        for x in xrange(size):
            array[x,y] *= random.uniform(ran1, ran2)
    return array 


if __name__ == "__main__":
    size = 512
    """
    array1 = make_array(2, .01)
    array1 *= .2
    array2 = make_array(2, .01, .1)
    array2 *= .8
    array3 = interpolate(array1, array2)
    make_simple_img(array3, "Terrain.png")
    """
    array1 = make_array(2, .005)
    array1 *= .4
    array2 = make_array(2, .01)
    array2 *= .4
    array3 = interpolate(array1, array2)
    array4 = make_array(6, .005, wlevel=.2)
    array4 *= .9
    array5 = interpolate(array3, array4, exx=.6)
    make_simple_img(array5, "terrain_interpolated_mount_hills.png")