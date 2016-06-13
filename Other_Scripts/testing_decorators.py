from functools import wraps


def itallic(fn):
    @wraps(fn)
    def wrapped():
        return "<i>" +fn() + "</i>"
    return wrapped

def bold(fn):
    @wraps(fn)
    def wrapped():
        return "<b>" +fn() + "</b>"
    return wrapped

@itallic
@bold
def hello():
    """A decorated Hello World"""
    return "Hello World"

print("{} {} {}".format(hello(), hello.__name__, hello.__doc__))
