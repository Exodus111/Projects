
def quad_overlap(iterable):
    itr1 = iter(iterable[::2])
    itr2 = iter(iterable[1::2])
    a,b,c,d = next(itr1), next(itr2), next(itr1), next(itr2)
    yield a,b,c,d
    for _ in iterable:
        a,b = next(itr1), next(itr2)
        yield c,d,a,b
        c,d = next(itr1), next(itr2)
        yield  a,b,c,d




mylist = [1,2,3,4,5,6,7,8,9,10,11,12]
mygen = quad_overlap(mylist)

for i in mygen:
    print(i)
