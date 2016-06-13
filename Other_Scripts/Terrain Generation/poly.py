import numpy as np
from PIL import Image, ImageDraw
from shapely.geometry import Point, Polygon, box
from vec2d import vec2d
from random import randint as rai
import math




class Poly(object):
    """This generates a polygon in a numpy Array"""
    def __init__(self, size, sides):
        self.size = size
        self.sides = sides
        self.array = np.zeros((size, size), dtype=np.float32)
        self.point = (size/2, size/2)
        self.minmax = (size/4, size/2)
        self.step = 360/sides
        self.generate()
        self.dlines = self.fix_list()
        self.collided = 0
        

    def generate(self):
        """Here we generate the polygon
            This method is called in the __init__
        """
        self.poly_list = []
        degrees = 90
        for side in xrange(self.sides):
            side = vec2d(self.point)
            side.angle = degrees
            side.length = rai(int(self.minmax[0]), int(self.minmax[1]))
            degrees += self.step
            x = self.point + side
            self.poly_list.append(x.inttup())

    def fix_list(self):
        """We need the generated vertexes to also include the points in between
            as well as our starting and ending points, to generate edges(lines)
            This method has to be called in code.
        """
        lines = zip(self.poly_list[0::2], self.poly_list[1::2])
        fixed = []
        x = 0
        for t in lines:
            if x != 0:
                f1 = [x[1], t[0]]
                fixed.append(f1)
            f2 = [t[0], t[1]]
            fixed.append(f2)
            x = t
        f3 = [lines[-1][1], lines[0][0]]
        fixed.append(f3)
        return fixed

    def make_line(self, a, b):
        """Here we generate our original edges
            This method is called from our draw2array method
        """
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

    def displace_lines(self, amount, times_to_loop):
        """Here we begin to displace our lines and set the values for their displacement.

            'amount' is the amount in pixels to move the center of the edge, the displacement
            will pick a random number between 'amount' and '-amount'.

            'times_to_loop' is the amount of displacements we want to do. 
            Any number over 10 is going to slow the computer down significantly. A good range is between 6 and 8.
        """
        for times in xrange(times_to_loop):
            self.dlines = self.displacement(self.dlines, amount)
            amount /= 2

    def displacement(self, lines, amount):
        """Displaces all our lines
            This method is called from the 'displace_lines' method.
        """
        new = []
        for line in lines:
            l1, l2 = self.displace(line[0], line[1], amount)
            new.append(l1)
            new.append(l2)
        return new

    def displace(self, a, b, amount):
        """
        Here we displace each individual line.
        This method is called from the displacement method.
        """
        av = vec2d(a)
        bv = vec2d(b)
        lv = bv - av
        hv = lv/2
        jv = av + hv
        jv.length += rai(-amount, amount)
        line1 = [av.inttup(), jv.inttup()]
        line2 = [jv.inttup(), bv.inttup()]
        return line1, line2
        
    def draw2array(self):
        """This method makes an array with our current information, 
        and flattens our edge information to just a collection and point tuples (x,y)"""
        lines = []
        for li in self.dlines:
            line = self.make_line(li[0], li[1])
            lines.append(line)
        self.lines = [item for sublist in lines for item in sublist]
        for x,y in self.lines:
            self.array[x,y] = 1

    def calc_box(self, centroid, closest_point):
        cx = centroid.x
        cy = centroid.y

        px1 = closest_point[0]
        py1 = closest_point[1]

        def find_op(p1, c1):
            if p1 > c1:
                return p1 - (p1 - c1)*2
            else:
                return p1 + (c1 - p1)*2

        px2 = find_op(px1, cx)
        py2 = find_op(py1, cy)
        xlist = sorted([px1, px2])
        ylist = sorted([py1, py2])

        return xlist[0], ylist[0], xlist[1], ylist[1]

    def bnw(self):
        """This is optional, but here we color our polygon.
            Warning: It's slow.
        """
        self.polygon = Polygon(self.lines)
        outer_box = self.polygon.bounds
        for y in xrange(int(outer_box[1]), int(outer_box[3])):
            for x in xrange(int(outer_box[0]), int(outer_box[2])):
                if self.array[x,y] != 1:
                    p = Point(x,y)
                    if self.polygon.contains(p):
                        self.array[x,y] = .5
                    else:
                        self.array[x,y] = -1


def draw_image(size, array):
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
    img.save("poly.png", "PNG")

if __name__ == "__main__":
    mypoly = Poly(512, 6)
    mypoly.displace_lines(100, 6)
    mypoly.draw2array()
    mypoly.bnw()
    draw_image(mypoly.size, mypoly.array)
