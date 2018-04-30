
lngst = [0, 25, 2, 1, 14, 1, 14, 1, 4, 6, 6, 7, 0, 10, 11]
size = len(lngst)
dList = []
for x in range(size - 1):
    if lngst[x] < lngst[x+1]: 
        l = [lngst[x], lngst[x+1]]
        dList.append(l)
print(dList)
