#!/usr/bin/python3

from collections import defaultdict
from tkinter import Tk, filedialog
from tkinter.ttk import Frame, Label, Entry, Button, Style
from path import Path

from db import DataBase
from gui_items import *
from mod_items import *

class Main(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.window = None
        self.size = (4096, 2160)
        self.width = self.size[0]
        self.height = self.size[1]
        self.canvasi = []
        self.db = DataBase()
        self.init_ui()

    def init_ui(self):
        self.parent.title("Node Writer")
        self.style = Style(self)                  # This doesn't seem to
        self.style.theme_use("alt")               # do anything in Windows.
        self.pack(fill="both", expand=True)

        self.menubar = TopMenuBar(self)
        self.parent.config(menu=self.menubar)

    def onNew(self):
        node = Node(self, numerate("Name"))
        node.insert_entry_field("Name", focus=True)
        node.ok_cancel_buttons()
        node.entries["Entry"]["Name"].bind("<Return>", lambda x : node.save())

    def save_info(self, name_id, entries, *args):
        if "Name" in name_id:
            name = "".join(entries["Entry"]["Name"])
            self.db.add_npc(name)
            self.canvasi.append(Canv(self, name))
            self.canvas_switch(name)
            self.menubar.add_button("show", name, self.canvas_switch)

    def canvas_switch(self, name):
        for canv in self.canvasi:
            if name == canv.name:
                canv.pack(fill="both", expand=True)
                self.parent.title(canv.name)
            else:
                canv.pack_forget()

    def save(self):
        fname = filedialog.asksaveasfile(parent=self, mode='w', title='Choose a filename', initialdir="./data")
        self.db.save(fname.name)

    def load(self):
        fname = filedialog.askopenfile(parent=self, mode='rb', title='Choose a file', initialdir="./data")
        self.db.load(fname.name)
        for name in self.db.names:
            canv = Canv(self, name)
            self.canvasi.append(canv)
            self.canvas_switch(name)
            self.menubar.add_button("show", name, self.canvas_switch)
            for node in self.db.nodes[name]:
                noname = numerate("Node")
                n = {}
                n[node] = {}
                n[node]["tags"] = self.db.tags[node]
                n[node]["text"] = self.db.text[node]
                n[node]["coords"] = self.db.coords[node]
                n[node]["links"] = self.db.links[node]
                canv.insert_sticker(node, n)
            for sticky in canv.stickies:
                for other in canv.stickies[sticky].links:
                    canv.stickies[sticky].connect2box(other, True)

    def save_image(self):
        for num, canv in enumerate(self.canvasi):
            x1, y1, x2, y2 = canv.bbox("all")
            canv.postscript(file="filetest{}.ps".format(num), colormode='color', x=x1-25, y=y1-25, width=x2+25, height=y2+25)
            print("Writing filetest{}.ps...".format(num))


    # Test function, to be removed.
    def get_info(self):
        for canv in self.canvasi:
            ca_dict = canv.config()
            print("{}{}".format(ca_dict["height"], ca_dict["width"]))


if __name__ == "__main__":
    root = Tk()
    root.attributes('-zoomed', True)
    app = Main(root)
    root.mainloop()
