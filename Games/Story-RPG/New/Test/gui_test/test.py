#!/usr/bin/python3

amount = 130
size = 8
amount_left = amount % size
pages = int(amount/size)

print(pages)
for page in range(pages):
    if page+1 == pages:
        print(page)
