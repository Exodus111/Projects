

def myfunc():
    print 'It works!'

def other():
    print 'Wrong'

mydict = {(1,2,3):myfunc, (4,5,6):other}
num = 7

for i in mydict:
    if num in i:
        mydict[i]()
