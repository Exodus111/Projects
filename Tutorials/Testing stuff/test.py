
class MyClass:
    def __init__(self, function):
        print("in the init.")
        self.function = function

    def __call__(self, *args, **kwargs):
        print("in the Callable")
        return self.function(*args, **kwargs)

@MyClass
def myfunc(a):
    return a

@MyClass
def mygen():
    for i in range(10):
        yield i

myiter = iter(mygen())

print(*myiter)
