from random import randint as rai
from PIL import Image, ImageDraw
import numpy as np
from vec2d import vec2d
import math

class Poly(object):
    def __init__(self, point, size, other_points):
        self.point = vec2d(point)
        self.edges = []
        self.verts = []
        self.size = size
        self.pointlist = other_points
        self.find_edges()

    def closest_point(self, point):
        closest = 99999
        the_point = vec2d(point)
        for p in self.pointlist:
            p = vec2d(p)
            dist = p.get_distance(the_point)
            if closest > dist:
                closest = dist
                the_point = p 
        return the_point

    def find_edges(self):
        a = vec2d(self.closest_point(self.point))
        b = self.point - a
        b.length /= 2
        c = a + b
        b.angle += 90
        self.trace_edges(c, b, a)

    def find_next_edge(self, point):
        a = vec2d(self.closest_point(point))
        b = self.point - a
        b.length /= 2
        b.angle += 90
        b = b.normalized()
        return b, a
        

    def trace_edges(self, start, direction, opposing_point):
        di = direction
        op = opposing_point
        self.edges = [start.inttup()]
        current = start
        dir_count = 1
        while True:
            point = current + di
            if dir_count > 50:
                break
            if op == vec2d(self.closest_point(point)):
                self.edges.append(point.inttup())
                point = current
                dir_count += 1
            else:
                di, op = self.find_next_edge(point)
                self.verts.append(current)
                print "changing direction"
                dir_count += 1


    def draw_edge(self, point, dire):
        dire = dire.normalized()
        outofbounds = False
        count = 0
        while count < 100:
            lpvec = point + (dire * count)
            lp = lpvec.inttup()
            if lp[0] <= 0 or lp[0] >= self.size or lp[1] <= 0 or lp[1] >= self.size:
                outofbounds = True
                break
            else:
                self.edges.append(lp)
            count += 1

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
myarray1, mypoints = gen_array_and_points(30)
mydict = point_dict(mypoints)    
#myarray2 = diagram(myarray1.copy(), mydict)
for i in mydict:
    i = Poly(i, size, [x for x in mydict.keys() if x != i])
    i.draw2array(myarray1)
    break

draw_image(myarray1, "my_voronoi1.png")
#draw_image(myarray2, "my_voronoi2.png")


