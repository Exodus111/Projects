mylist = [i for i in range(10)]
for x in range(20):
    print("This is X: {} \nThis is the modulus: {} ".format(x, (x % len(mylist))))
