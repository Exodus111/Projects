#!/usr/bin/python3
import os

line1 = [1,2,3]
line2 = [4,5,6]
line3 = [7,8,9]
while True:
    os.system("clear")
    print("", line1, "\n", line2, "\n", line3)
    inp = int(input(">> "))
    if inp in line1:
        line1[inp-1] = "X"
    if inp in line2:
        line2[inp-4] = "X"
    if inp in line3:
        line3[inp-7] = "X"
