#
# Node Writer. A Writing utility for Choice based dialogue systems.
#

from Tkinter import *

class Board(object):
    def __init__(self, master, w, h, obj):
        canv = Canvas(master, width=w, height=h)
        canv.create_window((200, 200), window=obj)
        canv.pack()


root = Tk()
label = Label(root, text="Node Writer")
label.pack()
text = Text(root)
text.insert(INSERT, "Hey there, this is the text area!")

board = Board(root, 960, 800, text)
mainloop()
