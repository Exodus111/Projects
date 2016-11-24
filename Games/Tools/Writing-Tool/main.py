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
        self.size = (960, 480)
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

    def save_info(self, name_id, entries, pos):
        if "Name" in name_id:
            name = "".join(entries["Entry"]["Name"])
            self.db.add_npc(name)
            self.canvasi.append(Canv(self, name, self.size))
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
        fname = filedialog.asksaveasfile(parent=self, mode='w', title='Choose a filename')
        self.db.save(fname.name)

    def load(self):
        fname = filedialog.askopenfile(parent=self, mode='rb', title='Choose a file')
        self.db.load(fname.name)
        for name in self.db.names:
            canv = Canv(self, name, self.size)
            self.canvasi.append(canv)
            self.canvas_switch(name)
            self.menubar.add_button("show", name, self.canvas_switch)
            for node in self.db.nodes[name]:
                n = {}
                n[node] = {}
                n[node]["tags"] = self.db.tags[node]
                n[node]["text"] = self.db.text[node]
                n[node]["coords"] = self.db.coords[node]
                n[node]["p_tags"] = self.db.p_tags[node]
                canv.insert_sticker(node, n)
            for sticky in canv.stickies:
                for other in canv.stickies[sticky].p_tags:
                    canv.stickies[sticky].my_line = canv.create_line(1,1,1,1, fill="green")
                    canv.stickies[sticky].connect2box(canv.stickies[other].w_id, other)

    # Test function, to be removed.
    def get_info(self):
        pass


if __name__ == "__main__":
    root = Tk()
    root.attributes('-zoomed', True)
    app = Main(root)
    root.mainloop()
