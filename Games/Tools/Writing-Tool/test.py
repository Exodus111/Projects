
def foo(a,b):
    return a+b

mydict = {}
tupleargs = (5,5)

mydict["func"] = foo
print(mydict["func"](*tupleargs))
