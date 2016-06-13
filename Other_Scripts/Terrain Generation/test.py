from random import randint as rai
from PIL import Image, ImageDraw
import numpy as np
from vec2d import vec2d
import math

class Poly(object):
    def __init__(self, point, area_points):
        self.point = vec2d(point)
        self.edges = []
        self.verts = []
        self.size = size
        self.area = area_points
        self.extrapolate()

    def extrapolate(self):
        for p in self.area:
            check = False
            eight_points = [(p[0]+1,p[1]+1), (p[0]+1,p[1]-1), (p[0]+1,p[1]), (p[0],p[1]+1), 
                            (p[0]-1,p[1]-1), (p[0]-1,p[1]+1), (p[0]-1,p[1]), (p[0],p[1]-1)]
            for sp in eight_points:
                if sp not in self.area:
                    check = True
            if check:
                self.edges.append(p)


    def draw2array(self, array):
        for p in self.edges:
            array[p[0], p[1]] = 1
        return array


def draw_image(array, name):
    """Here we draw our array to a .png image."""
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

def gen_array_and_points(num_cells):
    array = np.zeros((size, size), dtype=np.float32)
    pointlist = []
    for i in xrange(num_cells):
        pointlist.append((rai(0, size), rai(0, size)))
    return array, pointlist

def point_dict(points):
    point_dict = {}
    val = 2./len(points)
    num = 0
    for i in points:
        point_dict[i] = (val*num)-1
        num += 1
    return point_dict

def diagram_lists(points):
    point_dict = {item: [] for item in points}
    for y in xrange(size):
        for x in xrange(size):
            p = vec2d(x,y)
            minum = 999999
            a = (0,0)
            for i in points:
                i = vec2d(i)
                dist = i.get_distance(p)
                if minum > dist:
                    minum = dist
                    a = i.inttup()
            point_dict[a].append(p.inttup())
    return point_dict

def diagram(array, points):
    once = True
    for y in xrange(size):
        for x in xrange(size):
            shortest = 9999
            p = None
            for i in points.keys():
                dist = math.hypot(i[0]-x, i[1]-y)
                if dist < shortest:
                    shortest = dist
                    p = i
            array[x,y] = points[p]
    return array

def draw_points(array, mydict):
    for i in mydict.keys():
        if myarray[i[0],i[1]] < 0:
            myarray[i[0],i[1]] = 1
        else:
            myarray[i[0],i[1]] = -1


size = 512
print "Setting up Points"
myarray, mypoints = gen_array_and_points(6)
print "Getting area points"
mydict = diagram_lists(mypoints)
count = 3
for i in mydict:
    print "Making Polygon"
    poly = Poly(i, mydict[i])
    print "Drawing Polygon to array"
    myarray = poly.draw2array(myarray)
    if count <= 0:
        break
    count -= 1

draw_image(myarray, "my_vori.png")

