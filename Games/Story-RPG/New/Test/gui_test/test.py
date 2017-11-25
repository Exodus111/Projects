#!/usr/bin/python3

a = "block_card_name1"

for t in ("block_", "flag_", "card_"):
	a = a.replace(t, "")

print(a)


