#!/usr/bin/python3
#
# This file is intended as a simplified example for Stack Overflow.
# The original program is far greater and is a writing tool for branching dialogue, much like Twine.

from tkinter import Tk, Canvas, Frame, Text, Label

class Canv(Canvas):
    def __init__(self, parent):
        """Simple Canvas class."""
        Canvas.__init__(self, parent)
        self.parent = parent
        self.config(background="white", width=960, height=640)
        self.num = 1
        self.pack()
        self.element_list = []
        self.bindings()

    def bindings(self):
        """All the button bindings."""
        self.bind("<Button-1>", self.add_window)
        self.bind("<ButtonPress-2>", self.mark)
        self.bind("<B2-Motion>", self.drag)
        self.bind("<Button-3>", self.take_ps)
        self.bind("<Button-4>", self.show_alltags)

    def show_alltags(self, e):
        for element in self.element_list:
            print("Object id: {}".format(element.w_id))
            print("Tags are: {}".format(self.gettags(element.w_id)))

    def add_window(self, e):
        """Here I add the Label as a Canvas window.
           And include an Oval to mark its location.
        """
        text = "Textwindow {}".format(self.num)
        self.num += 1
        window = TextWindow(self, text)
        pos = (self.canvasx(e.x), self.canvasy(e.y))
        w_id = self.create_window(pos, window=window, state="normal")
        bbox = (pos[0]-50, pos[1]-50, pos[0]+50, pos[1]+50)
        self.create_oval(bbox, width=3, outline="green")
        window.w_id = w_id
        self.element_list.append(window)

    def mark(self, e):
        """Simple Mark to drag method."""
        self.scan_mark(e.x, e.y)

    def drag(self, e):
        """This drags, using the middle mouse button, the canvas to move around."""
        self.scan_dragto(e.x, e.y, 5)

    def take_ps(self, e):
        """Here I take a .ps file of the Canvas.
           Bear in mind the Canvas is virtually infinite, so I need to set the size of the .ps file
           to the bounding box of every current element on the Canvas.
        """
        x1, y1, x2, y2 = self.bbox("all")
        self.postscript(file="outfile.ps", colormode="color", x=x1, y=y1, width=x2, height=y2)
        print("Writing file outfile.ps...")

class TextWindow(Frame):
    def __init__(self, parent, text):
        """Very simple label class.
           Might have been overkill, I originally intended there to be more to this class,
            but it proved unnecesary for this example.
        """
        Frame.__init__(self, parent)
        self.pack()
        self.label = Label(self, text=text)
        self.label.pack()



if __name__ == "__main__":   #<---Boilerplate code to run tkinter.
    root = Tk()
    app = Canv(root)
    root.mainloop()
