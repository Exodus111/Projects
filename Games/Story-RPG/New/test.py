#!/usr/bin/python3


def myfunc():
	"""
	>>> myfunc()
	4
	"""
	return 4

if __name__ == "__main__":
	from doctest import testmod
	testmod() 


