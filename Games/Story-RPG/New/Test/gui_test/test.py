#!/usr/bin/python3
"""
a = ["a", "b", "c"]

t = "check"*any([(i in ("d", "e", "f")) for i in a]) or "not check"
print(t)
"""

print(True and True and (False or True))