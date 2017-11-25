#!/usr/bin/python3
from screeninfo import get_monitors
_M = [m for m in get__monitors()][0]
SIZE = (_M.width, _M.height)
