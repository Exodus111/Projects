def flatten(aList):
    new = []
    for x in aList:
        if type(x) == list:
            x = flatten(x)
        elif type(x) != list:
            new.append(x)
    return new

mylist = [[1,'a',['cat'],2],[[[3]],'dog'],4,5]

print(flatten(mylist))
