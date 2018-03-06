#!/usr/bin/python3
"""
a = ["a", "b", "c"]

t = "check"*any([(i in ("d", "e", "f")) for i in a]) or "not check"
print(t)
"""

mylist = [2, 3, 4, 5]

for n in mylist:
	if n == 4:
		break

print(n)