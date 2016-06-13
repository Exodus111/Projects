#
# Notepad style testing ground for random code.
#
#

class Class1:
    j = 5
    def some_method(self):
        self.j += 5

s = Class1()
s.some_method()
print(s.j)

"""
import numpy as np
from path import Path

import json

data = {"test1": {"2ndtest1": "3rdtest1"}, "test3": {"2ndtest3": "3rdtest3"}, "test2": {"2ndtest2": "3rdtest2"}, "test4": {"2ndtest4": "3rdtest4"}}

with open('data.txt', 'w') as outfile:
     json.dump(data, outfile, sort_keys=True, indent=4)

with open("data.txt", "r") as outfile:
    mytext = outfile.read()

mydict = json.loads(mytext)

mystring = mydict["test1"]["2ndtest1"]

print mydict
print mystring


size = (10,10)

nparray = np.zeros(size, "int16")

nparray[5][5] = 2

print nparray

import dis

def myfunc():
    return [i+100 for i in xrange(100) if i % 2 == 0]

#print dis.dis(myfunc)

import numpy as np
np.set_printoptions(threshold=np.inf)

with open("./save/bg_savemap1.npy", "r") as outfile:
    myarray = np.load(outfile)

print myarray

mylist = [1, 2, 3]

def testfunc():
    global mylist
    del mylist[:]
    mylist.append(4)
    return mylist

print(testfunc())
"""
