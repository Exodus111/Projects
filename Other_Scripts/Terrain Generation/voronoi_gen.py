from scipy.spatial import Voronoi
from random import randint as rai
from PIL import Image, ImageDraw
from vec2d import vec2d
import numpy as np
import math

size = 512
class Polygon(object):
    def __init__(self, center, vertex_list):
        self.point = center
        self.vertexes = vertex_list

def draw_image(array):
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
    img.save("voronoi.png", "PNG")

def gen_array_and_points(num_cells):
    array = np.zeros((size, size), dtype=np.float32)
    pointlist = []
    for i in xrange(num_cells):
        pointlist.append((rai(0, size), rai(0, size)))
    return array, pointlist

def gen_voronoi(array, points):
    vor = Voronoi(points)
    verts = vor.vertices
    n = len(verts)
    lines = []
    for p in xrange(len(verts)):
        if p+1 < n:
            line = make_line(verts[p], verts[p+1])
            lines.append(line)
    for lin in lines:
        for l in lin:
            if l[0] >= size or l[1] >= size:
                pass
            else:    
                array[l[0],l[1]] = -1
    return array

def generate_voronoi(array, points):
    for y in xrange(size):
        for x in xrange(size):
            draw = False
            a = b = c = math.hypot(size-1, size-1)
            for cell in xrange(len(points)):
                cell = math.hypot(points[cell][0]-x, points[cell][1]-y)
                if a >= cell:
                    a = cell
                elif b >= cell:
                    b = cell
            d = b - a
            if d > 0 and d < 1:
                array[x,y] = 1
    return array

def make_line(a, b):
        a = (int(round(a[0])), int(round(a[1])))
        b = (int(round(b[0])), int(round(b[1])))
        av = vec2d(a) 
        bv = vec2d(b)
        line = []
        between = bv - av
        endl = between.length
        l = 1
        while l < endl:
            between.length = l
            x = av + between
            line.append(x.inttup())
            l += 1
        return line

myarray, mypoints = gen_array_and_points(10)
myarray1 = gen_voronoi(myarray, mypoints)
myarray2 = generate_voronoi(myarray1, mypoints)
draw_image(myarray2)

