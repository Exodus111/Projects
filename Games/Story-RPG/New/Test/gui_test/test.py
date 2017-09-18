#!/usr/bin/python3

a = 10
b = 4

for i in range(100):
    print("i: ", i)
    if i == a:
        print("Found a.")
        for n in range(a):
            print("n: ", n)
            if n == b:
                print("Found b.")
                break
        break
