import timeit

lo1, la1, lo2, la2 = -72.345, 34.343, -61.823, 54.826
num = 5000000

t1 = timeit.Timer("p1.great_circle(%f,%f,%f,%f)" % (lo1, la1, lo2, la2), "import p1")
t2 = timeit.Timer("c1.great_circle(%f,%f,%f,%f)" % (lo1, la1, lo2, la2), "import c1")
t3 = timeit.Timer("c2.great_circle(%f,%f,%f,%f)" % (lo1, la1, lo2, la2), "import c2")
t4 = timeit.Timer("c3.great_circle(%f,%f,%f,%f,%f)" % (lo1, la1, lo2, la2, num), "import c3")


print "Pure Python function", t1.timeit(num), "sec"
print "Cython function (Python math)", t2.timeit(num), "sec"
print "Cython function (Using trig function from math.h)", t3.timeit(num), "sec"
print "Cython function (Using C defined function)", t4.timeit(), "sec"
