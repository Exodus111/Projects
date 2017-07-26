
conv = lambda num: tuple([float("{0:.2f}".format((1.0/255) * n)) for n in num])

print(conv((111, 83, 61)))
