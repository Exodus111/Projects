import numpy as np
from PIL import Image, ImageDraw
from shapely.geometry import Point, Polygon
from vec2d import vec2d
from random import randint as rai




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
        self.draw()
        

    def generate(self):
        self.poly_list = []
        degrees = 90
        for side in xrange(self.sides):
            side = vec2d(self.point)
            side.angle = degrees
            side.length = rai(int(self.minmax[0]), int(self.minmax[1]))
            degrees += self.step
            x = self.point + side
            self.poly_list.append(x.inttup())

    def make_line(self, a, b):
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

    def fix_list(self):
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

    def draw(self):
        dlines = self.fix_list()
        amount = 60
        for times in xrange(4):
            dlines = self.displacement(dlines, amount)
            amount /= 2
        lines = []
        for li in dlines:
            line = self.make_line(li[0], li[1])
            lines.append(line)
        self.lines = [item for sublist in lines for item in sublist]
        for x,y in self.lines:
            self.array[x,y] = 1

    def displacement(self, lines, amount):
        new = []
        for line in lines:
            l1, l2 = self.displace(line[0], line[1], amount)
            new.append(l1)
            new.append(l2)
        return new

    def displace(self, a, b, amount):
        av = vec2d(a)
        bv = vec2d(b)
        lv = bv - av
        hv = lv/2
        jv = av + hv
        jv.length += rai(-amount, amount)
        line1 = [av.inttup(), jv.inttup()]
        line2 = [jv.inttup(), bv.inttup()]
        return line1, line2

    def bnw(self, inside=False):
        poly = Polygon(self.lines)
        for y in xrange(self.size):
            for x in xrange(self.size):
                p = Point(x,y)
                if p.intersects(poly):
                    self.array[x,y] = 1
                else:
                    self.array[x,y] = -1


    def draw_image(self):
        img = Image.new("I", (self.size, self.size))
        draw = ImageDraw.Draw(img)
        x = y = 0
        for x in xrange(self.size):
            for y in xrange(self.size):
                va = self.array[x,y]
                va = (va + 1)/2 * 0xFFFF
                va = int(round(va))
                draw.point((x, y), va)
        img.save("river.png", "PNG")


mypoly = Poly(512, 6)
mypoly.bnw()
mypoly.draw_image()        




