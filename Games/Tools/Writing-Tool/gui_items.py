from collections import defaultdict
from functools import partial
from tkinter import Canvas, Menu
from mod_items import *

class Canv(Canvas):
    def __init__(self, parent, name, size):
        Canvas.__init__(self, parent)
        self.parent = parent
        self.name = name
        self.background = "white"
        self.size = size
        self.width = size[0]
        self.height = size[1]
        self.info = defaultdict(dict)
        self.num = defaultdict(int)
        self.sticky_size = (250, 220)
        self.stickies = []
        self.lines = {}
        self.bind("<ButtonPress-1>", self.smark)
        self.bind("<B1-Motion>", self.sdrag)
        self.bind("<Button-3>", self.insert_node)

    def smark(self, pos):
        self.scan_mark(pos.x, pos.y)

    def sdrag(self, pos):
        self.scan_dragto(pos.x, pos.y, 5)

    def insert_node(self, e):
        pos = (e.x, e.y)
        node = Node(self, numerate(self.num, "Node"), pos)
        node.insert_entry_field("tags", focus=True)
        node.insert_text_field("text")
        node.ok_cancel_buttons()

    def save_info(self, name, entries, pos):
        if "Node" in name:
            node = {name:{"tags":entries["Entry"]["tags"],
                        "text":entries["Text"]["text"]}}
            # Fix Later----->#self.parent.db.add_nodes(self.name, node)
            self.insert_sticker(name, node, pos)

    def insert_sticker(self, name, node, pos):
        sticker = Sticker(self, pos, name)
        sticker.add_entry(node[name]["tags"])
        sticker.add_text(node[name]["text"])
        sticker.add_buttons()
        w_id = self.create_window(pos, window=sticker)
        sticker.draw_box()

class TopMenuBar(Menu):
    def __init__(self, parent):
        Menu.__init__(self, parent)
        self.parent = parent
        self.newmenu = Menu(self)
        self.showmenu = Menu(self)
        self.newmenu.add_command(label="NPC", command=self.parent.onNew)
        self.newmenu.add_separator()
        self.newmenu.add_command(label="Save", command=self.parent.save)
        self.newmenu.add_command(label="Load", command=self.parent.load)
        self.showmenu.add_command(label="Info", command=self.parent.get_info)
        self.newmenu.add_separator()
        self.showmenu.add_separator()
        self.add_cascade(label="New", menu=self.newmenu)
        self.add_cascade(label="Show", menu=self.showmenu)
        self.add_command(label="Exit", command=self.parent.quit)

    def add_button(self, menu, name, call):
        func = partial(call, name)
        if menu == "new":
            self.newmenu.add_command(label=name, command=func)
        elif menu == "show":
            self.showmenu.add_command(label=name, command=func)


if __name__ == "__main__":
    pass    #<--- For testing!
