from vec2d import vec2d
import numpy as np
from PIL import Image, ImageDraw
from random import randint as rai

def draw_image(name, size, array):
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

def make_line(a, b):
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

def intersect(line1, line2):
        def line(p1, p2):
            A = (p1[1] - p2[1])
            B = (p2[0] - p1[0])
            C = (p1[0]*p2[1] - p2[0]*p1[1])
            return A, B, -C

        L1 = line(*line1)
        L2 = line(*line2)
        D  = L1[0] * L2[1] - L1[1] * L2[0]
        Dx = L1[2] * L2[1] - L1[1] * L2[2]
        Dy = L1[0] * L2[2] - L1[2] * L2[0]
        if D != 0:
            x = Dx / D
            y = Dy / D
            inter1 = False
            inter2 = False
            l1x = sorted((line1[0][0], line1[1][0]))
            l1y = sorted((line1[0][1], line1[1][1]))
            l2x = sorted((line2[0][0], line2[1][0]))
            l2y = sorted((line2[0][1], line2[1][1]))

            if x > l1x[0] and x < l1x[1] and y > l1y[0] and y < l1y[1]:
                    inter1 =  True
            if x > l2x[0] and x < l2x[1] and y > l2y[0] and y < l2y[1]:
                inter2 = True
            if inter1 and inter2:
                return True
            else:
                return False
        else:
            return False

def intersect_old(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])
    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        return False
    else:
        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        inter1 = False
        inter2 = False
        l1x = sorted((line1[0][0], line1[1][0]))
        l1y = sorted((line1[0][1], line1[1][1]))
        l2x = sorted((line2[0][0], line2[1][0]))
        l2y = sorted((line2[0][1], line2[1][1]))

        if x >= l1x[0] and x <= l1x[1] and y >= l1y[0] and y <= l1y[1]:
                inter1 =  True
        if x >= l2x[0] and x <= l2x[1] and y >= l2y[0] and y <= l2y[1]:
            inter2 = True
        if inter1 and inter2:
            return True
        else:
            return False


size = 512
array = np.zeros((size, size), dtype=np.float32)
#running = 100
#while running > 0:
ps = []
for points in xrange(4):
    a = rai(0, size)
    b = rai(0, size)
    ps.append((a,b))
if intersect((ps[0], ps[1]), (ps[2], ps[3])):
    print "Lines colliding"
    #break
#running -= 1

line1 = make_line(ps[0], ps[1])
line2 = make_line(ps[2], ps[3])
for p in line1:
    array[p[0], p[1]] = 1
for p in line2:
    array[p[0], p[1]] = 1


draw_image("lines.png", size, array)
