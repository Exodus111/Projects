from functools import wraps
import time

RUNTEST = False

def _print(f, fname):
    print("{} returns: {}".format(fname, f))
    return f

def log(run):
        def decrated_function(func):
            if run:
                f_name = func.__name__
                ts = time.time()
                @wraps(func)
                def wrapper(*args, **kw):
                    if len(args) > 0:
                        print("Positional Arguments of function {}: ".format(f_name))
                        for i in args:
                            print("Type: {} Value: {}".format(type(i), i))
                    if len(kw) > 0:
                        print("Key Word Arguments of function {}: ".format(f_name))
                        for j in kw:
                            print("Type: {} Key word: {} Value: {}".format(type(j), j, kw[j]))
                    return _print(func(*args, **kw), f_name)
                te = time.time()
                print("Timing of function {}: ".format(f_name), te - ts)
                return wrapper
            else:
                return func
        return decrated_function

@log(RUNTEST)
def test_func(a, b, alist=[]):
    c = [a+b for i in range(10)]
    return c

test_func(1, 2, alist=[])
