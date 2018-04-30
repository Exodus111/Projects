def multiple2(x):
    if x == 0:
        return 0
    else:
        print(x, "+2")
        return multiple2(x-1) + 2

print("Final product: ", multiple2(100))