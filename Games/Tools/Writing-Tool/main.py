from collections import defaultdict
from tkinter import Tk
from tkinter.ttk import Frame, Label, Entry, Button, Style

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
        self.num = defaultdict(int)
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

    def save(self):
        pass

    def load(self):
        pass

    def onNew(self):
        node = Node(self, numerate(self.num, "Name"))
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
            else:
                canv.pack_forget()

    # Test function, to be removed.
    def get_info(self):
        self.db.save()


if __name__ == "__main__":
    root = Tk()
    root.attributes('-zoomed', True)
    app = Main(root)
    root.mainloop()
